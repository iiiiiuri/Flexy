function alert_flexy(text, isError) {
    const alertElement = document.createElement("div");
    alertElement.id = "alert-additional-content-2";
    alertElement.className = "fixed inset-0 flex items-center justify-center z-50";

    const overlay = document.createElement("div");
    overlay.className = "absolute inset-0 bg-black bg-opacity-50";
    alertElement.appendChild(overlay);

    const alertContent = document.createElement("div");
    alertContent.className = isError ? "animate-blink shadow-lg p-4 mb-4 text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800 relative z-10" : "animate-blink p-4 mb-4 text-green-800 border border-green-300 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800 relative z-10";
    alertContent.setAttribute("role", "alert");

    const okButtonClass = isError ? "mt-4 px-4 py-2 text-white bg-red-500 rounded hover:bg-red-700" : "mt-4 px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-700";

    const innerContent = `
        <div class="flex items-center">
            <svg class="flex-shrink-0 w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <span class="sr-only">Info</span>
            <h3 class="text-lg font-medium">${text}</h3>
        </div>
        <div class="flex justify-center">
        <button id="alert-ok-button" class="${okButtonClass}">OK</button>
        </div>
    `;

    alertContent.innerHTML = innerContent;
    alertElement.appendChild(alertContent);

    document.body.appendChild(alertElement);

    // Adicione um ouvinte de evento ao botão OK para remover o alerta quando clicado
    document.getElementById("alert-ok-button").addEventListener("click", function() {
        document.body.removeChild(alertElement);
    });
}

export { alert_flexy };