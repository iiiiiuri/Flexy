// Obtém o input e a tabela
const input = document.getElementById('searchInput');
const table = document.getElementById('table');

// Adiciona um evento de input ao input
input.addEventListener('input', function() {
    const searchText = input.value.toLowerCase();

    // Itera sobre as linhas da tabela
    Array.from(table.rows).forEach(function(row) {
        // Verifica se a linha é um cabeçalho da tabela
        if (row.querySelector('th')) {
            return;
        }

        const rowData = row.textContent.toLowerCase();

        // Exibe ou oculta a linha com base no texto digitado
        if (rowData.includes(searchText)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});