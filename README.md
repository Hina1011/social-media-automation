# Social Media Content Automation Platform

A comprehensive platform that automates social media content creation and scheduling for Instagram, LinkedIn, Facebook, and Twitter.

## Features

- **User Authentication**: Signup/Login with OTP verification
- **Role-based Access**: Individual and Company accounts
- **AI Content Generation**: 7-day post batches using Gemini 2.5 Pro
- **Multi-platform Posting**: Instagram, LinkedIn, Facebook, Twitter
- **LinkedIn Integration**: OAuth authentication and direct posting
- **Analytics Dashboard**: Growth and engagement tracking
- **Custom Scheduling**: Flexible posting schedules
- **Smart Content**: AI-generated captions, images, and hashtags

## Tech Stack

- **Frontend**: Vite + React.js + Tailwind CSS
- **Backend**: Python 3.10 + FastAPI
- **Database**: MongoDB Atlas (Cloud) or Local MongoDB
- **Authentication**: Gmail OTP
- **AI Integration**: Gemini 2.5 Pro API
- **LinkedIn Integration**: LinkedIn OAuth 2.0 + Marketing API
- **Scheduler**: Cron Jobs
- **Social APIs**: Meta API, LinkedIn API, Twitter API

## Project Structure

```
social-media-automation/
├── frontend/                 # React.js frontend application
├── backend/                  # FastAPI backend application
│   ├── utils/
│   │   └── linkedin_service.py  # LinkedIn OAuth and posting service
│   ├── routers/
│   │   ├── platforms.py      # Platform connection management
│   │   └── posts.py          # Post management with LinkedIn posting
│   └── LINKEDIN_SETUP.md     # LinkedIn integration setup guide
├── docs/                     # Documentation
└── README.md                 # This file
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- MongoDB Atlas account (recommended) or Local MongoDB
- Social Media API Keys
- LinkedIn Developer Account (for LinkedIn integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd social-media-automation
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**

   **Backend (.env file in backend directory):**
   ```env
   # MongoDB Atlas Configuration
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
   
   # Database Configuration
   DATABASE_NAME=social_media_automation
   
   # JWT Configuration
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Email Configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   
   # AI Configuration
   GEMINI_API_KEY=your-gemini-api-key
   
   # LinkedIn OAuth Configuration
   LINKEDIN_CLIENT_ID=your-linkedin-client-id
   LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
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
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   BASE_URL=http://localhost:8000
   ```

   **Frontend (.env file in frontend directory):**
   ```env
   VITE_API_URL=http://localhost:8000
   ```

5. **LinkedIn Integration Setup**

   The platform includes full LinkedIn integration with OAuth authentication and direct posting capabilities.

   **To set up LinkedIn integration:**
   
   1. Create a LinkedIn Developer account at https://developer.linkedin.com/
   2. Create a new LinkedIn app
   3. Configure OAuth 2.0 settings with redirect URI: `http://localhost:3000/linkedin-callback`
   4. Request access to "Sign In with LinkedIn" and "Marketing Developer Platform"
   5. Add your LinkedIn credentials to the `.env` file
   
   For detailed setup instructions, see `backend/LINKEDIN_SETUP.md`

6. **MongoDB Atlas Setup (Recommended)**
   
   The application is configured to use MongoDB Atlas by default. To set up:
   
   - Create a MongoDB Atlas account at https://www.mongodb.com/atlas
   - Create a new cluster
   - Get your connection string from the "Connect" button
   - Add your connection string to the `MONGODB_URL` environment variable
   - Whitelist your IP address in MongoDB Atlas
   
   For detailed setup instructions, see `backend/MONGODB_SETUP.md`

7. **Test Database Connection**
   ```bash
   cd backend
   python test_mongodb_connection.py
   ```

8. **Test LinkedIn Integration**
   ```bash
   cd backend
   python test_linkedin_integration.py
   ```

9. **Run the Application**
   ```bash
   # Backend (from backend directory)
   uvicorn main:app --reload
   
   # Frontend (from frontend directory)
   npm run dev
   ```

## LinkedIn Integration Features

The platform includes comprehensive LinkedIn integration:

- **OAuth 2.0 Authentication**: Secure user authentication with LinkedIn
- **Direct Posting**: Post AI-generated content directly to LinkedIn
- **Batch Posting**: Post multiple posts to LinkedIn at once
- **Token Management**: Automatic token refresh and validation
- **Profile Integration**: Access to user profile information
- **Image Support**: Post content with AI-generated images

### LinkedIn API Endpoints

- `GET /api/platforms/linkedin/auth-url` - Get LinkedIn OAuth URL
- `POST /api/platforms/linkedin/callback` - Handle OAuth callback
- `POST /api/platforms/linkedin/post` - Post content to LinkedIn
- `POST /api/posts/{post_id}/post-to-linkedin` - Post specific post to LinkedIn
- `POST /api/posts/batch-post-to-linkedin` - Batch post to LinkedIn

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License 