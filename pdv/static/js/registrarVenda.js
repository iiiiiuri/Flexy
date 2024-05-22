import { alert_flexy } from '../components/alert.js';
import { confirm_flexy } from '../components/confirm.js';

window.confirm_flexy = confirm_flexy;

function exibirFinalizarCompraUm() {
    document.getElementById("finalizarCompraUm").classList.remove('hidden');
}



function exibirSelecaoVendedor(){
    document.getElementById("selecaoVendedor").classList.remove('hidden');
    document.getElementById("finalizarCompraUm").classList.add('hidden');

}


//PRIMEIRO PASSO PARA FINALIZAR UMA VENDA, ADICIONAR ITENS AO RESUMO DE COMPRA
var botaoFinalizar = document.getElementById("finalizar-button");
botaoFinalizar.addEventListener("click", function() {
    var listaElements = document.querySelectorAll("#resumo-compra li");

    console.log(document.getElementById('total'));

    document.getElementById('valorTotal').value = document.getElementById('total').textContent;

    if(listaElements.length > 0){
        exibirFinalizarCompraUm();
    } else {
        alert_flexy("Adicione pelo menos um item ao resumo de compra antes de finalizar.", true);
    }
    
});

 
//SEGUNDO PASSO PARA FINALIZAR UMA VENDA, ADICIONAR PAGAMENTOS
var selectedPaymentMethod = null;
var troco = 0;

var botaoAdicionarPagamento = document.getElementById("adicionar-pagamento");
let codigosUsados = [];
botaoAdicionarPagamento.addEventListener("click", function() {
    var metodoPagamento = document.querySelector('#metodoPagamento').value;
    var valorApagarInput = document.querySelector('#valorApagar');
    var valorApagar = parseFloat(valorApagarInput.value);

if (metodoPagamento == "COD") {
    let codigoDesconto = document.getElementById('valorApagar').value;

    fetch('codVerify/' + codigoDesconto, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ codigo: codigoDesconto }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('codDesconto').value = codigoDesconto;
        console.log(codigosUsados);
        if (data.existe == true) {
            if (codigosUsados.includes(codigoDesconto)) {
                alert_flexy('Este código de desconto já foi usado.', true);
                return;
            } else {
                codigosUsados.push(codigoDesconto); // Adiciona o código à lista
            }


            let valorTotal = parseFloat(document.querySelector('#valorTotal').value.replace('R$', ''));
            let valorDesconto = data.valor_desconto;
            let novoValorTotal = valorTotal - valorDesconto;

            if (novoValorTotal < 0) {
                // O valor do desconto é maior que o valor total, então a diferença é o extorno
                let extorno = -novoValorTotal;
                novoValorTotal = 0;
                document.querySelector('#extornoCodigo').value = extorno.toFixed(2);
            }

            // Adicione o método de pagamento ao resumo de pagamento
            let resumoPagamento = document.getElementById('resumo-pagamento');
            let novoItem = document.createElement('li');
            novoItem.textContent = metodoPagamento + ' - ' + valorDesconto.toFixed(2);
            resumoPagamento.appendChild(novoItem);

            // Atualize o valor total
            document.querySelector('#valorTotal').value = 'R$ ' + novoValorTotal.toFixed(2);

            // Atualize a confirmação de pagamento
            atualizaConfirmacaoPagamento(novoValorTotal);
        } else {
            alert_flexy('Código de desconto inválido.', true);
            return;
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
    });
}
    

    // Verificar se o valor a pagar é um número
    if (isNaN(valorApagar)) {
        alert_flexy('Por favor, insira um número válido para o valor a pagar.', true);
        return;
    }

    // Verificar se o valor a pagar está vazio
    if (valorApagarInput.value.trim() === '') {
        alert_flexy('O valor a pagar não pode estar vazio.', true);
        return;
    }

    var valorTotal = parseFloat(document.querySelector('#valorTotal').value.replace('R$', ''));

    if (valorTotal === 0 && metodoPagamento === "DINHEIRO") {
        alert_flexy('Não é possível adicionar pagamento em dinheiro se o valor total da venda for zero.', true);
        return;
    }

    if(metodoPagamento != "COD"){
    if (valorApagar > valorTotal) {
        if (metodoPagamento == "DINHEIRO") {
            troco = (valorApagar - valorTotal).toFixed(2);
            valorApagar = valorTotal;
            document.querySelector('#troco').value = troco;
        } else {
            alert_flexy('O valor a pagar não pode ser maior que o valor total da venda.', true);
            return;
        }
    }
}

    var novoValorTotal = valorTotal - valorApagar;


    if (metodoPagamento != "COD") {
        document.querySelector('#valorTotal').value = 'R$ ' + novoValorTotal.toFixed(2);

        var novoItem = document.createElement('li');
        novoItem.textContent = metodoPagamento + ' - ' + valorApagar.toFixed(2);
    
        document.querySelector('#resumo-pagamento').appendChild(novoItem);
    
        atualizaConfirmacaoPagamento(novoValorTotal);
    }
});

function atualizaConfirmacaoPagamento(novoValorTotal){
    var botaoConfirmarPagamentos = document.getElementById('botaoConfirmarPagamentos');

    if (novoValorTotal <= 0) {
        botaoConfirmarPagamentos.disabled = false;
    } else {
        botaoConfirmarPagamentos.disabled = true;
    }
}

//EXIBE A TELA DE SELEÇÃO DE VENDEDOR
botaoConfirmarPagamentos.addEventListener("click", function(event) {
    if (!botaoConfirmarPagamentos.disabled) {
        exibirSelecaoVendedor();
    }
});

closeButton.addEventListener('click', function() {
document.getElementById('valorTotal').value = ' ';
document.getElementById('troco').value = ' ';
document.getElementById('codDesconto').value = ' ';
document.getElementById('extornoCodigo').value = ' ';
document.getElementById('valorApagar').value = ' ';
document.getElementById('resumo-pagamento').innerHTML = ' ';
});

function printReceipt(vendedor, valor_pix, valor_dinheiro, valor_cartao,valor_desconto, troco, itens, endereco, valor_extorno) {
    // Obtenha as informações que você precisa
    var horaVenda = new Date().toLocaleTimeString();
    var totalCompra = (valor_pix + valor_dinheiro + valor_cartao + valor_desconto).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    var dataCompra = new Date();
    var dataLimite = new Date();
    dataLimite.setDate(dataCompra.getDate() + 3);

    // Crie um novo iframe
    var iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);

    // Preencha o iframe com as informações
    iframe.contentDocument.write('<html><head><title>Recibo</title>');
    iframe.contentDocument.write('<style>');
    iframe.contentDocument.write('body { padding: 20px;  }');
    iframe.contentDocument.write('img { width: 600px; height: auto; margin-bottom: 20px; margin-left: auto; margin-right: auto; display: block; }');
    iframe.contentDocument.write('hr { margin-bottom: 10px; height: 20px; border: none; border-top: 10px solid #000; }');
    iframe.contentDocument.write('.total { font-size: 80px; margin-bottom: 20px; font-weight: bold;}');
    iframe.contentDocument.write('.infoVenda { font-size: 50px; margin-bottom: 5px; text-align: center;}');
    iframe.contentDocument.write('.subtotal { font-size: 40px; margin-bottom: 5px;}');
    iframe.contentDocument.write('th, td { font-size: 50px; }');
    iframe.contentDocument.write('table { width: 100%; margin-bottom: 20px; }');
    iframe.contentDocument.write('th, td { padding: 20px; }');
    iframe.contentDocument.write('</style>');
    iframe.contentDocument.write('</head><body>');
    iframe.contentDocument.write('<img src="/static/img/printLogo.svg" alt="Logo">');
    iframe.contentDocument.write('<p class="infoVenda">Venda realizada em '+ endereco +' , pelo vendedor ' + vendedor + ', as ' + horaVenda + ' do dia ' + new Date().toLocaleDateString() + '</p>');    
    iframe.contentDocument.write('<hr>');

    // Crie a tabela
    iframe.contentDocument.write('<table>');
    iframe.contentDocument.write('<thead><tr><th>COD</th><th>DESC</th><th>QTD</th><th>VALOR</th></tr></thead>');
    iframe.contentDocument.write('<tbody>');
    itens.forEach(function(item) {
        iframe.contentDocument.write('<tr><td>' + item.cod + '</td><td>' + item.produto + '</td><td>' + item.quantidade + '</td><td>' + parseFloat(item.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</td></tr>');
    });
    iframe.contentDocument.write('</tbody></table>');
    iframe.contentDocument.write('<hr>');

    // Total da compra
    iframe.contentDocument.write('<p class="total">TOTAL: ' + totalCompra + '</p>');

    
    if(valor_pix > 0){
        iframe.contentDocument.write('<p class="subtotal">PIX: ' + parseFloat(valor_pix).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</p>');
    }
    if(valor_cartao > 0){
        iframe.contentDocument.write('<p class="subtotal">CARTÃO: ' + parseFloat(valor_cartao).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</p>');
    }
    if(valor_dinheiro > 0){
        iframe.contentDocument.write('<p class="subtotal">DINHEIRO: ' + parseFloat(valor_dinheiro).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</p>');
    }
    if(valor_desconto > 0){
        iframe.contentDocument.write('<p class="subtotal">DESCONTO: ' + parseFloat(valor_desconto).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</p>');
    }
    if(troco > 0){
        iframe.contentDocument.write('<p class="subtotal">TROCO: ' + parseFloat(troco).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</p>');
    }
    if(valor_extorno > 0){
        iframe.contentDocument.write('<p class="subtotal">RESTANTE DE CRÉDITO: ' + parseFloat(valor_extorno).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) + '</p>');
    }
        iframe.contentDocument.write('<hr>');
    // Vendedor
    iframe.contentDocument.write('<p class="infoVenda">**Obs: Qualquer peça nesse cupom tem o limite de troca de no máximo 3 dias</p>');
    iframe.contentDocument.write('<p class="infoVenda">Data Limite para Troca: ' + dataLimite.toLocaleDateString() + '</p>');
    iframe.contentDocument.write('</body></html>');
    iframe.contentDocument.close();

    // Chame a função de impressão
    iframe.contentWindow.print();

    // Remova o iframe após a impressão
    iframe.contentWindow.onafterprint = function() {
        document.body.removeChild(iframe);
    }
}


// Adicionar um ouvinte de evento a cada botão de vendedor
document.querySelectorAll('[data-seller]').forEach(function(button) {
    // Adiciona um ouvinte de evento de clique a cada botão
    button.addEventListener('click', function() {
        // Obter o nome do vendedor do atributo 'data-seller' do botão
        var vendedor = button.getAttribute('data-seller');
        var endereco ;
        // Inicializar os valores de pagamento
        var valor_pix = 0;
        var valor_dinheiro = 0;
        var valor_cartao = 0;
        var valor_desconto = 0;

        // Iterar sobre os itens de resumo de pagamento
        Array.from(document.querySelectorAll('#resumo-pagamento li')).forEach(function(li) {
            // Separar o método de pagamento e o valor
            var [metodo, valor] = li.textContent.split(' - ');
            valor = parseFloat(valor);

            // Adicionar o valor ao método de pagamento correspondente
            switch (metodo.toUpperCase()) {
                case 'PIX':
                    valor_pix += valor;
                    break;
                case 'DINHEIRO':
                    valor_dinheiro += valor;
                    break;
                case 'CARTAO':
                    valor_cartao += valor;
                    break;
                case 'COD':
                    valor_desconto += valor;
                    break;
            }
        });

        // Obter o valor do troco
        var troco = parseFloat(document.querySelector('#troco').value);

        // Obter os itens da venda
        var itens = Array.from(document.querySelectorAll('#resumo-compra li')).map(function(li) {
            // Separar o código, o nome do produto, o valor e a quantidade
            var [cod, produto, valor, quantidade] = li.textContent.split(' - ');
            // Remover o 'R$' do valor e o '(x)' da quantidade
            valor = parseFloat(valor.replace('R$', '').trim());
            quantidade = parseInt(quantidade.match(/\d+/)[0]);
            return { cod, produto, valor, quantidade };
        });

        // Obter os descontos
        let descontos = {
            valor_desconto: valor_desconto,
            cod_desconto: document.getElementById('codDesconto').value,
            valor_extorno : document.getElementById('extornoCodigo').value
        }

        // Fazer uma solicitação POST para registrar a venda
        fetch('registrar_venda', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ vendedor, valor_pix, valor_dinheiro, valor_cartao, descontos, troco, itens }),
        })
        .then(response => response.json())
        .then(data => {
            // Fazer uma solicitação GET para obter os dados da empresa
            return fetch('dadosEmpresa/' + document.getElementById('usuario').textContent, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                var endereco = data['endereco'];

                // Ocultar a div 'selecaoVendedor'
                document.getElementById('selecaoVendedor').style.display = 'none';
                // Mostrar a div 'sucessoRegistro'
                document.getElementById('sucessoRegistro').style.display = 'block';
                // Imprimir o recibo
                printReceipt(vendedor, valor_pix, valor_dinheiro, valor_cartao,valor_desconto, troco, itens, endereco, descontos.valor_extorno);
                
                // Recarregar a página após um intervalo de tempo
                setTimeout(function() {
                    location.reload();
                }, 1000);
            } else {
                throw new Error('No data returned from server');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});