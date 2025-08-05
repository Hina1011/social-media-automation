# Image Generation Setup Guide

## Overview

The Social Media Automation Platform now supports AI-powered image generation for your social media posts. The system can generate images based on your user profile data (interests, profession, custom prompt) and the content of each post.

## Image Generation Options

### 1. **AI Image Generation (Recommended)**
- **Stable Diffusion API**: High-quality AI-generated images
- **DALL-E API**: OpenAI's image generation service
- **Midjourney API**: Professional-grade image generation

### 2. **Stock Photo Integration**
- **Unsplash API**: Free high-quality stock photos
- **Pexels API**: Additional stock photo options

### 3. **Fallback System**
- **Custom Placeholder Images**: Generated when APIs are unavailable
- **Professional Design**: Branded placeholder images

## Setup Instructions

### 1. **Environment Variables**

Add these to your `.env` file:

```env
# AI Image Generation APIs
STABLE_DIFFUSION_API_KEY=your-stable-diffusion-api-key
UNSPLASH_ACCESS_KEY=your-unsplash-access-key

# Optional: Additional services
DALLE_API_KEY=your-openai-api-key
MIDJOURNEY_API_KEY=your-midjourney-api-key
PEXELS_API_KEY=your-pexels-api-key
```

### 2. **API Key Setup**

#### **Stable Diffusion API**
1. Visit [Stability AI](https://platform.stability.ai/)
2. Create an account and get your API key
3. Add to `.env`: `STABLE_DIFFUSION_API_KEY=your-key`

#### **Unsplash API**
1. Visit [Unsplash Developers](https://unsplash.com/developers)
2. Create an application and get your access key
3. Add to `.env`: `UNSPLASH_ACCESS_KEY=your-key`

### 3. **Install Dependencies**

```bash
pip install Pillow>=9.0.0
```

### 4. **Create Static Directories**

The system will automatically create these directories:
- `static/images/generated/` - AI-generated images
- `static/images/placeholder/` - Fallback images

## How It Works

### **Image Generation Process**

1. **User Signs Up**: System captures interests, profession, custom prompt
2. **Post Generation**: When generating posts, the system:
   - Creates content based on user profile
   - Generates image prompts from content
   - Creates actual images using AI services
   - Saves images to local storage
   - Associates images with posts

### **Image Types Generated**

- **Instagram**: Square format (1024x1024), vibrant colors
- **LinkedIn**: Professional style, business-focused
- **Facebook**: Community-oriented, engaging visuals
- **Twitter**: Clean, minimal design

### **Fallback System**

If AI services are unavailable, the system creates:
- Professional placeholder images
- Branded with platform names
- Custom text overlays
- Consistent design language

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

## Customization

### **Image Styles**

You can customize image generation by modifying:
- `backend/utils/ai_generator.py` - Image generation logic
- `backend/utils/ai_generator.py` - Image prompt generation
- `backend/utils/ai_generator.py` - Placeholder image creation

### **Image Sizes**

Default sizes (can be customized):
- **Instagram**: 1024x1024
- **LinkedIn**: 1200x628
- **Facebook**: 1200x630
- **Twitter**: 1200x675

### **Image Quality**

- **AI Generated**: High quality, optimized for web
- **Stock Photos**: Original quality, optimized for web
- **Placeholders**: 85% JPEG quality, fast loading

## Troubleshooting

### **Common Issues**

1. **No Images Generated**
   - Check API keys in `.env`
   - Verify API quotas and limits
   - Check server logs for errors

2. **Images Not Displaying**
   - Ensure static file serving is enabled
   - Check image file permissions
   - Verify image URLs in database

3. **Poor Image Quality**
   - Upgrade to premium API plans
   - Adjust image generation parameters
   - Use higher resolution settings

### **Error Messages**

- **"API key not found"**: Add missing API keys to `.env`
- **"Image generation failed"**: Check API service status
- **"Image not accessible"**: Verify static file serving

## Cost Considerations

### **Free Options**
- **Unsplash API**: 50 requests/hour (free)
- **Placeholder Images**: Unlimited (generated locally)

### **Paid Options**
- **Stable Diffusion**: $0.002 per image
- **DALL-E**: $0.020 per image
- **Midjourney**: $0.10 per image

### **Recommendations**
- **Development**: Use Unsplash + placeholders
- **Production**: Use Stable Diffusion for best quality/cost ratio
- **Enterprise**: Use DALL-E or Midjourney for premium quality

## Security

### **Image Storage**
- Images stored locally in `static/images/generated/`
- No external image hosting required
- Secure file permissions

### **API Security**
- API keys stored in environment variables
- No keys exposed in client-side code
- Rate limiting to prevent abuse

## Performance

### **Optimization**
- Images compressed to 85% JPEG quality
- Lazy loading in frontend
- CDN-ready file structure
- Caching headers for static files

### **Scaling**
- Images generated on-demand
- No pre-generation required
- Efficient storage management
- Automatic cleanup of old images 