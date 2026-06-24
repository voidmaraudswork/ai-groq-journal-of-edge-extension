// This listener runs every time a tab is fully loaded or updated
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // Only log when the page finishes loading completely and has a valid web URL
  if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
    
    const activityData = {
      source: "Edge Extension",
      title: tab.title || "Untitled Page",
      url: tab.url,
      timestamp: new Date().toISOString()
    };

    // Send EVERYTHING directly to your local Python server
    fetch('http://127.0.0.1:8000/api/log-activity', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(activityData)
    })
    .then(response => console.log('Activity logged successfully'))
    .catch(err => console.error('Error sending data to backend:', err));
  }
});