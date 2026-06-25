document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const supplier = document.getElementById('supplier').value;
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');
    const statusBox = document.getElementById('status-box');
    const statusTitle = document.getElementById('status-title');
    const statusMessage = document.getElementById('status-message');
    const resultsList = document.getElementById('results-list');

    if (fileInput.files.length === 0) return;

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('supplier', supplier);
    formData.append('file', file);

    submitBtn.disabled = true;
    submitBtn.innerText = "Przetwarzanie...";
    statusBox.className = "status-loading";
    statusTitle.innerText = "Trwa import...";
    statusMessage.innerText = "Proszę czekać, dane są wysyłane do serwera.";
    resultsList.innerHTML = "";
    statusBox.style.display = "block";

    try {
        const response = await fetch('http://localhost:8000/api/import', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            statusBox.className = "status-success";
            statusTitle.innerText = "Sukces!";
            statusMessage.innerText = data.message;

            if (data.preview && data.preview.length > 0) {
                data.preview.forEach(item => {
                    const li = document.createElement('li');
                    li.innerText = item;
                    resultsList.appendChild(li);
                });
            }
        } else {
            // BŁĄD Z SERWERA (HTTP 400 / 422 / 500)
            statusBox.className = "status-error";
            statusTitle.innerText = "Błąd Importu";
            statusMessage.innerText = data.detail || data.message || "Wystąpił nieznany błąd po stronie serwera.";
        }

    } catch (error) {
        statusBox.className = "status-error";
        statusTitle.innerText = "Błąd Połączenia";
        statusMessage.innerText = "Nie można połączyć się z serwerem API. Czy Docker na pewno działa?";
        console.error(error);
    } finally {
        // Resetowanie stanu przycisku
        submitBtn.disabled = false;
        submitBtn.innerText = "Rozpocznij Import";
    }
});