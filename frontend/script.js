
const bugForm = document.getElementById("bugForm");
const formMessage = document.getElementById("formMessage");
const totalReports = document.getElementById("totalReports");

// Scroll to the submission form
function showSubmitForm() {
    bugForm.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

    document.getElementById("title").focus();
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

        bugForm.reset();

    } catch (error) {
        formMessage.style.color = "#ff7373";
        formMessage.textContent = error.message;
    }
});
