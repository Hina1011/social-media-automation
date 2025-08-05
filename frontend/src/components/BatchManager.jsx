import { useState, useEffect } from 'react'
import { Calendar, Plus, Check, Clock, RefreshCw } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { postsAPI } from '../services/api'

export function BatchManager({ onUpdate }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [batchStatus, setBatchStatus] = useState({
    currentBatch: 0,
    totalPosts: 0,
    approvedPosts: 0,
    remainingPosts: 0,
    nextBatchDate: null
  })

  useEffect(() => {
    calculateBatchStatus()
  }, [])

  const calculateBatchStatus = async () => {
    try {
      const response = await postsAPI.getPosts()
      const posts = response.data

      // Calculate batch status
      const totalPosts = posts.length
      const approvedPosts = posts.filter(post => post.status === 'approved').length
      const remainingPosts = totalPosts - approvedPosts

      // Find the next batch date (7 days after the last post)
      const lastPost = posts.sort((a, b) => new Date(b.scheduled_date) - new Date(a.scheduled_date))[0]
      const nextBatchDate = lastPost ? new Date(lastPost.scheduled_date) : new Date()
      nextBatchDate.setDate(nextBatchDate.getDate() + 7)

      setBatchStatus({
        currentBatch: Math.ceil(totalPosts / 7),
        totalPosts,
        approvedPosts,
        remainingPosts,
        nextBatchDate
      })
    } catch (error) {
      console.error('Error calculating batch status:', error)
    }
  }

  const generateNextBatch = async () => {
    setIsGenerating(true)
    try {
      const startDate = new Date(batchStatus.nextBatchDate)
      startDate.setHours(9, 0, 0, 0)

      const requestData = {
        custom_prompt: "Create engaging social media content for the next week",
        start_date: startDate.toISOString(),
        platforms: ['instagram', 'linkedin', 'facebook', 'twitter']
      }

      await postsAPI.generatePosts(requestData)
      await calculateBatchStatus()
      onUpdate()
      toast.success('Next batch of posts generated successfully!')
    } catch (error) {
      console.error('Error generating next batch:', error)
      toast.error('Failed to generate next batch')
    } finally {
      setIsGenerating(false)
    }
  }

  const generateSpecificDayBatch = async (dayOfWeek) => {
    setIsGenerating(true)
    try {
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      const dayName = dayNames[dayOfWeek]
      
      // Generate 7 posts for the next 7 occurrences of this day
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

        await postsAPI.generatePosts(requestData)
      }

      await calculateBatchStatus()
      onUpdate()
      toast.success(`Generated 7 posts for ${dayName}s!`)
    } catch (error) {
      console.error('Error generating day batch:', error)
      toast.error('Failed to generate day batch')
    } finally {
      setIsGenerating(false)
    }
  }

  const getProgressPercentage = () => {
    if (batchStatus.totalPosts === 0) return 0
    return Math.round((batchStatus.approvedPosts / batchStatus.totalPosts) * 100)
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-base font-semibold text-gray-900">Batch Management</h3>
        <div className="flex items-center space-x-1">
          <button
            onClick={() => generateSpecificDayBatch(1)} // Monday
            disabled={isGenerating}
            className="btn-secondary text-xs disabled:opacity-50 px-2 py-1"
          >
            Mondays
          </button>
          <button
            onClick={() => generateSpecificDayBatch(5)} // Friday
            disabled={isGenerating}
            className="btn-secondary text-xs disabled:opacity-50 px-2 py-1"
          >
            Fridays
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-3 mb-4">
        <div className="text-center">
          <div className="text-lg font-bold text-blue-600">{batchStatus.currentBatch}</div>
          <div className="text-xs text-gray-600">Batch</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-bold text-gray-900">{batchStatus.totalPosts}</div>
          <div className="text-xs text-gray-600">Total</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-bold text-green-600">{batchStatus.approvedPosts}</div>
          <div className="text-xs text-gray-600">Approved</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-bold text-orange-600">{batchStatus.remainingPosts}</div>
          <div className="text-xs text-gray-600">Pending</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium text-gray-700">Progress</span>
          <span className="text-xs text-gray-600">{getProgressPercentage()}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-1.5">
          <div 
            className="bg-green-500 h-1.5 rounded-full transition-all duration-300"
            style={{ width: `${getProgressPercentage()}%` }}
          ></div>
        </div>
      </div>

      {/* Next Batch Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4 text-blue-600" />
            <div>
              <h4 className="text-xs font-medium text-blue-900">Next Batch</h4>
              <p className="text-xs text-blue-700">
                {batchStatus.nextBatchDate ? 
                  `Starting ${batchStatus.nextBatchDate.toLocaleDateString()}` : 
                  'No next batch scheduled'
                }
              </p>
            </div>
          </div>
          <button
            onClick={generateNextBatch}
            disabled={isGenerating}
            className="btn-primary flex items-center text-xs disabled:opacity-50 px-2 py-1"
          >
            <Plus className="w-3 h-3 mr-1" />
            {isGenerating ? 'Generating...' : 'Generate'}
          </button>
        </div>
      </div>

      {/* Auto-generation Info */}
      {batchStatus.remainingPosts === 0 && batchStatus.totalPosts > 0 && (
        <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <Check className="w-4 h-4 text-green-600" />
            <span className="text-sm text-green-800">
              All posts in current batch are approved! Ready to generate next batch.
            </span>
          </div>
        </div>
      )}
    </div>
  )
} 