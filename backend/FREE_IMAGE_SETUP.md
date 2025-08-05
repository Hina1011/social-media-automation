# Free Image Generation Setup Guide

## Overview

Your Social Media Automation Platform is now configured to use **only free image generation options**:

1. **OpenAI DALL-E** (limited free credits)
2. **Unsplash API** (always free)
3. **Custom Placeholder Images** (fallback)

## Setup Instructions

### 1. **Environment Variables**

Add these to your `.env` file:

```env
# Free Image Generation APIs
OPENAI_API_KEY=your-openai-api-key
UNSPLASH_ACCESS_KEY=your-unsplash-access-key
```

### 2. **API Key Setup**

#### **OpenAI DALL-E API**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. **Free Credits**: New accounts get ~$5 in free credits (about 25 DALL-E images)
4. Add to `.env`: `OPENAI_API_KEY=sk-your-key-here`

#### **Unsplash API**
1. Visit [Unsplash Developers](https://unsplash.com/developers)
2. Create an application and get your access key
3. **Free Tier**: 50 requests/hour, 5,000 requests/month
4. Add to `.env`: `UNSPLASH_ACCESS_KEY=your-access-key`

### 3. **Install Dependencies**

```bash
pip install openai>=1.0.0 aiohttp>=3.8.0
```

## How It Works

### **Image Generation Priority**

1. **DALL-E First**: If you have free credits, generates AI images
2. **Unsplash Fallback**: If DALL-E fails or credits exhausted, uses stock photos
3. **Placeholder Last**: If both APIs fail, creates custom placeholder images

### **Cost Breakdown**

| Service | Cost | Free Tier | Best For |
|---------|------|-----------|----------|
| DALL-E | $0.020/image | ~25 free images | AI-generated content |
| Unsplash | Free | 5,000 requests/month | High-quality stock photos |
| Placeholders | Free | Unlimited | Fallback images |

## Testing

### **Test Image Generation**

```bash
cd backend
python test_image_generation.py
```

### **Manual Testing**

1. Login to the platform
2. Go to Posts page
3. Click "Generate Posts"
4. Check that images are generated and displayed

## API Limits & Best Practices

### **DALL-E Limits**
- **Free Credits**: ~$5 worth (25 images)
- **After Free Credits**: $0.020 per image
- **Rate Limit**: 50 requests/minute
- **Image Size**: 1024x1024 pixels

### **Unsplash Limits**
- **Free Tier**: 50 requests/hour, 5,000/month
- **Image Quality**: High resolution
- **Attribution**: Required (handled automatically)

### **Best Practices**
1. **Start with DALL-E** for unique AI-generated content
2. **Use Unsplash** for consistent, professional stock photos
3. **Monitor usage** to avoid exceeding limits
4. **Cache images** to reduce API calls

## Troubleshooting

### **Common Issues**

1. **"OpenAI API key not found"**
   - Add `OPENAI_API_KEY` to your `.env` file
   - Verify the key is correct

2. **"Unsplash API key not found"**
   - Add `UNSPLASH_ACCESS_KEY` to your `.env` file
   - Verify the key is correct

3. **"DALL-E quota exceeded"**
   - System will automatically fallback to Unsplash
   - No action needed

4. **"Unsplash rate limit exceeded"**
   - System will create placeholder images
   - Wait for rate limit to reset

### **Error Messages**

- **"Error with DALL-E"**: Check API key and credits
- **"Error with Unsplash"**: Check API key and rate limits
- **"Image not accessible"**: Check static file serving

## Cost Optimization

### **For Development**
- Use only Unsplash (completely free)
- Set `OPENAI_API_KEY=""` in `.env`

### **For Production**
- Use DALL-E for initial free credits
- Fallback to Unsplash for ongoing use
- Monitor usage to control costs

### **For Maximum Savings**
- Use only Unsplash API
- Create custom placeholder images
- No paid API costs

## Example .env Configuration

```env
# Database
MONGODB_URL=your-mongodb-atlas-url
DATABASE_NAME=social_media_automation

# AI Content Generation
GEMINI_API_KEY=your-gemini-api-key

# Free Image Generation
OPENAI_API_KEY=sk-your-openai-key
UNSPLASH_ACCESS_KEY=your-unsplash-key

# JWT
SECRET_KEY=your-secret-key
```

## Success Indicators

✅ **DALL-E Working**: AI-generated images appear in posts
✅ **Unsplash Working**: High-quality stock photos appear
✅ **Fallback Working**: Placeholder images appear when APIs fail
✅ **No Errors**: All image generation completes successfully

## Next Steps

1. **Add API keys** to your `.env` file
2. **Test generation** with the test script
3. **Monitor usage** to stay within free limits
4. **Enjoy free image generation** for your social media posts!

---

**Note**: This setup provides completely free image generation for your social media automation platform. DALL-E gives you AI-generated images with free credits, and Unsplash provides unlimited high-quality stock photos. 