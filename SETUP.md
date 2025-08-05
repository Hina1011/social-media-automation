# Social Media Automation Platform - Setup Guide

This guide will help you set up and run the Social Media Automation Platform on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **MongoDB** - [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git** - [Download Git](https://git-scm.com/)

## Quick Start (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd social-media-automation
   ```

2. **Run the startup script**
   ```bash
   python start.py
   ```

   This script will automatically:
   - Check your system requirements
   - Set up virtual environments
   - Install dependencies
   - Start both backend and frontend servers

3. **Configure environment variables**
   - Copy `backend/env.example` to `backend/.env`
   - Update the configuration with your API keys and settings

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup

If you prefer to set up manually or the startup script doesn't work:

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   
  python -m venv venv ```

3. **Activate virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

6. **Start the backend server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

## Environment Configuration

Create a `.env` file in the `backend` directory with the following variables:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=social_media_automation

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (Gmail OTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# Social Media API Keys
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
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

## Getting API Keys

### Gemini AI (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### Gmail App Password (Required for OTP)
1. Enable 2-factor authentication on your Google account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Generate an App Password for "Mail"
4. Add it to your `.env` file as `EMAIL_PASSWORD`

### Social Media APIs (Optional)
- **Facebook/Instagram**: [Facebook Developers](https://developers.facebook.com/)
- **LinkedIn**: [LinkedIn Developers](https://developer.linkedin.com/)
- **Twitter**: [Twitter Developer Portal](https://developer.twitter.com/)

## Project Structure

```
social-media-automation/
├── backend/                 # FastAPI backend
│   ├── models/             # Pydantic models
│   ├── routers/            # API routes
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration
│   ├── database.py         # Database connection
│   ├── main.py             # FastAPI app
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── main.tsx        # App entry point
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── start.py                # Startup script
├── README.md               # Project documentation
└── SETUP.md               # This file
```

## Features

### ✅ Implemented
- User authentication with JWT tokens
- Email OTP verification
- User registration and profile management
- AI-powered content generation using Gemini
- Social media platform connections
- Post management and scheduling
- Analytics dashboard
- Responsive UI with Tailwind CSS

### 🚧 In Development
- Automated posting to social media platforms
- Advanced analytics and reporting
- Image generation and management
- Team collaboration features
- Advanced scheduling options

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   
   # Kill process using port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **MongoDB connection failed**
   - Make sure MongoDB is running
   - Check your MongoDB connection string in `.env`

3. **Email not sending**
   - Verify your Gmail app password
   - Check if 2FA is enabled on your Google account

4. **AI content generation failing**
   - Verify your Gemini API key
   - Check your internet connection

### Getting Help

If you encounter any issues:

1. Check the console output for error messages
2. Verify all environment variables are set correctly
3. Ensure all dependencies are installed
4. Check that MongoDB is running
5. Review the API documentation at http://localhost:8000/docs

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Backend Deployment
1. Set up a production MongoDB instance
2. Configure environment variables for production
3. Use a production ASGI server like Gunicorn
4. Set up proper CORS origins

### Frontend Deployment
1. Build the production version: `npm run build`
2. Deploy the `dist` folder to your hosting service
3. Configure environment variables for production API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at http://localhost:8000/docs
- Review the troubleshooting section above

---

**Happy coding! 🚀** 