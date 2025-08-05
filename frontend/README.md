# Social Media Automation Frontend

A React-based frontend for the Social Media Automation Platform, built with JavaScript (not TypeScript).

## Features

- **Modern React**: Built with React 18 and functional components with hooks
- **JavaScript**: Pure JavaScript implementation (no TypeScript)
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Routing**: Client-side routing with React Router
- **Forms**: Form handling with React Hook Form
- **Charts**: Data visualization with Recharts
- **Icons**: Beautiful icons with Lucide React
- **Notifications**: Toast notifications with React Hot Toast

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **React Hook Form** - Form state management
- **Axios** - HTTP client
- **Recharts** - Chart library
- **Lucide React** - Icon library
- **React Hot Toast** - Toast notifications

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Linting

```bash
npm run lint
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout.jsx      # Main layout component
│   └── ProtectedRoute.jsx # Route protection component
├── contexts/           # React contexts
│   └── AuthContext.jsx # Authentication context
├── pages/              # Page components
│   ├── LandingPage.jsx # Landing page
│   ├── LoginPage.jsx   # Login page
│   ├── SignupPage.jsx  # Signup page
│   ├── DashboardPage.jsx # Dashboard
│   ├── ProfilePage.jsx # User profile
│   ├── PostsPage.jsx   # Posts management
│   ├── AnalyticsPage.jsx # Analytics
│   └── PlatformsPage.jsx # Platform connections
├── services/           # API services
│   └── api.js         # API client and endpoints
├── App.jsx            # Main app component
├── main.jsx           # App entry point
└── index.css          # Global styles
```

## Key Features

### Authentication
- JWT-based authentication
- Protected routes
- Login/signup forms
- User profile management

### Dashboard
- Overview of social media performance
- Quick actions
- Recent activity
- Platform connection status

### Content Management
- AI-powered post generation
- Post approval workflow
- Multi-platform posting
- Content scheduling

### Analytics
- Performance metrics
- Growth charts
- Platform-specific analytics
- Post performance tracking

### Platform Integration
- Connect multiple social media platforms
- Instagram, LinkedIn, Facebook, Twitter support
- Secure OAuth integration

## Development Notes

### JavaScript vs TypeScript
This project uses JavaScript instead of TypeScript for simplicity. All components are written in JSX with proper PropTypes or JSDoc comments for type safety.

### API Integration
The frontend communicates with the backend API through the `services/api.js` file, which provides a clean interface for all API calls.

### State Management
React Context is used for global state management (authentication, user data). Local component state is managed with React hooks.

### Styling
Tailwind CSS is used for styling with custom CSS classes defined in `index.css`. The design is responsive and follows modern UI/UX principles.

## Contributing

1. Follow the existing code style
2. Use functional components with hooks
3. Keep components small and focused
4. Add proper error handling
5. Test your changes thoroughly

## License

This project is part of the Social Media Automation Platform. 