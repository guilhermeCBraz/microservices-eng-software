#!/bin/bash

# Setup script para criar ambientes virtuais e instalar dependências

echo "🚀 Configurando microserviços..."

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Catálogo de Produtos
echo -e "${BLUE}📦 Configurando Catálogo de Produtos...${NC}"
cd product_catalog
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..
echo -e "${GREEN}✓ Catálogo de Produtos pronto${NC}"

# 2. Carrinho de Compras
echo -e "${BLUE}🛒 Configurando Carrinho de Compras...${NC}"
cd shopping_cart
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..
echo -e "${GREEN}✓ Carrinho de Compras pronto${NC}"

# 3. Orquestrador
echo -e "${BLUE}🎯 Configurando Orquestrador...${NC}"
cd orchestrator
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..
echo -e "${GREEN}✓ Orquestrador pronto${NC}"

echo ""
echo -e "${GREEN}✅ Todos os serviços foram configurados com sucesso!${NC}"
echo ""
echo "📝 Para executar os serviços, use:"
echo ""
echo "Terminal 1 - Catálogo de Produtos (Porto 5001):"
echo "  cd product_catalog && source venv/bin/activate && python app.py"
echo ""
echo "Terminal 2 - Carrinho de Compras (Porto 5002):"
echo "  cd shopping_cart && source venv/bin/activate && python app.py"
echo ""
echo "Terminal 3 - Orquestrador (Porto 5000):"
echo "  cd orchestrator && source venv/bin/activate && python app.py"
