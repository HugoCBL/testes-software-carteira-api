# 🏦 API de Carteira Digital: Avaliação de TDD via Testes de Mutação

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Testes](https://img.shields.io/badge/Testes-pytest-yellow)
![Mutação](https://img.shields.io/badge/Mutação-mutmut-red)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-success)

## 📌 Sobre o Projeto

Este projeto prático foca na intersecção entre **arquitetura de software** e **automação de testes**. O objetivo central é avaliar empiricamente a eficácia de uma suíte de testes desenvolvida sob a metodologia *Test-Driven Development* (TDD) em um microsserviço financeiro.

Para validar a robustez da lógica de negócios, utilizamos a engenharia de mutação (via `mutmut`) para injetar falhas deliberadas na Árvore de Sintaxe Abstrata (AST) do código e calcular o *Mutation Score*.

## 🏗️ Arquitetura e Domínio (DDD)

A API foi modelada aplicando conceitos de *Domain-Driven Design* para refletir regras financeiras reais, garantindo invariantes estritas:

* **`Carteira`**: Entidade central que gerencia saldo, limites diários e histórico.
* **`Transacao`**: Entidade estruturada (via `Enum` e `UUID`) que registra entradas, saídas e taxas.
* **`RegraTransferencia`**: Isola a lógica de negócio responsável pela isenção de taxas para transferências acima de limites pré-estabelecidos.

## 🧪 Metodologia de Testes

A suíte de testes (`pytest`) foi construída com foco em **Análise de Valor Limite (Boundary Testing)** e validação de exceções de domínio. As proteções incluem:

* Prevenção de saldos negativos na inicialização.
* Bloqueio de transferências com valores zerados ou negativos.
* Validação rigorosa de limites diários.
* Testes cirúrgicos no limite de isenção de taxas (ex: transferências de valor exato).

## 📖 Evolução do Experimento e Ameaças à Validade

O desenvolvimento deste experimento ocorreu em duas fases distintas, evidenciando as limitações das ferramentas de análise estática e a necessidade de amadurecimento da arquitetura:

* **Fase 1 (Abordagem Inicial):** O experimento começou com uma lógica de transferência simples e a ferramenta `mutatest`. Obtivemos 100% de Mutation Score (6/6 mutantes mortos). No entanto, a análise revelou um falso positivo qualitativo: a ferramenta focava apenas em operadores matemáticos (`+`, `-`) e era cega para a manipulação de estruturas de dados secundárias (como o `.append` em listas de histórico). O código era simples demais para gerar mutantes complexos.
* **Fase 2 (Refatoração para DDD e `mutmut`):** Para criar uma superfície de contato que realmente testasse a eficácia do TDD, a API foi reestruturada utilizando conceitos de *Domain-Driven Design* (DDD). Inserimos regras financeiras reais (taxas baseadas em limites e controle diário de saldo) e migramos para a ferramenta `mutmut`, que atua diretamente na Árvore de Sintaxe Abstrata (AST) de forma mais profunda e requer configuração de rotas específicas. 

Essa evolução permitiu escalar o experimento de 6 para 72 mutantes, revelando gargalos lógicos que a primeira fase havia mascarado.

## 📊 Resultados do Experimento (Mutation Score)

O código foi submetido a uma esteira automatizada de injeção de falhas utilizando a ferramenta `mutmut` rodando em um ambiente Linux via **GitHub Actions**.

### Placar Final

* **Total de Mutantes Injetados:** 72
* **Mutantes Mortos (Killed):** 44
* **Mutantes Sobreviventes (Survived):** 28
* **Mutation Score:** ~61.1%

### Análise

A suíte de TDD demonstrou **100% de eficácia** ao barrar mutações críticas de operadores matemáticos e relacionais (`<`, `>`, `>=`, `+=`, `-=`) nas lógicas de saldo e limites. Os mutantes sobreviventes concentraram-se em áreas não-críticas para a integridade financeira, como a alteração exata de strings de mensagens de erro (*Exception messages*) e inicializações de variáveis padrão, evidenciando pontos onde a cobertura de testes pode ser expandida no futuro.

## 🚀 Como Executar Localmente

### 1. Clone o repositório e ative o ambiente virtual

```bash
git clone https://github.com/HugoCBL/testes-software-carteira-api.git
cd testes-software-carteira-api
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install pytest mutmut
```

### 3. Execute a Suíte TDD (Fase Verde)

```bash
python -m pytest
```

### 4. Execute os Testes de Mutação localmente

```bash
mutmut run
```

> Nota: Para visualizar os detalhes de quais mutantes sobreviveram, utilize o comando `mutmut results`.

## ⚙️ Integração Contínua (CI/CD)

Este repositório conta com uma pipeline automatizada configurada via **GitHub Actions** (`.github/workflows/mutacao.yml`). A cada novo `push` na branch principal, um servidor é provisionado para executar a validação TDD e gerar um novo relatório de mutação, garantindo a integridade contínua da arquitetura.