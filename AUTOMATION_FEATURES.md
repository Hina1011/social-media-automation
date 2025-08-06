# Social Media Automation Features

## Overview

This platform now includes comprehensive automation features that handle the entire social media content lifecycle from generation to posting.

## Key Automation Features

### 1. Automatic Post Generation on Signup

**What happens:**
- When a user signs up as an "individual", the system automatically generates 7 days of posts
- Posts are created based on the user's interests and custom prompt
- All posts are initially marked as "pending_approval"

**Technical details:**
- Uses AI (Gemini 2.0) to generate engaging content
- Creates posts for multiple platforms (Instagram, LinkedIn, Facebook, Twitter)
- Generates appropriate hashtags and captions
- Schedules posts starting from the next day

### 2. Calendar View with Approval System

**Features:**
- Visual calendar showing all posts with status indicators
- Color-coded post status (pending, approved, scheduled, posted)
- Batch management with approval controls
- Time scheduling for posting

**Status Colors:**
- 🟡 Yellow: Pending approval
- 🟢 Green: Approved
- 🔵 Blue: Scheduled
- 🟣 Purple: Posted

### 3. Batch Approval System

**Process:**
1. User reviews generated posts in calendar view
2. Can approve entire batch with one click
3. Approved posts are automatically scheduled for posting
4. Next batch is generated after current one is approved

**API Endpoints:**
- `POST /api/posts/batch-approve` - Approve all posts in a batch
- `GET /api/posts/pending-approval` - Get posts pending approval
- `GET /api/posts/batches` - Get all user batches

### 4. Automatic Scheduling

**Features:**
- Posts are scheduled at user's preferred time (default: 9:00 AM)
- Scheduler runs every 60 seconds to check for due posts
- Posts are automatically published to connected platforms
- Failed posts are marked and logged

**Scheduling Process:**
1. User sets preferred posting time
2. Approved posts are scheduled at that time
3. Scheduler checks for due posts every minute
4. Posts are published to all connected platforms

### 5. Continuous Content Generation

**Process:**
1. When current batch is approved, next batch is automatically generated
2. New batch starts 7 days after the last post
3. User receives notification when new batch is ready
4. Cycle continues automatically

**API Endpoints:**
- `POST /api/posts/regenerate-next-batch` - Generate next 7 days of posts

### 6. Multi-Platform Integration

**Supported Platforms:**
- LinkedIn (with OAuth integration)
- Instagram (planned)
- Facebook (planned)
- Twitter (planned)

**Posting Process:**
1. Check which platforms are connected
2. Format content appropriately for each platform
3. Post simultaneously to all connected platforms
4. Track posting success/failure

### 7. Notification System

**Email Notifications:**
- **Batch Ready**: When new posts are generated and ready for approval
- **Approval Reminder**: When posts have been pending for too long
- **Posting Success**: When posts are successfully published

**Notification Triggers:**
- New batch generation
- Posts pending approval for 24+ hours
- Successful posting to platforms

## User Workflow

### For New Users:

1. **Signup**: Choose "Individual" account type
2. **Fill Form**: Provide interests, custom prompt, and other details
3. **Auto-Generation**: System generates 7 days of posts automatically
4. **Review**: User sees posts in calendar view
5. **Approve**: User approves posts with one click
6. **Automatic Posting**: Posts are scheduled and published automatically
7. **Continuous**: New batches are generated automatically

### For Existing Users:

1. **Login**: Access dashboard with pending approvals
2. **Review**: Check generated posts in calendar
3. **Approve**: Approve batch to start posting
4. **Monitor**: Track posting progress and analytics
5. **Repeat**: New batches are generated automatically

## Technical Architecture

### Backend Components:

1. **Scheduler Service** (`utils/scheduler.py`):
   - Runs every 60 seconds
   - Checks for due posts
   - Handles platform posting
   - Updates post status

2. **Notification Service** (`utils/notifications.py`):
   - Sends email notifications
   - Tracks user engagement
   - Manages notification timing

3. **AI Generator** (`utils/ai_generator.py`):
   - Generates content using Gemini 2.0
   - Creates platform-specific content
   - Handles image generation

4. **Batch Management** (`routers/posts.py`):
   - Handles batch approval
   - Manages post status
   - Coordinates with scheduler

### Database Schema Updates:

**Posts Collection:**
```javascript
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "caption": String,
  "hashtags": Array,
  "scheduled_date": String,
  "status": String, // "pending_approval", "approved", "scheduled", "posted", "failed"
  "platforms": Array,
  "batch_id": String,
  "is_auto_generated": Boolean,
  "approved_at": String,
  "posted_at": String,
  "posted_to": Array,
  "error_message": String
}
```

**Users Collection:**
```javascript
{
  "schedule_time": String, // "HH:MM" format
  "is_auto_generated": Boolean
}
```

## Configuration

### Environment Variables:

```env
# AI Configuration
GEMINI_API_KEY=your-gemini-api-key

# Email Configuration (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Platform API Keys
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

### Default Settings:

- **Posting Time**: 9:00 AM (user-configurable)
- **Batch Size**: 7 days
- **Scheduler Interval**: 60 seconds
- **Notification Delay**: 24 hours for reminders

## Monitoring and Analytics

### Dashboard Features:

1. **Automation Status**: Shows if automation is active
2. **Batch Overview**: Displays all batches with status
3. **Pending Approvals**: Highlights posts needing review
4. **Platform Status**: Shows connected platforms
5. **Recent Activity**: Tracks automation events

### Analytics Tracking:

- Posts generated per user
- Approval rates
- Posting success rates
- Platform performance
- User engagement metrics

## Error Handling

### Common Issues:

1. **AI Generation Failures**: Fallback content is generated
2. **Platform Posting Failures**: Posts are marked as failed with error details
3. **Scheduler Issues**: Logs are maintained for debugging
4. **Notification Failures**: Non-blocking, logged for review

### Recovery Mechanisms:

- Automatic retry for failed posts
- Fallback content generation
- Error logging and monitoring
- User notifications for critical issues

## Future Enhancements

### Planned Features:

1. **Advanced Scheduling**: Multiple posting times per day
2. **Content Templates**: Pre-defined content structures
3. **A/B Testing**: Test different content variations
4. **Advanced Analytics**: Detailed performance metrics
5. **Team Collaboration**: Multi-user approval workflows
6. **Content Calendar**: Advanced calendar management
7. **Platform-Specific Optimization**: Tailored content for each platform

### Integration Roadmap:

1. **Instagram API**: Direct posting to Instagram
2. **Facebook API**: Facebook page integration
3. **Twitter API**: Twitter posting capabilities
4. **TikTok API**: TikTok content management
5. **YouTube API**: Video content automation

## Support and Troubleshooting

### Common Questions:

**Q: How often are new batches generated?**
A: New batches are generated automatically after the current batch is approved.

**Q: Can I change the posting time?**
A: Yes, users can set their preferred posting time in the dashboard.

**Q: What happens if a post fails to publish?**
A: Failed posts are marked with error details and can be retried manually.

**Q: How do I connect social media platforms?**
A: Go to the Platforms page and follow the OAuth connection process.

### Debugging:

- Check application logs for scheduler errors
- Monitor email delivery for notification issues
- Review platform API responses for posting failures
- Verify AI generation logs for content issues

## Security Considerations

1. **API Key Management**: All keys are stored securely
2. **OAuth Tokens**: Platform tokens are encrypted
3. **User Data**: Personal information is protected
4. **Content Privacy**: Generated content is user-owned
5. **Platform Permissions**: Minimal required permissions only

This automation system provides a complete solution for social media content management, from generation to posting, with minimal user intervention required. 