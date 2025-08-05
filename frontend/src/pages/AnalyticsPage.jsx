import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext.jsx'
import { analyticsAPI } from '../services/api.js'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import {
  TrendingUp,
  Users,
  Heart,
  MessageCircle,
  Share2,
  Eye,
  Calendar,
  Filter
} from 'lucide-react'

export function AnalyticsPage() {
  const { user } = useAuth()
  const [analytics, setAnalytics] = useState({
    summary: {},
    growth: [],
    platformData: {},
    postsPerformance: []
  })
  const [isLoading, setIsLoading] = useState(true)
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [timeRange, setTimeRange] = useState(30)

  useEffect(() => {
    loadAnalytics()
  }, [timeRange])

  const loadAnalytics = async () => {
    try {
      const [summaryResponse, growthResponse, postsResponse] = await Promise.all([
        analyticsAPI.getSummary(),
        analyticsAPI.getGrowthAnalytics(timeRange),
        analyticsAPI.getPostsPerformance(10)
      ])

      setAnalytics({
        summary: summaryResponse.data,
        growth: growthResponse.data.growth_data || [],
        platformData: growthResponse.data.platform_data || {},
        postsPerformance: postsResponse.data || []
      })
    } catch (error) {
      console.error('Error loading analytics:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const platforms = ['instagram', 'linkedin', 'facebook', 'twitter']
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

  const getMetricCard = (title, value, change, icon, color) => (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
            <p className={`text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {change >= 0 ? '+' : ''}{change}% from last month
            </p>
          )}
        </div>
        <div className={`w-12 h-12 ${color} rounded-lg flex items-center justify-center`}>
          {icon}
        </div>
      </div>
    </div>
  )

  const getGrowthChart = () => {
    if (!analytics.growth || analytics.growth.length === 0) {
      return (
        <div className="flex items-center justify-center h-64 text-gray-500">
          No growth data available
        </div>
      )
    }

    return (
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={analytics.growth}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="followers" stroke="#3B82F6" strokeWidth={2} />
          <Line type="monotone" dataKey="engagement" stroke="#10B981" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    )
  }

  const getPlatformChart = () => {
    const platformData = Object.entries(analytics.platformData).map(([platform, data]) => ({
      name: platform,
      followers: data.followers || 0,
      engagement: data.engagement || 0
    }))

    if (platformData.length === 0) {
      return (
        <div className="flex items-center justify-center h-64 text-gray-500">
          No platform data available
        </div>
      )
    }

    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={platformData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="followers" fill="#3B82F6" />
          <Bar dataKey="engagement" fill="#10B981" />
        </BarChart>
      </ResponsiveContainer>
    )
  }

  const getPostsPerformanceChart = () => {
    if (!analytics.postsPerformance || analytics.postsPerformance.length === 0) {
      return (
        <div className="flex items-center justify-center h-64 text-gray-500">
          No posts performance data available
        </div>
      )
    }

    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={analytics.postsPerformance}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="platform" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="likes" fill="#EF4444" />
          <Bar dataKey="comments" fill="#F59E0B" />
          <Bar dataKey="shares" fill="#8B5CF6" />
        </BarChart>
      </ResponsiveContainer>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Track your social media performance and growth</p>
        </div>
        <div className="flex items-center space-x-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(Number(e.target.value))}
            className="input-field w-32"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {getMetricCard(
          'Total Followers',
          analytics.summary.total_followers?.toLocaleString() || '0',
          analytics.summary.followers_growth || 0,
          <Users className="w-6 h-6 text-white" />,
          'bg-blue-500'
        )}
        {getMetricCard(
          'Total Engagement',
          analytics.summary.total_engagement?.toLocaleString() || '0',
          analytics.summary.engagement_growth || 0,
          <Heart className="w-6 h-6 text-white" />,
          'bg-red-500'
        )}
        {getMetricCard(
          'Engagement Rate',
          `${analytics.summary.average_engagement_rate?.toFixed(1) || '0'}%`,
          analytics.summary.engagement_rate_growth || 0,
          <TrendingUp className="w-6 h-6 text-white" />,
          'bg-green-500'
        )}
        {getMetricCard(
          'Total Posts',
          analytics.summary.total_posts || '0',
          null,
          <Calendar className="w-6 h-6 text-white" />,
          'bg-purple-500'
        )}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Growth Chart */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Growth Over Time</h2>
          {getGrowthChart()}
        </div>

        {/* Platform Performance */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Platform Performance</h2>
          {getPlatformChart()}
        </div>
      </div>

      {/* Posts Performance */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Posts Performance</h2>
        {getPostsPerformanceChart()}
      </div>

      {/* Platform Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {platforms.map((platform, index) => {
          const platformData = analytics.platformData[platform] || {}
          return (
            <div key={platform} className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900 capitalize">{platform}</h3>
                <div className={`w-8 h-8 ${COLORS[index]} rounded-lg flex items-center justify-center`}>
                  <Share2 className="w-4 h-4 text-white" />
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Followers</span>
                  <span className="text-sm font-medium text-gray-900">
                    {platformData.followers?.toLocaleString() || '0'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Engagement</span>
                  <span className="text-sm font-medium text-gray-900">
                    {platformData.engagement?.toLocaleString() || '0'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Rate</span>
                  <span className="text-sm font-medium text-gray-900">
                    {platformData.engagement_rate?.toFixed(1) || '0'}%
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <div className="space-y-4">
          {analytics.postsPerformance.slice(0, 5).map((post, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-primary-600 capitalize">
                    {post.platform?.charAt(0)}
                  </span>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {post.caption?.substring(0, 50)}...
                  </p>
                  <p className="text-xs text-gray-500 capitalize">{post.platform}</p>
                </div>
              </div>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span className="flex items-center">
                  <Heart className="w-4 h-4 mr-1" />
                  {post.likes}
                </span>
                <span className="flex items-center">
                  <MessageCircle className="w-4 h-4 mr-1" />
                  {post.comments}
                </span>
                <span className="flex items-center">
                  <Share2 className="w-4 h-4 mr-1" />
                  {post.shares}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 