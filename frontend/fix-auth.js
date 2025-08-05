// Complete Authentication Fix Script
// Copy and paste this entire script into your browser console

(function() {
  console.log('🔧 Starting authentication fix...')
  
  // Set the valid token
  const validToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzUzNzg4MzUwfQ.X2JWJG4hDeY6IxP31XiYjCa_BQESjfK-EUMnFhdWJsU'
  
  // Clear any existing token
  localStorage.removeItem('token')
  
  // Set the new token
  localStorage.setItem('token', validToken)
  
  console.log('✅ Token set successfully!')
  console.log('🔍 Current token:', localStorage.getItem('token') ? 'Present' : 'Missing')
  
  // Test the token with a direct API call
  fetch('/api/auth/me', {
    headers: {
      'Authorization': `Bearer ${validToken}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('🧪 Auth test status:', response.status)
    if (response.ok) {
      console.log('✅ Authentication working!')
      console.log('🔄 Refreshing page in 2 seconds...')
      setTimeout(() => {
        window.location.reload()
      }, 2000)
    } else {
      console.log('❌ Authentication failed:', response.status)
    }
  })
  .catch(error => {
    console.log('❌ Auth test error:', error)
  })
  
  // Also test posts endpoint
  setTimeout(() => {
    fetch('/api/posts/', {
      headers: {
        'Authorization': `Bearer ${validToken}`,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('📝 Posts test status:', response.status)
      if (response.ok) {
        console.log('✅ Posts endpoint working!')
      } else {
        console.log('❌ Posts endpoint failed:', response.status)
      }
    })
    .catch(error => {
      console.log('❌ Posts test error:', error)
    })
  }, 1000)
  
})() 