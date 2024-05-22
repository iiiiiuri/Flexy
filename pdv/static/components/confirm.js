function confirm_flexy(text, isError, callback) {
    const confirmElement = document.createElement("div");
    confirmElement.id = "confirm-additional-content-2";
    confirmElement.className = "fixed inset-0 flex items-center justify-center z-50";

    const overlay = document.createElement("div");
    overlay.className = "absolute inset-0 bg-black bg-opacity-50";
    confirmElement.appendChild(overlay);

    const confirmContent = document.createElement("div");
    confirmContent.className = isError ? "animate-blink shadow-lg p-4 mb-4 text-yellow-800 border border-yellow-300 rounded-lg bg-yellow-50 dark:bg-gray-800 dark:text-yellow-400 dark:border-yellow-800 relative z-10" : "animate-blink p-4 mb-4 text-green-800 border border-green-300 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800 relative z-10";
    confirmContent.setAttribute("role", "alert");

    const okButtonClass = isError ? "mt-4 px-4 py-2 text-white bg-green-500 rounded hover:bg-green-700" : "mt-4 px-4 py-2 text-white bg-blue-500 rounded hover:bg-green-700";

    const innerContent = `
        <div class="flex items-center">
            <svg class="flex-shrink-0 w-4 h-4 me-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <span class="sr-only">Info</span>
            <h3 class="text-lg font-medium">${text}</h3>
        </div>
        <div class="flex justify-center space-x-2">
        <button id="confirm-ok-button" class="${okButtonClass}">OK</button>
        <button id="confirm-cancel-button" class="mt-4 px-4 py-2 text-white bg-red-500 rounded hover:bg-red-700">Cancel</button>
        </div>
    `;

    confirmContent.innerHTML = innerContent;
    confirmElement.appendChild(confirmContent);

    document.body.appendChild(confirmElement);

    // Add event listeners to the OK and Cancel buttons
    document.getElementById("confirm-ok-button").addEventListener("click", function() {
        document.body.removeChild(confirmElement);
        callback(true);
    });

    document.getElementById("confirm-cancel-button").addEventListener("click", function() {
        document.body.removeChild(confirmElement);
        callback(false);
    });
}

export { confirm_flexy };