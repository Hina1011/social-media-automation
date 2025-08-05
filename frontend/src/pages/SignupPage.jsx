import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useAuth } from '../contexts/AuthContext.jsx'
import { Eye, EyeOff, Mail, Lock, User, Building } from 'lucide-react'

export function SignupPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState(null)
  const [accountType, setAccountType] = useState('')
  const [selectedInterests, setSelectedInterests] = useState([])
  const { signup } = useAuth()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    setError,
    clearErrors,
    reset,
  } = useForm()

  const password = watch('password')

  // Predefined interests list
  const interestsList = [
    'Technology', 'Music', 'Sports', 'Reading', 'Travel', 'Cooking', 'Photography', 'Art',
    'Fitness', 'Gaming', 'Fashion', 'Business', 'Education', 'Health', 'Food', 'Movies',
    'Nature', 'Science', 'Politics', 'Beauty', 'Automotive', 'Finance', 'Real Estate'
  ]

  const handleInterestChange = (interest) => {
    setSelectedInterests(prev => 
      prev.includes(interest)
        ? prev.filter(i => i !== interest)
        : [...prev, interest]
    )
  }

  const onSubmit = async (data) => {
    setIsLoading(true)
    setApiError(null)
    
    // Validate interests
    if (selectedInterests.length < 5) {
      setApiError('Please select at least 5 interests')
      setIsLoading(false)
      return
    }

    // Ensure all required fields are present
    const payload = {
      ...data,
      role: accountType,
      profession: data.profession,
      interests: selectedInterests,
      company_name: accountType === 'company' ? data.company_name : '',
      website: accountType === 'company' ? data.website : '',
      industry: accountType === 'company' ? data.industry : '',
    }
    try {
      await signup(payload)
      navigate('/login')
    } catch (error) {
      if (error.response?.data?.detail) {
        setApiError(error.response.data.detail)
      } else {
        setApiError('Signup failed. Please check your input.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  // Step 1: Account type selection
  if (!accountType) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary-100">
            <span className="text-2xl font-bold text-primary-600">SA</span>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <div className="mt-8 space-y-4">
            <button
              className="w-full py-2 px-4 border border-primary-600 text-primary-600 rounded hover:bg-primary-50 font-medium"
              onClick={() => setAccountType('individual')}
            >
              Sign up as Individual
            </button>
            <button
              className="w-full py-2 px-4 border border-primary-600 text-primary-600 rounded hover:bg-primary-50 font-medium"
              onClick={() => setAccountType('company')}
            >
              Sign up as Company
            </button>
          </div>
          <div className="text-center mt-4">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link
                to="/login"
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Sign in here
              </Link>
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Step 2: Show the form
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary-100">
            <span className="text-2xl font-bold text-primary-600">SA</span>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {accountType === 'company' ? 'Company Signup' : 'Individual Signup'}
          </h2>
          <button
            className="mt-2 text-xs text-primary-600 underline"
            onClick={() => { setAccountType(''); reset(); setSelectedInterests([]); }}
          >
            &larr; Change account type
          </button>
        </div>

        {apiError && (
          <div className="bg-red-100 text-red-700 p-2 rounded text-sm">
            {Array.isArray(apiError)
              ? apiError.map((err, idx) => <div key={idx}>{err.msg || JSON.stringify(err)}</div>)
              : apiError}
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
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
                Email address
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

            <div>
              <label htmlFor="mobile_number" className="block text-sm font-medium text-gray-700">
                Mobile Number
              </label>
              <input
                id="mobile_number"
                type="text"
                {...register('mobile_number', {
                  required: 'Mobile number is required',
                  pattern: {
                    value: /^\+?1?\d{9,15}$/,
                    message: 'Invalid mobile number',
                  },
                })}
                className={`input-field ${errors.mobile_number ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="e.g. +12345678901"
              />
              {errors.mobile_number && (
                <p className="mt-1 text-sm text-red-600">{errors.mobile_number.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="profession" className="block text-sm font-medium text-gray-700">
                Profession
              </label>
              <input
                id="profession"
                type="text"
                {...register('profession', {
                  required: 'Profession is required',
                  minLength: {
                    value: 2,
                    message: 'Profession must be at least 2 characters',
                  },
                })}
                className={`input-field ${errors.profession ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="e.g. Student, Doctor, Engineer"
              />
              {errors.profession && (
                <p className="mt-1 text-sm text-red-600">{errors.profession.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Interests (select at least 5)
              </label>
              <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto border rounded p-2">
                {interestsList.map((interest) => (
                  <label key={interest} className="flex items-center space-x-2 text-sm">
                    <input
                      type="checkbox"
                      checked={selectedInterests.includes(interest)}
                      onChange={() => handleInterestChange(interest)}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span>{interest}</span>
                  </label>
                ))}
              </div>
              {selectedInterests.length < 5 && (
                <p className="mt-1 text-sm text-red-600">
                  Please select at least 5 interests ({selectedInterests.length}/5)
                </p>
              )}
            </div>

            <div>
              <label htmlFor="custom_prompt" className="block text-sm font-medium text-gray-700">
                Custom Prompt
              </label>
              <input
                id="custom_prompt"
                type="text"
                {...register('custom_prompt', {
                  required: 'Custom prompt is required',
                  minLength: {
                    value: 10,
                    message: 'Custom prompt must be at least 10 characters',
                  },
                })}
                className={`input-field ${errors.custom_prompt ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                placeholder="e.g. I want to automate my social media posts."
              />
              {errors.custom_prompt && (
                <p className="mt-1 text-sm text-red-600">{errors.custom_prompt.message}</p>
              )}
            </div>

            {/* Company fields (only for company) */}
            {accountType === 'company' && (
              <>
                <div>
                  <label htmlFor="company_name" className="block text-sm font-medium text-gray-700">
                    Company Name
                  </label>
                  <input
                    id="company_name"
                    type="text"
                    {...register('company_name', {
                      required: 'Company name is required',
                      minLength: { value: 2, message: 'Company name must be at least 2 characters' },
                    })}
                    className={`input-field ${errors.company_name ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                    placeholder="Company name"
                  />
                  {errors.company_name && (
                    <p className="mt-1 text-sm text-red-600">{errors.company_name.message}</p>
                  )}
                </div>
                <div>
                  <label htmlFor="website" className="block text-sm font-medium text-gray-700">
                    Website
                  </label>
                  <input
                    id="website"
                    type="text"
                    {...register('website', {
                      required: 'Website is required',
                    })}
                    className={`input-field ${errors.website ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                    placeholder="Website"
                  />
                  {errors.website && (
                    <p className="mt-1 text-sm text-red-600">{errors.website.message}</p>
                  )}
                </div>
                <div>
                  <label htmlFor="industry" className="block text-sm font-medium text-gray-700">
                    Industry
                  </label>
                  <input
                    id="industry"
                    type="text"
                    {...register('industry', {
                      required: 'Industry is required',
                    })}
                    className={`input-field ${errors.industry ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''}`}
                    placeholder="Industry"
                  />
                  {errors.industry && (
                    <p className="mt-1 text-sm text-red-600">{errors.industry.message}</p>
                  )}
                </div>
              </>
            )}

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters',
                    },
                  })}
                  className={`input-field pl-10 pr-10 ${
                    errors.password ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''
                  }`}
                  placeholder="Create a password"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirm Password
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  {...register('confirmPassword', {
                    required: 'Please confirm your password',
                    validate: (value) => value === password || 'Passwords do not match',
                  })}
                  className={`input-field pl-10 pr-10 ${
                    errors.confirmPassword ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : ''
                  }`}
                  placeholder="Confirm your password"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Creating account...
                </div>
              ) : (
                'Create account'
              )}
            </button>
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link
                to="/login"
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Sign in here
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  )
} 