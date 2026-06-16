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

O desenvolvimento deste experimento ocorreu em fases distintas, evidenciando as limitações das ferramentas de análise estática e a necessidade de amadurecimento da arquitetura:

### Fase 1 (Abordagem Inicial)

O experimento começou com uma lógica de transferência simples e a ferramenta `mutatest`. Obtivemos 100% de Mutation Score (6/6 mutantes mortos). No entanto, a análise revelou um falso positivo qualitativo: a ferramenta focava apenas em operadores matemáticos (`+`, `-`) e era cega para a manipulação de estruturas de dados secundárias (como o `.append` em listas de histórico). O código era simples demais para gerar mutantes complexos.

### Fase 2 - v1 (Refatoração para DDD e `mutmut`)

Para criar uma superfície de contato que realmente testasse a eficácia do TDD, a API foi reestruturada utilizando conceitos de *Domain-Driven Design* (DDD). Inserimos regras financeiras reais e migramos para a ferramenta `mutmut`, que atua diretamente na Árvore de Sintaxe Abstrata (AST). O experimento escalou para 72 mutantes, revelando que testes de exceção simples não capturavam mutações textuais.

### Fase 2 - v2 (Refinamento Estrito)

A partir da análise dos sobreviventes da etapa anterior, a suíte de testes foi blindada utilizando o parâmetro `match` do `pytest` para garantir a correspondência exata das strings de erro do domínio. Essa refatoração erradicou os mutantes de texto, elevando significativamente o placar final.

## 📊 Histórico de Resultados (Mutation Score)

O código foi submetido a uma esteira automatizada de injeção de falhas rodando em um ambiente Linux via **GitHub Actions**. Abaixo está o registro da evolução da nossa suíte de testes contra os mutantes:

### 1️⃣ Fase 1: Ferramenta Básica (`mutatest`)

* **Total Injetado:** 6
* **Mortos (Killed):** 6
* **Sobreviventes:** 0
* **Mutation Score:** 100% *(Considerado um falso positivo devido à baixa complexidade arquitetural)*

### 2️⃣ Fase 2 (v1): Arquitetura DDD sem amarração de strings (`mutmut`)

* **Total Injetado:** 72
* **Mortos (Killed):** 44
* **Sobreviventes:** 28
* **Mutation Score:** ~61.1% *(Revelou gargalos na validação de mensagens de erro)*

### 3️⃣ Fase 2 (v2): Arquitetura DDD blindada (`mutmut` estrito) - Placar Final

* **Total Injetado:** 72
* **Mortos (Killed):** 54
* **Sobreviventes:** 18
* **Mutation Score:** 75.0%

## 📈 Análise Conclusiva

A suíte de TDD demonstrou **100% de eficácia** ao barrar mutações críticas de operadores matemáticos e relacionais (`<`, `>`, `>=`, `+=`, `-=`) nas lógicas de saldo e limites desde a primeira injeção do `mutmut`.

A adoção posterior de asserções estritas nas exceções (`match="..."`) neutralizou com sucesso as mutações de string textuais, comprovando o ciclo *Red-Green-Refactor* do TDD.

Os 18 mutantes que sobreviveram na versão final encontram-se isolados em inicializações padrão de variáveis internas, não representando ameaça à integridade financeira da aplicação.

## 🚀 Como Executar Localmente

### 1. Clone o repositório e ative o ambiente virtual

```bash
git clone https://github.com/HugoCBL/testes-software-carteira-api.git
cd testes-software-carteira-api

python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
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

> **Nota:** Para visualizar os detalhes dos mutantes sobreviventes, utilize:

```bash
mutmut results
```

## ⚙️ Integração Contínua (CI/CD)

Este repositório conta com uma pipeline automatizada configurada via **GitHub Actions** (`.github/workflows/mutacao.yml`).

A cada novo `push` na branch principal, um ambiente Linux é provisionado automaticamente para:

1. Instalar as dependências do projeto;
2. Executar toda a suíte de testes TDD;
3. Rodar a análise de mutação com `mutmut`;
4. Gerar relatórios de cobertura e qualidade.

Dessa forma, garante-se a integridade contínua da arquitetura e da lógica de negócio da aplicação.