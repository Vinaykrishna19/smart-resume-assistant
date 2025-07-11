document.addEventListener("DOMContentLoaded", function () {
  // Tab switching logic
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabs = document.querySelectorAll(".tab-content");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabs.forEach(tab => tab.classList.add("hidden"));
      document.getElementById(btn.dataset.tab).classList.remove("hidden");
    });
  });

  // ANALYZE
  const analyzeForm = document.getElementById("analyze-form");
  const resumeAnalyze = document.getElementById("resume-analyze");
  const analyzeResult = document.getElementById("analyze-result");
  const analyzeDownloadJson = document.getElementById("analyze-download-json");
  const analyzeDownloadPdf = document.getElementById("analyze-download-pdf");
  const analyzeSpinner = document.getElementById("analyze-spinner");


  // MATCH
  const matchForm = document.getElementById("match-form");
  const resumeMatch = document.getElementById("resume-match");
  const jdFile = document.getElementById("jd-file");
  const jdText = document.getElementById("jd-text");
  const matchResult = document.getElementById("match-result");
  const matchDownloadJson = document.getElementById("match-download-json");
  const matchDownloadPdf = document.getElementById("match-download-pdf");
  const matchSpinner = document.getElementById("match-spinner");

  let lastAnalyzeData = null;
  let lastMatchData = null;

  // Analyze Resume Handler
  analyzeForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = resumeAnalyze.files[0];
    if (!file) return alert("Upload a resume!");

    analyzeResult.textContent = "";
    analyzeDownloadJson.disabled = true;
    analyzeDownloadPdf.disabled = true;

    const button = analyzeForm.querySelector("button[type='submit']");
    button.disabled = true;
    button.textContent = "Analyzing Resume";
    analyzeSpinner.classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/analyze-pdf", {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error("Analysis failed");
      const data = await res.json();
      lastAnalyzeData = data;
      analyzeResult.textContent = JSON.stringify(data, null, 2);
      analyzeDownloadJson.disabled = false;
      analyzeDownloadPdf.disabled = false;
    } catch (err) {
      analyzeResult.textContent = "❌ Failed to analyze.";
      console.error(err);
    } finally {
      button.disabled = false;
      button.textContent = "Analyze Resume";
      analyzeSpinner.classList.add("hidden");
    }
  });


  // (Removed duplicate/incomplete event listener for matchForm)


  // Match Resume to JD
  matchForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const resume = resumeMatch.files[0];
    const jd_file = jdFile.files[0];
    const jd_text = jdText.value.trim();

    if (!resume) return alert("Upload a resume!");
    if (!jd_file && !jd_text) return alert("Upload JD file or enter JD text");

    matchResult.textContent = "";
    matchDownloadJson.disabled = true;
    matchDownloadPdf.disabled = true;

    const button = matchForm.querySelector("button[type='submit']");
    button.disabled = true;
    button.textContent = "Matching Resume";
    matchSpinner.classList.remove("hidden");

    const formData = new FormData();
    formData.append("resume_file", resume);
    if (jd_file) formData.append("jd_file", jd_file);
    if (jd_text) formData.append("jd_text", jd_text);

    try {
      const res = await fetch("http://localhost:8000/match-files", {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error("Matching failed");
      const data = await res.json();
      lastMatchData = data;
      matchResult.textContent = JSON.stringify(data, null, 2);
      matchDownloadJson.disabled = false;
      matchDownloadPdf.disabled = false;
    } catch (err) {
      matchResult.textContent = "❌ Failed to match.";
      console.error(err);
    } finally {
      button.disabled = false;
      button.textContent = "Match Resume";
      matchSpinner.classList.add("hidden");

    }
  });


  // Download JSON (analyze)
  analyzeDownloadJson.addEventListener("click", () => {
    if (!lastAnalyzeData) return;
    const blob = new Blob([JSON.stringify(lastAnalyzeData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    triggerDownload(url, "analyze_result.json");
  });

  // Download PDF (analyze)
  analyzeDownloadPdf.addEventListener("click", async () => {
    if (!lastAnalyzeData) return;
    const res = await fetch("http://localhost:8000/download/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastAnalyzeData)
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    triggerDownload(url, "analyze_result.pdf");
  });

  // Download JSON (match)
  matchDownloadJson.addEventListener("click", () => {
    if (!lastMatchData) return;
    const blob = new Blob([JSON.stringify(lastMatchData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    triggerDownload(url, "match_result.json");
  });

  // Download PDF (match)
  matchDownloadPdf.addEventListener("click", async () => {
    if (!lastMatchData) return;
    const res = await fetch("http://localhost:8000/download/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastMatchData)
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    triggerDownload(url, "match_result.pdf");
  });

  // Trigger download
  function triggerDownload(url, filename) {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
});
