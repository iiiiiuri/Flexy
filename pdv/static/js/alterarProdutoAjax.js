$(document).ready(function() {
    $('.edit-item').click(function() {
        var id = $(this).data('id');
        var url = 'itemSelecionado/' + id;

        // Buscar os dados do produto
        $.get(url, function(data) {
            // Preencher os campos de input com os dados do produto
            $('#id').val(data.produtoSelecionado.id);
            $('#codigo').val(data.produtoSelecionado.codigo);
            $('#nome').val(data.produtoSelecionado.nome);
            $('#cor').val(data.produtoSelecionado.cor);
            $('#categoria').val(data.produtoSelecionado.categoria);
            $('#subcategoria').val(data.produtoSelecionado.subcategoria);
            $('#preco').val(data.produtoSelecionado.preco);
            $('#tamanho').val(data.produtoSelecionado.tamanho);
            $('#estoque').val(data.produtoSelecionado.estoque);
            $('#editForm').attr('action', 'editar/' + data.produtoSelecionado.id);
        });
    });
});