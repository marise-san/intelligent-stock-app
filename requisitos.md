# Especificação de Requisitos - Sistema de Gestão de Estoque

## 1. Visão Geral

O sistema de gestão de estoque visa automatizar e otimizar o controle de produtos do supermercado, garantindo informações precisas e em tempo real sobre a quantidade de itens disponíveis, suas movimentações e validades.

## 2. Requisitos Funcionais

### 2.1. Gestão de Produtos

- **RF001:** O sistema deve permitir o cadastro de novos produtos, armazenando as seguintes informações:
    - Código de Barras (único)
    - Nome do Produto
    - Descrição
    - Categoria (ex: mercearia, açougue, padaria, limpeza, etc.)
    - Fornecedor
    - Preço de Custo
    - Preço de Venda
    - Unidade de Medida (ex: unidade, kg, litro)
    - Quantidade Mínima em Estoque
    - Data de Validade

- **RF002:** O sistema deve permitir a edição dos dados de um produto cadastrado.
- **RF003:** O sistema deve permitir a exclusão de um produto.
- **RF004:** O sistema deve permitir a consulta de produtos por nome, código de barras ou categoria.

### 2.2. Controle de Estoque

- **RF005:** O sistema deve registrar a entrada de produtos no estoque, atualizando a quantidade disponível.
- **RF006:** O sistema deve registrar a saída de produtos do estoque (venda), atualizando a quantidade disponível.
- **RF007:** O sistema deve permitir o ajuste manual de estoque para correção de divergências (perdas, danos, etc.).
- **RF008:** O sistema deve gerar alertas visuais quando a quantidade de um produto atingir o nível mínimo pré-definido.
- **RF009:** O sistema deve gerar alertas para produtos próximos da data de validade.

### 2.3. Relatórios

- **RF010:** O sistema deve gerar um relatório de inventário com a lista de todos os produtos e suas respectivas quantidades em estoque.
- **RF011:** O sistema deve gerar um relatório de movimentação de estoque por período, mostrando entradas e saídas.
- **RF012:** O sistema deve gerar um relatório de produtos com baixo estoque.
- **RF013:** O sistema deve gerar um relatório de produtos próximos do vencimento.

### 2.4. Gestão de Usuários

- **RF014:** O sistema deve ter um controle de acesso com dois níveis de permissão:
    - **Administrador:** Acesso total a todas as funcionalidades.
    - **Operador:** Acesso limitado ao registro de entradas e saídas de produtos.

## 3. Requisitos Não Funcionais

- **RNF001:** O sistema deve ser desenvolvido como uma aplicação web, acessível através de um navegador.
- **RNF002:** A interface do usuário deve ser intuitiva, clara e de fácil utilização (boa UX/UI).
- **RNF003:** O sistema deve utilizar o banco de dados SQLite para armazenamento dos dados.
- **RNF004:** O backend do sistema deve ser desenvolvido em Python, utilizando o framework Flask.
- **RNF005:** O sistema deve registrar logs de erros em um arquivo `error.log` para facilitar a depuração.
- **RNF006:** O sistema deve apresentar saídas no console para cada funcionalidade executada, informando o status da operação.
- **RNF007:** O projeto deve ser modularizado, separando as responsabilidades em diferentes diretórios (ex: `database`, `models`, `controllers`, `static`, `templates`).
- **RNF008:** O sistema deve ser performático, com tempos de resposta rápidos para as operações do dia a dia.
- **RNF009:** A segurança dos dados deve ser garantida, especialmente no que diz respeito ao controle de acesso.

## 4. Tecnologias

- **Linguagem de Programação:** Python 3.x
- **Framework Web:** Flask
- **Banco de Dados:** SQLite 3
- **Frontend:** HTML5, CSS3, JavaScript
- **Bibliotecas Python (sugestões):**
    - `Flask`
    - `Flask-SQLAlchemy` (para ORM)
    - `Flask-WTF` (para formulários)
    - `python-dotenv` (para variáveis de ambiente)
