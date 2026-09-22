import type { PlasmoCSConfig } from "plasmo"

export const config: PlasmoCSConfig = {
  matches: [
    "https://*.jobstreet.com/*",
    "https://*.jobstreet.com.my/*",
    "https://*.myfuturejobs.gov.my/*"
  ],
  run_at: "document_idle"
}

console.log("Job Tracker Extension active on job portal.")

window.addEventListener("load", () => {
  const observer = new MutationObserver(() => {
    if (!document.getElementById("job-tracker-btn")) {
      injectTrackerButton()
    }
  })
  observer.observe(document.body, { childList: true, subtree: true })
})

function injectTrackerButton() {
  const targetElement = document.querySelector("h1") || document.body
  if (!targetElement) return

  const trackBtn = document.createElement("button")
  trackBtn.id = "job-tracker-btn"
  trackBtn.innerText = "📌 Track Application"
  trackBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999999;
    background-color: #2563eb;
    color: white;
    padding: 10px 16px;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    font-family: sans-serif;
  `

  trackBtn.onclick = async () => {
    const jobData = extractJobDetails()
    try {
      const response = await httpTrackRequest(jobData)
      if (response.ok) {
        trackBtn.innerText = "✅ Tracked!"
        trackBtn.style.backgroundColor = "#16a34a"
        setTimeout(() => {
          trackBtn.innerText = "📌 Track Application"
          trackBtn.style.backgroundColor = "#2563eb"
        }, 3000)
      } else {
        alert("Failed to track job application.")
      }
    } catch (err) {
      console.error("Tracking error:", err)
      alert("Could not connect to FastAPI backend at http://localhost:8000. Make sure your server is running!")
    }
  }

  document.body.appendChild(trackBtn)
}

function extractJobDetails() {
  const title = document.querySelector("h1")?.innerText || document.title
  const companyElem = document.querySelector('[data-automation="advertiser-name"]') || document.querySelector('.company-name')
  const company = companyElem ? companyElem.textContent?.trim() || "Unknown Company" : "Unknown Company"
  
  const platform = window.location.hostname.includes("jobstreet") ? "JobStreet" : "MYFutureJobs"

  return {
    job_title: title.trim(),
    company: company,
    source_platform: platform,
    job_url: window.location.href,
    status: "Applied",
    salary_range: "Not Specified"
  }
}

async function httpTrackRequest(data: any) {
  return await fetch("http://localhost:8000/api/track", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
}