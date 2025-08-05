# LinkedIn OAuth Setup Guide - Fix "Bummer, something went wrong" Error

## Current Issue
You're getting a LinkedIn OAuth error page saying "Bummer, something went wrong" when trying to connect LinkedIn. This is because your LinkedIn app is not properly configured.

## Step-by-Step Fix

### 1. Create LinkedIn App (If you haven't already)

1. Go to [LinkedIn Developers](https://developer.linkedin.com/)
2. Click "Create App" or "Get Started"
3. Sign in with your LinkedIn account
4. Complete the developer registration process

### 2. Configure Your LinkedIn App

1. **In your LinkedIn app dashboard:**
   - Go to "Auth" tab
   - Add these redirect URLs:
     - `http://localhost:3000/linkedin-callback`
     - `http://localhost:5173/linkedin-callback` (if using Vite dev server)
   - Save the changes

2. **Request API Permissions:**
   - Go to "Products" tab
   - Request access to:
     - "Sign In with LinkedIn"
     - "Marketing Developer Platform"
   - Wait for approval (may take 24-48 hours)

### 3. Get Your Credentials

1. **In your LinkedIn app dashboard:**
   - Go to "Auth" tab
   - Copy your **Client ID** and **Client Secret**

### 4. Create .env File

Create a file named `.env` in your `backend` directory with this content:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=social_media_automation

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (Gmail OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# Image Generation APIs (Free Options Only)
OPENAI_API_KEY=your-openai-api-key
UNSPLASH_ACCESS_KEY=your-unsplash-access-key

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID=your-linkedin-client-id-here
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret-here
LINKEDIN_REDIRECT_URI=http://localhost:3000/linkedin-callback
LINKEDIN_SCOPE=r_liteprofile r_emailaddress w_member_social

# Other Social Media API Keys
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret
INSTAGRAM_USERNAME=your-instagram-username
INSTAGRAM_PASSWORD=your-instagram-password

# Application Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
BASE_URL=http://localhost:8000
```

### 5. Replace Placeholder Values

Replace these values in your `.env` file:

- `your-linkedin-client-id-here` → Your actual LinkedIn Client ID
- `your-linkedin-client-secret-here` → Your actual LinkedIn Client Secret
- `your-gemini-api-key` → Your Gemini AI API key
- `your-email@gmail.com` → Your Gmail address
- `your-app-password` → Your Gmail app password

### 6. Restart Your Backend Server

After creating the `.env` file:

```bash
cd backend
python start_server.py
```

### 7. Test the Connection

1. Go to your frontend application
2. Navigate to Platforms page
3. Click "Connect LinkedIn"
4. You should now be redirected to LinkedIn's authorization page
5. Complete the OAuth flow

## Common Issues and Solutions

### Issue 1: "Invalid redirect URI"
**Solution:** Make sure the redirect URI in your LinkedIn app exactly matches:
- `http://localhost:3000/linkedin-callback`

### Issue 2: "Invalid client_id"
**Solution:** 
- Verify your LinkedIn Client ID is correct
- Make sure your app is approved and active
- Check that you've copied the Client ID correctly

### Issue 3: "Insufficient permissions"
**Solution:**
- Request the required permissions in your LinkedIn app
- Make sure the app is approved for the Marketing Developer Platform
- Wait for approval (can take 24-48 hours)

### Issue 4: App not approved
**Solution:**
- LinkedIn requires manual approval for Marketing Developer Platform
- Submit your app for review
- Provide a clear description of how you'll use the API
- Wait for approval email

## Debug Steps

If you're still having issues:

1. **Check your .env file:**
   ```bash
   cd backend
   cat .env
   ```

2. **Check LinkedIn app settings:**
   - Verify redirect URIs are correct
   - Check that permissions are approved
   - Ensure app is active

3. **Check backend logs:**
   ```bash
   cd backend
   python start_server.py
   ```
   Look for any error messages when requesting the auth URL.

4. **Test the auth URL directly:**
   - Go to your backend: `http://localhost:8000/api/platforms/linkedin/auth-url`
   - Check if it returns a valid LinkedIn URL

## Security Notes

- Never commit your `.env` file to version control
- Keep your LinkedIn Client Secret secure
- Use HTTPS in production
- Regularly rotate your API keys

## Next Steps

Once LinkedIn is connected:
1. Test posting content to LinkedIn
2. Set up other social media platforms
3. Configure your AI content generation
4. Start automating your social media posts

## Support

If you continue to have issues:
1. Check the LinkedIn Developer Console for app status
2. Review LinkedIn API documentation
3. Check your application logs for detailed error messages
4. Verify all environment variables are correctly set 