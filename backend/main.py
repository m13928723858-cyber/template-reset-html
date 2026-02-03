import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import shutil
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量（确保从正确的路径加载）
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# 打印调试信息
print(f"加载 .env 文件: {env_path}")
print(f"DOLPHIN_API_KEY 是否设置: {'是' if os.getenv('DOLPHIN_API_KEY') else '否'}")
if os.getenv('DOLPHIN_API_KEY'):
    print(f"DOLPHIN_API_KEY 前10位: {os.getenv('DOLPHIN_API_KEY')[:10]}...")

# 核心服务
from services.image_crawler import ImageCrawler
from services.competitor_generator import CompetitorGenerator
from services.content_generator import ContentGenerator
from services.template_filler_v2 import TemplateFiller
from utils.task_manager import TaskManager
import json
import asyncio

app = FastAPI(title="AI智能页面生成系统 API", version="2.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化目录
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./outputs"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", "./temp"))

for directory in [UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 任务管理器
task_manager = TaskManager()

# Pydantic 模型
class GenerateRequest(BaseModel):
    """生成页面请求模型"""
    winner_name: str
    product_type: str
    user_image_url: Optional[str] = None

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: Dict[str, Any]
    error: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "AI智能页面生成系统 API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.post("/api/upload-image")
async def upload_image_only(file: UploadFile = File(...)):
    """上传用户产品图片"""
    try:
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail=f"只支持图片格式，当前类型: {file.content_type}")
        
        # 生成唯一文件名
        image_id = str(uuid.uuid4())
        image_path = UPLOAD_DIR / f"user_{image_id}{Path(file.filename).suffix}"
        
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "image_id": image_id,
            "image_url": str(image_path),
            "message": "图片上传成功"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    """获取任务状态"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return task

@app.get("/api/download/{task_id}")
async def download_result(task_id: str):
    """下载处理后的文件"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="任务尚未完成")
    
    output_file = task.get("output_file")
    if not output_file or not os.path.exists(output_file):
        raise HTTPException(status_code=404, detail="输出文件不存在")
    
    return FileResponse(
        output_file,
        media_type="application/zip",
        filename=f"brand_swap_{task_id}.zip"
    )

@app.delete("/api/task/{task_id}")
async def delete_task(task_id: str):
    """删除任务及相关文件"""
    try:
        task = task_manager.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 删除相关文件
        upload_file = UPLOAD_DIR / f"{task_id}.zip"
        if upload_file.exists():
            upload_file.unlink()
        
        temp_dir = TEMP_DIR / task_id
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        
        output_file = task.get("output_file")
        if output_file and os.path.exists(output_file):
            os.unlink(output_file)
        
        # 删除任务记录
        task_manager.delete_task(task_id)
        
        return {"message": "任务已删除"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

@app.post("/api/generate")
async def generate_page(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    生成页面API：直接生成页面（不需要上传ZIP）
    只需要提供 Winner 名称、产品类型和用户图片
    """
    try:
        # 生成任务 ID
        task_id = str(uuid.uuid4())
        
        # 创建任务
        task_manager.create_task(task_id, "")
        
        # 在后台处理
        background_tasks.add_task(
            process_generate,
            task_id,
            request.winner_name,
            request.product_type,
            request.user_image_url
        )
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": "任务已开始处理"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")

async def process_generate(task_id: str, winner_name: str, product_type: str, user_image_url: Optional[str]):
    """
    生成页面的主要逻辑：不需要ZIP文件，直接生成页面
    """
    try:
        print(f"\n{'='*60}")
        print(f"[Task {task_id}] 新架构 - 开始处理")
        print(f"  - Winner: {winner_name}")
        print(f"  - 产品类型: {product_type}")
        print(f"  - 用户图片: {user_image_url}")
        print(f"{'='*60}\n")
        
        # 更新状态
        task_manager.update_task(task_id, {
            "status": "processing",
            "progress": {
                "stage": "initializing",
                "percentage": 0,
                "message": "初始化..."
            }
        })
        
        # Step 1: 生成竞品
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "generating_competitors",
                "percentage": 10,
                "message": "正在生成竞品..."
            }
        })
        
        comp_gen = CompetitorGenerator()
        competitors = await comp_gen.generate(winner_name, product_type, num_competitors=4)
        
        print(f"[Task {task_id}] 生成竞品: {competitors}")
        
        # 确保有4个竞品
        if len(competitors) < 4:
            print(f"[Task {task_id}] ⚠️ 竞品数量不足，补充到4个")
            while len(competitors) < 4:
                competitors.append(f"Generic {product_type} Brand {len(competitors) + 1}")
        
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "competitors_generated",
                "percentage": 20,
                "message": f"已生成4个竞品: {', '.join(competitors)}",
                "competitors": competitors
            }
        })
        
        # Step 2: 生成内容
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "generating_content",
                "percentage": 30,
                "message": "正在生成营销文案..."
            }
        })
        
        # 加载 compact_template_v2（包含 other_lists）
        compact_template_path = Path(__file__).parent / "compact_template_v2.json"
        with open(compact_template_path, 'r', encoding='utf-8') as f:
            compact_template = json.load(f)
        
        content_gen = ContentGenerator()
        content_result = await content_gen.generate(
            winner_name=winner_name,
            product_type=product_type,
            competitors=competitors,
            compact_template=compact_template
        )
        
        print(f"[Task {task_id}] 内容生成完成")
        
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "content_generated",
                "percentage": 50,
                "message": f"已生成 {len(content_result['content']['headings'])} 个标题、{len(content_result['content']['paragraphs'])} 个段落",
                "token_usage": content_result['token_usage']['total_tokens']
            }
        })
        
        # Step 3: 爬取图片
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "crawling_images",
                "percentage": 60,
                "message": "正在爬取产品图片..."
            }
        })
        
        crawler = ImageCrawler()
        image_urls = await crawler.crawl_by_keywords(content_result['image_keywords'])
        
        print(f"[Task {task_id}] 图片爬取完成")
        
        # 下载图片到本地
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "downloading_images",
                "percentage": 70,
                "message": "正在下载图片到本地..."
            }
        })
        
        # 创建图片保存目录（使用 image 文件夹，与模板一致）
        images_dir = OUTPUT_DIR / task_id / "image"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # 下载图片
        local_image_paths = await crawler.download_images(image_urls, str(images_dir))
        
        # 处理用户上传的图片
        if user_image_url:
            for img_id, path in local_image_paths.items():
                if path == "USER_UPLOADED":
                    # 复制用户图片到输出目录
                    import shutil
                    user_img_path = Path(user_image_url)
                    if user_img_path.exists():
                        dest_path = images_dir / f"{img_id}{user_img_path.suffix}"
                        shutil.copy(user_img_path, dest_path)
                        local_image_paths[img_id] = f"./image/{dest_path.name}"
                        print(f"[Task {task_id}] 复制用户图片: {img_id}")
        
        # 转换为相对路径（使用 ./image/ 路径）
        relative_image_paths = {}
        for img_id, path in local_image_paths.items():
            if path and path != "USER_UPLOADED" and path is not None:
                # 转换为相对于HTML的路径
                relative_image_paths[img_id] = f"./image/{Path(path).name}"
            else:
                relative_image_paths[img_id] = path
        
        print(f"[Task {task_id}] 图片下载完成")
        
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "images_downloaded",
                "percentage": 75,
                "message": f"已下载 {sum(1 for v in local_image_paths.values() if v and v != 'USER_UPLOADED' and v is not None)} 张图片"
            }
        })
        
        # Step 4: 填充模板
        task_manager.update_task(task_id, {
            "progress": {
                "stage": "filling_template",
                "percentage": 85,
                "message": "正在填充模板..."
            }
        })
        
        template_path = Path(__file__).parent.parent / "top5Grounded Footwear" / "index.html"
        filler = TemplateFiller(str(template_path))
        
        # 🆕 提取Winner品牌名称（从content_result中获取）
        winner_brand = content_result.get('winner_brand', None)
        
        filled_html = filler.fill_template(
            content_data=content_result['content'],
            image_urls=relative_image_paths,
            user_image_path=None,  # 已经在 relative_image_paths 中处理
            winner_brand=winner_brand  # 🆕 传递品牌名称
        )
        
        # 保存结果
        output_dir = OUTPUT_DIR / task_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_html_path = output_dir / "index.html"
        filler.save(str(output_html_path))
        
        # 复制CSS和图片文件夹
        template_dir = Path(__file__).parent.parent / "top5Grounded Footwear"
        for item in ['css', 'image', 'images']:
            src = template_dir / item
            if src.exists():
                dst = output_dir / item
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
        
        # 打包成ZIP
        output_zip = OUTPUT_DIR / f"{task_id}.zip"
        shutil.make_archive(str(output_zip.with_suffix('')), 'zip', str(output_dir))
        
        print(f"[Task {task_id}] 处理完成")
        
        # 完成
        task_manager.update_task(task_id, {
            "status": "completed",
            "progress": {
                "stage": "completed",
                "percentage": 100,
                "message": "处理完成！"
            },
            "output_file": str(output_zip),
            "report": {
                "competitors": competitors,
                "token_usage": content_result['token_usage']['total_tokens'],
                "images_crawled": sum(1 for v in image_urls.values() if v and v != 'USER_UPLOADED'),
                "content_generated": {
                    "headings": len(content_result['content'].get('headings', [])),
                    "paragraphs": len(content_result['content'].get('paragraphs', [])),
                    "other_lists": len(content_result['content'].get('other_lists', [])),
                    "buttons": len(content_result['content'].get('buttons', [])),
                    "disclaimer": 'disclaimer' in content_result['content']
                }
            }
        })
        
    except Exception as e:
        print(f"[Task {task_id}] 处理失败: {e}")
        import traceback
        traceback.print_exc()
        
        task_manager.update_task(task_id, {
            "status": "failed",
            "error": str(e),
            "progress": {
                "stage": "failed",
                "percentage": 0,
                "message": f"处理失败: {str(e)}"
            }
        })

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
