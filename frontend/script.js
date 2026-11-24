"use strict";

const bugForm = document.getElementById("bugForm");
const formMessage = document.getElementById("formMessage");
const totalReports = document.getElementById("totalReports");
const analysisResults = document.getElementById("analysisResults");
const submitButton = document.getElementById("submitButton");
const fileInput = document.getElementById("file");
const fileLabel = document.getElementById("fileLabel");
const fileDropzone = document.getElementById("fileDropzone");
const copyTraceBtn = document.getElementById("copyTraceBtn");

let reportCount = 0;

// Active sidebar link handling
document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
        document.querySelectorAll(".nav-link").forEach(el => el.classList.remove("active"));
        link.classList.add("active");
    });
});

// File upload preview feedback
if (fileInput) {
    fileInput.addEventListener("change", () => {
        const selected = fileInput.files[0];
        if (selected) {
            const sizeKB = (selected.size / 1024).toFixed(1);
            fileLabel.innerHTML = `<strong>${selected.name}</strong> (${sizeKB} KB)`;
            fileDropzone.classList.add("has-file");
        } else {
            fileLabel.innerHTML = `<strong>Click to upload</strong> or drag and drop log file`;
            fileDropzone.classList.remove("has-file");
        }
    });
}

// Copy stack trace button
if (copyTraceBtn) {
    copyTraceBtn.addEventListener("click", async () => {
        const traceText = document.getElementById("codePath").textContent;
        try {
            await navigator.clipboard.writeText(traceText);
            copyTraceBtn.textContent = "Copied!";
            setTimeout(() => {
                copyTraceBtn.textContent = "Copy";
            }, 1800);
        } catch {
            copyTraceBtn.textContent = "Failed";
            setTimeout(() => {
                copyTraceBtn.textContent = "Copy";
            }, 1800);
        }
    });
}

// Smooth scroll to form
function showSubmitForm() {
    document.getElementById("submit-section").scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
    document.getElementById("title").focus();
}

function displayValue(value) {
    if (value === null || value === undefined || value === "") {
        return "Not available";
    }
    if (typeof value === "object") {
        return JSON.stringify(value, null, 2);
    }
    return String(value);
}

function getField(object, names, fallback = null) {
    if (!object || typeof object !== "object") {
        return fallback;
    }
    for (const name of names) {
        if (object[name] !== undefined && object[name] !== null && object[name] !== "") {
            return object[name];
        }
    }
    return fallback;
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = displayValue(value);
    }
}

function setConfidence(valueId, barId, value) {
    const valueElement = document.getElementById(valueId);
    const barElement = document.getElementById(barId);
    if (!valueElement || !barElement) return;

    let score = Number(value);
    if (value === null || value === undefined || value === "" || !Number.isFinite(score)) {
        valueElement.textContent = "Not available";
        barElement.style.width = "0%";
        return;
    }

    if (score >= 0 && score <= 1) {
        score *= 100;
    }
    score = Math.max(0, Math.min(100, score));

    valueElement.textContent = `${score.toFixed(1)}%`;
    barElement.style.width = `${score}%`;
}

function updateSeverity(severity) {
    const element = document.getElementById("severity");
    const level = String(severity || "").trim().toLowerCase();

    element.textContent = displayValue(severity);
    element.className = "severity-value";

    if (["critical", "high", "medium", "low"].includes(level)) {
        element.classList.add(`severity-${level}`);
    }

    document.querySelectorAll(".severity-track span").forEach(item => {
        item.classList.toggle("selected", item.dataset.level === level);
    });
}

function updateAgentStatus(selector, successful) {
    document.querySelectorAll(selector).forEach(element => {
        element.textContent = successful ? "Completed" : "Incomplete";
        element.classList.toggle("status-complete", successful);
        element.classList.toggle("status-incomplete", !successful);
    });
}

function displayCodePath(logs) {
    const codePath = document.getElementById("codePath");
    const path = getField(logs, [
        "probable_code_path",
        "code_path",
        "stack_trace",
        "traceback",
        "call_stack"
    ]);

    if (Array.isArray(path)) {
        codePath.textContent = path.length
            ? path.map(displayValue).join("\n")
            : "No code path detected.";
    } else if (typeof path === "string" && path.trim()) {
        codePath.textContent = path;
    } else {
        codePath.textContent = "No code path detected in the submitted logs.";
    }
}

function displayAnalysis(analysis, reportId) {
    if (!analysis || typeof analysis !== "object") {
        throw new Error("The server did not return valid analysis data.");
    }

    analysisResults.style.display = "block";

    const triage = analysis.triage || {};
    const logs = analysis.log_analysis || {};

    const triageAvailable = Object.keys(triage).length > 0;
    const logsAvailable = Object.keys(logs).length > 0;

    const resolvedReportId =
        reportId ||
        analysis.report_id ||
        analysis.id ||
        "Not available";
    setText("reportId", resolvedReportId);

    // Triage Agent
    updateSeverity(getField(triage, ["severity", "bug_severity", "severity_level"]));
    setText("priority", getField(triage, ["priority", "bug_priority"]));
    setText("component", getField(triage, ["affected_component", "component", "affected_components"]));
    setText("triageReasoning", getField(triage, ["reasoning", "explanation", "classification_reasoning", "reason"]));
    setConfidence("triageConfidence", "triageConfidenceBar", getField(triage, ["confidence_score", "confidence", "confidence_percentage"]));

    // Log Analysis Agent
    setText("exceptionType", getField(logs, ["exception_type", "error_type", "exception", "exception_name"]));
    setText("errorMessage", getField(logs, ["error_message", "message", "error", "exception_message"]));
    setText("failureFile", getField(logs, ["failure_file", "file_name", "filename", "file"]));
    setText("failureMethod", getField(logs, ["failure_method", "method_name", "function_name", "function"]));
    setText("failureLine", getField(logs, ["failure_line", "line_number", "line"]));
    setText("failureClass", getField(logs, ["failure_class", "class_name", "class"]));
    setText("logReasoning", getField(logs, ["reasoning", "analysis_reasoning", "explanation", "reason"]));
    setConfidence("logConfidence", "logConfidenceBar", getField(logs, ["confidence_score", "confidence", "confidence_percentage"]));

    displayCodePath(logs);

    updateAgentStatus(".triage-card .completed", triageAvailable);
    updateAgentStatus(".log-card .completed", logsAvailable);

    const hasErrors = Array.isArray(analysis.errors) && analysis.errors.length > 0;
    const status = document.getElementById("resultsStatus");
    status.innerHTML = "";

    const dot = document.createElement("span");
    dot.className = "system-dot";

    const statusText = document.createElement("span");
    statusText.textContent = (triageAvailable && logsAvailable && !hasErrors)
        ? "Analysis complete"
        : "Partial analysis";

    status.append(dot, statusText);

    if (hasErrors) {
        formMessage.style.color = "#d97706";
        formMessage.textContent = "Report received. " + analysis.errors.join(" ");
    }

    analysisResults.scrollIntoView({ behavior: "smooth", block: "start" });
}

bugForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const file = fileInput.files[0];

    if (!title) {
        formMessage.textContent = "Please enter a bug title.";
        formMessage.style.color = "#dc2626";
        return;
    }

    if (!description && !file) {
        formMessage.textContent = "Please provide an issue description or upload a diagnostic log.";
        formMessage.style.color = "#dc2626";
        return;
    }

    if (file && file.size > 1024 * 1024) {
        formMessage.textContent = "File size must not exceed 1 MB.";
        formMessage.style.color = "#dc2626";
        return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    if (file) {
        formData.append("file", file);
    }

    submitButton.disabled = true;
    submitButton.textContent = "Analyzing...";
    formMessage.style.color = "#5b4ee6";
    formMessage.textContent = "Running Triage and Log Analysis agents...";
    analysisResults.style.display = "none";

    try {
        const response = await fetch("/submit", {
            method: "POST",
            body: formData
        });

        const rawText = await response.text();
        let result = {};
        try {
            result = rawText ? JSON.parse(rawText) : {};
        } catch {
            throw new Error(`Server returned an unexpected response (${response.status}).`);
        }

        if (!response.ok) {
            throw new Error(result.detail || `Bug submission failed (${response.status}).`);
        }

        if (!result.analysis) {
            throw new Error("The report was received, but no analysis was returned.");
        }

        reportCount++;
        totalReports.textContent = reportCount;

        const idDisplay = result.report_id || result.analysis.report_id || result.id;
        formMessage.style.color = "#0f9d6e";
        formMessage.textContent = idDisplay
            ? `Report diagnosed successfully. ID: ${idDisplay}`
            : "Report diagnosed successfully.";

        displayAnalysis(result.analysis, idDisplay);
        bugForm.reset();
        fileLabel.innerHTML = `<strong>Click to upload</strong> or drag and drop log file`;
        fileDropzone.classList.remove("has-file");

    } catch (error) {
        formMessage.style.color = "#dc2626";
        formMessage.textContent = error.message;
        console.error("Submission error:", error);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Analyze bug report →";
    }
});