// content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getJobData") {
    // Attempt to find job description text automatically
    const selectors = ['.job-description', '#jobDescriptionText', '[class*="description"]'];
    let foundText = "";
    
    for (let s of selectors) {
      let el = document.querySelector(s);
      if (el) { foundText = el.innerText; break; }
    }

    // Fallback: If nothing found, use whatever the user highlighted
    const selectedText = window.getSelection().toString();
    sendResponse({ 
      description: selectedText || foundText || document.body.innerText.substring(0, 5000) 
    });
  }
  return true;
});