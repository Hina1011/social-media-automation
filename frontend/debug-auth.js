// Debug script to check authentication status
// Run this in your browser console

console.log('🔍 Debugging Authentication...')

// Check if token exists
const token = localStorage.getItem('token')
console.log('Token exists:', !!token)
if (token) {
  console.log('Token preview:', token.substring(0, 20) + '...')
}

// Check if user is logged in
const user = JSON.parse(localStorage.getItem('user') || 'null')
console.log('User data:', user)

// Test API call
async function testAPI() {
  try {
    const response = await fetch('/api/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('API Response Status:', response.status)
    
    if (response.ok) {
      const data = await response.json()
      console.log('API Response Data:', data)
    } else {
      const error = await response.text()
      console.log('API Error:', error)
    }
  } catch (error) {
    console.log('API Call Error:', error)
  }
}

// Test posts endpoint
async function testPosts() {
  try {
    const response = await fetch('/api/posts/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('Posts API Response Status:', response.status)
    
    if (response.ok) {
      const data = await response.json()
      console.log('Posts API Response Data:', data)
    } else {
      const error = await response.text()
      console.log('Posts API Error:', error)
    }
  } catch (error) {
    console.log('Posts API Call Error:', error)
  }
}

// Run tests
console.log('\n🧪 Running API Tests...')
testAPI()
testPosts()

// Helper function to set token manually
function setToken(manualToken) {
  localStorage.setItem('token', manualToken)
  console.log('Token set manually. Please refresh the page.')
}

console.log('\n💡 To set token manually, use: setToken("your-jwt-token-here")') 