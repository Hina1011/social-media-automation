import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import { analyticsAPI, platformsAPI, postsAPI } from '../services/api.js'
import { CalendarView } from '../components/CalendarView.jsx'
import { BatchManager } from '../components/BatchManager.jsx'
import {
  Users,
  TrendingUp,
  Calendar,
  Share2,
  Plus,
  BarChart3,
  FileText,
  Settings,
  ArrowRight,
  Grid3X3
} from 'lucide-react'

export function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    totalFollowers: 0,
    totalEngagement: 0,
    averageEngagementRate: 0,
    totalPosts: 0
  })
  const [platformStatus, setPlatformStatus] = useState({
    instagram: false,
    linkedin: false,
    facebook: false,
    twitter: false
  })
  const [isLoading, setIsLoading] = useState(true)
  const [viewMode, setViewMode] = useState('calendar') // 'calendar' or 'overview'

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [analyticsResponse, platformResponse] = await Promise.all([
        analyticsAPI.getSummary(),
        platformsAPI.getStatus()
      ])

      setStats({
        totalFollowers: analyticsResponse.data.total_followers || 0,
        totalEngagement: analyticsResponse.data.total_engagement || 0,
        averageEngagementRate: analyticsResponse.data.average_engagement_rate || 0,
        totalPosts: analyticsResponse.data.top_posts?.length || 0
      })

      setPlatformStatus(platformResponse.data)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const quickActions = [
    {
      title: 'Generate Posts',
      description: 'Create AI-powered content for your social media',
      icon: Plus,
      href: '/posts',
      color: 'bg-blue-500'
    },
    {
      title: 'View Analytics',
      description: 'Check your performance and growth metrics',
      icon: BarChart3,
      href: '/analytics',
      color: 'bg-green-500'
    },
    {
      title: 'Connect Platforms',
      description: 'Link your social media accounts',
      icon: Share2,
      href: '/platforms',
      color: 'bg-purple-500'
    },
    {
      title: 'Manage Profile',
      description: 'Update your account settings and preferences',
      icon: Settings,
      href: '/profile',
      color: 'bg-orange-500'
    }
  ]

  const connectedPlatforms = Object.values(platformStatus).filter(Boolean).length

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">
          Welcome back, {user?.full_name?.split(' ')[0]}! 👋
        </h1>
        <p className="text-primary-100">
          Manage your social media content with our AI-powered calendar
        </p>
      </div>

      {/* View Mode Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => setViewMode('calendar')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              viewMode === 'calendar'
                ? 'bg-white text-primary-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Calendar className="w-4 h-4 inline mr-2" />
            Calendar View
          </button>
          <button
            onClick={() => setViewMode('overview')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              viewMode === 'overview'
                ? 'bg-white text-primary-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Grid3X3 className="w-4 h-4 inline mr-2" />
            Overview
          </button>
        </div>

        {/* Quick Stats */}
        <div className="flex items-center space-x-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-gray-600">Approved</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span className="text-gray-600">Scheduled</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
            <span className="text-gray-600">Draft</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      {viewMode === 'calendar' ? (
        <div className="space-y-6">
          <BatchManager onUpdate={loadDashboardData} />
          <CalendarView />
        </div>
      ) : (
        <div className="space-y-6">
          {/* Stats Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Users className="w-5 h-5 text-blue-600" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Followers</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalFollowers.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Engagement</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalEngagement.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                    <BarChart3 className="w-5 h-5 text-purple-600" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Engagement Rate</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.averageEngagementRate.toFixed(1)}%</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                    <FileText className="w-5 h-5 text-orange-600" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Posts</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalPosts}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Platform Status */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Platform Connections</h2>
              <Link
                to="/platforms"
                className="text-sm text-primary-600 hover:text-primary-500 font-medium"
              >
                Manage
              </Link>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(platformStatus).map(([platform, isConnected]) => (
                <div key={platform} className="text-center">
                  <div className={`w-12 h-12 mx-auto rounded-lg flex items-center justify-center mb-2 ${
                    isConnected ? 'bg-green-100' : 'bg-gray-100'
                  }`}>
                    <Share2 className={`w-6 h-6 ${
                      isConnected ? 'text-green-600' : 'text-gray-400'
                    }`} />
                  </div>
                  <p className="text-sm font-medium text-gray-900 capitalize">{platform}</p>
                  <p className={`text-xs ${
                    isConnected ? 'text-green-600' : 'text-gray-500'
                  }`}>
                    {isConnected ? 'Connected' : 'Not Connected'}
                  </p>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                {connectedPlatforms === 0
                  ? 'No platforms connected. Connect your social media accounts to start posting.'
                  : `${connectedPlatforms} platform${connectedPlatforms > 1 ? 's' : ''} connected.`
                }
              </p>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {quickActions.map((action, index) => (
                <Link
                  key={index}
                  to={action.href}
                  className="group p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all"
                >
                  <div className="flex items-center">
                    <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center mr-3`}>
                      <action.icon className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-sm font-medium text-gray-900 group-hover:text-primary-600">
                        {action.title}
                      </h3>
                      <p className="text-xs text-gray-500 mt-1">{action.description}</p>
                    </div>
                    <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-primary-600 transition-colors" />
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
              <Link
                to="/posts"
                className="text-sm text-primary-600 hover:text-primary-500 font-medium"
              >
                View All
              </Link>
            </div>
            <div className="space-y-3">
              <div className="flex items-center p-3 bg-gray-50 rounded-lg">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <Calendar className="w-4 h-4 text-blue-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">New posts generated</p>
                  <p className="text-xs text-gray-500">7 posts scheduled for next week</p>
                </div>
                <span className="text-xs text-gray-400">2 hours ago</span>
              </div>

              <div className="flex items-center p-3 bg-gray-50 rounded-lg">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                  <TrendingUp className="w-4 h-4 text-green-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">Engagement increased</p>
                  <p className="text-xs text-gray-500">Your posts got 15% more likes this week</p>
                </div>
                <span className="text-xs text-gray-400">1 day ago</span>
              </div>

              <div className="flex items-center p-3 bg-gray-50 rounded-lg">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                  <Users className="w-4 h-4 text-purple-600" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">New followers</p>
                  <p className="text-xs text-gray-500">You gained 25 new followers</p>
                </div>
                <span className="text-xs text-gray-400">3 days ago</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 