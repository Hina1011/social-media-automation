import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Plus, Check, X, Trash2, FileText, Calendar, Linkedin, Share2 } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { postsAPI, platformsAPI } from '../services/api'

export function PostsPage() {
  const [posts, setPosts] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [showGenerateForm, setShowGenerateForm] = useState(false)
  const [selectedPosts, setSelectedPosts] = useState([])
  const [isPostingToLinkedIn, setIsPostingToLinkedIn] = useState(false)
  const [linkedinConnected, setLinkedinConnected] = useState(false)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm()

  useEffect(() => {
    loadPosts()
    checkLinkedInConnection()
  }, [])

  const checkLinkedInConnection = async () => {
    try {
      const response = await platformsAPI.getStatus()
      setLinkedinConnected(response.data.linkedin || false)
    } catch (error) {
      console.error('Error checking LinkedIn connection:', error)
      setLinkedinConnected(false)
    }
  }

  const loadPosts = async () => {
    try {
      const response = await postsAPI.getPosts()
      setPosts(response.data)
    } catch (error) {
      console.error('Error loading posts:', error)
      toast.error('Failed to load posts')
    } finally {
      setIsLoading(false)
    }
  }

  const handleGeneratePosts = async (data) => {
    setIsGenerating(true)
    try {
      // Calculate start date (tomorrow)
      const startDate = new Date()
      startDate.setDate(startDate.getDate() + 1)
      startDate.setHours(9, 0, 0, 0) // Set to 9 AM

      const requestData = {
        custom_prompt: data.custom_prompt || "Create engaging social media content that resonates with my audience",
        start_date: startDate.toISOString(),
        platforms: data.platforms || ['instagram', 'linkedin', 'facebook', 'twitter']
      }

      const response = await postsAPI.generatePosts(requestData)
      setPosts(response.data)
      setShowGenerateForm(false)
      reset()
      toast.success('Posts generated successfully!')
    } catch (error) {
      console.error('Error generating posts:', error)
      toast.error('Failed to generate posts')
    } finally {
      setIsGenerating(false)
    }
  }

  const handlePostToggle = (postId) => {
    setSelectedPosts(prev => 
      prev.includes(postId) 
        ? prev.filter(id => id !== postId)
        : [...prev, postId]
    )
  }

  const handleApprovePosts = async () => {
    if (selectedPosts.length === 0) {
      toast.error('Please select posts to approve')
      return
    }

    try {
      await postsAPI.approvePosts({ post_ids: selectedPosts })
      setSelectedPosts([])
      loadPosts()
      toast.success('Posts approved successfully!')
    } catch (error) {
      console.error('Error approving posts:', error)
      toast.error('Failed to approve posts')
    }
  }

  const handlePostToLinkedIn = async (postId) => {
    if (!linkedinConnected) {
      toast.error('Please connect your LinkedIn account first')
      return
    }

    setIsPostingToLinkedIn(true)
    try {
      const response = await postsAPI.postToLinkedIn(postId)
      
      if (response.data.success) {
        toast.success('Post shared on LinkedIn successfully!')
        // Update the post status in the UI
        setPosts(prev => prev.map(post => 
          post._id === postId 
            ? { ...post, status: 'posted', posted_to_linkedin: true }
            : post
        ))
      } else {
        toast.error(response.data.message || 'Failed to post to LinkedIn')
      }
    } catch (error) {
      console.error('Error posting to LinkedIn:', error)
      if (error.response?.data?.detail) {
        toast.error(error.response.data.detail)
      } else {
        toast.error('Failed to post to LinkedIn')
      }
    } finally {
      setIsPostingToLinkedIn(false)
    }
  }

  const handleBatchPostToLinkedIn = async () => {
    if (!linkedinConnected) {
      toast.error('Please connect your LinkedIn account first')
      return
    }

    if (selectedPosts.length === 0) {
      toast.error('Please select posts to share on LinkedIn')
      return
    }

    setIsPostingToLinkedIn(true)
    try {
      const response = await postsAPI.batchPostToLinkedIn(selectedPosts)
      
      if (response.data.success) {
        toast.success(`Posted ${response.data.successful_posts} out of ${response.data.total_posts} posts to LinkedIn!`)
        setSelectedPosts([])
        loadPosts() // Reload to get updated status
      } else {
        toast.error('Failed to post some posts to LinkedIn')
      }
    } catch (error) {
      console.error('Error batch posting to LinkedIn:', error)
      toast.error('Failed to post to LinkedIn')
    } finally {
      setIsPostingToLinkedIn(false)
    }
  }

  const handleDeletePost = async (postId) => {
    if (!confirm('Are you sure you want to delete this post?')) return

    try {
      await postsAPI.deletePost(postId)
      setPosts(prev => prev.filter(post => post._id !== postId))
      toast.success('Post deleted successfully!')
    } catch (error) {
      console.error('Error deleting post:', error)
      toast.error('Failed to delete post')
    }
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      draft: { color: 'bg-gray-100 text-gray-800', label: 'Draft' },
      approved: { color: 'bg-green-100 text-green-800', label: 'Approved' },
      scheduled: { color: 'bg-blue-100 text-blue-800', label: 'Scheduled' },
      published: { color: 'bg-purple-100 text-purple-800', label: 'Published' }
    }
    
    const config = statusConfig[status] || statusConfig.draft
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    )
  }

  const getPlatformIcon = (platform) => {
    const platformColors = {
      instagram: 'text-pink-600',
      linkedin: 'text-blue-600',
      facebook: 'text-blue-500',
      twitter: 'text-blue-400'
    }
    return (
      <span className={`text-sm font-medium capitalize ${platformColors[platform] || 'text-gray-600'}`}>
        {platform}
      </span>
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
          <h1 className="text-2xl font-bold text-gray-900">Posts</h1>
          <p className="text-gray-600">Manage and generate your social media content</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setShowGenerateForm(true)}
            className="btn-primary flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            Generate Posts
          </button>
        </div>
      </div>

      {/* Generate Form Modal */}
      {showGenerateForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Generate New Posts</h2>
            <form onSubmit={handleSubmit(handleGeneratePosts)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Custom Prompt (Optional)
                </label>
                <textarea
                  {...register('custom_prompt')}
                  placeholder="Describe the type of content you want to generate..."
                  className="input-field"
                  rows={3}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Platforms
                </label>
                <div className="space-y-2">
                  {['instagram', 'linkedin', 'facebook', 'twitter'].map((platform) => (
                    <label key={platform} className="flex items-center">
                      <input
                        type="checkbox"
                        value={platform}
                        {...register('platforms')}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700 capitalize">{platform}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowGenerateForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isGenerating}
                  className="btn-primary disabled:opacity-50"
                >
                  {isGenerating ? 'Generating...' : 'Generate'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Actions Bar */}
      {selectedPosts.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-blue-800">
              {selectedPosts.length} post{selectedPosts.length > 1 ? 's' : ''} selected
            </span>
            <div className="flex space-x-2">
              <button
                onClick={handleApprovePosts}
                className="btn-primary flex items-center"
              >
                <Check className="w-4 h-4 mr-2" />
                Approve Selected
              </button>
              {linkedinConnected && (
                <button
                  onClick={handleBatchPostToLinkedIn}
                  disabled={isPostingToLinkedIn}
                  className="btn-secondary flex items-center disabled:opacity-50"
                >
                  <Linkedin className="w-4 h-4 mr-2" />
                  {isPostingToLinkedIn ? 'Posting...' : 'Post to LinkedIn'}
                </button>
              )}
              <button
                onClick={() => setSelectedPosts([])}
                className="btn-secondary flex items-center"
              >
                <X className="w-4 h-4 mr-2" />
                Clear Selection
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Posts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <div key={post._id} className="card">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-2">
                {getPlatformIcon(post.platform)}
                {getStatusBadge(post.status)}
              </div>
              <div className="flex items-center space-x-1">
                <button
                  onClick={() => handlePostToggle(post._id)}
                  className={`p-1 rounded ${
                    selectedPosts.includes(post._id)
                      ? 'bg-primary-100 text-primary-600'
                      : 'text-gray-400 hover:text-gray-600'
                  }`}
                >
                  <Check className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDeletePost(post._id)}
                  className="p-1 text-gray-400 hover:text-red-600 rounded"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="space-y-3">
              {/* Generated Image */}
              {post.image_url && (
                <div className="mb-3">
                  <img 
                    src={`http://localhost:8000${post.image_url}`}
                    alt="Generated content"
                    className="w-full h-48 object-cover rounded-lg"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}
              
              <div>
                <h3 className="text-sm font-medium text-gray-900 mb-1">Caption</h3>
                <p className="text-sm text-gray-600 line-clamp-3">
                  {post.caption}
                </p>
              </div>

              {post.hashtags && post.hashtags.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-gray-900 mb-1">Hashtags</h3>
                  <div className="flex flex-wrap gap-1">
                    {post.hashtags.slice(0, 5).map((hashtag, index) => (
                      <span key={index} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {hashtag}
                      </span>
                    ))}
                    {post.hashtags.length > 5 && (
                      <span className="text-xs text-gray-500">+{post.hashtags.length - 5} more</span>
                    )}
                  </div>
                </div>
              )}

              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>
                  <Calendar className="w-3 h-3 inline mr-1" />
                  {new Date(post.scheduled_date).toLocaleDateString()}
                </span>
                <span>
                  {post.call_to_action && 'CTA included'}
                </span>
              </div>

              {/* LinkedIn Post Button */}
              {linkedinConnected && (
                <div className="pt-2 border-t border-gray-100">
                  <button
                    onClick={() => handlePostToLinkedIn(post._id)}
                    disabled={isPostingToLinkedIn || post.posted_to_linkedin}
                    className={`w-full flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      post.posted_to_linkedin
                        ? 'bg-green-100 text-green-700 cursor-not-allowed'
                        : isPostingToLinkedIn
                        ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                    }`}
                  >
                    <Linkedin className="w-4 h-4 mr-2" />
                    {post.posted_to_linkedin 
                      ? 'Posted to LinkedIn' 
                      : isPostingToLinkedIn 
                      ? 'Posting...' 
                      : 'Post to LinkedIn'
                    }
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {posts.length === 0 && (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No posts yet</h3>
          <p className="text-gray-600 mb-6">
            Generate your first batch of AI-powered social media posts to get started.
          </p>
          <button
            onClick={() => setShowGenerateForm(true)}
            className="btn-primary"
          >
            Generate Posts
          </button>
        </div>
      )}
    </div>
  )
} 