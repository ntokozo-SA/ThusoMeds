document.getElementById('triageForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('name').value,
        age: document.getElementById('age').value,
        symptoms: document.getElementById('symptoms').value
    };

    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('/triage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        document.getElementById('loading').style.display = 'none';
        document.getElementById('ticketNumber').textContent = result.ticketNumber;
        document.getElementById('severityLevel').textContent = result.severityLevel;

    } catch (err) {
        console.error(err);
        document.getElementById('loading').style.display = 'none';
        alert('Error submitting the form!');
    }
});
