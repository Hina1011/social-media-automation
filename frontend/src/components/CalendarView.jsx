import { useState, useEffect } from 'react'
import { Calendar, ChevronLeft, ChevronRight, Plus, Edit, RefreshCw, Upload, Check, Clock, X } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { postsAPI } from '../services/api'
import { PostApprovalModal } from './PostApprovalModal.jsx'

export function CalendarView() {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [posts, setPosts] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [selectedDate, setSelectedDate] = useState(null)
  const [showPostModal, setShowPostModal] = useState(false)
  const [selectedPost, setSelectedPost] = useState(null)

  useEffect(() => {
    loadPosts()
  }, [])

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

  // Generate calendar days for current month
  const generateCalendarDays = () => {
    const year = currentDate.getFullYear()
    const month = currentDate.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const startDate = new Date(firstDay)
    startDate.setDate(startDate.getDate() - firstDay.getDay())

    const days = []
    const currentDay = new Date(startDate)

    while (currentDay <= lastDay || days.length < 42) {
      days.push(new Date(currentDay))
      currentDay.setDate(currentDay.getDate() + 1)
    }

    return days
  }

  // Get posts for a specific date
  const getPostsForDate = (date) => {
    return posts.filter(post => {
      const postDate = new Date(post.scheduled_date)
      return postDate.toDateString() === date.toDateString()
    })
  }

  // Navigate to previous month
  const goToPreviousMonth = () => {
    setCurrentDate(prev => {
      const newDate = new Date(prev)
      newDate.setMonth(newDate.getMonth() - 1)
      return newDate
    })
  }

  // Navigate to next month
  const goToNextMonth = () => {
    setCurrentDate(prev => {
      const newDate = new Date(prev)
      newDate.setMonth(newDate.getMonth() + 1)
      return newDate
    })
  }

  // Generate posts for specific date
  const generatePostsForDate = async (date) => {
    setIsGenerating(true)
    try {
      const startDate = new Date(date)
      startDate.setHours(9, 0, 0, 0)

      const requestData = {
        custom_prompt: "Create engaging social media content for this specific date",
        start_date: startDate.toISOString(),
        platforms: ['instagram', 'linkedin', 'facebook', 'twitter']
      }

      await postsAPI.generatePosts(requestData)
      await loadPosts()
      toast.success('Posts generated for selected date!')
    } catch (error) {
      console.error('Error generating posts:', error)
      toast.error('Failed to generate posts')
    } finally {
      setIsGenerating(false)
    }
  }

  // Generate posts for specific day of week (e.g., all Mondays)
  const generatePostsForDayOfWeek = async (dayOfWeek) => {
    setIsGenerating(true)
    try {
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      const dayName = dayNames[dayOfWeek]
      
      // Generate 7 posts for the next 7 occurrences of this day
      const posts = []
      const startDate = new Date()
      
      for (let i = 0; i < 7; i++) {
        const targetDate = new Date(startDate)
        const daysUntilTarget = (dayOfWeek - targetDate.getDay() + 7) % 7
        targetDate.setDate(targetDate.getDate() + daysUntilTarget + (i * 7))
        targetDate.setHours(9, 0, 0, 0)

        const requestData = {
          custom_prompt: `Create engaging social media content for ${dayName}`,
          start_date: targetDate.toISOString(),
          platforms: ['instagram', 'linkedin', 'facebook', 'twitter']
        }

        const response = await postsAPI.generatePosts(requestData)
        posts.push(...response.data)
      }

      await loadPosts()
      toast.success(`Generated 7 posts for ${dayName}s!`)
    } catch (error) {
      console.error('Error generating posts:', error)
      toast.error('Failed to generate posts')
    } finally {
      setIsGenerating(false)
    }
  }

  // Handle date click
  const handleDateClick = (date) => {
    // Don't allow clicking on past dates
    const isPastDate = date < new Date(new Date().setHours(0, 0, 0, 0))
    if (isPastDate) {
      toast.error('Cannot edit past dates')
      return
    }

    const postsForDate = getPostsForDate(date)
    if (postsForDate.length > 0) {
      setSelectedPost(postsForDate[0])
      setSelectedDate(date)
      setShowPostModal(true)
    } else {
      setSelectedDate(date)
      setShowPostModal(true)
    }
  }

  // Approve post
  const approvePost = async (postId) => {
    try {
      await postsAPI.approvePosts({ post_ids: [postId] })
      await loadPosts()
      toast.success('Post approved!')
    } catch (error) {
      console.error('Error approving post:', error)
      toast.error('Failed to approve post')
    }
  }

  // Regenerate post content
  const regeneratePost = async (postId) => {
    try {
      await postsAPI.regeneratePost(postId)
      await loadPosts()
      toast.success('Post content regenerated!')
    } catch (error) {
      console.error('Error regenerating post:', error)
      toast.error('Failed to regenerate post')
    }
  }

  const calendarDays = generateCalendarDays()
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Calendar Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <h2 className="text-lg font-semibold text-gray-900">Content Calendar</h2>
          <div className="flex items-center space-x-1">
            <button
              onClick={goToPreviousMonth}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-sm font-medium text-gray-700">
              {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
            </span>
            <button
              onClick={goToNextMonth}
              className="p-1 hover:bg-gray-100 rounded"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="flex items-center space-x-1">
          <button
            onClick={() => generatePostsForDayOfWeek(1)} // Monday
            disabled={isGenerating}
            className="btn-secondary text-xs disabled:opacity-50 px-2 py-1"
          >
            Mondays
          </button>
          <button
            onClick={() => generatePostsForDayOfWeek(5)} // Friday
            disabled={isGenerating}
            className="btn-secondary text-xs disabled:opacity-50 px-2 py-1"
          >
            Fridays
          </button>
        </div>
      </div>

              {/* Calendar Grid */}
        <div className="bg-white rounded-lg shadow-sm border">
          {/* Day Headers */}
          <div className="grid grid-cols-7 gap-1 bg-gray-100 p-2">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center">
                <span className="text-xs font-medium text-gray-500">{day}</span>
              </div>
            ))}
          </div>

          {/* Calendar Days */}
          <div className="grid grid-cols-7 gap-1 bg-gray-100 p-2">
            {calendarDays.map((date, index) => {
              const postsForDate = getPostsForDate(date)
              const isCurrentMonth = date.getMonth() === currentDate.getMonth()
              const isToday = date.toDateString() === new Date().toDateString()
              const isPastDate = date < new Date(new Date().setHours(0, 0, 0, 0))
              const hasPosts = postsForDate.length > 0
              const mainPost = postsForDate[0] // Get the first post for the main image

              return (
                <div
                  key={index}
                  onClick={() => !isPastDate && isCurrentMonth && handleDateClick(date)}
                  className={`aspect-square bg-white rounded-lg cursor-pointer transition-all ${
                    !isCurrentMonth ? 'opacity-30' : ''
                  } ${isPastDate ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-md'} ${
                    isToday ? 'ring-2 ring-blue-500' : ''
                  }`}
                >
                  {/* Date Number */}
                  <div className="p-2">
                    <span className={`text-sm font-medium ${
                      isToday ? 'text-blue-600' : ''
                    } ${!isCurrentMonth ? 'text-gray-400' : 'text-gray-600'} ${isPastDate ? 'text-gray-400' : ''}`}>
                      {date.getDate()}
                    </span>
                  </div>

                  {/* Circular Image Thumbnail - Like the reference */}
                  {hasPosts && isCurrentMonth && !isPastDate && mainPost.image_url && (
                    <div className="flex justify-center items-center px-2 pb-2">
                      <div className="relative w-12 h-12 rounded-full overflow-hidden">
                        <img
                          src={`http://localhost:8000${mainPost.image_url}`}
                          alt={`${mainPost.platform} post`}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'flex';
                          }}
                        />
                        <div className="w-full h-full bg-gray-200 flex items-center justify-center" style={{display: 'none'}}>
                          <span className="text-xs text-gray-500">📷</span>
                        </div>
                        {/* Date overlay on image */}
                        <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                          <span className="text-white text-xs font-bold">{date.getDate()}</span>
                        </div>
                        {/* Status indicator */}
                        <div className="absolute top-1 right-1 w-2 h-2">
                          <div className={`w-full h-full rounded-full ${
                            mainPost.status === 'approved' ? 'bg-green-500' :
                            mainPost.status === 'scheduled' ? 'bg-blue-500' :
                            'bg-gray-400'
                          }`} />
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Text-only posts or no posts */}
                  {(!hasPosts || !mainPost?.image_url) && isCurrentMonth && !isPastDate && (
                    <div className="flex justify-center items-center px-2 pb-2">
                      {hasPosts ? (
                        <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                          <span className="text-xs text-gray-500">📝</span>
                        </div>
                      ) : (
                        <div className="w-12 h-12 bg-gray-50 rounded-full flex items-center justify-center">
                          <Plus className="w-4 h-4 text-gray-400" />
                        </div>
                      )}
                    </div>
                  )}

                  {/* Previous month dates - minimal display */}
                  {!isCurrentMonth && (
                    <div className="flex justify-center items-center px-2 pb-2">
                      <div className="w-12 h-12 bg-transparent"></div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

      {/* Post Modal */}
      {showPostModal && selectedPost && (
        <PostApprovalModal
          post={selectedPost}
          onClose={() => setShowPostModal(false)}
          onUpdate={loadPosts}
        />
      )}

      {/* Generate Posts Modal */}
      {showPostModal && !selectedPost && selectedDate && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Generate Posts for {selectedDate.toLocaleDateString()}
              </h3>
              <button
                onClick={() => setShowPostModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="text-center py-8">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Plus className="w-8 h-8 text-gray-400" />
              </div>
              <h4 className="text-lg font-medium text-gray-900 mb-2">No posts for this date</h4>
              <p className="text-gray-600 mb-4">
                Generate content for {selectedDate.toLocaleDateString()} to get started.
              </p>
              <button
                onClick={() => generatePostsForDate(selectedDate)}
                disabled={isGenerating}
                className="btn-primary disabled:opacity-50"
              >
                {isGenerating ? 'Generating...' : 'Generate Posts'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 