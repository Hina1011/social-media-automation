import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext.jsx'
import { platformsAPI } from '../services/api.js'
import { InstagramLoginModal } from '../components/InstagramLoginModal.jsx'
import {
  Instagram,
  Linkedin,
  Facebook,
  Twitter,
  Link as LinkIcon,
  Unlink,
  CheckCircle,
  AlertCircle,
  ExternalLink
} from 'lucide-react'
import toast from 'react-hot-toast'

export function PlatformsPage() {
  const { user } = useAuth()
  const [connections, setConnections] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isConnecting, setIsConnecting] = useState(false)
  const [selectedPlatform, setSelectedPlatform] = useState(null)
  const [showInstagramModal, setShowInstagramModal] = useState(false)

  useEffect(() => {
    loadConnections()
    // Check for OAuth callback parameters
    checkOAuthCallback()
  }, [])

  const checkOAuthCallback = () => {
    // LinkedIn callback is now handled by the dedicated LinkedInCallbackPage
    // Clean up any leftover URL parameters
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.get('code') || urlParams.get('state')) {
      window.history.replaceState({}, document.title, window.location.pathname)
    }
  }



  const loadConnections = async () => {
    try {
      console.log('🔗 Loading platform connections...')
      
      // First try to load from localStorage (for frontend-only connections)
      const localConnections = JSON.parse(localStorage.getItem('platform_connections') || '[]')
      console.log('🔗 Local connections:', localConnections)
      
      // Then try to load from backend
      try {
        const response = await platformsAPI.getConnections()
        console.log('✅ Backend connections loaded:', response.data)
        
        // Merge local and backend connections
        const allConnections = [...localConnections, ...response.data]
        const uniqueConnections = allConnections.filter((connection, index, self) => 
          index === self.findIndex(c => c.platform === connection.platform)
        )
        
        setConnections(uniqueConnections)
      } catch (error) {
        console.log('⚠️ Backend connection failed, using local connections only')
        setConnections(localConnections)
      }
      
    } catch (error) {
      console.error('❌ Error loading connections:', error)
      toast.error('Failed to load platform connections')
    } finally {
      setIsLoading(false)
    }
  }

  const handleConnectPlatform = async (platform) => {
    if (platform === 'instagram') {
      // Show Instagram login modal for frontend-only connection
      setShowInstagramModal(true)
      return
    }
    
    if (platform === 'linkedin') {
      // Handle LinkedIn OAuth
      await handleLinkedInConnect()
      return
    }
    
    setIsConnecting(true)
    setSelectedPlatform(platform)
    
    try {
      console.log(`🔗 Connecting to ${platform}...`)
      
      // For other platforms, try backend connection
      const response = await platformsAPI.connectPlatform({
        platform,
        auth_code: null
      })
      
      console.log('🔗 Platform connection response:', response.data)
      
      if (response.data.auth_url) {
        // Redirect to OAuth URL for other platforms
        console.log(`🔗 Redirecting to ${platform} OAuth...`)
        window.location.href = response.data.auth_url
        return
      }
      
      // For other platforms or if no OAuth URL, handle as before
      setConnections(prev => [...prev, response.data])
      toast.success(`${platform} connected successfully!`)
    } catch (error) {
      console.error('❌ Error connecting platform:', error)
      
      // Check if it's an authentication error
      if (error.response?.status === 401 || error.response?.status === 403) {
        toast.error('Authentication error. Please try again.')
        return
      }
      
      // Check if it's a network error
      if (error.code === 'NETWORK_ERROR' || error.message?.includes('Network Error')) {
        toast.error('Network error. Please check your connection and try again.')
        return
      }
      
      toast.error(`Failed to connect ${platform}`)
    } finally {
      setIsConnecting(false)
      setSelectedPlatform(null)
    }
  }

  const handleLinkedInConnect = async () => {
    try {
      setIsConnecting(true)
      setSelectedPlatform('linkedin')
      
      console.log('🔗 Starting LinkedIn connection process...')
      console.log('🔗 Current user:', user)
      
      // Check if user is logged in
      if (!user || !user.email) {
        console.error('❌ User not logged in or email not available')
        toast.error('Please log in to connect LinkedIn')
        navigate('/login')
        return
      }
      
      // Check token
      const token = localStorage.getItem('token')
      console.log('🔗 Auth token exists:', !!token)
      if (!token) {
        console.error('❌ No auth token found')
        toast.error('Please log in to connect LinkedIn')
        navigate('/login')
        return
      }
      
      // Get LinkedIn auth URL
      console.log('🔗 Requesting LinkedIn auth URL...')
      try {
        const response = await platformsAPI.getLinkedInAuthUrl()
        console.log('🔗 LinkedIn auth URL response:', response.data)
        
        if (response.data.auth_url) {
          // Store state in localStorage for verification
          localStorage.setItem('linkedin_auth_state', response.data.state)
          console.log('🔗 Stored state in localStorage:', response.data.state)
          
          // Log the URL we're redirecting to
          console.log('🔗 About to redirect to:', response.data.auth_url)
          
          // Redirect to LinkedIn OAuth
          window.location.assign(response.data.auth_url)
        } else {
          console.error('❌ No auth URL in response:', response.data)
          toast.error('Failed to get LinkedIn authorization URL')
        }
      } catch (error) {
        console.error('❌ Error in getLinkedInAuthUrl:', error)
        if (error.response) {
          console.error('Response:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        } else if (error.request) {
          console.error('Request made but no response:', error.request)
        } else {
          console.error('Error details:', error.message)
        }
        toast.error('Failed to connect LinkedIn')
      }
    } catch (error) {
      console.error('❌ Outer error handler:', error)
      toast.error('Failed to connect LinkedIn')
    } finally {
      setIsConnecting(false)
      setSelectedPlatform(null)
    }
  }

  const handleDisconnectPlatform = async (platform) => {
    if (!confirm(`Are you sure you want to disconnect ${platform}?`)) return

    try {
      // For Instagram, remove from localStorage
      if (platform === 'instagram') {
        const localConnections = JSON.parse(localStorage.getItem('platform_connections') || '[]')
        const updatedConnections = localConnections.filter(conn => conn.platform !== 'instagram')
        localStorage.setItem('platform_connections', JSON.stringify(updatedConnections))
        setConnections(prev => prev.filter(conn => conn.platform !== 'instagram'))
        toast.success(`${platform} disconnected successfully!`)
        return
      }
      
      // For other platforms, use backend
      await platformsAPI.disconnectPlatform(platform)
      setConnections(prev => prev.filter(conn => conn.platform !== platform))
      toast.success(`${platform} disconnected successfully!`)
    } catch (error) {
      console.error('Error disconnecting platform:', error)
      
      // Check if it's an authentication error
      if (error.response?.status === 401 || error.response?.status === 403) {
        toast.error('Authentication error. Please try again.')
        return
      }
      
      // Check if it's a network error
      if (error.code === 'NETWORK_ERROR' || error.message?.includes('Network Error')) {
        toast.error('Network error. Please check your connection and try again.')
        return
      }
      
      toast.error(`Failed to disconnect ${platform}`)
    }
  }

  const handleInstagramSuccess = (connection) => {
    setConnections(prev => {
      const filtered = prev.filter(conn => conn.platform !== 'instagram')
      return [...filtered, connection]
    })
  }

  const platforms = [
    {
      name: 'instagram',
      icon: Instagram,
      color: 'text-pink-600',
      bgColor: 'bg-pink-100',
      description: 'Share photos and stories with your audience',
      features: ['Post photos and videos', 'Share stories', 'Engage with followers']
    },
    {
      name: 'linkedin',
      icon: Linkedin,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      description: 'Professional networking and business content',
      features: ['Share professional updates', 'Publish articles', 'Network with industry leaders', 'Post AI-generated content']
    },
    {
      name: 'facebook',
      icon: Facebook,
      color: 'text-blue-500',
      bgColor: 'bg-blue-100',
      description: 'Connect with friends and share content',
      features: ['Post updates', 'Share photos and videos', 'Create events']
    },
    {
      name: 'twitter',
      icon: Twitter,
      color: 'text-blue-400',
      bgColor: 'bg-blue-100',
      description: 'Share thoughts and engage in conversations',
      features: ['Tweet updates', 'Engage in discussions', 'Share links and media']
    }
  ]

  const getPlatformStatus = (platformName) => {
    return connections.find(conn => conn.platform === platformName)
  }

  const getPlatformCard = (platform) => {
    const connection = getPlatformStatus(platform.name)
    const isConnecting = selectedPlatform === platform.name

    return (
      <div key={platform.name} className="card">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`w-12 h-12 ${platform.bgColor} rounded-lg flex items-center justify-center`}>
              <platform.icon className={`w-6 h-6 ${platform.color}`} />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 capitalize">{platform.name}</h3>
              <p className="text-sm text-gray-600">{platform.description}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {connection ? (
              <div className="flex items-center text-green-600">
                <CheckCircle className="w-5 h-5 mr-1" />
                <span className="text-sm font-medium">Connected</span>
              </div>
            ) : (
              <div className="flex items-center text-gray-500">
                <AlertCircle className="w-5 h-5 mr-1" />
                <span className="text-sm font-medium">Not Connected</span>
              </div>
            )}
          </div>
        </div>

        <div className="space-y-3 mb-6">
          <h4 className="text-sm font-medium text-gray-900">Features:</h4>
          <ul className="space-y-1">
            {platform.features.map((feature, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-center">
                <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                {feature}
              </li>
            ))}
          </ul>
        </div>

        {connection ? (
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Connected as:</span>
              <span className="font-medium text-gray-900">
                {connection.platform_username || connection.account_name || 'Connected User'}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Connected on:</span>
              <span className="text-gray-900">
                {new Date(connection.created_at || connection.connected_at).toLocaleDateString()}
              </span>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleDisconnectPlatform(platform.name)}
                className="btn-danger flex items-center flex-1 justify-center"
              >
                <Unlink className="w-4 h-4 mr-2" />
                Disconnect
              </button>
              <button className="btn-secondary flex items-center">
                <ExternalLink className="w-4 h-4 mr-2" />
                View
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={() => handleConnectPlatform(platform.name)}
            disabled={isConnecting}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isConnecting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Connecting...
              </>
            ) : (
              <>
                <LinkIcon className="w-4 h-4 mr-2" />
                Connect {platform.name}
              </>
            )}
          </button>
        )}
      </div>
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
          <h1 className="text-2xl font-bold text-gray-900">Platform Connections</h1>
          <p className="text-gray-600">Connect your social media accounts to start posting</p>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600">
            {connections.length} of {platforms.length} platforms connected
          </span>
        </div>
      </div>

      {/* Connection Status */}
      {connections.length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-green-800">Platforms Connected</h3>
              <p className="text-sm text-green-700">
                You can now generate and schedule content for your connected platforms.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Platform Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {platforms.map(getPlatformCard)}
      </div>

      {/* Connection Tips */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Connection Tips</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">Before Connecting</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• Ensure you have admin access to your accounts</li>
              <li>• Make sure your accounts are public or business accounts</li>
              <li>• Have your login credentials ready</li>
              <li>• Review the permissions we'll request</li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">After Connecting</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• You can start generating content immediately</li>
              <li>• Review and approve posts before scheduling</li>
              <li>• Monitor your analytics and performance</li>
              <li>• Disconnect anytime from your account settings</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Security Notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start">
          <AlertCircle className="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="text-sm font-medium text-blue-800">Security & Privacy</h3>
            <p className="text-sm text-blue-700 mt-1">
              We use industry-standard OAuth protocols to securely connect your accounts. 
              We never store your passwords and only request the minimum permissions needed 
              to post content on your behalf. You can revoke access at any time.
            </p>
          </div>
        </div>
      </div>

      {/* Instagram Login Modal */}
      <InstagramLoginModal
        isOpen={showInstagramModal}
        onClose={() => setShowInstagramModal(false)}
        onSuccess={handleInstagramSuccess}
      />
    </div>
  )
} 