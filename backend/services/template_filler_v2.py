"""
TemplateFiller V2 - 增强版模板填充器
支持产品卡片的优点/缺点列表智能替换
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional, List


class TemplateFiller:
    """模板填充器V2：智能处理产品卡片结构"""
    
    def __init__(self, template_path: str, product_cards_structure_path: Optional[str] = None):
        """
        初始化模板填充器
        
        Args:
            template_path: 模板 HTML 文件路径
            product_cards_structure_path: 产品卡片结构文件路径
        """
        self.template_path = Path(template_path)
        
        if not self.template_path.exists():
            raise FileNotFoundError(f"模板文件不存在: {template_path}")
        
        # 读取模板
        with open(self.template_path, 'r', encoding='utf-8') as f:
            self.template_html = f.read()
        
        self.soup = BeautifulSoup(self.template_html, 'html.parser')
        
        # 加载产品卡片结构
        if product_cards_structure_path is None:
            product_cards_structure_path = Path(__file__).parent.parent / "product_cards_structure.json"
        
        self.cards_structure_path = Path(product_cards_structure_path)
        if self.cards_structure_path.exists():
            with open(self.cards_structure_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.original_cards = data.get('product_cards', [])
        else:
            print(f"[TemplateFiller] ⚠️ 产品卡片结构文件不存在: {product_cards_structure_path}")
            self.original_cards = []
        
        print(f"[TemplateFiller] 已加载模板: {self.template_path}")
        print(f"[TemplateFiller] 已加载 {len(self.original_cards)} 个产品卡片结构")
    
    def fill_template(
        self,
        content_data: Dict[str, Any],
        image_urls: Dict[str, str],
        user_image_path: Optional[str] = None,
        winner_brand: Optional[str] = None
    ) -> str:
        """
        填充模板
        
        Args:
            content_data: 生成的内容数据 (包含 product_cards, headings, paragraphs, buttons)
            image_urls: 图片URL字典 {image_id: url}
            user_image_path: 用户上传的图片路径
            winner_brand: Winner产品的品牌名称（用于Logo alt文本）
        
        Returns:
            填充后的 HTML
        """
        print(f"\n{'='*60}")
        print(f"🎨 开始填充模板 (V2)")
        print(f"{'='*60}\n")
        
        # 1. 替换产品卡片（优先）
        if 'product_cards' in content_data:
            self._fill_product_cards(content_data['product_cards'])
        
        # 2. 替换标题
        if 'headings' in content_data:
            self._fill_headings(content_data['headings'])
        
        # 3. 替换段落
        if 'paragraphs' in content_data:
            self._fill_paragraphs(content_data['paragraphs'])
        
        # 4. 替换其他列表
        if 'other_lists' in content_data:
            self._fill_other_lists(content_data['other_lists'])
        
        # 5. 替换按钮
        if 'buttons' in content_data:
            self._fill_buttons(content_data['buttons'])
        
        # 6. 替换 disclaimer
        if 'disclaimer' in content_data:
            self._fill_disclaimer(content_data['disclaimer'])
        
        # 7. 替换图片
        self._fill_images(image_urls, user_image_path, winner_brand)
        
        print(f"\n{'='*60}")
        print(f"✅ 模板填充完成")
        print(f"{'='*60}\n")
        
        return str(self.soup)
    
    def _fill_product_cards(self, new_cards: List[Dict[str, Any]]):
        """
        替换产品卡片内容（包括优点和缺点列表）
        所有Winner卡片（rank=1）使用统一的文案
        
        Args:
            new_cards: 新的产品卡片数据
        """
        print(f"[TemplateFiller] 替换产品卡片...")
        
        if not new_cards:
            print(f"[TemplateFiller] ⚠️ 没有产品卡片数据")
            return
        
        # 找到Winner卡片（rank=1）
        winner_card = None
        for card in new_cards:
            if card.get('rank') == 1:
                winner_card = card
                break
        
        # 遍历所有原始卡片结构
        for i, original_card in enumerate(self.original_cards):
            # 判断当前卡片是Winner还是竞品
            original_rank = original_card.get('rank')
            
            # 如果是Winner卡片（rank="1"），使用Winner数据
            if original_rank == "1" and winner_card:
                new_card = winner_card
                print(f"\n[TemplateFiller] 处理Winner卡片 #{i+1}: {new_card.get('product_name', 'Unknown')} (使用统一文案)")
            # 如果是竞品卡片，使用对应的竞品数据
            elif original_rank in ["2", "3", "4", "5"]:
                rank_index = int(original_rank) - 1  # rank 2 -> index 1
                if rank_index < len(new_cards):
                    new_card = new_cards[rank_index]
                    print(f"\n[TemplateFiller] 处理竞品卡片 #{original_rank}: {new_card.get('product_name', 'Unknown')}")
                else:
                    print(f"\n[TemplateFiller] ⚠️ 跳过卡片 #{i+1}: 没有对应的数据")
                    continue
            else:
                print(f"\n[TemplateFiller] ⚠️ 跳过卡片 #{i+1}: 未知rank")
                continue
            
            # 替换产品名称
            if 'product_name' in new_card and 'html_structure' in original_card:
                self._replace_by_content_id(
                    original_card['html_structure'].get('product_name', {}).get('data_content_id'),
                    new_card['product_name']
                )
            
            # 替换评分
            if 'rating_score' in new_card:
                self._replace_by_content_id(
                    original_card['html_structure'].get('rating_score', {}).get('data_content_id'),
                    str(new_card['rating_score'])
                )
            
            # 替换评分标题
            if 'rating_title' in new_card:
                self._replace_by_content_id(
                    original_card['html_structure'].get('rating_title', {}).get('data_content_id'),
                    new_card['rating_title']
                )
            
            # 替换评论数
            if 'review_count' in new_card:
                self._replace_by_content_id(
                    original_card['html_structure'].get('review_count', {}).get('data_content_id'),
                    new_card['review_count']
                )
            
            # 替换折扣标题（如果有）
            if 'discount_heading' in new_card and new_card['discount_heading']:
                self._replace_by_content_id(
                    original_card['html_structure'].get('discount_heading', {}).get('data_content_id'),
                    new_card['discount_heading']
                )
            
            # 替换CTA按钮（所有卡片都替换，包括Winner）
            if 'cta_button_text' in new_card:
                # 替换主CTA按钮
                self._replace_by_content_id(
                    original_card['html_structure'].get('cta_button', {}).get('data_content_id'),
                    new_card['cta_button_text']
                )
                
                # 替换所有额外的CTA按钮（如果有）
                if 'all_cta_buttons' in original_card['html_structure']:
                    for extra_btn in original_card['html_structure']['all_cta_buttons'][1:]:  # 跳过第一个（已处理）
                        self._replace_by_content_id(
                            extra_btn['data_content_id'],
                            new_card['cta_button_text']
                        )
            
            # 替换优点列表
            if 'pros' in new_card:
                pros_content_id = original_card['html_structure'].get('pros', {}).get('data_content_id')
                self._replace_list_by_content_id(pros_content_id, new_card['pros'], icon_class='far fa-hand-point-right')
                print(f"  ✓ 替换了 {len(new_card['pros'])} 个优点")
            
            # 替换缺点列表
            if 'cons' in new_card:
                cons_content_id = original_card['html_structure'].get('cons', {}).get('data_content_id')
                self._replace_list_by_content_id(cons_content_id, new_card['cons'], icon_class='far fa-times-circle')
                print(f"  ✓ 替换了 {len(new_card['cons'])} 个缺点")
        
        print(f"\n[TemplateFiller] ✓ 已替换所有产品卡片")
    
    def _replace_by_content_id(self, content_id: Optional[str], new_text: str):
        """
        根据 data-content-id 替换元素文本（保留原有标签）
        
        Args:
            content_id: data-content-id 属性值
            new_text: 新文本
        """
        if not content_id:
            return
        
        elem = self.soup.find(attrs={'data-content-id': content_id})
        if elem:
            # 保留HTML标签和属性，只替换文本内容
            # 清空所有子节点（包括文本和标签）
            for child in list(elem.children):
                child.extract()
            
            # 设置新的文本内容
            elem.string = new_text
    
    def _replace_list_by_content_id(self, content_id: Optional[str], items: List[str], icon_class: str = ''):
        """
        根据 data-content-id 替换列表内容
        
        Args:
            content_id: data-content-id 属性值
            items: 新的列表项
            icon_class: 图标类名
        """
        if not content_id or not items:
            return
        
        ul_elem = self.soup.find('ul', attrs={'data-content-id': content_id})
        if not ul_elem:
            return
        
        # 获取第一个 li 作为模板
        template_li = ul_elem.find('li', class_='elementor-icon-list-item')
        if not template_li:
            return
        
        # 清空列表
        ul_elem.clear()
        
        # 为每个新项创建 li
        for i, item_text in enumerate(items):
            # 克隆模板 li
            new_li = self.soup.new_tag('li', **{'class': 'elementor-icon-list-item', 'data-content-id': f'{content_id}_item_{i}'})
            
            # 创建图标 span
            icon_span = self.soup.new_tag('span', **{'class': 'elementor-icon-list-icon'})
            icon_i = self.soup.new_tag('i', **{'aria-hidden': 'true', 'class': icon_class})
            icon_span.append(icon_i)
            icon_span.append(' ')
            
            # 创建文本 span
            text_span = self.soup.new_tag('span', **{'class': 'elementor-icon-list-text'})
            text_span.string = item_text
            
            # 组装 li
            new_li.append(icon_span)
            new_li.append(text_span)
            
            # 添加到 ul
            ul_elem.append(new_li)
    
    def _fill_headings(self, headings: List[str]):
        """替换标题（非产品卡片部分）"""
        print(f"[TemplateFiller] 替换其他标题...")
        
        if not headings:
            return
        
        # 收集所有产品卡片相关的 content_id（需要跳过的）
        card_content_ids = set()
        for card in self.original_cards:
            if 'html_structure' in card:
                # 产品名称
                if card['html_structure'].get('product_name', {}).get('data_content_id'):
                    card_content_ids.add(card['html_structure']['product_name']['data_content_id'])
                # 评分分数
                if card['html_structure'].get('rating_score', {}).get('data_content_id'):
                    card_content_ids.add(card['html_structure']['rating_score']['data_content_id'])
                # 评分标题
                if card['html_structure'].get('rating_title', {}).get('data_content_id'):
                    card_content_ids.add(card['html_structure']['rating_title']['data_content_id'])
                # 折扣标题
                if card['html_structure'].get('discount_heading', {}).get('data_content_id'):
                    card_content_ids.add(card['html_structure']['discount_heading']['data_content_id'])
        
        count = 0
        heading_index = 0
        # 查找所有标题元素
        all_headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading_elem in all_headings:
            # 跳过产品卡片内的标题（已经处理过）
            content_id = heading_elem.get('data-content-id')
            if content_id and content_id in card_content_ids:
                print(f"[TemplateFiller] 跳过产品卡片标题: {content_id}")
                continue
            
            # 替换为新标题
            if heading_index < len(headings):
                heading_elem.string = headings[heading_index]
                heading_index += 1
                count += 1
        
        print(f"[TemplateFiller] ✓ 已替换 {count} 个其他标题")
    
    def _fill_paragraphs(self, paragraphs: List[str]):
        """替换段落（跳过产品卡片内的段落和免责声明）"""
        print(f"[TemplateFiller] 替换段落...")
        
        if not paragraphs:
            return
        
        # 收集需要跳过的段落 content_id
        skip_paragraph_ids = set()
        
        # 1. 跳过产品卡片内的段落（review_count）
        for card in self.original_cards:
            if 'html_structure' in card:
                if card['html_structure'].get('review_count', {}).get('data_content_id'):
                    skip_paragraph_ids.add(card['html_structure']['review_count']['data_content_id'])
        
        # 2. 跳过免责声明段落（通常是最后两个段落）
        # 我们通过检查段落内容来识别
        all_paragraphs = self.soup.find_all('p')
        for p in all_paragraphs:
            text = p.get_text(strip=True)
            if 'Affiliate Disclosure' in text or 'Disclaimer' in text or \
               ('not intended or implied to be a substitute' in text and len(text) > 200):
                content_id = p.get('data-content-id')
                if content_id:
                    skip_paragraph_ids.add(content_id)
        
        count = 0
        paragraph_index = 0
        
        for p_elem in all_paragraphs:
            content_id = p_elem.get('data-content-id')
            
            # 跳过产品卡片和免责声明的段落
            if content_id and content_id in skip_paragraph_ids:
                continue
            
            # 替换段落
            if paragraph_index < len(paragraphs):
                p_elem.string = paragraphs[paragraph_index]
                paragraph_index += 1
                count += 1
        
        print(f"[TemplateFiller] ✓ 已替换 {count} 个段落")
    
    def _fill_other_lists(self, other_lists: List[List[str]]):
        """替换其他列表（非产品卡片的列表）"""
        print(f"[TemplateFiller] 替换其他列表...")
        
        if not other_lists:
            return
        
        # 收集所有产品卡片相关的列表 content_id（需要跳过的）
        card_list_ids = set()
        for card in self.original_cards:
            if 'html_structure' in card:
                if card['html_structure'].get('pros', {}).get('data_content_id'):
                    card_list_ids.add(card['html_structure']['pros']['data_content_id'])
                if card['html_structure'].get('cons', {}).get('data_content_id'):
                    card_list_ids.add(card['html_structure']['cons']['data_content_id'])
        
        # 查找所有列表元素（ul 和 ol）
        all_lists = self.soup.find_all(['ul', 'ol'])
        
        list_index = 0
        count = 0
        
        for list_elem in all_lists:
            # 跳过产品卡片内的列表
            content_id = list_elem.get('data-content-id')
            if content_id and content_id in card_list_ids:
                continue
            
            # 替换为新列表内容
            if list_index < len(other_lists):
                new_items = other_lists[list_index]
                
                # 清空列表
                list_elem.clear()
                
                # 添加新的列表项
                for i, item_text in enumerate(new_items):
                    new_li = self.soup.new_tag('li', **{'data-content-id': f'{content_id}_item_{i}' if content_id else f'li_new_{i}'})
                    new_li.string = item_text
                    list_elem.append(new_li)
                
                print(f"  ✓ 替换列表 {content_id or '(无ID)'}: {len(new_items)} 项")
                list_index += 1
                count += 1
        
        print(f"[TemplateFiller] ✓ 已替换 {count} 个其他列表")
    
    def _fill_disclaimer(self, disclaimer: Dict[str, str]):
        """替换免责声明"""
        print(f"[TemplateFiller] 替换免责声明...")
        
        if not disclaimer:
            return
        
        # 查找包含 "Affiliate Disclosure" 或 "Disclaimer" 的段落
        all_paragraphs = self.soup.find_all('p')
        
        disclaimer_found = False
        for i, p in enumerate(all_paragraphs):
            text = p.get_text(strip=True)
            
            # 找到标题段落
            if 'Affiliate Disclosure' in text or 'Disclaimer' in text:
                # 替换标题
                if 'title' in disclaimer:
                    p.string = disclaimer['title']
                    print(f"  ✓ 替换免责声明标题")
                
                # 替换下一个段落（内容）
                if i + 1 < len(all_paragraphs) and 'content' in disclaimer:
                    all_paragraphs[i + 1].string = disclaimer['content']
                    print(f"  ✓ 替换免责声明内容")
                
                disclaimer_found = True
                break
        
        if disclaimer_found:
            print(f"[TemplateFiller] ✓ 已替换免责声明")
        else:
            print(f"[TemplateFiller] ⚠️ 未找到免责声明位置")
    
    def _fill_buttons(self, buttons: List[str]):
        """替换按钮（跳过排名按钮和产品卡片CTA按钮）"""
        print(f"[TemplateFiller] 替换按钮...")
        
        if not buttons:
            return
        
        # 收集需要跳过的按钮 content_id
        skip_button_ids = set()
        
        # 1. 跳过产品卡片的所有CTA按钮
        for card in self.original_cards:
            if 'html_structure' in card:
                # 主CTA按钮
                if card['html_structure'].get('cta_button', {}).get('data_content_id'):
                    skip_button_ids.add(card['html_structure']['cta_button']['data_content_id'])
                
                # 所有额外的CTA按钮
                if 'all_cta_buttons' in card['html_structure']:
                    for btn in card['html_structure']['all_cta_buttons']:
                        skip_button_ids.add(btn['data_content_id'])
        
        # 2. 跳过排名按钮（这些是产品卡片上方的排名标签按钮，应该保持原样）
        rank_button_ids = ['link_1', 'link_5', 'link_7', 'link_9', 'link_11', 'link_13', 'link_22']
        skip_button_ids.update(rank_button_ids)
        
        count = 0
        all_buttons = self.soup.find_all('a', class_='elementor-button')
        
        for i, text in enumerate(buttons):
            if i >= len(all_buttons):
                break
            
            button_elem = all_buttons[i]
            content_id = button_elem.get('data-content-id')
            
            # 跳过排名按钮和产品卡片CTA按钮
            if content_id and content_id in skip_button_ids:
                print(f"[TemplateFiller] 跳过排名/CTA按钮: {content_id}")
                continue
            
            span = button_elem.find('span', class_='elementor-button-text')
            if span:
                span.string = text
            else:
                button_elem.string = text
            
            count += 1
        
        print(f"[TemplateFiller] ✓ 已替换 {count} 个按钮")
    
    def _fill_images(self, image_urls: Dict[str, str], user_image_path: Optional[str] = None, winner_brand: Optional[str] = None):
        """替换图片"""
        print(f"[TemplateFiller] 替换图片...")
        
        if not image_urls:
            print(f"[TemplateFiller] ⚠️ 没有图片数据")
            return
        
        count = 0
        all_images = self.soup.find_all('img')
        
        print(f"[TemplateFiller] 找到 {len(all_images)} 个图片元素")
        print(f"[TemplateFiller] 需要替换 {len(image_urls)} 个图片")
        
        for image_id, url in image_urls.items():
            # 处理用户上传的图片
            if url == "USER_UPLOADED":
                if user_image_path:
                    url = user_image_path
                else:
                    print(f"[TemplateFiller] ⚠️ {image_id}: 缺少用户上传的图片")
                    continue
            
            # 跳过失败的图片
            if url is None or url == "":
                print(f"[TemplateFiller] ⚠️ {image_id}: 图片URL为空，跳过")
                continue
            
            # 从 image_id 提取索引 (例如 "image_1" -> 0)
            try:
                index = int(image_id.split('_')[1]) - 1
            except (IndexError, ValueError):
                print(f"[TemplateFiller] ⚠️ {image_id}: 无效的图片ID格式")
                continue
            
            if index >= len(all_images):
                print(f"[TemplateFiller] ⚠️ {image_id}: 索引超出范围 ({index} >= {len(all_images)})")
                continue
            
            img = all_images[index]
            
            # 替换图片 URL
            old_src = img.get('src', '')
            img['src'] = url
            
            # 同时更新 srcset 和 data-src (如果存在)
            if img.get('srcset'):
                img['srcset'] = url
            if img.get('data-src'):
                img['data-src'] = url
            
            # 🆕 如果是Logo图片（image_12）且提供了品牌名称，更新alt文本
            if image_id == 'image_12' and winner_brand:
                old_alt = img.get('alt', '')
                new_alt = f"{winner_brand} Logo"
                img['alt'] = new_alt
                print(f"[TemplateFiller] ✓ {image_id}: 更新Logo alt文本: '{old_alt}' -> '{new_alt}'")
            
            print(f"[TemplateFiller] ✓ {image_id}: {old_src[:50]}... -> {url[:50]}...")
            count += 1
        
        print(f"[TemplateFiller] ✓ 已替换 {count} 个图片")
    
    def save(self, output_path: str):
        """
        保存填充后的模板
        
        Args:
            output_path: 输出文件路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(self.soup))
        
        print(f"[TemplateFiller] 💾 已保存到: {output_file}")
