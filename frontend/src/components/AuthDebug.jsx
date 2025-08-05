import React, { useState, useEffect } from 'react'
import { api } from '../services/api.js'

export function AuthDebug() {
  const [debugInfo, setDebugInfo] = useState({})
  const [testResult, setTestResult] = useState(null)

  useEffect(() => {
    updateDebugInfo()
  }, [])

  const updateDebugInfo = () => {
    const token = localStorage.getItem('token')
    setDebugInfo({
      hasToken: !!token,
      tokenPreview: token ? `${token.substring(0, 20)}...` : 'No token',
      tokenLength: token ? token.length : 0,
      currentUrl: window.location.href,
      userAgent: navigator.userAgent
    })
  }

  const testAuth = async () => {
    try {
      setTestResult({ loading: true, error: null, data: null })
      const response = await api.get('/auth/me')
      setTestResult({ loading: false, error: null, data: response.data })
    } catch (error) {
      setTestResult({ 
        loading: false, 
        error: error.response?.data || error.message, 
        data: null 
      })
    }
  }

  const testPosts = async () => {
    try {
      setTestResult({ loading: true, error: null, data: null })
      const response = await api.get('/posts/')
      setTestResult({ loading: false, error: null, data: response.data })
    } catch (error) {
      setTestResult({ 
        loading: false, 
        error: error.response?.data || error.message, 
        data: null 
      })
    }
  }

  const setTestToken = () => {
    const testToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzUzNzg4MzUwfQ.X2JWJG4hDeY6IxP31XiYjCa_BQESjfK-EUMnFhdWJsU'
    localStorage.setItem('token', testToken)
    updateDebugInfo()
  }

  const clearToken = () => {
    localStorage.removeItem('token')
    updateDebugInfo()
  }

  return (
    <div className="p-4 bg-gray-100 rounded-lg m-4">
      <h3 className="text-lg font-bold mb-4">🔍 Authentication Debug</h3>
      
      <div className="mb-4">
        <h4 className="font-semibold">Current State:</h4>
        <pre className="bg-white p-2 rounded text-sm">
          {JSON.stringify(debugInfo, null, 2)}
        </pre>
      </div>

      <div className="mb-4 space-x-2">
        <button 
          onClick={setTestToken}
          className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
        >
          Set Test Token
        </button>
        <button 
          onClick={clearToken}
          className="bg-red-500 text-white px-3 py-1 rounded text-sm"
        >
          Clear Token
        </button>
        <button 
          onClick={updateDebugInfo}
          className="bg-gray-500 text-white px-3 py-1 rounded text-sm"
        >
          Refresh Info
        </button>
      </div>

      <div className="mb-4 space-x-2">
        <button 
          onClick={testAuth}
          className="bg-green-500 text-white px-3 py-1 rounded text-sm"
        >
          Test /auth/me
        </button>
        <button 
          onClick={testPosts}
          className="bg-purple-500 text-white px-3 py-1 rounded text-sm"
        >
          Test /posts/
        </button>
      </div>

      {testResult && (
        <div className="mb-4">
          <h4 className="font-semibold">Test Result:</h4>
          {testResult.loading ? (
            <p>Loading...</p>
          ) : testResult.error ? (
            <div className="bg-red-100 p-2 rounded">
              <p className="text-red-700">Error: {JSON.stringify(testResult.error, null, 2)}</p>
            </div>
          ) : (
            <div className="bg-green-100 p-2 rounded">
              <p className="text-green-700">Success: {JSON.stringify(testResult.data, null, 2)}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
} 