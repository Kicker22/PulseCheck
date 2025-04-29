const API_BASE_URL = "http://127.0.0.1:8000";

// When the page loads, fetch the available encounters
window.onload = function() {
    fetchEncounters();
};

function fetchEncounters() {
    fetch(`${API_BASE_URL}/encounters`)
    .then(response => response.json())
    .then(data => {
        const encounterList = document.getElementById('encounter-list');

        if (!data || Object.keys(data).length === 0) {
            encounterList.innerHTML = '<p>No encounters available.</p>';
            return;
        }

        let html = '';

        Object.entries(data).forEach(([id, encounter]) => {
            // add provider role to providers
            const providerNames = encounter.providers.map(provider => `${provider.name} (${provider.role})`).join(', ');
            html += `
                <div>
                    <input type="radio" name="encounter" value="${id}" id="${id}">
                    <label for="${id}">${encounter.patient_name} - ${encounter.unit} - ${providerNames}</label>
                </div>
            `;
        });

        encounterList.innerHTML += html;
    })
    .catch(error => {
        console.error('Error fetching encounters:', error);
        document.getElementById('encounter-list').innerHTML = '<p>Error loading encounters.</p>';
    });
}

function submitFeedback() {
    const selectedEncounter = document.querySelector('input[name="encounter"]:checked');
    const feedbackText = document.getElementById('feedback-text').value.trim();

    if (!selectedEncounter) {
        alert('Please select an encounter.');
        return;
    }

    if (!feedbackText) {
        alert('Please enter your feedback.');
        return;
    }

    const feedbackData = {
        encounter_id: selectedEncounter.value,
        feedback_text: feedbackText
    };

    fetch(`${API_BASE_URL}/feedback`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to submit feedback.');
        }
        return response.json();
    })
    .then(data => {
        alert('Feedback submitted successfully!');
        // Reset form
        document.getElementById('feedback-text').value = '';
        selectedEncounter.checked = false;
        // Optionally, refresh encounters list if you want to hide completed ones
        // fetchEncounters();
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
        alert('Error submitting feedback. Please try again.');
    });
}

