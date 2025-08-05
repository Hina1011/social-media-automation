# Instagram OAuth Setup Guide

This guide will help you set up Instagram OAuth integration for the Social Media Automation Platform.

## Prerequisites

1. A Facebook Developer Account
2. An Instagram Business or Creator Account
3. A Facebook App (to access Instagram API)

## Step 1: Create a Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "Create App"
3. Choose "Business" as the app type
4. Fill in your app details and create the app

## Step 2: Add Instagram Basic Display

1. In your Facebook App dashboard, go to "Add Products"
2. Find "Instagram Basic Display" and click "Set Up"
3. Follow the setup wizard

## Step 3: Configure Instagram Basic Display

1. Go to "Instagram Basic Display" → "Basic Display"
2. Add your redirect URI: `http://localhost:3000/auth/instagram/callback`
3. Save changes

## Step 4: Get Your App Credentials

1. Go to "Settings" → "Basic"
2. Copy your "App ID" (this is your `INSTAGRAM_CLIENT_ID`)
3. Copy your "App Secret" (this is your `INSTAGRAM_CLIENT_SECRET`)

## Step 5: Update Configuration

1. Open `backend/config/instagram.py`
2. Replace the placeholder values:

```python
INSTAGRAM_CLIENT_ID = "your_actual_app_id_here"
INSTAGRAM_CLIENT_SECRET = "your_actual_app_secret_here"
```

## Step 6: Test the Integration

1. Start your backend server: `python main.py`
2. Start your frontend server: `npm run dev`
3. Go to the Platforms page
4. Click "Connect" on Instagram
5. You should be redirected to Instagram's authorization page
6. After authorization, you'll be redirected back to your app

## Troubleshooting

### Common Issues:

1. **"Invalid redirect URI" error**
   - Make sure the redirect URI in your Facebook App matches exactly: `http://localhost:3000/auth/instagram/callback`

2. **"App not approved" error**
   - Your app needs to be in development mode or approved by Facebook
   - Add your Instagram account as a test user in the app settings

3. **"Invalid client_id" error**
   - Double-check your `INSTAGRAM_CLIENT_ID` in the config file

4. **"Invalid client_secret" error**
   - Double-check your `INSTAGRAM_CLIENT_SECRET` in the config file

### Development Mode

During development, your app will be in "Development Mode" which means:
- Only you and test users can use the app
- You can add up to 25 test users
- No app review is required

### Production Deployment

For production deployment:
1. Submit your app for review
2. Update the redirect URI to your production domain
3. Update the configuration with production URLs

## API Permissions

The Instagram Basic Display API provides access to:
- User profile information
- User media (photos and videos)
- Basic insights

## Security Notes

- Never commit your `INSTAGRAM_CLIENT_SECRET` to version control
- Use environment variables for production
- Store access tokens securely in your database
- Implement token refresh logic for expired tokens

## Next Steps

After successful Instagram integration:
1. Implement token refresh logic
2. Add Instagram posting functionality
3. Implement media upload to Instagram
4. Add Instagram analytics 