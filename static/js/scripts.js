document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById("fileInput");
    formData.append("file", fileInput.files[0]);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<div class='text-center'>Procesando...</div>";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Error en la predicción.");
        }

        const data = await response.json();

        // Mostrar resultados con diseño mejorado
        resultDiv.innerHTML = `
            <h3 class="text-center mt-4">Resultado:</h3>
            <div class="alert alert-success text-center">
                <strong>Clase Predicha:</strong> ${data.predicted_class} <br>
                <strong>Confianza:</strong> ${data.confidence}
            </div>
            <h4 class="mt-4">Recomendaciones:</h4>
            <ul class="list-group">
                ${data.specific_recommendations.map(r => `<li class="list-group-item">${r}</li>`).join("")}
            </ul>
        `;
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="alert alert-danger text-center">
                Error: ${error.message}
            </div>
        `;
    }
});