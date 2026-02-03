import os
import aiohttp
import asyncio
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup

load_dotenv()

class ImageCrawler:
    """图片爬虫：从多个免费图片网站爬取品牌产品图片"""
    
    def __init__(self):
        self.images_per_brand = int(os.getenv("IMAGES_PER_BRAND", 10))
        self.timeout = int(os.getenv("CRAWL_TIMEOUT", 30))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def crawl_brand_images(self, brands: List[str], product_type: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        爬取多个品牌的产品图片
        
        Args:
            brands: 品牌列表
            product_type: 产品类型
        
        Returns:
            品牌图片字典 {brand_name: [image_data]}
        """
        tasks = []
        for brand in brands:
            tasks.append(self._crawl_single_brand(brand, product_type))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        brand_images = {}
        for brand, result in zip(brands, results):
            if isinstance(result, Exception):
                print(f"爬取 {brand} 图片失败: {result}")
                brand_images[brand] = []
            else:
                brand_images[brand] = result
        
        return brand_images
    
    async def _crawl_single_brand(self, brand: str, product_type: str) -> List[Dict[str, Any]]:
        """爬取单个品牌的图片"""
        search_query = f"{brand} {product_type}"
        all_images = []
        
        print(f"[ImageCrawler] 开始爬取品牌: {brand}")
        
        # 尝试多个图片源
        sources = [
            self._crawl_unsplash,
            self._crawl_pexels,
            self._crawl_pixabay,
            self._crawl_bing,
        ]
        
        for source_func in sources:
            try:
                print(f"[ImageCrawler] 尝试从 {source_func.__name__} 爬取 {brand}...")
                images = await asyncio.wait_for(source_func(search_query), timeout=10)
                print(f"[ImageCrawler] 从 {source_func.__name__} 获取到 {len(images)} 张图片")
                all_images.extend(images)
                
                # 如果已经获取足够的图片，停止
                if len(all_images) >= self.images_per_brand:
                    print(f"[ImageCrawler] {brand} 已获取足够图片 ({len(all_images)})")
                    break
            except asyncio.TimeoutError:
                print(f"[ImageCrawler] 从 {source_func.__name__} 爬取超时")
                continue
            except Exception as e:
                print(f"[ImageCrawler] 从 {source_func.__name__} 爬取失败: {e}")
                continue
        
        print(f"[ImageCrawler] {brand} 最终获取 {len(all_images)} 张图片")
        
        # 返回指定数量的图片
        return all_images[:self.images_per_brand]
    
    async def _crawl_unsplash(self, query: str) -> List[Dict[str, Any]]:
        """从 Unsplash 爬取图片"""
        url = f"https://unsplash.com/napi/search/photos"
        params = {
            "query": query,
            "per_page": 20,
            "page": 1
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        images = []
                        
                        for item in data.get("results", []):
                            images.append({
                                "brand": query.split()[0],
                                "url": item.get("urls", {}).get("regular"),
                                "thumbnail": item.get("urls", {}).get("thumb"),
                                "title": item.get("description", ""),
                                "source": "unsplash.com",
                                "width": item.get("width", 0),
                                "height": item.get("height", 0)
                            })
                        
                        return images
                    else:
                        print(f"Unsplash 返回状态码: {response.status}")
                        return []
        except Exception as e:
            print(f"Unsplash 爬取失败: {e}")
            return []
    
    async def _crawl_pexels(self, query: str) -> List[Dict[str, Any]]:
        """从 Pexels 爬取图片"""
        # Pexels 需要 API Key，这里使用网页爬取
        url = f"https://www.pexels.com/search/{query.replace(' ', '%20')}/"
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        images = []
                        
                        # 查找图片元素
                        img_elements = soup.find_all('img', class_=re.compile('photo-item'))
                        
                        for img in img_elements[:10]:
                            src = img.get('src') or img.get('data-src')
                            if src and 'images.pexels.com' in src:
                                images.append({
                                    "brand": query.split()[0],
                                    "url": src,
                                    "thumbnail": src,
                                    "title": img.get('alt', ''),
                                    "source": "pexels.com",
                                    "width": 0,
                                    "height": 0
                                })
                        
                        return images
                    else:
                        print(f"Pexels 返回状态码: {response.status}")
                        return []
        except Exception as e:
            print(f"Pexels 爬取失败: {e}")
            return []
    
    async def _crawl_pixabay(self, query: str) -> List[Dict[str, Any]]:
        """从 Pixabay 爬取图片"""
        url = f"https://pixabay.com/api/"
        
        # Pixabay 需要 API Key，这里使用网页爬取
        web_url = f"https://pixabay.com/images/search/{query.replace(' ', '%20')}/"
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(web_url, headers=self.headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        images = []
                        
                        # 查找图片元素
                        img_elements = soup.find_all('img', {'data-lazy': True})
                        
                        for img in img_elements[:10]:
                            src = img.get('data-lazy') or img.get('src')
                            if src and 'pixabay.com' in src:
                                images.append({
                                    "brand": query.split()[0],
                                    "url": src,
                                    "thumbnail": src,
                                    "title": img.get('alt', ''),
                                    "source": "pixabay.com",
                                    "width": 0,
                                    "height": 0
                                })
                        
                        return images
                    else:
                        print(f"Pixabay 返回状态码: {response.status}")
                        return []
        except Exception as e:
            print(f"Pixabay 爬取失败: {e}")
            return []
    
    async def _crawl_bing(self, query: str) -> List[Dict[str, Any]]:
        """从 Bing Images 爬取图片"""
        url = f"https://www.bing.com/images/search"
        params = {
            "q": query,
            "first": 1,
            "count": 20
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params, headers=self.headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        images = []
                        
                        # 查找图片链接
                        img_elements = soup.find_all('a', class_='iusc')
                        
                        for element in img_elements[:10]:
                            m = element.get('m')
                            if m:
                                try:
                                    import json
                                    data = json.loads(m)
                                    images.append({
                                        "brand": query.split()[0],
                                        "url": data.get('murl'),
                                        "thumbnail": data.get('turl'),
                                        "title": data.get('t', ''),
                                        "source": "bing.com",
                                        "width": 0,
                                        "height": 0
                                    })
                                except:
                                    continue
                        
                        return images
                    else:
                        print(f"Bing 返回状态码: {response.status}")
                        return []
        except Exception as e:
            print(f"Bing 爬取失败: {e}")
            return []
    
    async def crawl_by_keywords(
        self,
        image_keywords: Dict[str, str],
        max_retries: int = 3
    ) -> Dict[str, str]:
        """
        根据关键词爬取图片（新增方法）
        
        Args:
            image_keywords: 图片关键词字典 {image_id: keyword}
            max_retries: 最大重试次数
        
        Returns:
            图片URL字典 {image_id: url}
        """
        print(f"\n{'='*60}")
        print(f"🖼️ 根据关键词爬取图片")
        print(f"{'='*60}")
        print(f"需要爬取: {len(image_keywords)} 张图片")
        print(f"{'='*60}\n")
        
        image_urls = {}
        
        for image_id, keyword in image_keywords.items():
            # 跳过用户上传的图片
            if keyword == "USER_UPLOADED":
                print(f"[ImageCrawler] {image_id}: 用户上传（跳过）")
                image_urls[image_id] = "USER_UPLOADED"
                continue
            
            print(f"[ImageCrawler] {image_id}: 搜索 '{keyword}'")
            
            # 尝试爬取
            for attempt in range(max_retries):
                try:
                    images = await self._crawl_single_brand(keyword, "")
                    
                    if images and len(images) > 0:
                        # 使用第一张图片
                        image_urls[image_id] = images[0]['url']
                        print(f"[ImageCrawler] ✓ {image_id}: 成功获取图片")
                        break
                    else:
                        print(f"[ImageCrawler] ⚠️ {image_id}: 未找到图片 (尝试 {attempt+1}/{max_retries})")
                        
                except Exception as e:
                    print(f"[ImageCrawler] ✗ {image_id}: 爬取失败 - {e} (尝试 {attempt+1}/{max_retries})")
                
                # 如果是最后一次尝试仍失败
                if attempt == max_retries - 1:
                    print(f"[ImageCrawler] ✗ {image_id}: 所有尝试失败，使用占位图")
                    image_urls[image_id] = None
        
        print(f"\n{'='*60}")
        print(f"✅ 图片爬取完成")
        print(f"{'='*60}")
        print(f"成功: {sum(1 for v in image_urls.values() if v and v != 'USER_UPLOADED')} 张")
        print(f"用户上传: {sum(1 for v in image_urls.values() if v == 'USER_UPLOADED')} 张")
        print(f"失败: {sum(1 for v in image_urls.values() if v is None)} 张")
        print(f"{'='*60}\n")
        
        return image_urls
    
    async def download_images(
        self,
        image_urls: Dict[str, str],
        output_dir: str
    ) -> Dict[str, str]:
        """
        批量下载图片（新增方法）
        
        Args:
            image_urls: 图片URL字典 {image_id: url}
            output_dir: 输出目录
        
        Returns:
            本地路径字典 {image_id: local_path}
        """
        print(f"\n{'='*60}")
        print(f"📥 批量下载图片")
        print(f"{'='*60}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        local_paths = {}
        
        for image_id, url in image_urls.items():
            if url == "USER_UPLOADED":
                print(f"[ImageCrawler] {image_id}: 用户上传（跳过下载）")
                local_paths[image_id] = "USER_UPLOADED"
                continue
            
            if url is None:
                print(f"[ImageCrawler] {image_id}: 无URL（跳过）")
                local_paths[image_id] = None
                continue
            
            # 生成文件名
            file_ext = Path(url).suffix or '.jpg'
            file_name = f"{image_id}{file_ext}"
            save_path = output_path / file_name
            
            print(f"[ImageCrawler] {image_id}: 下载中...")
            
            success = await self.download_image(url, str(save_path))
            
            if success:
                local_paths[image_id] = str(save_path)
                print(f"[ImageCrawler] ✓ {image_id}: 下载成功")
            else:
                local_paths[image_id] = None
                print(f"[ImageCrawler] ✗ {image_id}: 下载失败")
        
        print(f"\n{'='*60}")
        print(f"✅ 下载完成")
        print(f"{'='*60}")
        print(f"成功: {sum(1 for v in local_paths.values() if v and v != 'USER_UPLOADED')} 张")
        print(f"失败: {sum(1 for v in local_paths.values() if v is None)} 张")
        print(f"{'='*60}\n")
        
        return local_paths
    
    async def download_image(self, url: str, save_path: str) -> bool:
        """
        下载图片到本地
        
        Args:
            url: 图片 URL
            save_path: 保存路径
        
        Returns:
            是否成功
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=self.timeout) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # 确保目录存在
                        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(save_path, 'wb') as f:
                            f.write(content)
                        
                        return True
                    else:
                        print(f"下载图片失败: {url}, 状态码: {response.status}")
                        return False
        except Exception as e:
            print(f"下载图片异常: {url}, 错误: {e}")
            return False
