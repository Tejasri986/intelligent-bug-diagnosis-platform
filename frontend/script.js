
const bugForm = document.getElementById("bugForm");
const formMessage = document.getElementById("formMessage");
const totalReports = document.getElementById("totalReports");
const analysisResults = document.getElementById("analysisResults");

// Scroll to the submission form
function showSubmitForm() {
    bugForm.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

    document.getElementById("title").focus();
}

// Safely display empty values
function displayValue(value) {
    return value !== null && value !== undefined && value !== ""
        ? value
        : "Not available";
}

// Display diagnosis results
function displayAnalysis(analysis) {
    analysisResults.style.display = "block";

    const triage = analysis.triage;
    const logs = analysis.log_analysis;

    document.getElementById("severity").textContent =
        displayValue(triage?.severity);

    document.getElementById("priority").textContent =
        displayValue(triage?.priority);

    document.getElementById("component").textContent =
        displayValue(triage?.affected_component);

    document.getElementById("triageConfidence").textContent =
        triage ? triage.confidence_score + "%" : "Not available";

    document.getElementById("triageReasoning").textContent =
        displayValue(triage?.reasoning);

    document.getElementById("exceptionType").textContent =
        displayValue(logs?.exception_type);

    document.getElementById("errorMessage").textContent =
        displayValue(logs?.error_message);

    document.getElementById("failureFile").textContent =
        displayValue(logs?.failure_file);

    document.getElementById("failureMethod").textContent =
        displayValue(logs?.failure_method);

    document.getElementById("failureLine").textContent =
        displayValue(logs?.failure_line);

    document.getElementById("logConfidence").textContent =
        logs ? logs.confidence_score + "%" : "Not available";

    document.getElementById("logReasoning").textContent =
        displayValue(logs?.reasoning);

    document.getElementById("codePath").textContent =
        logs?.probable_code_path?.length
            ? logs.probable_code_path.join("\n")
            : "No code path detected.";

    if (analysis.errors?.length) {
        formMessage.textContent +=
            " Some analysis steps could not be completed.";
    }

    analysisResults.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

// Submit bug report to FastAPI
bugForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const file = document.getElementById("file").files[0];

    const formData = new FormData();

    formData.append("title", title);
    formData.append("description", description);

    if (file) {
        formData.append("file", file);
    }

    formMessage.style.color = "#a99cff";
    formMessage.textContent = "Submitting your bug report...";

    analysisResults.style.display = "none";

    try {
        const response = await fetch("/submit", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Submission failed");
        }

        formMessage.style.color = "#35d6a0";
        formMessage.textContent =
            "Success! Your Report ID: " + result.report_id;

        totalReports.textContent =
            Number(totalReports.textContent) + 1;

        if (result.analysis) {
            displayAnalysis(result.analysis);
        }

        bugForm.reset();

    } catch (error) {
        formMessage.style.color = "#ff7373";
        formMessage.textContent = error.message;
    }
});
