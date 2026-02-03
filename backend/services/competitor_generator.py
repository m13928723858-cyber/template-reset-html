"""
竞品生成器：使用AI生成竞品列表
"""
import os
import json
import re
from pathlib import Path
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class CompetitorGenerator:
    """使用AI生成竞品列表"""
    
    def __init__(self):
        api_key = os.getenv("DOLPHIN_API_KEY")
        base_url = os.getenv("DOLPHIN_BASE_URL", "https://dolphin-chat.ihippogame.com/api/v1")
        
        if not api_key:
            raise ValueError("DOLPHIN_API_KEY 未设置")
        
        print(f"[CompetitorGenerator] 初始化 OpenAI 客户端")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        self.model = "gemini-3-flash-preview"  # 使用允许的模型
        
        # Token统计
        self.total_tokens_used = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
    
    async def generate(
        self, 
        winner_name: str, 
        product_type: str,
        num_competitors: int = 4
    ) -> List[str]:
        """
        生成竞品列表
        
        Args:
            winner_name: Winner产品名称
            product_type: 产品类型
            num_competitors: 竞品数量（默认4个）
        
        Returns:
            竞品名称列表
        """
        print(f"\n{'='*60}")
        print(f"🤖 开始生成竞品")
        print(f"{'='*60}")
        print(f"Winner: {winner_name}")
        print(f"产品类型: {product_type}")
        print(f"需要生成: {num_competitors} 个竞品")
        print(f"{'='*60}\n")
        
        prompt = self._build_prompt(winner_name, product_type, num_competitors)
        
        try:
            print(f"[CompetitorGenerator] 🤖 调用 AI 生成竞品...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a product market analyst. You know all major brands in the {product_type} market. Return only valid JSON arrays."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=5000  # 增加token限制，避免JSON被截断
            )
            
            # 记录token使用
            if hasattr(response, 'usage') and response.usage:
                self.total_prompt_tokens += response.usage.prompt_tokens
                self.total_completion_tokens += response.usage.completion_tokens
                self.total_tokens_used += response.usage.total_tokens
                
                print(f"[CompetitorGenerator] 📊 Token消耗:")
                print(f"  - 输入: {response.usage.prompt_tokens}")
                print(f"  - 输出: {response.usage.completion_tokens}")
                print(f"  - 总计: {response.usage.total_tokens}")
            
            result = response.choices[0].message.content.strip()
            print(f"[CompetitorGenerator] AI 原始返回: {result[:200]}...")
            
            # 解析返回的JSON
            competitors = self._parse_response(result, num_competitors)
            
            if len(competitors) == num_competitors:
                print(f"\n{'='*60}")
                print(f"✅ 竞品生成成功")
                print(f"{'='*60}")
                for i, comp in enumerate(competitors, 1):
                    print(f"{i}. {comp}")
                print(f"{'='*60}\n")
                
                return competitors
            else:
                print(f"[CompetitorGenerator] ⚠️ 生成数量不足: {len(competitors)}/{num_competitors}")
                # 如果数量不足，补充通用名称
                while len(competitors) < num_competitors:
                    competitors.append(f"Competitor {len(competitors) + 1}")
                return competitors
        
        except Exception as e:
            print(f"[CompetitorGenerator] ✗ 生成失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 返回默认竞品
            return [f"Competitor {i+1}" for i in range(num_competitors)]
    
    def _build_prompt(self, winner_name: str, product_type: str, num_competitors: int) -> str:
        """构建AI prompt"""
        
        prompt = f"""Generate exactly {num_competitors} real competitor products for: {winner_name}

Product type: {product_type}

Requirements:
1. Return ONLY {num_competitors} competitor names
2. These should be REAL, well-known brands in the {product_type} market
3. Do NOT include {winner_name} in the list
4. Format: JSON array of strings
5. Each name should be the full product name (Brand + Product Type)

Example format: ["Brand A {product_type}", "Brand B {product_type}", "Brand C {product_type}", "Brand D {product_type}"]

Return ONLY the JSON array, no explanations:"""

        return prompt
    
    def _parse_response(self, response_text: str, expected_count: int) -> List[str]:
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
        
        print(f"[CompetitorGenerator] 清理后的文本: {text[:200]}...")
        
        # 尝试解析JSON
        try:
            competitors = json.loads(text)
            
            if isinstance(competitors, list):
                # 过滤和清理
                competitors = [str(c).strip() for c in competitors if c]
                print(f"[CompetitorGenerator] ✓ JSON解析成功: {len(competitors)} 个竞品")
                return competitors[:expected_count]
            else:
                print(f"[CompetitorGenerator] ✗ 返回格式错误: 不是数组")
                return []
        
        except json.JSONDecodeError as e:
            print(f"[CompetitorGenerator] ✗ JSON解析失败: {e}")
            
            # 尝试修复不完整的JSON
            competitors = self._fix_incomplete_json(text, expected_count)
            if competitors:
                return competitors
            
            # 尝试正则提取
            print(f"[CompetitorGenerator] 尝试正则提取...")
            matches = re.findall(r'"([^"]+)"', text)
            if matches:
                print(f"[CompetitorGenerator] ✓ 正则提取成功: {len(matches)} 个")
                return matches[:expected_count]
            
            return []
    
    def _fix_incomplete_json(self, text: str, expected_count: int) -> List[str]:
        """修复不完整的JSON"""
        try:
            # 如果JSON被截断，尝试补全
            if not text.endswith(']'):
                # 找到最后一个完整的引号
                last_complete_quote = -1
                quote_count = 0
                for i, char in enumerate(text):
                    if char == '"' and (i == 0 or text[i-1] != '\\'):
                        quote_count += 1
                        if quote_count % 2 == 0:  # 偶数个引号表示完整
                            last_complete_quote = i
                
                if last_complete_quote > 0:
                    text = text[:last_complete_quote + 1]
                
                # 移除末尾的逗号和空格
                text = text.rstrip().rstrip(',').rstrip()
                
                # 补全结束括号
                if not text.endswith(']'):
                    text += ']'
                
                print(f"[CompetitorGenerator] 尝试修复JSON: {text[:200]}...")
                
                competitors = json.loads(text)
                if isinstance(competitors, list):
                    print(f"[CompetitorGenerator] ✓ JSON修复成功: {len(competitors)} 个")
                    return [str(c).strip() for c in competitors if c][:expected_count]
        except Exception as e:
            print(f"[CompetitorGenerator] ✗ JSON修复失败: {e}")
        
        return []
    
    def get_token_stats(self) -> dict:
        """获取token统计"""
        return {
            "total_tokens": self.total_tokens_used,
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens
        }
