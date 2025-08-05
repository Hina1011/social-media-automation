// Run this in your browser console to set the authentication token
// Copy and paste this entire script into your browser console

(function() {
  const testToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzUzNzg4MzUwfQ.X2JWJG4hDeY6IxP31XiYjCa_BQESjfK-EUMnFhdWJsU'
  
  localStorage.setItem('token', testToken)
  
  console.log('✅ Token set successfully!')
  console.log('🔄 Refreshing page...')
  
  // Refresh the page after 1 second
  setTimeout(() => {
    window.location.reload()
  }, 1000)
})() 