const form = document.getElementById("paperForm");
const generateBtn = document.getElementById("generateBtn");
const pdfInput = document.getElementById("pdf_file");
const fileName = document.getElementById("fileName");

if (pdfInput) {
    pdfInput.addEventListener("change", function () {
        const file = this.files[0];
        if (!file) {
            fileName.textContent = "No file selected";
            return;
        }
        if (!file.name.toLowerCase().endsWith(".pdf")) {
            alert("Please select a PDF file.");
            this.value = "";
            fileName.textContent = "No file selected";
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            alert("PDF size must be 10 MB or less.");
            this.value = "";
            fileName.textContent = "No file selected";
            return;
        }
        fileName.textContent = "Selected: " + file.name;
    });
}

if (form && generateBtn) {
    form.addEventListener("submit", function (event) {
        if (!form.reportValidity()) {
            event.preventDefault();
            return;
        }
        generateBtn.disabled = true;
        generateBtn.textContent = "⏳ Generating your paper...";
    });
}
