"""
内容生成器：使用AI生成文案和图片搜索关键词
"""
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class ContentGenerator:
    """使用AI生成文案和图片搜索关键词"""
    
    def __init__(self):
        api_key = os.getenv("DOLPHIN_API_KEY")
        base_url = os.getenv("DOLPHIN_BASE_URL", "https://dolphin-chat.ihippogame.com/api/v1")
        
        if not api_key:
            raise ValueError("DOLPHIN_API_KEY 未设置")
        
        print(f"[ContentGenerator] 初始化 OpenAI 客户端")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        self.model = "gemini-3-flash-preview"  # 使用允许的模型
        
        # Token统计
        self.total_tokens_used = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.api_call_count = 0
    
    async def generate(
        self,
        compact_template: Dict[str, Any],
        winner_name: str,
        product_type: str,
        competitors: List[str]
    ) -> Dict[str, Any]:
        """
        生成新文案和图片搜索关键词
        
        Args:
            compact_template: 精简的模板数据
            winner_name: Winner产品名称
            product_type: 产品类型
            competitors: 竞品列表（4个）
        
        Returns:
            新内容数据结构
        """
        print(f"\n{'='*60}")
        print(f"🤖 开始生成内容")
        print(f"{'='*60}")
        print(f"Winner: {winner_name}")
        print(f"产品类型: {product_type}")
        print(f"竞品: {', '.join(competitors)}")
        print(f"{'='*60}\n")
        
        # 生成文案
        new_content = await self._generate_content(
            compact_template, winner_name, product_type, competitors
        )
        
        # 生成图片搜索关键词（包括品牌Logo）
        image_keywords, winner_brand = await self._generate_image_keywords(
            winner_name, product_type, competitors
        )
        
        # 合并结果
        result = {
            "winner_name": winner_name,
            "product_type": product_type,
            "competitors": competitors,
            "winner_brand": winner_brand,  # 🆕 添加品牌名称
            "content": new_content,
            "image_keywords": image_keywords,
            "token_usage": {
                "total_tokens": self.total_tokens_used,
                "prompt_tokens": self.total_prompt_tokens,
                "completion_tokens": self.total_completion_tokens,
                "api_calls": self.api_call_count
            }
        }
        
        print(f"\n{'='*60}")
        print(f"✅ 内容生成完成")
        print(f"{'='*60}")
        print(f"📊 Token消耗: {self.total_tokens_used:,}")
        print(f"📝 生成内容:")
        print(f"  - 标题: {len(new_content.get('headings', []))} 个")
        print(f"  - 段落: {len(new_content.get('paragraphs', []))} 个")
        print(f"  - 列表: {len(new_content.get('lists', []))} 个")
        print(f"  - 按钮: {len(new_content.get('buttons', []))} 个")
        print(f"🖼️ 图片关键词: {len(image_keywords)} 个")
        print(f"{'='*60}\n")
        
        return result
    
    async def _generate_content(
        self,
        compact_template: Dict[str, Any],
        winner_name: str,
        product_type: str,
        competitors: List[str]
    ) -> Dict[str, Any]:
        """生成新文案"""
        
        prompt = self._build_content_prompt(
            compact_template, winner_name, product_type, competitors
        )
        
        try:
            print(f"[ContentGenerator] 🤖 调用AI生成文案...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_message(product_type, winner_name)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=16000
            )
            
            # 记录token
            if hasattr(response, 'usage') and response.usage:
                self.api_call_count += 1
                self.total_prompt_tokens += response.usage.prompt_tokens
                self.total_completion_tokens += response.usage.completion_tokens
                self.total_tokens_used += response.usage.total_tokens
                
                print(f"[ContentGenerator] 📊 Token消耗:")
                print(f"  - 输入: {response.usage.prompt_tokens:,}")
                print(f"  - 输出: {response.usage.completion_tokens:,}")
                print(f"  - 总计: {response.usage.total_tokens:,}")
            
            result_text = response.choices[0].message.content.strip()
            
            # 解析JSON
            new_content = self._parse_json_response(result_text, compact_template)
            
            print(f"[ContentGenerator] ✓ 文案生成成功")
            
            return new_content
        
        except Exception as e:
            print(f"[ContentGenerator] ✗ 文案生成失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 返回原模板（回退）
            print(f"[ContentGenerator] ⚠️ 使用原模板作为回退")
            return compact_template
    
    def _build_content_prompt(
        self,
        compact_template: Dict[str, Any],
        winner_name: str,
        product_type: str,
        competitors: List[str]
    ) -> str:
        """构建文案生成prompt"""
        
        competitors_str = ', '.join(competitors)
        
        # 构建示例模板（包含产品卡片结构）
        sample_template = {
            "title": compact_template["title"],
            "headings": compact_template.get("headings", [])[:5],
            "paragraphs": compact_template.get("paragraphs", [])[:3],
            "product_cards": [
                {
                    "rank": 1,
                    "product_name": "Winner Product Name",
                    "rating_score": "9.8",
                    "rating_title": "\"The Ultimate Choice\"",
                    "review_count": "4,215 Reviews",
                    "discount_heading": "50% Off Limited Time",
                    "cta_button_text": "Visit Official Site",
                    "pros": [
                        "Specific feature 1 with details",
                        "Specific feature 2 with measurements",
                        "Specific feature 3 with benefits",
                        "Specific feature 4 with real-world use",
                        "Specific feature 5 with unique advantage"
                    ],
                    "cons": [
                        "Minor limitation 1 (acceptable trade-off)",
                        "Minor limitation 2 (not a deal-breaker)",
                        "Minor limitation 3 (manageable)",
                        "Minor limitation 4 (worth it for the benefits)",
                        "Minor limitation 5 (easily overlooked)"
                    ]
                },
                {
                    "rank": 2,
                    "product_name": "Competitor 1 Name",
                    "rating_score": "9.3",
                    "rating_title": "\"Good But Pricey\"",
                    "review_count": "2,150 Reviews",
                    "cta_button_text": "View Product",
                    "pros": [
                        "Specific feature 1",
                        "Specific feature 2",
                        "Specific feature 3",
                        "Specific feature 4",
                        "Specific feature 5"
                    ],
                    "cons": [
                        "Significant limitation 1",
                        "Significant limitation 2",
                        "Significant limitation 3",
                        "Significant limitation 4",
                        "Significant limitation 5"
                    ]
                }
            ],
            "buttons": compact_template.get("buttons", [])[:5],
            "other_lists": compact_template.get("other_lists", []),
            "disclaimer": {
                "title": "Affiliate Disclosure:",
                "content": "Disclaimer text about the product..."
            },
            "total_counts": {
                "headings": len(compact_template.get("headings", [])),
                "paragraphs": len(compact_template.get("paragraphs", [])),
                "product_cards": len(compact_template.get("product_cards", [])),
                "buttons": len(compact_template.get("buttons", [])),
                "other_lists": len(compact_template.get("other_lists", []))
            }
        }
        
        prompt = f"""You are a professional product reviewer and blogger specializing in {product_type} products. Write in American English with a conversational, personal tone as if sharing your hands-on testing experience.

TASK: Rewrite ALL content to create an in-depth product review article for "{winner_name}".

PRODUCT CONTEXT:
- Winner Product (MAIN): {winner_name}
- Product Type: {product_type}
- Competitors (for comparison): {competitors_str}

TEMPLATE STRUCTURE (showing examples):
{json.dumps(sample_template, indent=2, ensure_ascii=False)}

WRITING STYLE REQUIREMENTS:
1. **Tone & Voice**:
   - American English, conversational and relatable
   - Write as a reviewer sharing personal testing experience
   - Use phrases like "I tested", "In my experience", "After using for weeks"
   - Be enthusiastic but honest about the Winner product

2. **Introduction Paragraph** (MANDATORY):
   - MUST start with "Gone are the days when..."
   - Contrast old/traditional solutions with the Winner's modern approach
   - Example: "Gone are the days when you had to [old problem]. With {winner_name}, [new solution]..."
   - Make it engaging and relatable (3-4 sentences)

3. **Deep Dive Section** - "Why {winner_name} Is the Top Pick?":
   - Create a detailed analysis section with 3 core feature explanations
   - Each feature should have:
     * A descriptive heading (e.g., "Advanced Technology", "Superior Comfort")
     * 2-3 sentences explaining the feature in detail
     * Real-world benefits and use cases
   - End with a summary paragraph tying all features together

4. **Product Descriptions**:
   - Use vivid, descriptive language
   - Include sensory details (how it looks, feels, performs)
   - Mention real-world scenarios and use cases
   - Compare features naturally within the text

CRITICAL REQUIREMENTS:
1. **Return SAME JSON structure** - Generate ALL items (see total_counts above)
2. **Product Cards** - Generate {len(compact_template.get("product_cards", []))} cards:
   - Card #1 (Rank 1): {winner_name} - HERO product, EXACTLY 5 specific pros, EXACTLY 5 specific cons
   - Cards #2-5 (Rank 2-5): {competitors_str} - Competitors, EXACTLY 5 specific pros, EXACTLY 5 specific cons
   - Each card MUST have: product_name, rating_score, rating_title, review_count, pros[], cons[], cta_button_text
   - **Pros/Cons Quality Requirements**:
     * Each pro/con must be SPECIFIC and DETAILED (not generic)
     * Include real features, measurements, or tangible benefits
     * Winner pros should highlight unique advantages
     * Winner cons should be minor/acceptable trade-offs
     * Competitor cons should be more significant limitations
     * Examples of GOOD pros: "Waterproof up to 50 meters", "Battery lasts 3 days of heavy use", "Weighs only 150g"
     * Examples of BAD pros: "Good quality", "Nice design", "Works well" (too vague)
3. **Rating Score Format** - VERY IMPORTANT:
   - rating_score MUST be a numeric string (e.g., "9.8", "9.3", "8.5")
   - DO NOT use words or text for rating_score
   - Valid: "9.8", "9.5", "8.9"
   - Invalid: "Excellent", "9.8/10", "High"
   - Winner should have highest score (9.7-9.9)
   - Competitors should have lower scores (8.5-9.5)
4. **Rating Title Format** - Product-specific short quote:
   - rating_title should be a SHORT quoted phrase (3-5 words) that describes the product
   - Must be in quotes: "The Best Choice", "Premium Quality", "Great Value"
   - Each product should have a UNIQUE rating_title that reflects its characteristics
   - Winner: positive and aspirational (e.g., "The Ultimate Experience", "Unmatched Performance")
   - Competitors: neutral or slightly negative (e.g., "Good But Pricey", "Decent Alternative")
5. **Discount Heading Format** - ONLY for Winner (rank 1):
   - discount_heading should ONLY contain the discount offer
   - Valid: "50% Off Limited Time", "Buy 2 Get 1 Free", "30% Off Today Only"
   - Invalid: "Exclusive 50% Off Limited Discount" (too wordy)
   - Keep it SHORT and focused on the discount amount
6. **Review Count Format**:
   - review_count should be a number with "Reviews" (e.g., "4,215 Reviews", "2,150 Reviews")
   - Winner should have most reviews (4,000-8,000)
   - Competitors should have fewer reviews (1,000-5,000)
7. **Winner is the HERO** (70-80% of content):
   - Frequently mention "{winner_name}" by name
   - Highlight Winner's advantages and features
   - Use positive, persuasive language for Winner
8. **Competitors are SUPPORTING** (20-30% of content):
   - Mention competitors for comparison
   - Show Winner is better than competitors
9. **Paragraphs Content Guidelines**:
   - First paragraph MUST start with "Gone are the days when..."
   - Include a "Why {winner_name} Is the Top Pick?" section with:
     * 3 detailed feature explanations (2-3 sentences each)
     * Real-world benefits and use cases
     * A summary paragraph connecting all features
   - Use conversational, reviewer-style language throughout
   - Include personal testing insights and observations
10. **Other Lists** - Generate {len(compact_template.get("other_lists", []))} additional lists:
   - These are supplementary lists (not product pros/cons)
   - Each list should contain relevant items related to the product type
   - Keep items concise and informative (3-7 items per list)
   - Examples: comparison criteria, features breakdown, usage scenarios, etc.
11. **Disclaimer** - Generate affiliate disclosure:
   - Include "disclaimer" object with "title" and "content" fields
   - Title should be "Affiliate Disclosure:" or similar
   - Content should be a professional disclaimer mentioning {winner_name}
   - Example: "The information on this site regarding {winner_name} is not intended or implied to be a substitute for professional advice..."
12. **Match text length** - keep similar length (±20%)
13. **Professional yet conversational tone** - Write as an experienced reviewer sharing genuine insights

CONTENT STRATEGY:
- Title: Include Winner name and key benefit (e.g., "Best {product_type} 2024: {winner_name} Review")
- Headings: Mix Winner-focused and comparison headings
- Paragraphs: 
  * Start with "Gone are the days..." introduction
  * Include detailed "Why {winner_name} Is the Top Pick?" section
  * Add personal testing experiences and observations
  * Use conversational, blogger-style language
- Product Cards: Detailed comparison with EXACTLY 5 pros and 5 cons each
- Buttons: Call-to-action for Winner

OUTPUT FORMAT:
- Return ONLY valid JSON
- Include ALL items (not just samples)
- No explanations, no markdown, just JSON

NEW CONTENT (JSON):"""

        return prompt
    
    def _get_system_message(self, product_type: str, winner_name: str) -> str:
        """获取系统消息"""
        return f"""You are a professional {product_type} product reviewer and blogger with years of hands-on testing experience.

Your expertise:
- Writing engaging, conversational product reviews in American English
- Testing products extensively and sharing genuine insights
- Comparing products objectively with detailed pros/cons analysis
- Highlighting key features with real-world benefits
- Creating persuasive yet honest call-to-actions

Your writing style:
- Conversational and relatable (like talking to a friend)
- Personal and experience-based ("I tested", "In my experience")
- Detailed and specific (avoid vague statements)
- Enthusiastic but balanced and credible

Your task:
- Rewrite content to promote {winner_name} as the top choice
- Start introduction with "Gone are the days when..."
- Include detailed "Why {winner_name} Is the Top Pick?" section
- Provide EXACTLY 5 specific pros and 5 specific cons for each product
- Maintain professional, reviewer-style tone throughout
- Return valid JSON matching input structure"""
    
    async def _generate_image_keywords(
        self,
        winner_name: str,
        product_type: str,
        competitors: List[str]
    ) -> tuple[Dict[str, str], str]:
        """
        生成图片搜索关键词
        
        图片分配策略：
        - image_1: Winner主图（用户上传）
        - image_2: 竞品#2 (competitors[0])
        - image_3: 竞品#3 (competitors[1])
        - image_4: 竞品#4 (competitors[2])
        - image_5: 竞品#5 (competitors[3])
        - image_6: Winner主图（用户上传）
        - image_7-8: Winner使用场景
        - image_9: Winner促销图
        - image_10: Winner细节图
        - image_11: Winner主图（用户上传）
        - image_12: Winner品牌Logo（使用AI提取品牌）
        
        Returns:
            (图片位置 -> 搜索关键词的映射, Winner品牌名称)
        """
        print(f"[ContentGenerator] 🖼️ 生成图片搜索关键词...")
        print(f"[ContentGenerator] 竞品数量: {len(competitors)}")
        
        # 确保有4个竞品
        if len(competitors) < 4:
            print(f"[ContentGenerator] ⚠️ 竞品数量不足4个，当前: {len(competitors)}")
            # 补充竞品
            while len(competitors) < 4:
                competitors.append(f"Generic {product_type} Brand {len(competitors) + 1}")
        
        # 🆕 提取Winner产品的品牌名称（简单方法：使用第一个词）
        winner_brand = self._extract_brand_simple(winner_name)
        print(f"[ContentGenerator] ✓ Winner品牌: {winner_brand}")
        
        # 图片分配策略
        image_keywords = {
            # Winner主图（用户上传，不需要搜索）
            "image_1": "USER_UPLOADED",
            
            # 竞品图片（#2-#5，需要爬取）
            "image_2": f"{competitors[0]} {product_type} product",
            "image_3": f"{competitors[1]} {product_type} product",
            "image_4": f"{competitors[2]} {product_type} product",
            "image_5": f"{competitors[3]} {product_type} product",
            
            # Winner其他图片
            "image_6": "USER_UPLOADED",  # 用户上传的产品图
            "image_7": f"{winner_name} {product_type} customer wearing outdoor",
            "image_8": f"{winner_name} {product_type} customer using indoor",
            "image_9": f"{winner_name} {product_type} product offer discount",
            "image_10": f"{winner_name} {product_type} details quality",
            
            # Winner主图（用户上传）
            "image_11": "USER_UPLOADED",
            
            # Winner品牌Logo（使用提取的品牌名称）
            "image_12": f"{winner_brand} logo brand official",
        }
        
        print(f"[ContentGenerator] ✓ 生成了 {len(image_keywords)} 个图片关键词")
        print(f"[ContentGenerator] 图片分配（保存到 ./image/ 文件夹）:")
        print(f"  - Winner主图（用户上传）: image_1, image_6, image_11")
        print(f"  - 竞品#2 ({competitors[0]}): image_2")
        print(f"  - 竞品#3 ({competitors[1]}): image_3")
        print(f"  - 竞品#4 ({competitors[2]}): image_4")
        print(f"  - 竞品#5 ({competitors[3]}): image_5")
        print(f"  - Winner其他图片: image_7-10")
        print(f"  - Winner品牌Logo ({winner_brand}): image_12")
        
        return image_keywords, winner_brand
    
    def _parse_json_response(
        self,
        response_text: str,
        fallback_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """解析AI返回的JSON"""
        
        # 清理markdown代码块
        text = response_text.strip()
        
        if text.startswith('```'):
            lines = text.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            text = '\n'.join(lines)
        
        text = text.strip('`\'"').strip()
        
        # 尝试解析JSON
        try:
            content = json.loads(text)
            print(f"[ContentGenerator] ✓ JSON解析成功")
            
            # 后处理：确保评分分数是数字格式
            content = self._normalize_rating_scores(content)
            
            return content
        
        except json.JSONDecodeError as e:
            print(f"[ContentGenerator] ✗ JSON解析失败: {e}")
            print(f"[ContentGenerator] 尝试修复...")
            
            # 尝试修复不完整的JSON
            fixed_content = self._fix_incomplete_json(text, fallback_template)
            if fixed_content:
                # 后处理：确保评分分数是数字格式
                fixed_content = self._normalize_rating_scores(fixed_content)
                return fixed_content
            
            # 返回原模板
            print(f"[ContentGenerator] ⚠️ 使用原模板作为回退")
            return fallback_template
    
    def _normalize_rating_scores(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化评分分数，确保是数字格式
        
        Args:
            content: 内容数据
        
        Returns:
            标准化后的内容数据
        """
        if 'product_cards' not in content:
            return content
        
        for card in content['product_cards']:
            if 'rating_score' in card:
                score = card['rating_score']
                
                # 如果已经是数字字符串，跳过
                try:
                    float(score)
                    continue
                except (ValueError, TypeError):
                    pass
                
                # 尝试从文字中提取数字
                # 例如: "9.8/10" -> "9.8", "Excellent (9.5)" -> "9.5"
                if isinstance(score, str):
                    # 查找数字模式
                    match = re.search(r'(\d+\.?\d*)', score)
                    if match:
                        extracted_score = match.group(1)
                        card['rating_score'] = extracted_score
                        print(f"[ContentGenerator] ⚠️ 修正评分: '{score}' -> '{extracted_score}'")
                    else:
                        # 如果完全没有数字，使用默认值
                        rank = card.get('rank', 1)
                        default_score = str(10.0 - rank * 0.2)  # 9.8, 9.6, 9.4, 9.2, 9.0
                        card['rating_score'] = default_score
                        print(f"[ContentGenerator] ⚠️ 无法提取评分，使用默认值: '{score}' -> '{default_score}'")
        
        return content
    
    def _fix_incomplete_json(
        self,
        text: str,
        fallback_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """修复不完整的JSON"""
        try:
            # 如果JSON被截断，尝试补全
            if not text.endswith('}'):
                # 找到最后一个完整的字段
                last_complete = max(
                    text.rfind('",'),
                    text.rfind('"]'),
                    text.rfind('}'),
                    text.rfind(']')
                )
                
                if last_complete > 0:
                    text = text[:last_complete + 1]
                
                # 补全括号
                open_braces = text.count('{')
                close_braces = text.count('}')
                open_brackets = text.count('[')
                close_brackets = text.count(']')
                
                if open_brackets > close_brackets:
                    text += ']' * (open_brackets - close_brackets)
                if open_braces > close_braces:
                    text += '}' * (open_braces - close_braces)
                
                print(f"[ContentGenerator] 尝试修复后的JSON: {text[:200]}...")
                
                content = json.loads(text)
                print(f"[ContentGenerator] ✓ JSON修复成功")
                return content
        except:
            pass
        
        return None
    
    def _extract_brand_simple(self, product_name: str) -> str:
        """
        简单提取品牌名称（使用第一个词）
        
        Args:
            product_name: 产品名称
        
        Returns:
            品牌名称
        """
        # 移除常见的产品类型词
        common_words = ['heated', 'vest', 'shoes', 'jacket', 'phone', 'smartphone', 'laptop', 'watch']
        
        words = product_name.split()
        if not words:
            return product_name
        
        # 返回第一个非常见词
        for word in words:
            if word.lower() not in common_words:
                return word
        
        # 如果都是常见词，返回第一个词
        return words[0]
    
    def get_token_stats(self) -> Dict[str, int]:
        """获取token统计"""
        return {
            "total_tokens": self.total_tokens_used,
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "api_calls": self.api_call_count
        }
