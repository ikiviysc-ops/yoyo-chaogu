// Test script to reproduce the fetch issue
fetch('http://127.0.0.1:8001/api/stocks/selection')
  .then(response => {
    console.log('Response status:', response.status);
    return response.json();
  })
  .then(data => {
    console.log('Data:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });