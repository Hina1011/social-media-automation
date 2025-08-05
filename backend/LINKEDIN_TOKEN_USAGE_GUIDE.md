# LinkedIn OAuth Access Token Usage Guide

## Overview
Your LinkedIn OAuth 2.0 access token is the key that allows your social media automation platform to post content to LinkedIn on your behalf. Here's exactly where and how it's used throughout the application.

## 1. Token Storage and Management

### Where Tokens Are Stored
```python
# In backend/models/platform_connection.py
class PlatformConnectionBase(BaseModel):
    platform: Literal["instagram", "linkedin", "facebook", "twitter"]
    is_connected: bool = False
    access_token: Optional[str] = None          # ← Your LinkedIn access token
    refresh_token: Optional[str] = None         # ← LinkedIn refresh token
    platform_user_id: Optional[str] = None
    platform_username: Optional[str] = None
    expires_at: Optional[datetime] = None       # ← Token expiration
```

### Database Storage
- **Collection**: `platform_connections`
- **Document Structure**:
```json
{
  "user_id": "user_object_id",
  "platform": "linkedin",
  "is_connected": true,
  "access_token": "AQV...",           // Your LinkedIn access token
  "refresh_token": "AQV...",          // Refresh token for renewal
  "platform_user_id": "linkedin_user_id",
  "platform_username": "your_linkedin_username",
  "expires_at": "2024-12-31T23:59:59Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 2. Token Usage in API Endpoints

### A. Individual Post to LinkedIn
**Endpoint**: `POST /api/posts/{post_id}/post-to-linkedin`

**How the token is used**:
```python
# 1. Retrieve stored access token
access_token = linkedin_connection.get("access_token")

# 2. Validate token and refresh if needed
is_valid = await linkedin_service.validate_token(access_token)
if not is_valid:
    # Refresh token using refresh_token
    token_data = await linkedin_service.refresh_access_token(refresh_token)
    access_token = token_data["access_token"]

# 3. Use token to post content
result = await linkedin_service.create_post(access_token, content, image_url)
```

### B. Batch Post to LinkedIn
**Endpoint**: `POST /api/posts/batch-post-to-linkedin`

**How the token is used**:
```python
# Same token validation and refresh logic
# Then posts multiple posts using the same access token
for post_id in post_ids:
    result = await linkedin_service.create_post(access_token, content, image_url)
```

### C. Direct LinkedIn Post
**Endpoint**: `POST /api/platforms/linkedin/post`

**How the token is used**:
```python
# Direct posting without going through the posts collection
result = await linkedin_service.create_post(access_token, content, image_url)
```

## 3. Token Usage in LinkedIn Service

### A. Creating Posts
```python
# backend/utils/linkedin_service.py - create_post method
async def create_post(self, access_token: str, content: str, image_url: str = None):
    headers = {
        "Authorization": f"Bearer {access_token}",  # ← Token used here
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # 1. Get user profile using token
    profile_response = requests.get(f"{self.base_url}/me", headers=headers)
    
    # 2. Create post using token
    post_response = requests.post(
        f"{self.base_url}/ugcPosts",
        headers=headers,  # ← Token used here
        json=post_data
    )
```

### B. Token Validation
```python
# backend/utils/linkedin_service.py - validate_token method
async def validate_token(self, access_token: str) -> bool:
    headers = {
        "Authorization": f"Bearer {access_token}",  # ← Token used here
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{self.base_url}/me", headers=headers)
    return response.status_code == 200
```

### C. Token Refresh
```python
# backend/utils/linkedin_service.py - refresh_access_token method
async def refresh_access_token(self, refresh_token: str):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": self.client_id,
        "client_secret": self.client_secret
    }
    
    response = requests.post(token_url, data=data)
    # Returns new access_token and refresh_token
```

## 4. Frontend Usage

### A. Connecting LinkedIn Account
```javascript
// frontend/src/pages/PlatformsPage.jsx
const handleLinkedInConnect = async () => {
    // 1. Get LinkedIn auth URL (no token needed yet)
    const response = await platformsAPI.getLinkedInAuthUrl()
    
    // 2. Redirect to LinkedIn OAuth
    window.location.href = response.data.auth_url
}

// 3. Handle OAuth callback
const handleLinkedInCallback = async (authCode) => {
    // Exchange auth code for access token
    const response = await platformsAPI.linkedinCallback({
        platform: 'linkedin',
        auth_code: authCode
    })
    // Token is now stored in database
}
```

### B. Posting to LinkedIn
```javascript
// frontend/src/services/api.js
export const postsAPI = {
    // Post single post to LinkedIn
    postToLinkedIn: (postId) => {
        return api.post(`/posts/${postId}/post-to-linkedin`)
        // Backend uses stored access token
    },
    
    // Batch post to LinkedIn
    batchPostToLinkedIn: (postIds) => {
        return api.post('/posts/batch-post-to-linkedin', { post_ids: postIds })
        // Backend uses stored access token
    }
}
```

## 5. Token Lifecycle

### A. Initial OAuth Flow
1. **User clicks "Connect LinkedIn"**
2. **Redirect to LinkedIn OAuth**: `https://linkedin.com/oauth/v2/authorization?...`
3. **User authorizes app**
4. **LinkedIn redirects back** with authorization code
5. **Backend exchanges code for tokens**:
   ```python
   token_data = await linkedin_service.exchange_code_for_token(auth_code)
   # Returns: access_token, refresh_token, expires_in
   ```
6. **Tokens stored in database**

### B. Token Usage Flow
1. **User creates/approves post**
2. **User clicks "Post to LinkedIn"**
3. **Backend retrieves stored access token**
4. **Backend validates token**:
   ```python
   is_valid = await linkedin_service.validate_token(access_token)
   ```
5. **If valid**: Use token to post content
6. **If expired**: Refresh token automatically
7. **Post content to LinkedIn** using token

### C. Token Refresh Flow
1. **Token expires** (typically 60 days)
2. **Backend detects invalid token**
3. **Backend uses refresh token** to get new access token
4. **New tokens stored** in database
5. **Continue with posting**

## 6. Security Considerations

### A. Token Storage Security
- **Encrypted in database** (if using MongoDB encryption)
- **Never logged** in application logs
- **Never exposed** to frontend
- **Stored per user** in platform_connections collection

### B. Token Usage Security
- **HTTPS only** for all API calls
- **Token validation** before each use
- **Automatic refresh** when expired
- **Error handling** for invalid tokens

### C. Token Permissions
Your LinkedIn access token has these permissions:
- `r_liteprofile`: Read basic profile information
- `r_emailaddress`: Read email address  
- `w_member_social`: Create and manage posts

## 7. Error Handling

### A. Token Expired
```python
if not is_valid:
    # Try to refresh token
    token_data = await linkedin_service.refresh_access_token(refresh_token)
    if token_data:
        # Update database with new token
        access_token = token_data["access_token"]
    else:
        # User needs to reconnect LinkedIn
        raise HTTPException("LinkedIn token expired")
```

### B. Invalid Token
```python
# LinkedIn API returns 401 Unauthorized
if response.status_code == 401:
    # Token is invalid, user needs to reconnect
    raise HTTPException("LinkedIn authentication failed")
```

## 8. Monitoring and Debugging

### A. Check Token Status
```bash
# Test your LinkedIn configuration
cd backend
python test_linkedin_config.py
```

### B. View Token in Database
```javascript
// In MongoDB shell
use social_media_automation
db.platform_connections.find({platform: "linkedin"})
```

### C. Check Token Validity
```python
# In your application
is_valid = await linkedin_service.validate_token(access_token)
print(f"Token valid: {is_valid}")
```

## 9. Production Considerations

### A. Token Rotation
- LinkedIn tokens expire after 60 days
- Refresh tokens can be used to get new access tokens
- If refresh fails, user must reconnect

### B. Rate Limits
- LinkedIn API has rate limits
- Monitor usage to avoid hitting limits
- Implement retry logic for failed requests

### C. Backup Strategy
- Store refresh tokens securely
- Implement fallback for token refresh failures
- Provide clear user messaging for reconnection

## Summary

Your LinkedIn OAuth access token is used in these key places:

1. **Token Storage**: MongoDB `platform_connections` collection
2. **Token Validation**: Before each LinkedIn API call
3. **Token Refresh**: When token expires (automatic)
4. **Content Posting**: All LinkedIn posts use the token
5. **Profile Access**: Getting user profile information
6. **Image Uploads**: Posting images to LinkedIn

The token is automatically managed by the system - you don't need to handle it manually. Once you connect your LinkedIn account, the platform will use the stored token to post your AI-generated content automatically. 