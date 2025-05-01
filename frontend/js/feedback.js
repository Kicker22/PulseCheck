// Get token from URL
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get("token");

const encounterSection = document.getElementById("encounter-details");
const submitBtn = document.getElementById("submit-feedback");
const feedbackText = document.getElementById("feedback-text");

// Store token-decoded encounter ID
let encounterId = null;

if (!token) {
    encounterSection.innerHTML = "<p>Missing feedback token.</p>";
    submitBtn.disabled = true;
} else {
    fetch(`/validateToken?token=${token}`)
        .then(response => {
            if (!response.ok) throw new Error("Invalid or expired token");
            return response.json();
        })
        .then(data => {
            encounterId = data.encounter_id;
            encounterSection.innerHTML = `
                <p>We found your visit (ID: ${encounterId}). Please provide your feedback below.</p>
            `;
            submitBtn.disabled = false;
        })
        .catch(error => {
            console.error("Token validation failed:", error);
            encounterSection.innerHTML = "<p>Invalid or expired feedback link.</p>";
            submitBtn.disabled = true;
        });
}

// Feedback submit handler
submitBtn.addEventListener("click", () => {
    const text = feedbackText.value.trim();

    if (!text) {
        alert("Please enter feedback before submitting.");
        return;
    }

    fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            encounter_id: encounterId,
            feedback_text: text
        })
    })
        .then(response => {
            if (!response.ok) throw new Error("Submission failed");
            return response.json();
        })
        .then(data => {
            alert("Thank you for your feedback!");
            feedbackText.value = "";
            submitBtn.disabled = true;
        })
        .catch(error => {
            console.error("Error submitting feedback:", error);
            alert("An error occurred while submitting your feedback. Please try again.");
        });
});
