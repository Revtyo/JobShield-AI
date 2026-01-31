// popup.js

let globalScrapedJD = "";

// 1. Automatic Scrape on Startup
window.addEventListener('DOMContentLoaded', async () => {
    const statusEl = document.getElementById('scrapeStatus');
    try {
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
        const [{result}] = await chrome.scripting.executeScript({
            target: {tabId: tab.id},
            func: () => {
                const selectors = [
                    '.jobs-description__container', 
                    '#jobDescriptionText',           
                    '.description__text',            
                    'main'                           
                ];
                for (let s of selectors) {
                    let el = document.querySelector(s);
                    if (el && el.innerText.length > 100) return el.innerText;
                }
                return window.getSelection().toString() || document.body.innerText;
            }
        });

        if (result && result.length > 50) {
            globalScrapedJD = result;
            statusEl.innerText = "✅ Job details detected automatically";
            statusEl.style.color = "#27ae60";
        }
    } catch (err) {
        console.error("Scrape Error:", err);
    }
});

// 2. Analysis Trigger
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const resultsDiv = document.getElementById('results');
    const strengthDiv = document.getElementById('strength');
    const aiDiv = document.getElementById('airisk');
    const atsDiv = document.getElementById('atsStatus');
    const keywordsDiv = document.getElementById('missingKeywords');
    const fileInput = document.getElementById('resumeFile');

    if (!fileInput.files[0]) {
        alert("Please upload a PDF resume first!");
        return;
    }
    if (!globalScrapedJD) {
        alert("No job details found on this page.");
        return;
    }

    resultsDiv.style.display = "block";
    strengthDiv.innerText = "Processing PDF...";
    aiDiv.innerText = "";
    atsDiv.innerText = "";
    keywordsDiv.innerText = "";

    try {
        const formData = new FormData();
        formData.append("resume_file", fileInput.files[0]);
        formData.append("job_description", globalScrapedJD);

        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();

        // 3. Update UI
        strengthDiv.innerHTML = `Strength: <span style="color:#27ae60">${data.probability_score}%</span>`;
        aiDiv.innerHTML = `AI Detection: <b>${data.ai_risk}</b>`;
        
        let atsHtml = `ATS Status: <b>${data.ats_status}</b>`;
        if (data.ats_flags && data.ats_flags.length > 0) {
            atsHtml += `<ul style="font-size:11px; color:#c0392b; margin:5px 0 0 15px;">`;
            data.ats_flags.forEach(flag => { atsHtml += `<li>${flag}</li>`; });
            atsHtml += `</ul>`;
        }
        atsDiv.innerHTML = atsHtml;

        // --- UPDATED KEYWORD HTML LOGIC ---
        if (data.missing_keywords && data.missing_keywords.length > 0) {
            let listHtml = `<ul style="padding-left: 20px; color: #c0392b; font-weight: 500; margin-top: 5px;">`;
            data.missing_keywords.forEach(skill => {
                listHtml += `<li>${skill}</li>`;
            });
            listHtml += `</ul>`;
            keywordsDiv.innerHTML = listHtml;
        } else {
            keywordsDiv.innerText = "No major gaps found!";
        }

    } catch (err) {
        strengthDiv.innerText = "Analysis Failed";
        aiDiv.innerText = "Check backend connection.";
        console.error("Analysis Error:", err);
    }
});