# LinkedIn Integration Setup Guide

This guide will help you set up LinkedIn OAuth integration for your social media automation platform.

## Prerequisites

1. A LinkedIn Developer Account
2. A LinkedIn App
3. Valid LinkedIn API credentials

## Step 1: Create a LinkedIn Developer Account

1. Go to [LinkedIn Developers](https://developer.linkedin.com/)
2. Click "Create App" or "Get Started"
3. Sign in with your LinkedIn account
4. Complete the developer registration process

## Step 2: Create a LinkedIn App

1. In the LinkedIn Developer Console, click "Create App"
2. Fill in the required information:
   - **App Name**: Your app name (e.g., "Social Media Automation")
   - **LinkedIn Page**: Your LinkedIn company page (optional)
   - **App Logo**: Upload a logo for your app
3. Click "Create App"

## Step 3: Configure OAuth 2.0 Settings

1. In your app dashboard, go to "Auth" tab
2. Add your redirect URLs:
   - **Development**: `http://localhost:3000/linkedin-callback`
   - **Production**: `https://yourdomain.com/linkedin-callback`
3. Save the changes

## Step 4: Get API Credentials

1. In your app dashboard, go to "Products" tab
2. Request access to "Sign In with LinkedIn" and "Marketing Developer Platform"
3. Go to "Auth" tab to find your credentials:
   - **Client ID**: Your LinkedIn app's client ID
   - **Client Secret**: Your LinkedIn app's client secret

## Step 5: Configure Environment Variables

Add the following variables to your `.env` file:

```env
# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID=your_linkedin_client_id_here
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:3000/linkedin-callback
LINKEDIN_SCOPE=r_liteprofile r_emailaddress w_member_social
```

## Step 6: Install Dependencies

Make sure you have the required Python packages:

```bash
pip install requests>=2.31.0
```

## Step 7: Test the Integration

1. Start your backend server
2. Go to your frontend application
3. Navigate to the Platforms page
4. Click "Connect LinkedIn"
5. Complete the OAuth flow
6. Test posting content to LinkedIn

## API Endpoints

### Get LinkedIn Auth URL
```
GET /api/platforms/linkedin/auth-url
```
Returns the LinkedIn OAuth authorization URL.

### LinkedIn OAuth Callback
```
POST /api/platforms/linkedin/callback
```
Handles the OAuth callback and stores the access token.

### Post to LinkedIn
```
POST /api/platforms/linkedin/post
```
Posts content directly to LinkedIn.

### Post Specific Post to LinkedIn
```
POST /api/posts/{post_id}/post-to-linkedin
```
Posts a specific generated post to LinkedIn.

### Batch Post to LinkedIn
```
POST /api/posts/batch-post-to-linkedin
```
Posts multiple posts to LinkedIn at once.

## LinkedIn API Permissions

The integration uses the following LinkedIn API permissions:

- **r_liteprofile**: Read basic profile information
- **r_emailaddress**: Read email address
- **w_member_social**: Create and manage posts

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**
   - Make sure the redirect URI in your LinkedIn app matches exactly
   - Check for trailing slashes and protocol (http vs https)

2. **"Invalid client_id" error**
   - Verify your LinkedIn Client ID is correct
   - Make sure the app is approved and active

3. **"Insufficient permissions" error**
   - Request the required permissions in your LinkedIn app
   - Make sure the app is approved for the Marketing Developer Platform

4. **Token expiration**
   - The system automatically refreshes tokens when needed
   - If refresh fails, users need to reconnect their LinkedIn account

### Debug Mode

Enable debug logging by setting the log level in your backend:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **Never expose your Client Secret** in frontend code
2. **Store tokens securely** in your database
3. **Implement proper error handling** for token refresh
4. **Use HTTPS** in production
5. **Validate all user inputs** before posting

## Rate Limits

LinkedIn API has rate limits:
- **Profile API**: 100 requests per day
- **Posts API**: 100 posts per day
- **Image Upload**: 100 uploads per day

Monitor your usage to avoid hitting limits.

## Production Deployment

For production deployment:

1. Update redirect URIs to use HTTPS
2. Set up proper error monitoring
3. Implement retry logic for failed posts
4. Add comprehensive logging
5. Set up monitoring for rate limits

## Support

If you encounter issues:

1. Check the LinkedIn Developer Console for app status
2. Review the LinkedIn API documentation
3. Check your application logs for detailed error messages
4. Verify your environment variables are correctly set

## Example Usage

### Frontend Integration

```javascript
// Get LinkedIn auth URL
const response = await api.get('/platforms/linkedin/auth-url');
const authUrl = response.data.auth_url;

// Redirect user to LinkedIn
window.location.href = authUrl;

// Handle callback
const handleLinkedInCallback = async (authCode) => {
  const response = await api.post('/platforms/linkedin/callback', {
    platform: 'linkedin',
    auth_code: authCode
  });
  
  if (response.data.success) {
    console.log('LinkedIn connected successfully!');
  }
};

// Post to LinkedIn
const postToLinkedIn = async (postId) => {
  const response = await api.post(`/posts/${postId}/post-to-linkedin`);
  
  if (response.data.success) {
    console.log('Post shared on LinkedIn!');
  }
};
```

This setup will allow your users to connect their LinkedIn accounts and automatically post AI-generated content to their LinkedIn profiles. 