const API_BASE_URL = "http://localhost:8000/api/import";

const uploadForm = document.getElementById("uploadForm");
const supplierSelect = document.getElementById("supplier");
const fileInput = document.getElementById("fileInput");
const submitBtn = document.getElementById("submitBtn");

const statusBox = document.getElementById("status-box");
const statusTitle = document.getElementById("status-title");
const statusMessage = document.getElementById("status-message");
const resultsList = document.getElementById("results-list");

const previewSection = document.getElementById("preview-section");
const previewCount = document.getElementById("preview-count");
const previewTableHead = document.getElementById("preview-table-head");
const previewTableBody = document.getElementById("preview-table-body");

const showCurrentBtn = document.getElementById("showCurrentBtn");

uploadForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const supplier = supplierSelect.value;
    const file = fileInput.files[0];

    if (!supplier) {
        showStatus("error", "Błąd", "Wybierz profil dostawcy.");
        return;
    }

    if (!file) {
        showStatus("error", "Błąd", "Wybierz plik do importu.");
        return;
    }

    clearPreviewTable();
    showStatus("loading", "Trwa wczytywanie", "Plik jest wysyłany i przetwarzany...");
    submitBtn.disabled = true;
    submitBtn.textContent = "Przetwarzanie...";

    try {
        const formData = new FormData();
        formData.append("supplier", supplier);
        formData.append("file", file);

        const uploadResponse = await fetch(`${API_BASE_URL}/preview`, {
            method: "POST",
            body: formData
        });

        const uploadResult = await uploadResponse.json();

        if (!uploadResponse.ok) {
            throw new Error(uploadResult.detail || "Nie udało się wczytać pliku.");
        }

        const importId = uploadResult.import_id;

        if (!importId) {
            throw new Error("Backend nie zwrócił import_id.");
        }

        showStatus(
            "success",
            "Podgląd przygotowany",
            `Import ID: ${importId}. Zapisano: ${uploadResult.saved_count}, pominięto: ${uploadResult.skipped_count}.`
        );

        renderResultList(uploadResult.preview);

        const previewResponse = await fetch(`${API_BASE_URL}/preview/${importId}`);
        const previewResult = await previewResponse.json();

        if (!previewResponse.ok) {
            throw new Error(previewResult.detail || "Nie udało się pobrać danych podglądu.");
        }

        renderPreviewTable(previewResult.rows || []);
    } catch (error) {
        showStatus("error", "Błąd", error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Wczytaj podgląd importu";
    }
});

function showStatus(type, title, message) {
    statusBox.style.display = "block";
    statusBox.className = "";

    if (type === "success") {
        statusBox.classList.add("status-success");
    }

    if (type === "error") {
        statusBox.classList.add("status-error");
    }

    if (type === "loading") {
        statusBox.classList.add("status-loading");
    }

    statusTitle.textContent = title;
    statusMessage.textContent = message;
}

function renderResultList(items) {
    resultsList.innerHTML = "";

    if (!items || items.length === 0) {
        return;
    }

    items.forEach(function (item) {
        const li = document.createElement("li");
        li.textContent = item;
        resultsList.appendChild(li);
    });
}

function renderPreviewTable(rows) {
    clearPreviewTable();

    if (!rows || rows.length === 0) {
        previewSection.style.display = "none";
        showStatus("error", "Brak danych", "Import nie zwrócił żadnych rekordów do wyświetlenia.");
        return;
    }

    previewSection.style.display = "block";
    previewCount.textContent = `Liczba rekordów: ${rows.length}`;

    const columns = [
        "id",
        "supplier_id",
        "product_key",
        "solid_index",
        "collection",
        "color",
        "marking_fronts",
        "solid_type",
        "front_color",
        "weight",
        "width_block",
        "height_block",
        "depth_block",
        "number_doors",
        "number_drawers",
        "handle_material",
        "drawer_type",
        "hinge_type",
        "description_block",
        "number_packages",
        "bed_frame_material",
        "shelf_material",
        "equipment_product",
        "status",
        "created_at",
        "updated_at"
    ];

    const headerRow = document.createElement("tr");

    columns.forEach(function (column) {
        const th = document.createElement("th");
        th.textContent = column;
        headerRow.appendChild(th);
    });

    previewTableHead.appendChild(headerRow);

    rows.forEach(function (row) {
        const tr = document.createElement("tr");

        columns.forEach(function (column) {
            const td = document.createElement("td");
            const value = row[column];

            td.textContent = formatCellValue(value);
            tr.appendChild(td);
        });

        previewTableBody.appendChild(tr);
    });
}

function clearPreviewTable() {
    previewTableHead.innerHTML = "";
    previewTableBody.innerHTML = "";
    previewCount.textContent = "";
    previewSection.style.display = "none";
}

function formatCellValue(value) {
    if (value === null || value === undefined || value === "") {
        return "-";
    }

    return value;
}


showCurrentBtn.addEventListener("click", async function () {
    clearPreviewTable();

    showStatus("loading", "Pobieranie danych", "Pobieram aktualne dane z tabeli tymczasowej...");

    showCurrentBtn.disabled = true;
    showCurrentBtn.textContent = "Pobieranie...";

    try {
        const response = await fetch(`${API_BASE_URL}/current`);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Nie udało się pobrać aktualnych danych.");
        }

        if (!result.rows || result.rows.length === 0) {
            showStatus("error", "Brak danych", "Tabela tymczasowa jest pusta.");
            return;
        }

        showStatus(
            "success",
            "Dane pobrane",
            `Pobrano aktualne dane z tabeli tymczasowej. Liczba rekordów: ${result.count}.`
        );

        renderPreviewTable(result.rows);

    } catch (error) {
        showStatus("error", "Błąd", error.message);
    } finally {
        showCurrentBtn.disabled = false;
        showCurrentBtn.textContent = "Pokaż aktualne dane";
    }
});