import { useEffect, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { platformsAPI } from '../services/api.js'
import { toast } from 'react-hot-toast'

export function LinkedInCallbackPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const processedRef = useRef(false)

  useEffect(() => {
    const handleCallback = async () => {
      // Prevent multiple executions
      if (processedRef.current) {
        return
      }
      processedRef.current = true

      try {
        const code = searchParams.get('code')
        const state = searchParams.get('state')
        const error = searchParams.get('error')
        const storedState = localStorage.getItem('linkedin_auth_state')

        console.log('🔗 LinkedIn callback parameters:', {
          code: code ? `${code.substring(0, 10)}...` : null,
          state,
          error,
          storedState
        })

        if (error) {
          console.error('LinkedIn OAuth error:', error)
          toast.error('LinkedIn connection failed')
          navigate('/platforms')
          return
        }

        if (!code) {
          console.error('No authorization code received')
          toast.error('No authorization code received from LinkedIn')
          navigate('/platforms')
          return
        }

        if (!state || state !== storedState) {
          console.error('State mismatch:', { received: state, stored: storedState })
          toast.error('Invalid state parameter')
          navigate('/platforms')
          return
        }

        console.log('🔗 State verification successful, processing callback...')
        
        console.log('🔗 Preparing callback request with:', {
          code: code ? `${code.substring(0, 10)}...` : null,
          state,
          storedState
        })

        // Call the backend to exchange code for token
        const response = await platformsAPI.linkedinCallback({
          platform: 'linkedin',
          auth_code: code,
          state: state
        })

        if (response.data.success) {
          toast.success('LinkedIn connected successfully!')
        } else {
          toast.error('Failed to connect LinkedIn')
        }

      } catch (error) {
        console.error('LinkedIn callback error:', error)
        toast.error('Failed to connect LinkedIn')
      } finally {
        // Redirect to platforms page after a short delay
        setTimeout(() => {
          navigate('/platforms')
        }, 2000)
      }
    }

    handleCallback()
  }, [searchParams, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Connecting LinkedIn...
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Processing your LinkedIn connection...
          </p>
        </div>
        
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    </div>
  )
}