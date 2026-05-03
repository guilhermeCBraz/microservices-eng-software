# E-Commerce com Microserviços

Um pequeno e-commerce implementado com 3 microserviços em Flask, demonstrando o padrão de arquitetura de microserviços.

## Arquitetura

### 1. **Orquestrador** (Porto 5000)
Serviço responsável por coordenar os demais e expor as principais operações do e-commerce.

**Rotas:**
- `GET /` - Listar todos os produtos disponíveis
- `GET /cart/<user_id>` - Visualizar carrinho do usuário
- `POST /order` - Criar um pedido (coordena produto + carrinho)

### 2. **Catálogo de Produtos** (Porto 5001)
Serviço que gerencia o catálogo de produtos disponíveis.

**Rotas:**
- `GET /products` - Listar todos os produtos
- `GET /products/<product_id>` - Obter detalhes de um produto

### 3. **Carrinho de Compras** (Porto 5002)
Serviço que gerencia os carrinhos de compras dos usuários.

**Rotas:**
- `GET /cart/<user_id>` - Visualizar carrinho do usuário
- `POST /cart/<user_id>/add` - Adicionar item ao carrinho

## Como Executar

### Pré-requisitos
- Python 3.7+
- pip

### Instalação

1. Instale as dependências de cada serviço:

```bash
# Catálogo de Produtos
cd product_catalog
pip install -r requirements.txt

# Carrinho de Compras
cd ../shopping_cart
pip install -r requirements.txt

# Orquestrador
cd ../orchestrator
pip install -r requirements.txt
```

### Executar os Serviços

Abra 3 terminais diferentes e execute cada serviço:

**Terminal 1 - Catálogo de Produtos:**
```bash
cd product_catalog
python app.py
```

**Terminal 2 - Carrinho de Compras:**
```bash
cd shopping_cart
python app.py
```

**Terminal 3 - Orquestrador:**
```bash
cd orchestrator
python app.py
```

## Exemplos de Uso

### 1. Listar produtos
```bash
curl http://localhost:5000/
```

### 2. Visualizar carrinho vazio
```bash
curl http://localhost:5000/cart/1
```

### 3. Criar um pedido (adicionar produto ao carrinho)
```bash
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 2}'
```

### 4. Visualizar carrinho atualizado
```bash
curl http://localhost:5000/cart/1
```

### 5. Adicionar outro produto
```bash
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 1}'
```

## Fluxo de Uma Compra

1. **Cliente acessa o orquestrador** (`GET /`)
   - Recebe lista de produtos disponíveis

2. **Cliente cria um pedido** (`POST /order`)
   - Orquestrador consulta o serviço de catálogo para validar o produto
   - Orquestrador envia o produto para o serviço de carrinho adicionar
   - Retorna o pedido criado com o carrinho atualizado

3. **Cliente visualiza seu carrinho** (`GET /cart/<user_id>`)
   - Orquestrador consulta o carrinho do usuário
   - Retorna os items e o total da compra

## Conceitos Demonstrados

✅ **Separação de Responsabilidades**: Cada serviço tem uma função específica
✅ **Comunicação entre Serviços**: Orquestrador coordena via HTTP/REST
✅ **Escalabilidade**: Serviços podem ser escalados independentemente
✅ **Modularidade**: Fácil adicionar novos serviços (ex: Pagamento, Entrega)
✅ **Simplicidade**: Implementação mínima sem complexidades desnecessárias

## Possíveis Extensões

- Adicionar serviço de **Pagamento**
- Adicionar serviço de **Cálculo de Frete**
- Implementar **banco de dados** (ex: SQLite, PostgreSQL)
- Adicionar **autenticação** (JWT)
- Implementar **logs centralizados**
- Adicionar **tratamento de erros** mais robusto
