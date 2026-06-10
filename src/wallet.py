from enum import Enum
from datetime import datetime
import uuid

class TipoTransacao(Enum):
    DEPOSITO = "DEPOSITO"
    TRANSFERENCIA_SAIDA = "TRANSFERENCIA_SAIDA"
    TRANSFERENCIA_ENTRADA = "TRANSFERENCIA_ENTRADA"

class ValorInvalidoError(Exception):
    pass

class SaldoInsuficienteError(Exception):
    pass

class LimiteExcedidoError(Exception):
    pass

class Transacao:
    """Entidade que representa uma movimentação financeira no extrato."""
    def __init__(self, tipo: TipoTransacao, valor: float, taxa: float = 0.0):
        self.id = str(uuid.uuid4())
        self.tipo = tipo
        self.valor = valor
        self.taxa = taxa
        self.data_hora = datetime.now()

class RegraTransferencia:
    """Isola a lógica de negócio das taxas (Fácil de testar e mutar)."""
    TAXA_FIXA = 5.0
    LIMITE_ISENCAO_TAXA = 1000.0

    @staticmethod
    def calcular_taxa(valor: float) -> float:
        if valor >= RegraTransferencia.LIMITE_ISENCAO_TAXA:
            return 0.0
        return RegraTransferencia.TAXA_FIXA

class Carteira:
    def __init__(self, titular: str, saldo_inicial: float = 0.0, limite_diario: float = 5000.0):
        if saldo_inicial < 0:
            raise ValorInvalidoError("O saldo inicial não pode ser negativo.")
        
        self.titular = titular
        self._saldo = saldo_inicial
        self.limite_diario = limite_diario
        self.historico: list[Transacao] = []

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self._saldo += valor
        self.historico.append(Transacao(TipoTransacao.DEPOSITO, valor))

    def transferir(self, destino: 'Carteira', valor: float):
        #validações básicas
        if valor <= 0:
            raise ValorInvalidoError("O valor da transferência deve ser maior que zero.")
        
        if valor > self.limite_diario:
            raise LimiteExcedidoError(f"A transferência excede o limite diário de {self.limite_diario}.")

        # calculo de custos da regra de negócio
        taxa = RegraTransferencia.calcular_taxa(valor)
        custo_total = valor + taxa

        #validação de saldo
        if self._saldo < custo_total:
            raise SaldoInsuficienteError("Saldo insuficiente para cobrir o valor e as taxas.")

        #débito e crédito
        self._saldo -= custo_total
        destino._saldo += valor
        self.limite_diario -= valor

        #registro de historico 
        self.historico.append(
            Transacao(TipoTransacao.TRANSFERENCIA_SAIDA, valor, taxa)
        )
        destino.historico.append(
            Transacao(TipoTransacao.TRANSFERENCIA_ENTRADA, valor, 0.0)
        )