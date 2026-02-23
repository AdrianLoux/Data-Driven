# Análise de Fidelidade e Segmentação de Clientes (RFM) - E-commerce

Este projeto analisa o comportamento de compra de um e-commerce brasileiro (Olist) para segmentar clientes e identificar oportunidades de retenção e crescimento.

## 📌 Problema de Negócio
A empresa precisava entender quem são seus clientes mais valiosos e quais estão em risco de abandono (Churn) para otimizar os investimentos de marketing.

## 🛠️ Tecnologias Utilizadas
- **Python 3.12**
- **Pandas**: Limpeza e manipulação de dados.
- **Matplotlib/Seaborn/Squarify**: Visualização de dados.
- **Técnica RFM**: Recência, Frequência e Valor Monetário.

## 🚀 Etapas do Projeto
1. **Limpeza de Dados**: Cruzamento de tabelas de pedidos, pagamentos e clientes.
2. **Tratamento Temporal**: Conversão de strings para datetime para cálculos de recência.
3. **Cálculo de Scores**: Atribuição de notas de 1 a 5 baseada em quartis estatísticos.
4. **Segmentação**: Classificação dos clientes em categorias como "Campeões", "Leais", "Em Risco" e "Perdidos".

## 📊 Principais Insights
- (Exemplo) 15% da base de clientes são "Campeões", sendo responsáveis por X% do faturamento.
- Identificamos um grande volume de "Clientes em Risco", sugerindo uma campanha de reativação.

## 📂 Como rodar o projeto
1. Clone o repositório.
2. Baixe o dataset no Kaggle (link aqui).
3. Execute o script `teste.py`.
