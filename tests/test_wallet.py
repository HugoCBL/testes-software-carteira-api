import pytest
from wallet import (
    Carteira, 
    ValorInvalidoError, 
    SaldoInsuficienteError, 
    LimiteExcedidoError, 
    TipoTransacao, 
    RegraTransferencia
)

#TESTES DE INICIALIZAÇÃO E DEPÓSITO
def test_inicializacao_carteira_nao_pode_ter_saldo_negativo():
    with pytest.raises(ValorInvalidoError, match="O saldo inicial não pode ser negativo."):
        Carteira("Hugo", saldo_inicial=-10.0)

def test_deposito_com_valor_valido_aumenta_saldo_e_registra_historico():
    carteira = Carteira("Hugo", saldo_inicial=0.0)
    carteira.depositar(100.0)
    
    assert carteira.saldo == 100.0
    assert len(carteira.historico) == 1
    assert carteira.historico[0].tipo == TipoTransacao.DEPOSITO
    assert carteira.historico[0].valor == 100.0

def test_deposito_com_valor_zero_ou_negativo_lanca_excecao():
    carteira = Carteira("Hugo")
    #adicionado match para capturar os mutantes de texto no depósito
    with pytest.raises(ValorInvalidoError, match="O valor do depósito deve ser positivo."):
        carteira.depositar(0.0)
    with pytest.raises(ValorInvalidoError, match="O valor do depósito deve ser positivo."):
        carteira.depositar(-50.0)

#TESTES DE TRANSFERÊNCIA - EXCEÇÕES
def test_transferencia_valor_zero_ou_negativo_lanca_excecao():
    origem = Carteira("Hugo", saldo_inicial=100.0)
    destino = Carteira("Loja", saldo_inicial=0.0)
    
    #match para capturar os mutantes de texto na transferência
    with pytest.raises(ValorInvalidoError, match="O valor da transferência deve ser maior que zero."):
        origem.transferir(destino, 0.0)
    with pytest.raises(ValorInvalidoError, match="O valor da transferência deve ser maior que zero."):
        origem.transferir(destino, -10.0)

def test_transferencia_acima_do_limite_diario_lanca_excecao():
    #limite padrão é 5000
    origem = Carteira("Hugo", saldo_inicial=10000.0, limite_diario=5000.0)
    destino = Carteira("Loja", saldo_inicial=0.0)
    
    #match para validar a mensagem de limite
    with pytest.raises(LimiteExcedidoError, match="A transferência excede o limite diário de 5000.0."):
        origem.transferir(destino, 5000.01)

def test_transferencia_sem_saldo_para_cobrir_valor_e_taxa_lanca_excecao():
    origem = Carteira("Hugo", saldo_inicial=100.0)
    destino = Carteira("Loja", saldo_inicial=0.0)
    
    #match para validar a mensagem de saldo
    with pytest.raises(SaldoInsuficienteError, match="Saldo insuficiente para cobrir o valor e as taxas."):
        origem.transferir(destino, 100.0)

#TESTES DE TRANSFERÊNCIA - REGRAS DE NEGÓCIO E LIMITES
def test_transferencia_com_cobranca_de_taxa_abaixo_da_isencao():
    origem = Carteira("Hugo", saldo_inicial=500.0, limite_diario=1000.0)
    destino = Carteira("Loja", saldo_inicial=0.0)
   
    origem.transferir(destino, 100.0)
    
    assert origem.saldo == 395.0 
    assert destino.saldo == 100.0
    assert origem.limite_diario == 900.0 #limite só debita o valor real 

def test_transferencia_exata_no_limite_de_isencao_nao_cobra_taxa():
    #teste para matar mutantes no operador `>=`
    origem = Carteira("Hugo", saldo_inicial=1500.0)
    destino = Carteira("Loja", saldo_inicial=0.0)
    
    origem.transferir(destino, 1000.0)
    
    assert origem.saldo == 500.0
    assert destino.saldo == 1000.0

#TESTES DE HISTÓRICO DE TRANSAÇÕES
def test_transferencia_registra_historico_correto_na_origem_e_destino():
    origem = Carteira("Hugo", saldo_inicial=200.0)
    destino = Carteira("Loja", saldo_inicial=0.0)
    
    origem.transferir(destino, 50.0) #taxa será 5.0
    
    #verifica extrato da origem
    transacao_origem = origem.historico[0]
    assert transacao_origem.tipo == TipoTransacao.TRANSFERENCIA_SAIDA
    assert transacao_origem.valor == 50.0
    assert transacao_origem.taxa == 5.0
    
    #verifica extrato do destino
    transacao_destino = destino.historico[0]
    assert transacao_destino.tipo == TipoTransacao.TRANSFERENCIA_ENTRADA
    assert transacao_destino.valor == 50.0
    assert transacao_destino.taxa == 0.0