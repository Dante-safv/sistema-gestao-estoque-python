# Sistema de Gestão de Estoque em Python

Sistema de gestão de estoque desenvolvido em **Python**, com controle de usuários, fornecedores, movimentações de estoque e gestão financeira.

O projeto utiliza arquivos locais (**JSON e CSV**) para persistência de dados e foi pensado para simular um fluxo real de uso em pequenas e médias operações.

---

## Funcionalidades

### 📦 Estoque
- Cadastro e edição de produtos *(restrito ao ADMIN)*
- Controle de entrada e saída de produtos
- Atualização automática das quantidades em estoque
- Definição e alerta de estoque mínimo
- Histórico completo de movimentações

### 🏭 Fornecedores
- Cadastro e edição de fornecedores
- Associação de produtos a fornecedores
- Importação e exportação de fornecedores via CSV

### 💰 Financeiro
- Registro de movimentações financeiras
- Controle de entradas e saídas
- Cálculo de valores relacionados às operações de estoque
- Histórico financeiro persistido em arquivo

### 👥 Usuários e Permissões
- Sistema de autenticação com login
- Gerenciamento de usuários *(exclusivo do ADMIN)*
- Controle de acesso por **roles**:
  - **ADMIN** – acesso total ao sistema
  - **GERENTE** – gestão operacional e financeira
  - **CONTADOR** – acesso a relatórios e financeiro
  - **OPERADOR** – operações de entrada, saída e consulta
- Caso não exista usuário cadastrado, o sistema permite inicialização com um **usuário ADMIN padrão**

### 📁 Importação / Exportação
- Importação de dados via arquivos CSV
- Exportação de produtos, fornecedores, histórico e dados financeiros
- Validação para evitar duplicidade de registros

### 💾 Persistência de Dados
- Armazenamento em arquivos JSON
- Leitura e escrita estruturada
- Criação automática dos arquivos caso não existam

---

## Estrutura do Projeto

- `main.py` – ponto de entrada do sistema  
- `estoque.py` – regras e controle de estoque  
- `fornecedores.py` – gerenciamento de fornecedores  
- `financeiro.py` – controle financeiro  
- `historico.py` – registro de operações  
- `usuarios.py` – autenticação e gestão de usuários  
- `persistencia.py` – leitura e escrita de dados  
- `validacoes.py` – validações de dados  
- `utils.py` – funções auxiliares  
- `dados.py` – armazenamento em memória durante execução  
- `constantes.py` – definição de roles e configurações  

---

## Como Executar o Projeto

```bash
git clone https://github.com/Dante-safv/sistema-gestao-estoque-python.git
cd sistema-gestao-estoque-python
python main.py

## Execução

O sistema pode ser executado diretamente após a clonagem, **sem necessidade de dependências externas**.

---

## Tecnologias Utilizadas
- Python 3
- Git
- GitHub

---

## Objetivo do Projeto

Projeto desenvolvido para **estudo e portfólio**, com foco em:

- Organização e modularização de código
- Separação de responsabilidades
- Lógica de negócio aplicada a um cenário real
- Controle de acesso por permissões
- Versionamento com Git
