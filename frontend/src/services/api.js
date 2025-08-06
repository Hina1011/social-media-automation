import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      // Debug: log the request being made
      console.log('🔐 Making authenticated request:', config.method?.toUpperCase(), config.url)
      console.log('🔑 Token present:', !!token)
      console.log('📋 Headers:', config.headers)
    } else {
      console.log('⚠️ No token found for request:', config.method?.toUpperCase(), config.url)
    }
    return config
  },
  (error) => {
    console.error('❌ Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => {
    console.log('✅ Response received:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('❌ Response error:', error.response?.status, error.config?.url, error.response?.data)
    
    // Check if this is a delete operation that should not trigger logout
    const isDeleteOperation = error.config?.method === 'delete' && error.config?.url?.includes('/posts/')
    
    // Check if this is a platform operation that should be handled gracefully
    const isPlatformOperation = error.config?.url?.includes('/platforms')
    
    console.log('🔍 Error analysis:')
    console.log('  - Status:', error.response?.status)
    console.log('  - URL:', error.config?.url)
    console.log('  - Method:', error.config?.method)
    console.log('  - Is Delete Operation:', isDeleteOperation)
    console.log('  - Is Platform Operation:', isPlatformOperation)
    
    if (error.response?.status === 401 && !isDeleteOperation && !isPlatformOperation) {
      console.log('🔒 Unauthorized - redirecting to login')
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else if (error.response?.status === 403 && !isDeleteOperation && !isPlatformOperation) {
      console.log('🚫 Forbidden - checking token')
      const token = localStorage.getItem('token')
      if (!token) {
        console.log('🔑 No token found - redirecting to login')
        window.location.href = '/login'
      } else {
        console.log('🔑 Token exists but still getting 403 - token might be invalid')
        // Try to refresh the token or redirect to login
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    } else if (isDeleteOperation) {
      console.log('🗑️ Delete operation failed, but not logging out user')
    } else if (isPlatformOperation) {
      console.log('🔗 Platform operation failed, but not logging out user')
    } else {
      console.log('🔍 Other operation failed, status:', error.response?.status)
    }
    return Promise.reject(error)
  }
)

// Helper function to ensure token is set
export const ensureToken = () => {
  const token = localStorage.getItem('token')
  console.log('🔑 ensureToken called, token exists:', !!token)
  if (!token) {
    console.log('🔑 No token found - redirecting to login')
    window.location.href = '/login'
    return false
  }
  console.log('🔑 Token found, length:', token.length)
  return true
}

// API endpoints
export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  signup: (data) => api.post('/auth/signup', data),
  requestOTP: (data) => api.post('/auth/request-otp', data),
  verifyOTP: (data) => api.post('/auth/verify-otp', data),
  getMe: () => api.get('/auth/me'),
}

export const usersAPI = {
  getProfile: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/users/profile')
  },
  updateProfile: (data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.put('/users/profile', data)
  },
  completeProfile: (data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/users/complete-profile', data)
  },
  getInterests: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/users/interests')
  },
  deleteAccount: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.delete('/users/account')
  },
}

export const postsAPI = {
  generatePosts: (data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/posts/generate', data)
  },
  getPosts: (params) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/posts/', { params })
  },
  getUserPosts: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/posts/')
  },
  getPost: (id) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get(`/posts/${id}`)
  },
  updatePost: (id, data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.put(`/posts/${id}`, data)
  },
  approvePosts: (data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/posts/approve', data)
  },
  deletePost: (id) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.delete(`/posts/${id}`).catch(error => {
      // Don't trigger automatic logout for delete operations
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.log('Delete operation failed due to auth error, but not logging out')
        // Return a custom error that won't trigger logout
        return Promise.reject({
          ...error,
          preventLogout: true
        })
      }
      return Promise.reject(error)
    })
  },
  regeneratePost: (id) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post(`/posts/${id}/regenerate`)
  },
  // New automation endpoints
  batchApprove: (batchId) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/posts/batch-approve', { batch_id: batchId })
  },
  regenerateNextBatch: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/posts/regenerate-next-batch')
  },
  getPendingApprovalPosts: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/posts/pending-approval')
  },
  getUserBatches: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/posts/batches')
  },
  updateScheduleTime: (scheduleTime) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.put('/posts/schedule-time', { schedule_time: scheduleTime })
  },
  // LinkedIn posting endpoints
  postToLinkedIn: (postId) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post(`/posts/${postId}/post-to-linkedin`)
  },
  batchPostToLinkedIn: (postIds) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/posts/batch-post-to-linkedin', { post_ids: postIds })
  },
}

export const platformsAPI = {
  getConnections: () => {
    console.log('🔗 getConnections called')
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    console.log('🔗 Token verified, making API call to /platforms')
    return api.get('/platforms')
  },
  connectPlatform: (data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/platforms/connect', data)
  },
  disconnectPlatform: (platform) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.delete(`/platforms/disconnect/${platform}`)
  },
  getStatus: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/platforms/status')
  },
  // LinkedIn-specific endpoints
  getLinkedInAuthUrl: () => {
    console.log('🔗 Getting LinkedIn auth URL...')
    if (!ensureToken()) {
      console.error('❌ No token available for LinkedIn auth URL request')
      return Promise.reject(new Error('No token'))
    }
    const token = localStorage.getItem('token')
    console.log('🔗 Token:', token ? `${token.substring(0, 20)}...` : 'null')
    console.log('🔗 Token verified, requesting LinkedIn auth URL...')
    return api.get('/platforms/linkedin/auth-url', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => {
        console.log('✅ LinkedIn auth URL response:', response.data)
        return response
      })
      .catch(error => {
        console.error('❌ Error getting LinkedIn auth URL:', error)
        if (error.response) {
          console.error('Response status:', error.response.status)
          console.error('Response data:', error.response.data)
          console.error('Response headers:', error.response.headers)
        }
        throw error
      })
  },
  linkedinCallback: (data) => {
    console.log('🔗 Sending LinkedIn callback request:', {
      ...data,
      auth_code: data.auth_code ? `${data.auth_code.substring(0, 10)}...` : null
    })
    return api.post('/platforms/linkedin/callback', data)
      .then(response => {
        console.log('✅ LinkedIn callback response:', response.data)
        return response
      })
      .catch(error => {
        console.error('❌ LinkedIn callback error:', error)
        if (error.response) {
          console.error('Response status:', error.response.status)
          console.error('Response data:', error.response.data)
          console.error('Response headers:', error.response.headers)
        }
        throw error
      })
  },
  postToLinkedIn: (content, imageUrl = null) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/platforms/linkedin/post', { content, image_url: imageUrl })
  },
}

export const analyticsAPI = {
  getSummary: () => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/analytics/summary')
  },
  getPlatformAnalytics: (platform, days) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get(`/analytics/platform/${platform}`, { params: { days } })
  },
  trackAnalytics: (data) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.post('/analytics/track', data)
  },
  getGrowthAnalytics: (days) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/analytics/growth', { params: { days } })
  },
  getPostsPerformance: (limit) => {
    if (!ensureToken()) return Promise.reject(new Error('No token'))
    return api.get('/analytics/posts-performance', { params: { limit } })
  },
}