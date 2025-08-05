import google.generativeai as genai
from config import settings
import logging
from typing import List, Dict, Any
import json
import random
import requests
import base64
import os
import aiohttp
import openai
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Configure OpenAI API
if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY


class AIContentGenerator:
    def __init__(self):
        self.model = model
        
    async def generate_post_caption(self, interests: List[str], custom_prompt: str, platform: str) -> Dict[str, Any]:
        """Generate a social media post caption using AI."""
        try:
            prompt = f"""
            Create an engaging social media post for {platform} based on these interests: {', '.join(interests)}
            
            Custom prompt: {custom_prompt}
            
            Generate:
            1. A compelling caption (max 2200 characters for Instagram, 280 for Twitter, 3000 for LinkedIn/Facebook)
            2. 10-15 relevant hashtags
            3. A call-to-action
            
            Format the response as JSON:
            {{
                "caption": "The main caption text",
                "hashtags": ["#hashtag1", "#hashtag2", ...],
                "call_to_action": "CTA text"
            }}
            
            Make it engaging, authentic, and platform-appropriate.
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            
            return {
                "caption": result.get("caption", ""),
                "hashtags": result.get("hashtags", []),
                "call_to_action": result.get("call_to_action", "")
            }
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return self._generate_fallback_caption(interests, custom_prompt, platform)
    
    async def generate_image_prompt(self, caption: str, interests: List[str]) -> str:
        """Generate an image prompt for AI image generation."""
        try:
            prompt = f"""
            Based on this social media caption: "{caption}"
            And these interests: {', '.join(interests)}
            
            Create a detailed image prompt for AI image generation that would complement this post.
            Focus on visual elements that would make the post more engaging.
            
            Return only the image prompt, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating image prompt: {e}")
            return f"Professional social media content related to {', '.join(interests[:3])}"
    
    async def generate_ai_image(self, image_prompt: str, platform: str) -> str:
        """Generate an image using DALL-E or Unsplash fallback."""
        try:
            # Try DALL-E first (if API key is available)
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                dalle_image_url = await self._generate_with_dalle(image_prompt, platform)
                if dalle_image_url:
                    return dalle_image_url
            
            # Fallback to Unsplash
            if hasattr(settings, 'UNSPLASH_ACCESS_KEY') and settings.UNSPLASH_ACCESS_KEY:
                unsplash_image_url = await self._generate_with_unsplash(image_prompt, platform)
                if unsplash_image_url:
                    return unsplash_image_url
            
            # Final fallback: create placeholder
            return await self._create_simple_placeholder(image_prompt, platform)
                
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return await self._create_simple_placeholder(image_prompt, platform)
    
    async def _generate_with_dalle(self, image_prompt: str, platform: str) -> str:
        """Generate image using OpenAI DALL-E API."""
        try:
            # Create a platform-specific prompt
            platform_prompts = {
                "instagram": f"{image_prompt}, vibrant colors, square format, social media content",
                "linkedin": f"{image_prompt}, professional, business style, clean design",
                "facebook": f"{image_prompt}, community focused, engaging, warm colors",
                "twitter": f"{image_prompt}, clean, minimal, modern design"
            }
            
            dalle_prompt = platform_prompts.get(platform, f"{image_prompt}, professional social media content")
            
            response = openai.Image.create(
                prompt=dalle_prompt,
                n=1,
                size="1024x1024"
            )
            
            image_url = response['data'][0]['url']
            
            # Download and save the image locally
            saved_path = await self._download_and_save_image(image_url, platform, "dalle")
            return saved_path
            
        except Exception as e:
            logger.error(f"Error with DALL-E: {e}")
            return None
    
    async def _generate_with_unsplash(self, image_prompt: str, platform: str) -> str:
        """Generate image using Unsplash API."""
        try:
            # Extract key terms from the prompt for search
            search_terms = " ".join(image_prompt.split()[:5])  # Use first 5 words
            
            unsplash_url = "https://api.unsplash.com/photos/random"
            params = {
                "query": search_terms,
                "orientation": "squarish",
                "client_id": settings.unsplash_access_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(unsplash_url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        image_url = data['urls']['regular']
                        
                        # Download and save the image locally
                        saved_path = await self._download_and_save_image(image_url, platform, "unsplash")
                        return saved_path
                    else:
                        logger.error(f"Unsplash API error: {resp.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error with Unsplash: {e}")
            return None
    
    async def _create_simple_placeholder(self, image_prompt: str, platform: str) -> str:
        """Create a simple placeholder image."""
        try:
            # Create a simple colored background with text
            width, height = 1024, 1024
            
            # Create image with gradient
            image = Image.new('RGB', (width, height), color='#f0f0f0')
            draw = ImageDraw.Draw(image)
            
            # Add some design elements
            draw.rectangle([0, 0, width, height//3], fill='#4f46e5')
            draw.rectangle([0, height//3, width, height], fill='#ffffff')
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Add platform name
            draw.text((width//2, height//4), platform.upper(), fill='white', font=font, anchor='mm')
            
            # Add prompt text (truncated)
            prompt_text = image_prompt[:50] + "..." if len(image_prompt) > 50 else image_prompt
            draw.text((width//2, height//2), prompt_text, fill='#374151', font=font, anchor='mm')
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"placeholder_{platform}_{timestamp}.jpg"
            image_path = f"static/images/generated/{filename}"
            
            # Ensure directory exists
            os.makedirs("static/images/generated", exist_ok=True)
            
            image.save(image_path, "JPEG", quality=85)
            return f"/{image_path}"
            
        except Exception as e:
            logger.error(f"Error creating placeholder: {e}")
            return "/static/images/placeholder.jpg"
    
    async def _download_and_save_image(self, image_url: str, platform: str, source: str) -> str:
        """Download and save image from URL."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        image = Image.open(io.BytesIO(image_data))
                        
                        # Save image
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{source}_{platform}_{timestamp}.jpg"
                        image_path = f"static/images/generated/{filename}"
                        
                        # Ensure directory exists
                        os.makedirs("static/images/generated", exist_ok=True)
                        
                        image.save(image_path, "JPEG", quality=85)
                        return f"/{image_path}"
                    else:
                        logger.error(f"Failed to download image: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return None
    
    async def generate_7_day_batch(self, interests: List[str], custom_prompt: str, 
                                 platforms: List[str], start_date: datetime) -> List[Dict[str, Any]]:
        """Generate 7 days of social media posts with images."""
        posts = []
        
        for i in range(7):
            post_date = start_date + timedelta(days=i)
            
            # Generate content for each platform
            for platform in platforms:
                caption_data = await self.generate_post_caption(interests, custom_prompt, platform)
                image_prompt = await self.generate_image_prompt(caption_data["caption"], interests)
                
                # Generate actual image
                image_url = await self.generate_ai_image(image_prompt, platform)
                
                post = {
                    "platform": platform,
                    "scheduled_date": post_date,
                    "caption": caption_data["caption"],
                    "hashtags": caption_data["hashtags"],
                    "call_to_action": caption_data["call_to_action"],
                    "image_prompt": image_prompt,
                    "image_url": image_url,
                    "status": "draft"
                }
                
                posts.append(post)
        
        return posts

    async def generate_single_post(self, interests: List[str], platform: str, custom_prompt: str, scheduled_date: datetime) -> Dict[str, Any]:
        """Generate a single social media post."""
        try:
            # Generate caption
            caption_data = await self.generate_post_caption(interests, custom_prompt, platform)
            
            # Generate image prompt
            image_prompt = await self.generate_image_prompt(caption_data["caption"], interests)
            
            # Generate image
            image_url = await self.generate_ai_image(image_prompt, platform)
            
            post = {
                "caption": caption_data["caption"],
                "hashtags": caption_data["hashtags"],
                "call_to_action": caption_data["call_to_action"],
                "image_prompt": image_prompt,
                "image_url": image_url,
                "platform": platform,
                "scheduled_date": scheduled_date.isoformat()
            }
            
            return post
            
        except Exception as e:
            logger.error(f"Error generating single post: {e}")
            return self._generate_fallback_single_post(interests, platform, custom_prompt, scheduled_date)

    def _generate_fallback_single_post(self, interests: List[str], platform: str, custom_prompt: str, scheduled_date: datetime) -> Dict[str, Any]:
        """Generate a fallback single post when AI generation fails."""
        fallback_captions = {
            "instagram": f"Exciting content about {', '.join(interests[:2])}! 📸✨",
            "linkedin": f"Professional insights on {', '.join(interests[:2])}. Let's connect! 💼",
            "facebook": f"Sharing thoughts on {', '.join(interests[:2])}. What do you think? 🤔",
            "twitter": f"Quick thoughts on {', '.join(interests[:2])} #content"
        }
        
        fallback_hashtags = {
            "instagram": ["#content", "#socialmedia", "#engagement", "#growth", "#digital"],
            "linkedin": ["#professional", "#networking", "#business", "#career", "#growth"],
            "facebook": ["#community", "#sharing", "#thoughts", "#discussion", "#social"],
            "twitter": ["#content", "#social", "#digital", "#engagement", "#growth"]
        }
        
        return {
            "caption": fallback_captions.get(platform, fallback_captions["instagram"]),
            "hashtags": fallback_hashtags.get(platform, fallback_hashtags["instagram"]),
            "call_to_action": "What are your thoughts?",
            "image_prompt": f"Professional social media content related to {', '.join(interests[:3])}",
            "image_url": None,
            "platform": platform,
            "scheduled_date": scheduled_date.isoformat()
        }
    
    def _generate_fallback_caption(self, interests: List[str], custom_prompt: str, platform: str) -> Dict[str, Any]:
        """Generate a fallback caption if AI fails."""
        interest = random.choice(interests)
        
        fallback_captions = {
            "instagram": f"🌟 Embracing the journey of {interest.lower()}! {custom_prompt} #inspiration #growth #motivation",
            "twitter": f"🚀 {interest} insights: {custom_prompt[:100]}... #motivation #success",
            "linkedin": f"Professional insights on {interest}: {custom_prompt[:150]}... #professional #growth #networking",
            "facebook": f"Sharing thoughts on {interest}: {custom_prompt[:200]}... #community #inspiration #growth"
        }
        
        return {
            "caption": fallback_captions.get(platform, fallback_captions["instagram"]),
            "hashtags": [f"#{interest.lower()}", "#motivation", "#inspiration", "#growth", "#success"],
            "call_to_action": "What's your take on this? Share your thoughts below! 👇"
        }


# Global instance
ai_generator = AIContentGenerator() 