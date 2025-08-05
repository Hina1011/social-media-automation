import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useAuth } from '../contexts/AuthContext.jsx'
import { usersAPI } from '../services/api.js'
import { User, Mail, Building, CheckCircle, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

export function ProfilePage() {
  const { user, updateUser } = useAuth()
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [availableInterests, setAvailableInterests] = useState([])

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch
  } = useForm()

  const selectedInterests = watch('interests', [])

  useEffect(() => {
    loadProfileData()
  }, [])

  const loadProfileData = async () => {
    try {
      const [profileResponse, interestsResponse] = await Promise.all([
        usersAPI.getProfile(),
        usersAPI.getInterests()
      ])

      const profileData = profileResponse.data
      setAvailableInterests(interestsResponse.data.interests || [])

      // Set form values
      setValue('full_name', profileData.full_name || '')
      setValue('email', profileData.email || '')
      setValue('role', profileData.role || 'individual')
      setValue('interests', profileData.interests || [])
      setValue('custom_prompt', profileData.custom_prompt || '')
    } catch (error) {
      console.error('Error loading profile data:', error)
      toast.error('Failed to load profile data')
    }
  }

  const onSubmit = async (data) => {
    setIsSaving(true)
    try {
      const response = await usersAPI.updateProfile(data)
      updateUser(response.data)
      toast.success('Profile updated successfully!')
    } catch (error) {
      console.error('Error updating profile:', error)
      toast.error('Failed to update profile')
    } finally {
      setIsSaving(false)
    }
  }

  const handleInterestToggle = (interest) => {
    const currentInterests = selectedInterests || []
    const updatedInterests = currentInterests.includes(interest)
      ? currentInterests.filter(i => i !== interest)
      : [...currentInterests, interest]
    
    setValue('interests', updatedInterests)
  }

  const handleCompleteProfile = async (data) => {
    setIsSaving(true)
    try {
      const response = await usersAPI.completeProfile(data)
      updateUser(response.data.user)
      toast.success('Profile completed successfully!')
    } catch (error) {
      console.error('Error completing profile:', error)
      toast.error('Failed to complete profile')
    } finally {
      setIsSaving(false)
    }
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
          <h1 className="text-2xl font-bold text-gray-900">Profile Settings</h1>
          <p className="text-gray-600">Manage your account information and preferences</p>
        </div>
        <div className="flex items-center space-x-2">
          {user?.is_verified ? (
            <div className="flex items-center text-green-600">
              <CheckCircle className="w-5 h-5 mr-1" />
              <span className="text-sm font-medium">Verified</span>
            </div>
          ) : (
            <div className="flex items-center text-yellow-600">
              <AlertCircle className="w-5 h-5 mr-1" />
              <span className="text-sm font-medium">Unverified</span>
            </div>
          )}
        </div>
      </div>

      {/* Profile Completion Status */}
      {!user?.is_profile_complete && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-yellow-600 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-yellow-800">Complete your profile</h3>
              <p className="text-sm text-yellow-700">
                Add your interests and custom prompt to get better AI-generated content.
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Form */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">Basic Information</h2>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
                    Full Name
                  </label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <User className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="full_name"
                      type="text"
                      {...register('full_name', {
                        required: 'Full name is required',
                        minLength: {
                          value: 2,
                          message: 'Full name must be at least 2 characters',
                        },
                      })}
                      className={`input-field pl-10 ${
                        errors.full_name ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''
                      }`}
                      placeholder="Enter your full name"
                    />
                  </div>
                  {errors.full_name && (
                    <p className="mt-1 text-sm text-red-600">{errors.full_name.message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                    Email Address
                  </label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Mail className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="email"
                      type="email"
                      {...register('email', {
                        required: 'Email is required',
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: 'Invalid email address',
                        },
                      })}
                      className={`input-field pl-10 ${
                        errors.email ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''
                      }`}
                      placeholder="Enter your email"
                    />
                  </div>
                  {errors.email && (
                    <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700">
                  Account Type
                </label>
                <div className="mt-1">
                  <select
                    id="role"
                    {...register('role', { required: 'Please select an account type' })}
                    className="input-field"
                  >
                    <option value="individual">Individual</option>
                    <option value="company">Company</option>
                  </select>
                </div>
                {errors.role && (
                  <p className="mt-1 text-sm text-red-600">{errors.role.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="custom_prompt" className="block text-sm font-medium text-gray-700">
                  Custom Prompt
                </label>
                <div className="mt-1">
                  <textarea
                    id="custom_prompt"
                    rows={4}
                    {...register('custom_prompt')}
                    className="input-field"
                    placeholder="Describe your brand, style, or any specific requirements for content generation..."
                  />
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  This helps AI generate content that better matches your brand and style.
                </p>
              </div>

              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Interests Selection */}
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Interests</h2>
            <p className="text-sm text-gray-600 mb-4">
              Select topics that interest you to get better content suggestions.
            </p>
            
            <div className="space-y-3">
              {availableInterests.map((interest) => (
                <label key={interest} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedInterests?.includes(interest) || false}
                    onChange={() => handleInterestToggle(interest)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700 capitalize">{interest}</span>
                </label>
              ))}
            </div>

            {!user?.is_profile_complete && (
              <div className="mt-6">
                <button
                  onClick={handleSubmit(handleCompleteProfile)}
                  disabled={isSaving}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSaving ? 'Completing...' : 'Complete Profile'}
                </button>
              </div>
            )}
          </div>

          {/* Account Info */}
          <div className="card mt-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Member since</span>
                <span className="text-sm font-medium text-gray-900">
                  {new Date(user?.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Account type</span>
                <span className="text-sm font-medium text-gray-900 capitalize">
                  {user?.role}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Profile status</span>
                <span className={`text-sm font-medium ${
                  user?.is_profile_complete ? 'text-green-600' : 'text-yellow-600'
                }`}>
                  {user?.is_profile_complete ? 'Complete' : 'Incomplete'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 