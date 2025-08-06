import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext.jsx'
import { postsAPI } from '../services/api.js'
import { 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  RefreshCw,
  Eye,
  Calendar,
  TrendingUp
} from 'lucide-react'

export function BatchManager({ onUpdate }) {
  const { user } = useAuth()
  const [batches, setBatches] = useState([])
  const [pendingPosts, setPendingPosts] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedBatch, setSelectedBatch] = useState(null)
  const [showBatchDetails, setShowBatchDetails] = useState(false)

  useEffect(() => {
    loadBatchData()
  }, [])

  const loadBatchData = async () => {
    try {
      setIsLoading(true)
      const [batchesResponse, pendingResponse] = await Promise.all([
        postsAPI.getUserBatches(),
        postsAPI.getPendingApprovalPosts()
      ])

      setBatches(batchesResponse.data || [])
      setPendingPosts(pendingResponse.data || [])
    } catch (error) {
      console.error('Error loading batch data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleBatchApprove = async (batchId) => {
    try {
      await postsAPI.batchApprove(batchId)
      await loadBatchData()
      if (onUpdate) onUpdate()
      alert('Batch approved successfully! Posts will be scheduled for posting.')
    } catch (error) {
      console.error('Error approving batch:', error)
      alert('Error approving batch. Please try again.')
    }
  }

  const handleRegenerateNextBatch = async () => {
    try {
      await postsAPI.regenerateNextBatch()
      await loadBatchData()
      if (onUpdate) onUpdate()
      alert('Next batch generated successfully! Please review and approve.')
    } catch (error) {
      console.error('Error regenerating batch:', error)
      alert('Error generating next batch. Please try again.')
    }
  }

  const getBatchStatus = (batch) => {
    if (batch.pending_count > 0) return 'pending'
    if (batch.approved_count > 0 && batch.posted_count === 0) return 'approved'
    if (batch.posted_count > 0) return 'posted'
    return 'draft'
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return <AlertCircle className="w-5 h-5 text-yellow-600" />
      case 'approved': return <CheckCircle className="w-5 h-5 text-green-600" />
      case 'posted': return <TrendingUp className="w-5 h-5 text-purple-600" />
      default: return <Clock className="w-5 h-5 text-gray-600" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'approved': return 'bg-green-100 text-green-800'
      case 'posted': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const pendingBatch = batches.find(batch => batch.pending_count > 0)

  return (
    <div className="space-y-6">
      {/* Pending Approval Alert */}
      {pendingPosts.length > 0 && (
        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                <AlertCircle className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-yellow-800">
                  Posts Ready for Approval
                </h3>
                <p className="text-sm text-yellow-700">
                  {pendingPosts.length} posts are waiting for your approval
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowBatchDetails(true)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Eye className="w-4 h-4" />
                <span>Review Posts</span>
              </button>
              
              <button
                onClick={() => handleBatchApprove(pendingBatch?.batch_id)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <CheckCircle className="w-4 h-4" />
                <span>Approve All</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Batch Overview */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Batch Overview</h3>
          <button
            onClick={handleRegenerateNextBatch}
            className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Generate Next Batch</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {batches.map((batch) => {
            const status = getBatchStatus(batch)
            return (
              <div key={batch.batch_id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(status)}
                    <span className="text-sm font-medium text-gray-900">
                      Batch {batch.batch_id?.split('_')[1]}
                    </span>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(status)}`}>
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Total Posts:</span>
                    <span className="font-medium">{batch.total_posts}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Pending:</span>
                    <span className="text-yellow-600 font-medium">{batch.pending_count}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Approved:</span>
                    <span className="text-green-600 font-medium">{batch.approved_count}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Posted:</span>
                    <span className="text-purple-600 font-medium">{batch.posted_count}</span>
                  </div>
                </div>

                <div className="text-xs text-gray-500 mb-3">
                  Created: {new Date(batch.created_at).toLocaleDateString()}
                </div>

                {batch.pending_count > 0 && (
                  <button
                    onClick={() => handleBatchApprove(batch.batch_id)}
                    className="w-full px-3 py-2 text-sm bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                  >
                    Approve Batch
                  </button>
                )}
              </div>
            )
          })}
        </div>

        {batches.length === 0 && (
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Calendar className="w-8 h-8 text-gray-400" />
            </div>
            <h4 className="text-lg font-medium text-gray-900 mb-2">No batches yet</h4>
            <p className="text-gray-600 mb-4">
              Your first batch will be generated automatically when you sign up.
            </p>
            <button
              onClick={handleRegenerateNextBatch}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Generate First Batch
            </button>
          </div>
        )}
      </div>

      {/* Batch Details Modal */}
      {showBatchDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900">
                Review Posts - Batch {pendingBatch?.batch_id?.split('_')[1]}
              </h3>
              <button
                onClick={() => setShowBatchDetails(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {pendingPosts.map((post) => (
                <div key={post._id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-sm text-gray-500">
                      {new Date(post.scheduled_date).toLocaleDateString()}
                    </span>
                    <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                      Pending
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-900 mb-3 line-clamp-4">
                    {post.caption}
                  </p>
                  
                  <div className="flex items-center space-x-2 mb-3">
                    {post.platforms?.map((platform) => (
                      <span key={platform} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {platform}
                      </span>
                    ))}
                  </div>
                  
                  {post.hashtags && post.hashtags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {post.hashtags.slice(0, 5).map((hashtag, index) => (
                        <span key={index} className="text-xs bg-blue-100 text-blue-600 px-2 py-1 rounded">
                          {hashtag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between mt-6 pt-6 border-t border-gray-200">
              <div className="text-sm text-gray-600">
                {pendingPosts.length} posts ready for approval
              </div>
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => setShowBatchDetails(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    handleBatchApprove(pendingBatch?.batch_id)
                    setShowBatchDetails(false)
                  }}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Approve All Posts
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 