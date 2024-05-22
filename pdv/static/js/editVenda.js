import { alert_flexy } from '../components/alert.js';
import { confirm_flexy } from '../components/confirm.js';

window.confirm_flexy = confirm_flexy;
let selectedProduto = null; // Defina selectedProduto no escopo do documento

$(document).ready(function() {
    // Função auxiliar para formatar o valor como dinheiro
    function formatarDinheiro(valor) {
        return 'R$ ' + valor.toFixed(2).replace('.', ',').replace(/(\d)(?=(\d{3})+\,)/g, '$1.');
    }

    // Função para lidar com o evento change no selectProdutoVenda
    function handleSelectProdutoVendaChange(data) {
        var selectedProdutoCodigo = $(this).val();
        selectedProduto = data.venda_selecionada.produtos.find(function(produto) {
            return produto.codigo == selectedProdutoCodigo;
        });

        if (selectedProduto) {
            $('#qtdProdutosNaVenda').val('');
            $('#qtdProdutosNaVenda').val(selectedProduto.quantidade).attr({
                'max': selectedProduto.quantidade,
                'min': 1
            });

            var valorTotal = selectedProduto.valor_unitario * $('#qtdProdutosNaVenda').val();
            if (valorTotal < 0) {
                valorTotal = 0; // Defina o valor total para zero
            }
            $('#valorQtdSelecionada').val(formatarDinheiro(valorTotal));

            var produtosDisponiveis = data.produtos_disponiveis.filter(function(produto) {
                return produto.valor_unitario >= selectedProduto.valor_unitario;
            });
            $('#selectProdutoDesejado').empty();
            $.each(produtosDisponiveis, function(index, produto) {
                $('#selectProdutoDesejado').append(new Option(produto.nome, produto.codigo));
            });
        }

        $('#devolucao').removeClass('hidden');
        document.getElementById('overlay').classList.remove('hidden');
    }

    // Função para lidar com o evento input em qtdProdutosNaVenda
    function handleQtdProdutosNaVendaInput(data) {
        var max = parseInt($(this).attr('max'));
        var min = parseInt($(this).attr('min'));
        var value = parseInt($(this).val());

        if (value > max) {
            $(this).val(max);
        } else if (value < min) {
            $(this).val(min);
        }

        if (selectedProduto) {
            var valorTotal = selectedProduto.valor_unitario * value;
            if (valorTotal < 0) {
                valorTotal = 0; // Defina o valor total para zero
            }
            $('#valorQtdSelecionada').val(formatarDinheiro(valorTotal));
        }
    }

    // Função para lidar com o evento de clique no botão de fechamento
    function handleCloseButtonClick() {
        $('#devolucao').addClass('hidden');
        document.getElementById('overlay').classList.add('hidden');
    }

    // Função para lidar com o evento de clique no botão de edição da venda
    function handleEditVendaClick() {
        var id = $(this).data('id');
        var url = 'dadosVenda/' + id;

        $.get(url, function(data) {
            if (data.error) {
                alert_flexy(data.error, true);
                return;
            }

            $('#idVenda').text(data.venda_selecionada.venda);
            $('#selectProdutoVenda').empty();

            $.each(data.venda_selecionada.produtos, function(index, produto) {
                if (produto.quantidade > 0) {
                    $('#selectProdutoVenda').append(new Option(produto.nome, produto.codigo));
                }
            });

            $('#selectProdutoVenda').change(function() {
                handleSelectProdutoVendaChange.call(this, data);
            }).change();

            $('#qtdProdutosNaVenda').on('input', function() {
                handleQtdProdutosNaVendaInput.call(this, data);
            });

        });

        $('#closeButtonDevolucao').click(handleCloseButtonClick);
    }

    // Adiciona um evento de clique ao botão de edição da venda
    $('.edit-venda').click(handleEditVendaClick);

    // Função para gerar um código de desconto aleatório
    function gerarCodigoDesconto() {
        return Math.floor(Math.random() * 10000);
    }

    // Função para imprimir o código de desconto
    function printCode(nome, cnpj, endereco, codigo, valor) {
        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);

        var doc = iframe.contentWindow.document;
        doc.open();
        doc.write(`
            <html>
                <head>
                    <title>Código de desconto</title>
                    <style>
                        @media print {
                            body { padding: 20px; }
                            img { width: 600px; height: auto; margin-bottom: 20px; margin-left: auto; margin-right: auto; display: block; }
                            hr { margin-bottom: 10px; height: 20px; border: none; border-top: 10px solid #000; }
                            .total { font-size: 80px; margin-bottom: 20px; font-weight: bold; }
                            .infoVenda { font-size: 50px; margin-bottom: 5px; text-align: center; }
                            .subtotal { font-size: 40px; margin-bottom: 5px; }
                            th, td { font-size: 50px; }
                            table { width: 100%; margin-bottom: 20px; }
                            th, td { padding: 20px; }
                            .codigo { font-size: 70px; }
                            .nomeEmpresa { font-size: 50px; margin-bottom: 5px; }
                            .valorDesconto { font-size: 50px; margin-bottom: 5px; }
                        }
                    </style>
                </head>
                <body>
                    <img src="/static/img/printLogo.svg" alt="Logo">
                    <p class="infoVenda">Código de desconto gerado para empresa ${nome}, CNPJ: ${cnpj}, com endereço em ${endereco}</p>
                    <hr>
                    <h2 class="codigo">Código: ${codigo}</h2>
                    <h2 class="valorDesconto">Valor Desconto: ${valor}</h2>
                </body>
            </html>
        `);
        doc.close();

        iframe.style.display = 'block';
        iframe.contentWindow.print();
    }

    // Adiciona um evento de clique ao botão de geração de código
    document.getElementById("handle_geradorCodigo").addEventListener("click", function() {
        const codVenda = document.getElementById("idVenda").textContent;
        const produtoAntigo = document.getElementById("selectProdutoVenda").value;
        const qtdProdutoAntigo = document.getElementById("qtdProdutosNaVenda").value;
        const valorDesconto = document.getElementById("valorQtdSelecionada").value;

        const codigoSalvo = gerarCodigoDesconto();

        const data = {
            codVenda: codVenda,
            produtos: {
                produtoAntigo: produtoAntigo,
                qtdProdutoAntigo: qtdProdutoAntigo,
            },
            codigoGerado: {
                cod: codigoSalvo,
                valor: valorDesconto
            }
        };

        fetch('dadosEmpresa/' + document.getElementById('usuario').textContent, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    var nome = data['nome'];
                    var cnpj = data['cnpj'];
                    var endereco = data['endereco'];
                    var numero = data['numero'];
                    var bairro = data['bairro'];
                    var enderecoCompleto = endereco + ', ' + numero + ', ' + bairro;


                    printCode(nome, cnpj, enderecoCompleto, codigoSalvo, valorDesconto);

                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                }
            });


        fetch('troca/' + data.codVenda, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Sucesso:', data);
            })
            .catch((error) => {
                console.error('Erro:', error);
            });
    });
});