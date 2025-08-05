import { useState, useRef } from 'react'
import { Check, X, RefreshCw, Calendar, Clock, Upload, Edit, Save, Trash2, Image as ImageIcon } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { postsAPI } from '../services/api'

export function PostApprovalModal({ post, onClose, onUpdate }) {
  const [isApproving, setIsApproving] = useState(false)
  const [isRegenerating, setIsRegenerating] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [customPrompt, setCustomPrompt] = useState('')
  const [editedCaption, setEditedCaption] = useState(post.caption)
  const [uploadedImage, setUploadedImage] = useState(null)
  const fileInputRef = useRef(null)

  const handleApprove = async () => {
    setIsApproving(true)
    try {
      await postsAPI.approvePosts({ post_ids: [post._id] })
      toast.success('Post approved!')
      onUpdate()
      onClose()
    } catch (error) {
      console.error('Error approving post:', error)
      toast.error('Failed to approve post')
    } finally {
      setIsApproving(false)
    }
  }

  const handleRegenerate = async () => {
    if (!customPrompt.trim()) {
      toast.error('Please enter a custom prompt for regeneration')
      return
    }
    
    setIsRegenerating(true)
    try {
      // First update the post with custom prompt
      await postsAPI.updatePost(post._id, { custom_prompt: customPrompt })
      // Then regenerate
      await postsAPI.regeneratePost(post._id)
      toast.success('Post content regenerated with custom prompt!')
      onUpdate()
      setCustomPrompt('')
    } catch (error) {
      console.error('Error regenerating post:', error)
      toast.error('Failed to regenerate post')
    } finally {
      setIsRegenerating(false)
    }
  }

  const handleSaveChanges = async () => {
    setIsSaving(true)
    try {
      const updateData = { caption: editedCaption }
      if (uploadedImage) {
        // Handle image upload here
        updateData.image_url = uploadedImage
      }
      
      await postsAPI.updatePost(post._id, updateData)
      toast.success('Changes saved successfully!')
      onUpdate()
      setIsEditing(false)
      setUploadedImage(null)
    } catch (error) {
      console.error('Error saving changes:', error)
      toast.error('Failed to save changes')
    } finally {
      setIsSaving(false)
    }
  }

  const handleDeletePost = async () => {
    if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
      return
    }
    
    setIsDeleting(true)
    try {
      const response = await postsAPI.deletePost(post._id)
      console.log('Delete response:', response)
      toast.success('Post deleted successfully!')
      onUpdate()
      onClose()
    } catch (error) {
      console.error('Error deleting post:', error)
      
      // Check if it's an authentication error
      if (error.response?.status === 401 || error.response?.status === 403) {
        toast.error('Authentication error. Please try again.')
        // Don't redirect to login, just show error
        return
      }
      
      // Check if it's a network error
      if (error.code === 'NETWORK_ERROR' || error.message?.includes('Network Error')) {
        toast.error('Network error. Please check your connection and try again.')
        return
      }
      
      // Check if it's a preventLogout error
      if (error.preventLogout) {
        toast.error('Unable to delete post. Please try again later.')
        return
      }
      
      // Generic error
      toast.error('Failed to delete post. Please try again.')
    } finally {
      setIsDeleting(false)
    }
  }

  const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        toast.error('Image size should be less than 5MB')
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImage(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleEditToggle = () => {
    if (isEditing) {
      setEditedCaption(post.caption)
      setUploadedImage(null)
    }
    setIsEditing(!isEditing)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-800'
      case 'scheduled':
        return 'bg-blue-100 text-blue-800'
      case 'published':
        return 'bg-purple-100 text-purple-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Post Details</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4">
          {/* Post Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-sm font-medium text-gray-700 capitalize">
                {post.platform}
              </span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(post.status)}`}>
                {post.status}
              </span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Calendar className="w-4 h-4" />
              <span>{new Date(post.scheduled_date).toLocaleDateString()}</span>
            </div>
          </div>

          {/* Custom Prompt Input */}
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-2">Custom Prompt for Regeneration</h4>
            <textarea
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="Enter your custom prompt to regenerate content..."
              className="w-full p-3 border border-gray-300 rounded-lg text-sm resize-none"
              rows={3}
            />
          </div>

          {/* Post Image */}
          <div className="relative">
            {uploadedImage ? (
              <img
                src={uploadedImage}
                alt="Uploaded content"
                className="w-full h-64 object-cover rounded-lg"
              />
            ) : post.image_url ? (
              <img
                src={`http://localhost:8000${post.image_url}`}
                alt="Post content"
                className="w-full h-64 object-cover rounded-lg"
              />
            ) : (
              <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                <span className="text-gray-400">No image</span>
              </div>
            )}
            <div className="absolute top-2 right-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded text-xs">
              📷 {uploadedImage ? 'Uploaded' : 'Generated'}
            </div>
          </div>

          {/* Post Content */}
          <div className="space-y-3">
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-2">Caption</h4>
              {isEditing ? (
                <textarea
                  value={editedCaption}
                  onChange={(e) => setEditedCaption(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg text-sm resize-none"
                  rows={4}
                />
              ) : (
                <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
                  {post.caption}
                </p>
              )}
            </div>

            {post.hashtags && post.hashtags.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">Hashtags</h4>
                <div className="flex flex-wrap gap-2">
                  {post.hashtags.map((hashtag, index) => (
                    <span key={index} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                      {hashtag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {post.call_to_action && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">Call to Action</h4>
                <p className="text-sm text-gray-700 bg-yellow-50 p-3 rounded-lg">
                  {post.call_to_action}
                </p>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-4 border-t">
            <div className="flex items-center space-x-2">
              <button
                onClick={handleRegenerate}
                disabled={isRegenerating || !customPrompt.trim()}
                className="btn-secondary flex items-center text-sm disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 mr-1 ${isRegenerating ? 'animate-spin' : ''}`} />
                {isRegenerating ? 'Regenerating...' : 'Regenerate'}
              </button>
              
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleImageUpload}
                accept="image/*"
                className="hidden"
              />
              <button 
                onClick={() => fileInputRef.current?.click()}
                className="btn-secondary flex items-center text-sm"
              >
                <ImageIcon className="w-4 h-4 mr-1" />
                Upload Image
              </button>
              
              <button
                onClick={handleEditToggle}
                className={`flex items-center text-sm ${
                  isEditing ? 'btn-primary' : 'btn-secondary'
                }`}
              >
                <Edit className="w-4 h-4 mr-1" />
                {isEditing ? 'Cancel Edit' : 'Edit Caption'}
              </button>
            </div>

            <div className="flex items-center space-x-2">
              {isEditing ? (
                <button
                  onClick={handleSaveChanges}
                  disabled={isSaving}
                  className="btn-primary flex items-center text-sm disabled:opacity-50"
                >
                  <Save className="w-4 h-4 mr-1" />
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
              ) : (
                <>
                  {post.status !== 'approved' ? (
                    <button
                      onClick={handleApprove}
                      disabled={isApproving}
                      className="btn-primary flex items-center text-sm disabled:opacity-50"
                    >
                      <Check className="w-4 h-4 mr-1" />
                      {isApproving ? 'Approving...' : 'Approve Post'}
                    </button>
                  ) : (
                    <div className="flex items-center space-x-2 text-green-600">
                      <Check className="w-4 h-4" />
                      <span className="text-sm font-medium">Approved</span>
                    </div>
                  )}
                  
                  <button
                    onClick={handleDeletePost}
                    disabled={isDeleting}
                    className="btn-secondary flex items-center text-sm text-red-600 hover:bg-red-50 disabled:opacity-50"
                  >
                    <Trash2 className="w-4 h-4 mr-1" />
                    {isDeleting ? 'Deleting...' : 'Delete'}
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Approval Info */}
          {post.status === 'approved' && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-3">
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-green-600" />
                <span className="text-sm text-green-800">
                  This post is approved and will be published on {new Date(post.scheduled_date).toLocaleDateString()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 