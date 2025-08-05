import { useState } from 'react'
import { X, Eye, EyeOff, Instagram, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'

export function InstagramLoginModal({ isOpen, onClose, onSuccess }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!username || !password) {
      toast.error('Please enter both username and password')
      return
    }

    setIsLoading(true)
    
    try {
      console.log('🔗 Attempting Instagram login...')
      
      // Simulate Instagram login process
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // For demo purposes, we'll simulate a successful login
      // In a real implementation, you would use Instagram's API or web scraping
      const mockConnection = {
        platform: 'instagram',
        is_connected: true,
        platform_username: username,
        access_token: 'mock_token_' + Date.now(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      
      console.log('✅ Instagram login successful:', mockConnection)
      
      // Store connection in localStorage for demo
      const existingConnections = JSON.parse(localStorage.getItem('platform_connections') || '[]')
      const updatedConnections = [...existingConnections.filter(c => c.platform !== 'instagram'), mockConnection]
      localStorage.setItem('platform_connections', JSON.stringify(updatedConnections))
      
      toast.success(`Instagram connected successfully as @${username}`)
      onSuccess(mockConnection)
      onClose()
      
    } catch (error) {
      console.error('❌ Instagram login failed:', error)
      toast.error('Failed to connect Instagram. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleClose = () => {
    if (!isLoading) {
      setUsername('')
      setPassword('')
      setShowPassword(false)
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <Instagram className="w-6 h-6 text-pink-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Connect Instagram
            </h2>
          </div>
          <button
            onClick={handleClose}
            disabled={isLoading}
            className="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          <div className="space-y-4">
            {/* Username */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                Instagram Username
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your Instagram username"
                disabled={isLoading}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent disabled:opacity-50"
                required
              />
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Instagram Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your Instagram password"
                  disabled={isLoading}
                  className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent disabled:opacity-50"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 disabled:opacity-50"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Warning */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
              <p className="text-sm text-yellow-800">
                ⚠️ <strong>Security Notice:</strong> This method stores credentials locally and may not work with 2FA enabled accounts.
              </p>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex space-x-3 mt-6">
            <button
              type="button"
              onClick={handleClose}
              disabled={isLoading}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-pink-600 text-white rounded-md hover:bg-pink-700 transition-colors disabled:opacity-50 flex items-center justify-center"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                  Connecting...
                </>
              ) : (
                'Connect Instagram'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
} 