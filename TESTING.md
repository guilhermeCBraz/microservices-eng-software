# 🧪 Guia de Testes dos Microserviços

## ✅ Status dos Serviços

Após executar os 3 serviços, verifique se estão rodando:

- **Catálogo de Produtos**: http://localhost:5001
- **Carrinho de Compras**: http://localhost:5002
- **Orquestrador**: http://localhost:5000

## 📋 Sequência de Testes

### 1️⃣ Listar Todos os Produtos
O orquestrador consulta o catálogo e lista todos os produtos:

```bash
curl http://localhost:5000/
```

**Resposta esperada:**
```json
{
  "message": "Welcome to E-Commerce",
  "products": [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 5},
    {"id": 2, "name": "Mouse", "price": 29.99, "stock": 50},
    {"id": 3, "name": "Teclado", "price": 79.99, "stock": 20},
    {"id": 4, "name": "Monitor", "price": 299.99, "stock": 10}
  ]
}
```

### 2️⃣ Visualizar Carrinho Vazio
O orquestrador consulta o carrinho do usuário 1 (ainda vazio):

```bash
curl http://localhost:5000/cart/1
```

**Resposta esperada:**
```json
{
  "user_id": 1,
  "items": [],
  "total": 0
}
```

### 3️⃣ Criar Primeiro Pedido
O orquestrador:
1. Valida o produto no catálogo (ID 1)
2. Adiciona ao carrinho do usuário 1
3. Retorna o pedido criado

```bash
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 2}'
```

**Resposta esperada:**
```json
{
  "message": "Order created successfully",
  "user_id": 1,
  "product": {
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "stock": 5
  },
  "cart": {
    "user_id": 1,
    "items": [
      {
        "product_id": 1,
        "product_name": "Laptop",
        "price": 999.99,
        "quantity": 2
      }
    ],
    "total": 1999.98
  }
}
```

### 4️⃣ Visualizar Carrinho Atualizado
Confirmar que o item foi adicionado:

```bash
curl http://localhost:5000/cart/1
```

**Resposta esperada:**
```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "product_name": "Laptop",
      "price": 999.99,
      "quantity": 2
    }
  ],
  "total": 1999.98
}
```

### 5️⃣ Adicionar Outro Produto
Adicionar o Mouse (ID 2) ao carrinho:

```bash
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 2, "quantity": 3}'
```

### 6️⃣ Carrinho com Múltiplos Itens
Verificar o carrinho com múltiplos produtos:

```bash
curl http://localhost:5000/cart/1
```

**Resposta esperada:**
```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "product_name": "Laptop",
      "price": 999.99,
      "quantity": 2
    },
    {
      "product_id": 2,
      "product_name": "Mouse",
      "price": 29.99,
      "quantity": 3
    }
  ],
  "total": 2089.95
}
```

### 7️⃣ Teste com Produto Inválido
Tentar criar pedido com ID de produto que não existe (ID 999):

```bash
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 999, "quantity": 1}'
```

**Resposta esperada:**
```json
{
  "error": "Product not found"
}
```

### 8️⃣ Carrinho de Outro Usuário
Testar se carrinhos são isolados por usuário:

```bash
# Usuário 2 cria um pedido
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "product_id": 3, "quantity": 1}'

# Usuário 2 visualiza seu carrinho (deve ter apenas 1 item)
curl http://localhost:5000/cart/2

# Usuário 1 ainda tem seus itens originais
curl http://localhost:5000/cart/1
```

### 9️⃣ Atualizar Quantidade de Item Existente
Se adicionar o mesmo produto, a quantidade deve aumentar:

```bash
# Adicionar mais 1 Laptop
curl -X POST http://localhost:5000/order \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 1}'

# Verificar que a quantidade do Laptop agora é 3 (2 + 1)
curl http://localhost:5000/cart/1
```

## 🔍 Testes Diretos nos Serviços

Você também pode testar cada serviço isoladamente:

### Catálogo de Produtos

```bash
# Listar todos
curl http://localhost:5001/products

# Obter um produto específico
curl http://localhost:5001/products/1

# Produto inexistente (deve retornar 404)
curl http://localhost:5001/products/999
```

### Carrinho de Compras

```bash
# Visualizar carrinho (mesmo vazio)
curl http://localhost:5002/cart/1

# Adicionar item direto (sem passar pelo orquestrador)
curl -X POST http://localhost:5002/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "product_name": "Laptop",
    "price": 999.99,
    "quantity": 2
  }'
```

## 📊 Fluxo Completo do E-Commerce

```
Cliente
  ↓
[GET /] → Orquestrador → Catálogo (GET /products) → Lista de Produtos
  ↓
[POST /order] → Orquestrador
                 ├─→ Catálogo (GET /products/<id>) [Validação]
                 └─→ Carrinho (POST /cart/<user_id>/add) [Adicionar]
  ↓
[GET /cart/<user_id>] → Orquestrador → Carrinho (GET /cart/<user_id>) → Carrinho Atualizado
```

## ✨ Conceitos Demonstrados

✅ **Comunicação HTTP/REST** entre serviços
✅ **Orquestração** de múltiplos serviços
✅ **Isolamento de dados** (carrinhos por usuário)
✅ **Tratamento de erros** (produto não encontrado)
✅ **Escalabilidade** (serviços independentes)
✅ **Simplicidade** (sem complexidades desnecessárias)

## 🚨 Solução de Problemas

### Erro: Connection refused
- Verifique se os 3 serviços estão rodando em terminais diferentes
- Verifique as portas: 5000, 5001, 5002

### Erro: 404 em GET /
- `GET /` só funciona no **Orquestrador** (porta 5000)
- Para o Carrinho: use `GET /cart/<user_id>`
- Para o Catálogo: use `GET /products`

### Erro: Product not found (201 → 404)
- Verifique se o `product_id` existe (IDs válidos: 1, 2, 3, 4)

### Erros CORS ou requisições lentas
- Aumente o timeout se necessário
- Verifique se todos os serviços estão respondendo
