# MongoDB Setup Guide for LinkedIn Integration

## The Problem
Your LinkedIn OAuth callback is failing because MongoDB is not running. The backend can't save the LinkedIn access token to the database.

## Quick Solution: MongoDB Atlas (Recommended)

### Step 1: Create MongoDB Atlas Account
1. Go to https://www.mongodb.com/atlas
2. Click "Try Free"
3. Create an account

### Step 2: Create a Free Cluster
1. Click "Build a Database"
2. Choose "FREE" tier (M0)
3. Choose a cloud provider (AWS, Google Cloud, or Azure)
4. Choose a region close to you
5. Click "Create"

### Step 3: Set Up Database Access
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and password (save these!)
5. Set privileges to "Read and write to any database"
6. Click "Add User"

### Step 4: Set Up Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. Click "Confirm"

### Step 5: Get Your Connection String
1. Go to "Database" in the left sidebar
2. Click "Connect"
3. Choose "Connect your application"
4. Copy the connection string

### Step 6: Update Your .env File
Add this line to your `.env` file:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/social_media_automation?retryWrites=true&w=majority
```

Replace:
- `<username>` with your database username
- `<password>` with your database password
- `<cluster>` with your cluster name

## Alternative: Install MongoDB Locally

### Step 1: Download MongoDB
1. Go to https://www.mongodb.com/try/download/community
2. Download MongoDB Community Server for Windows
3. Run the installer

### Step 2: Start MongoDB
```bash
# Start MongoDB service
mongod
```

### Step 3: Verify Connection
Your current configuration should work:
```env
MONGODB_URL=mongodb://localhost:27017
```

## Test the Setup

After setting up MongoDB, run:
```bash
python check_backend_status.py
```

You should see:
```
✅ Database connection successful
✅ Users collection has X users
```

## Next Steps

1. Set up MongoDB (Atlas or local)
2. Restart your backend server
3. Try the LinkedIn Connect button again
4. The OAuth flow should now complete successfully

## Troubleshooting

- **"Database connection not available"**: MongoDB is not running
- **"Authentication failed"**: Check your username/password in the connection string
- **"Network timeout"**: Check your internet connection and firewall settings 