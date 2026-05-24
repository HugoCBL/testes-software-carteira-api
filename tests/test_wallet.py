from src.wallet import Carteira

def test_saldo_inicial_deve_ser_cem():
    minha_carteira = Carteira(100)
    assert minha_carteira.saldo == 100

def test_transferencia_diminui_origem_e_aumenta_destino():
    #preparo
    carteira_origem = Carteira(100)
    carteira_destino = Carteira(0)
    
    #ação 
    carteira_origem.transferir(carteira_destino, 30)
    
    #verificação
    assert carteira_origem.saldo == 70
    assert carteira_destino.saldo == 30

def test_transferencia_deve_registrar_historico():
    #preparo
    carteira_origem = Carteira(100)
    carteira_destino = Carteira(0)
    
    #ação
    carteira_origem.transferir(carteira_destino, 30)
    
    #verificação (a carteira de origem tem que registrar a saída)
    assert len(carteira_origem.historico) == 1
    assert carteira_origem.historico[0] == {'tipo': 'saida', 'valor': 30}
    
    #verificação (a carteira de destino tem que registrar a entrada)
    assert len(carteira_destino.historico) == 1
    assert carteira_destino.historico[0] == {'tipo': 'entrada', 'valor': 30}