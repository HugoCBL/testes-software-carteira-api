# 📊 Avaliação de Eficácia TDD com Testes de Mutação

O projeto implementa o núcleo de regras de negócio de um microsserviço financeiro (API de Carteira Digital) com o objetivo de analisar a robustez lógica de suítes de teste.

---

## 🎯 Objetivo da Pesquisa

Avaliar empiricamente a eficácia de uma suíte de testes unitários desenvolvida sob a rigorosa metodologia **Test-Driven Development (TDD)**. Utiliza-se a técnica de **Teste de Mutação** para calcular o *Mutation Score* e mapear possíveis pontos cegos lógicos (falsos positivos) que sobrevivem mesmo com 100% de cobertura de código.

---

## 🛠️ Tecnologias e Ferramentas

- **Linguagem:** Python 3.13
- **Validação Estrutural:** `pytest` (Framework de testes unitários)
- **Injeção de Falhas Lógicas:** `mutatest` (Operador de mutação AST)

---

## 📁 Estrutura do Repositório

```text
.
├── src/                    # Código-fonte principal (Regras de negócio da Wallet)
├── tests/                  # Suíte de testes unitários (Ciclos Red-Green-Refactor)
├── dados_coletados/        # Relatórios brutos gerados pela ferramenta de mutação
├── .gitignore              # Bloqueio de artefatos e caches
└── README.md               # Documentação do projeto
```

---

## 🚀 Como Reproduzir o Experimento

Para garantir a reprodutibilidade do estudo, siga os passos abaixo em um terminal.

### 1. Clone o repositório e acesse a pasta

```bash
git clone https://github.com/SEU_USUARIO/testes-software-carteira-api.git
cd testes-software-carteira-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
```

#### Windows

```bash
.\venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Instale as dependências da pesquisa

```bash
pip install pytest mutatest
```

### 4. Execute a validação da suíte TDD (Fase Verde)

```bash
python -m pytest
```

### 5. Execute a injeção de falhas (Teste de Mutação)

```bash
mutatest --src src --testcmds "python -m pytest"
```

---

## 📈 Dados Coletados

Os relatórios completos de execução, detalhando os mutantes detectados (*Killed*) e as limitações mapeadas nos analisadores de sintaxe abstrata, encontram-se disponíveis na pasta `/dados_coletados`.

---

## 🔬 Resultados Preliminares

| Rodada Experimental | Funcionalidade Avaliada | Mutações Injetadas | Mutantes Detectados | Sobreviventes | Mutation Score |
|--------------------|-------------------------|--------------------|---------------------|----------------|----------------|
| Rodada 01 | Transferência de Saldo | 6 | 6 | 0 | 100,00% |
| Rodada 02 | Registro de Histórico | 6 | 6 | 0 | 100,00% |
| Total Acumulado | API Core (Wallet) | 12 | 12 | 0 | 100,00% |

---

## ⚠️ Limitações Identificadas

Durante a análise experimental, observou-se que a ferramenta de mutação concentrou as alterações principalmente em operadores aritméticos (`AugAssign_Sub` e `AugAssign_Add`), deixando de gerar mutações relevantes em estruturas compostas envolvendo listas e dicionários.

Isso evidencia uma limitação importante da engine de mutação utilizada, mesmo em cenários onde o *Mutation Score* atinge 100%.
