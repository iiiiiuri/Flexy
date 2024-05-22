import { alert_flexy } from '../components/alert.js';
import { confirm_flexy } from '../components/confirm.js';

function tratarCliqueAdicionarAoCarrinho(evento) {
    const urlProduto = evento.currentTarget.dataset.url;
    buscarDadosProduto(urlProduto)
        .then(dadosProduto => atualizarResumoCarrinho(dadosProduto, 'adicionar'));
        const total = calcularTotal();
        document.getElementById('total').textContent = `R$ ${total.toFixed(2)}`;
}

function tratarCliqueRemoverDoCarrinho(evento) {
    const codigoProduto = evento.currentTarget.dataset.cod;
    const resumoCarrinho = document.getElementById('resumo-compra');
    let itemListaProduto = Array.from(resumoCarrinho.children).find(li => li.dataset.cod === codigoProduto);
    if (itemListaProduto) {
        atualizarQuantidadeProduto(itemListaProduto, 'remover');
    }
    const total = calcularTotal();
    document.getElementById('total').textContent = `R$ ${total.toFixed(2)}`;
}
function buscarDadosProduto(url) {
    return fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(resposta => resposta.json());
}

function atualizarResumoCarrinho(dadosProduto, acao) {
    const resumoCarrinho = document.getElementById('resumo-compra');
    let itemListaProduto = Array.from(resumoCarrinho.children).find(li => li.dataset.cod === dadosProduto.compra.codigo.toString());
    
    if (!itemListaProduto && acao === 'adicionar') {
        // Verificar se há estoque disponível
        if (dadosProduto.compra.estoque <= 0) {
            alert_flexy("Produto fora de estoque.", true);
            return;
        }

        itemListaProduto = document.createElement('li');
        itemListaProduto.dataset.cod = dadosProduto.compra.codigo.toString();
        itemListaProduto.dataset.nome = dadosProduto.compra.nome;
        itemListaProduto.dataset.preco = dadosProduto.compra.preco;
        itemListaProduto.dataset.quantity = 1;
        itemListaProduto.textContent = `${dadosProduto.compra.codigo} - ${dadosProduto.compra.nome} - R$${dadosProduto.compra.preco} - (1x)`;
        resumoCarrinho.appendChild(itemListaProduto);
    } else if (itemListaProduto && acao === 'adicionar') {
        // Verificar se há estoque disponível
        if (dadosProduto.compra.estoque <= itemListaProduto.dataset.quantity) {
            alert_flexy("Produto fora de estoque.", true);
            return;
        }

        itemListaProduto.dataset.quantity = parseInt(itemListaProduto.dataset.quantity) + 1;
        itemListaProduto.textContent = `${dadosProduto.compra.codigo} - ${dadosProduto.compra.nome} - R$${dadosProduto.compra.preco} - (${itemListaProduto.dataset.quantity}x)`;
    } else if (itemListaProduto && acao === 'remover') {
        itemListaProduto.dataset.quantity = parseInt(itemListaProduto.dataset.quantity) - 1;
        if (itemListaProduto.dataset.quantity === 0) {
            resumoCarrinho.removeChild(itemListaProduto);
        } else {
            itemListaProduto.textContent = `${dadosProduto.compra.codigo} - ${dadosProduto.compra.nome} - R$${dadosProduto.compra.preco} - (${itemListaProduto.dataset.quantity}x)`;
        }
    }

    const total = calcularTotal();
    document.getElementById('total').textContent = `R$ ${total.toFixed(2)}`;
}


function atualizarQuantidadeProduto(itemListaProduto, acao) {
    let quantidade = parseInt(itemListaProduto.dataset.quantity);
    quantidade = acao === 'adicionar' ? quantidade + 1 : quantidade - 1;

    if (quantidade > 0) {
        itemListaProduto.dataset.quantity = quantidade;
        itemListaProduto.textContent = `${itemListaProduto.dataset.cod} - ${itemListaProduto.dataset.nome} - R$${itemListaProduto.dataset.preco} - (${quantidade}x)`;
    } else {
        itemListaProduto.parentElement.removeChild(itemListaProduto);
    }
}

function adicionarProdutoAoResumoCarrinho(dadosProduto, resumoCarrinho) {
    let itemListaProduto = document.createElement('li');
    itemListaProduto.dataset.quantity = 1;
    itemListaProduto.dataset.cod = dadosProduto.compra.codigo;
    itemListaProduto.dataset.nome = dadosProduto.compra.nome;
    itemListaProduto.dataset.preco = dadosProduto.compra.preco;
    itemListaProduto.textContent = `${dadosProduto.compra.codigo} - ${dadosProduto.compra.nome} - R$${dadosProduto.compra.preco} - (1x)`;
    resumoCarrinho.appendChild(itemListaProduto);
}


function calcularTotal() {
    const resumoCarrinho = document.getElementById('resumo-compra');
    let total = 0;
    Array.from(resumoCarrinho.children).forEach(item => {
        const preco = parseFloat(item.dataset.preco);
        const quantidade = parseInt(item.dataset.quantity);
        total += preco * quantidade;
    });
    return total;
}

document.querySelectorAll('.add-to-cart').forEach(botao => {
    const total = calcularTotal();
    
});

document.querySelectorAll('.add-to-cart').forEach(botao => {
    botao.addEventListener('click', tratarCliqueAdicionarAoCarrinho);
});

document.querySelectorAll('.remove-from-cart').forEach(botao => {
    botao.addEventListener('click', tratarCliqueRemoverDoCarrinho);
});