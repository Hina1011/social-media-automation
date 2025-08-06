import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext.jsx'
import { postsAPI } from '../services/api.js'
import { 
  Calendar, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Plus,
  RefreshCw,
  Settings,
  Eye,
  Edit
} from 'lucide-react'

export function CalendarView() {
  const { user } = useAuth()
  const [posts, setPosts] = useState([])
  const [batches, setBatches] = useState([])
  const [pendingPosts, setPendingPosts] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedBatch, setSelectedBatch] = useState(null)
  const [scheduleTime, setScheduleTime] = useState('09:00')
  const [showScheduleModal, setShowScheduleModal] = useState(false)
  const [currentMonth, setCurrentMonth] = useState(new Date())

  useEffect(() => {
    loadCalendarData()
  }, [])

  const loadCalendarData = async () => {
    try {
      setIsLoading(true)
      const [postsResponse, batchesResponse, pendingResponse] = await Promise.all([
        postsAPI.getUserPosts(),
        postsAPI.getUserBatches(),
        postsAPI.getPendingApprovalPosts()
      ])

      setPosts(postsResponse.data || [])
      setBatches(batchesResponse.data || [])
      setPendingPosts(pendingResponse.data || [])
    } catch (error) {
      console.error('Error loading calendar data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleBatchApprove = async (batchId) => {
    try {
      await postsAPI.batchApprove(batchId)
      await loadCalendarData()
      // Show success notification
      alert('Batch approved successfully! Posts will be scheduled for posting.')
    } catch (error) {
      console.error('Error approving batch:', error)
      alert('Error approving batch. Please try again.')
    }
  }

  const handleRegenerateNextBatch = async () => {
    try {
      await postsAPI.regenerateNextBatch()
      await loadCalendarData()
      alert('Next batch generated successfully! Please review and approve.')
    } catch (error) {
      console.error('Error regenerating batch:', error)
      alert('Error generating next batch. Please try again.')
    }
  }

  const handleUpdateScheduleTime = async () => {
    try {
      await postsAPI.updateScheduleTime(scheduleTime)
      setShowScheduleModal(false)
      alert('Schedule time updated successfully!')
    } catch (error) {
      console.error('Error updating schedule time:', error)
      alert('Error updating schedule time. Please try again.')
    }
  }

  const getPostsForDate = (date) => {
    const dateStr = date.toISOString().split('T')[0]
    return posts.filter(post => 
      post.scheduled_date && post.scheduled_date.startsWith(dateStr)
    )
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending_approval': return 'bg-yellow-100 text-yellow-800'
      case 'approved': return 'bg-green-100 text-green-800'
      case 'scheduled': return 'bg-blue-100 text-blue-800'
      case 'posted': return 'bg-purple-100 text-purple-800'
      case 'draft': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending_approval': return <AlertCircle className="w-4 h-4" />
      case 'approved': return <CheckCircle className="w-4 h-4" />
      case 'scheduled': return <Clock className="w-4 h-4" />
      case 'posted': return <CheckCircle className="w-4 h-4" />
      default: return <Eye className="w-4 h-4" />
    }
  }

  const renderCalendar = () => {
    const year = currentMonth.getFullYear()
    const month = currentMonth.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const startDate = new Date(firstDay)
    startDate.setDate(startDate.getDate() - firstDay.getDay())

    const calendar = []
    const currentDate = new Date(startDate)

    while (currentDate <= lastDay || calendar.length < 42) {
      calendar.push(new Date(currentDate))
      currentDate.setDate(currentDate.getDate() + 1)
    }

    return (
      <div className="grid grid-cols-7 gap-1">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="p-2 text-center text-sm font-medium text-gray-500">
            {day}
          </div>
        ))}
        
        {calendar.map((date, index) => {
          const dayPosts = getPostsForDate(date)
          const isCurrentMonth = date.getMonth() === month
          const isToday = date.toDateString() === new Date().toDateString()
          
          return (
            <div
              key={index}
              className={`min-h-24 p-1 border border-gray-200 ${
                isCurrentMonth ? 'bg-white' : 'bg-gray-50'
              } ${isToday ? 'ring-2 ring-primary-500' : ''}`}
            >
              <div className={`text-xs font-medium mb-1 ${
                isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
              } ${isToday ? 'text-primary-600 font-bold' : ''}`}>
                {date.getDate()}
              </div>
              
              <div className="space-y-1">
                {dayPosts.map((post, postIndex) => (
                  <div
                    key={post._id}
                    className={`text-xs p-1 rounded cursor-pointer hover:bg-gray-50 ${
                      getStatusColor(post.status)
                    }`}
                    title={`${post.caption?.substring(0, 50)}...`}
                  >
                    <div className="flex items-center space-x-1">
                      {getStatusIcon(post.status)}
                      <span className="truncate">
                        {post.caption?.substring(0, 20)}...
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
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
      {/* Header with controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-semibold text-gray-900">Content Calendar</h2>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
              className="p-2 text-gray-500 hover:text-gray-700"
            >
              ←
            </button>
            <span className="text-lg font-medium">
              {currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
            </span>
            <button
              onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
              className="p-2 text-gray-500 hover:text-gray-700"
            >
              →
            </button>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowScheduleModal(true)}
            className="flex items-center space-x-2 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
          >
            <Settings className="w-4 h-4" />
            Schedule Time
          </button>
          
          {pendingPosts.length > 0 && (
            <button
              onClick={() => handleRegenerateNextBatch()}
              className="flex items-center space-x-2 px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200"
            >
              <RefreshCw className="w-4 h-4" />
              Generate Next Batch
            </button>
          )}
        </div>
      </div>

      {/* Pending Approval Section */}
      {pendingPosts.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 text-yellow-600" />
              <h3 className="text-lg font-medium text-yellow-800">
                Posts Pending Approval ({pendingPosts.length})
              </h3>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleBatchApprove(pendingPosts[0]?.batch_id)}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
              >
                <CheckCircle className="w-4 h-4" />
                Approve All
              </button>
              
              <button
                onClick={() => setSelectedBatch(pendingPosts[0]?.batch_id)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <Eye className="w-4 h-4" />
                Review
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {pendingPosts.slice(0, 6).map((post) => (
              <div key={post._id} className="bg-white p-3 rounded-lg border border-yellow-200">
                <div className="flex items-start justify-between mb-2">
                  <span className="text-xs text-gray-500">
                    {new Date(post.scheduled_date).toLocaleDateString()}
                  </span>
                  <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                    Pending
                  </span>
                </div>
                <p className="text-sm text-gray-900 line-clamp-3">
                  {post.caption}
                </p>
                <div className="flex items-center space-x-2 mt-2">
                  {post.platforms?.map((platform) => (
                    <span key={platform} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                      {platform}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Calendar */}
      <div className="bg-white rounded-lg shadow">
        {renderCalendar()}
      </div>

      {/* Batch Summary */}
      {batches.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Batch Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {batches.map((batch) => (
              <div key={batch.batch_id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-900">
                    Batch {batch.batch_id?.split('_')[1]}
                  </span>
                  <span className="text-xs text-gray-500">
                    {new Date(batch.created_at).toLocaleDateString()}
                  </span>
                </div>
                
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span>Total:</span>
                    <span className="font-medium">{batch.total_posts}</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span>Pending:</span>
                    <span className="text-yellow-600 font-medium">{batch.pending_count}</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span>Approved:</span>
                    <span className="text-green-600 font-medium">{batch.approved_count}</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span>Posted:</span>
                    <span className="text-purple-600 font-medium">{batch.posted_count}</span>
                  </div>
                </div>
                
                {batch.pending_count > 0 && (
                  <button
                    onClick={() => handleBatchApprove(batch.batch_id)}
                    className="w-full mt-3 px-3 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    Approve Batch
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Schedule Time Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Set Posting Schedule</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Default Posting Time
                </label>
                <input
                  type="time"
                  value={scheduleTime}
                  onChange={(e) => setScheduleTime(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Posts will be scheduled at this time each day
                </p>
              </div>
              
              <div className="flex items-center space-x-3">
                <button
                  onClick={handleUpdateScheduleTime}
                  className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                >
                  Save Schedule
                </button>
                <button
                  onClick={() => setShowScheduleModal(false)}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 