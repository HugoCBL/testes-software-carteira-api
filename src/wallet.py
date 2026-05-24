class Carteira:
    def __init__(self, dinheiro_inicial):
        self.saldo = dinheiro_inicial
        self.historico = []  #extrato vazio
        
    def transferir(self, destino, valor):
        self.saldo -= valor
        destino.saldo += valor
        
        #registramos no extrato de quem enviou
        self.historico.append({'tipo': 'saida', 'valor': valor})
        
        #registramos no extrato de quem recebeu
        destino.historico.append({'tipo': 'entrada', 'valor': valor})