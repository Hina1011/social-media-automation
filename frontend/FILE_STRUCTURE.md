# Frontend File Structure

This document outlines the complete file structure of the Social Media Automation Platform frontend, converted from TypeScript to JavaScript.

## Root Directory

```
frontend/
├── .eslintrc.cjs          # ESLint configuration for JavaScript
├── .gitignore             # Git ignore rules
├── index.html             # Main HTML file
├── package.json           # Project dependencies and scripts
├── postcss.config.js      # PostCSS configuration
├── README.md              # Project documentation
├── tailwind.config.js     # Tailwind CSS configuration
├── vite.config.js         # Vite build configuration
└── FILE_STRUCTURE.md      # This file
```

## Source Directory (`src/`)

```
src/
├── App.jsx                # Main application component
├── index.css              # Global styles and Tailwind imports
├── main.jsx               # Application entry point
├── components/            # Reusable UI components
│   ├── Layout.jsx         # Main layout with sidebar navigation
│   └── ProtectedRoute.jsx # Route protection component
├── contexts/              # React contexts for state management
│   └── AuthContext.jsx    # Authentication context
├── pages/                 # Page components
│   ├── AnalyticsPage.jsx  # Analytics and reporting page
│   ├── DashboardPage.jsx  # Main dashboard page
│   ├── LandingPage.jsx    # Public landing page
│   ├── LoginPage.jsx      # User login page
│   ├── PlatformsPage.jsx  # Platform connection management
│   ├── PostsPage.jsx      # Content management page
│   ├── ProfilePage.jsx    # User profile settings
│   └── SignupPage.jsx     # User registration page
├── services/              # API and external services
│   └── api.js            # API client and endpoint definitions
└── utils/                 # Utility functions
    └── index.js          # Common helper functions
```

## File Details

### Configuration Files

1. **`.eslintrc.cjs`** - ESLint configuration for JavaScript
   - Configured for React development
   - Includes React Hooks and React Refresh plugins
   - No TypeScript dependencies

2. **`package.json`** - Project configuration
   - All TypeScript dependencies removed
   - JavaScript-only dependencies
   - Updated build scripts for JS/JSX files

3. **`vite.config.js`** - Vite build configuration
   - React plugin enabled
   - Path aliases configured
   - Development server proxy to backend

4. **`tailwind.config.js`** - Tailwind CSS configuration
   - Custom color palette (primary, secondary)
   - Custom animations and keyframes
   - Updated content paths for JS/JSX files only

5. **`postcss.config.js`** - PostCSS configuration
   - Tailwind CSS and Autoprefixer plugins

### Core Application Files

1. **`main.jsx`** - Application entry point
   - React 18 with Strict Mode
   - BrowserRouter for routing
   - Toaster for notifications

2. **`App.jsx`** - Main application component
   - Route definitions
   - Authentication provider wrapper
   - Protected route implementation

3. **`index.css`** - Global styles
   - Tailwind CSS imports
   - Custom component classes
   - Utility classes

### Components

1. **`Layout.jsx`** - Main layout component
   - Responsive sidebar navigation
   - Mobile menu support
   - User profile section

2. **`ProtectedRoute.jsx`** - Route protection
   - Authentication check
   - Loading states
   - Redirect to login

### Contexts

1. **`AuthContext.jsx`** - Authentication context
   - User state management
   - Login/logout functions
   - Token management

### Pages

1. **`LandingPage.jsx`** - Public landing page
   - Hero section
   - Features overview
   - Call-to-action sections

2. **`LoginPage.jsx`** - User authentication
   - Email/password form
   - Form validation
   - Error handling

3. **`SignupPage.jsx`** - User registration
   - Registration form
   - Account type selection
   - Password confirmation

4. **`DashboardPage.jsx`** - Main dashboard
   - Overview statistics
   - Quick actions
   - Recent activity

5. **`ProfilePage.jsx`** - User profile management
   - Profile information editing
   - Interests selection
   - Account settings

6. **`PostsPage.jsx`** - Content management
   - Post generation
   - Post approval workflow
   - Content scheduling

7. **`AnalyticsPage.jsx`** - Analytics and reporting
   - Performance metrics
   - Growth charts
   - Platform analytics

8. **`PlatformsPage.jsx`** - Platform connections
   - Social media platform integration
   - Connection management
   - Platform status

### Services

1. **`api.js`** - API client
   - Axios configuration
   - Request/response interceptors
   - API endpoint definitions

### Utils

1. **`index.js`** - Utility functions
   - CSS class merging
   - Date formatting
   - Text utilities
   - Common helper functions

## Conversion Summary

### From TypeScript to JavaScript

✅ **All TypeScript files converted to JavaScript**
- Removed all type annotations
- Removed interface definitions
- Removed generic types
- Updated file extensions (.tsx → .jsx, .ts → .js)

✅ **Configuration updated**
- ESLint configuration for JavaScript
- Vite configuration updated
- Package.json dependencies cleaned
- Tailwind config updated

✅ **Functionality preserved**
- All React components work identically
- All hooks and state management intact
- All API calls and data flow maintained
- All styling and UI components preserved

✅ **Additional files added**
- Utility functions for common operations
- Proper .gitignore file
- Comprehensive documentation

## Ready to Use

The frontend is now completely converted to JavaScript and ready for development. All files are present, properly configured, and the application should run without any issues.

### To start development:
```bash
cd frontend
npm install
npm run dev
```

### To build for production:
```bash
npm run build
``` 