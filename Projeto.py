import pandas as pd
import zipfile

# 1. Caminho para o seu ZIP
caminho_zip = r'C:\Users\Adria\Downloads\archive.zip'

# 2. Abrindo o ZIP e lendo os arquivos lá de dentro
with zipfile.ZipFile(caminho_zip, 'r') as z:
    # Lendo cada CSV especificando o nome do arquivo dentro do ZIP
    df_orders = pd.read_csv(z.open('olist_orders_dataset.csv'))
    df_payments = pd.read_csv(z.open('olist_order_payments_dataset.csv'))
    df_customers = pd.read_csv(z.open('olist_customers_dataset.csv'))

print("✅ Tabelas carregadas com sucesso via ZipFile!")

# 3. Vamos unir (Merge) as tabelas agora
# Primeiro: Unimos os pedidos com os pagamentos usando o 'order_id'
df_completo = pd.merge(df_orders, df_payments, on='order_id')

# Segundo: Unimos o resultado com os clientes usando o 'customer_id'
df_completo = pd.merge(df_completo, df_customers, on='customer_id')

print("\n--- Informações do Dataset Unificado ---")
print(df_completo.info())

print("\n--- Primeiras 5 linhas do cruzamento ---")
print(df_completo[['order_id', 'order_purchase_timestamp', 'payment_value', 'customer_unique_id']].head())

# 1. Converter a coluna de tempo para o formato Datetime
df_completo['order_purchase_timestamp'] = pd.to_datetime(df_completo['order_purchase_timestamp'])

# 2. Filtrar apenas o que nos interessa para o RFM
# Queremos: ID único do cliente, Data da compra e Valor pago
df_rfm_base = df_completo[['customer_unique_id', 'order_purchase_timestamp', 'payment_value']].copy()

# 3. Checar se existem valores nulos (importante para o portfólio!)
print("Valores nulos por coluna:")
print(df_rfm_base.isnull().sum())

# 4. Ver o intervalo de tempo do dataset (pra saber de quando são os dados)
print(f"\nData mínima: {df_rfm_base['order_purchase_timestamp'].min()}")
print(f"Data máxima: {df_rfm_base['order_purchase_timestamp'].max()}")

# Definindo a data de hoje (como se estivéssemos no dia seguinte à última compra do dataset)
agora = df_rfm_base['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# Agrupando por cliente para calcular R, F e M
df_rfm = df_rfm_base.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (agora - x.max()).days, # Recência
    'customer_unique_id': 'count',                                # Frequência
    'payment_value': 'sum'                                        # Monetário
})

# Renomeando as colunas
df_rfm.rename(columns={
    'order_purchase_timestamp': 'Recencia',
    'customer_unique_id': 'Frequencia',
    'payment_value': 'Monetario'
}, inplace=True)

print("\n--- Tabela RFM Inicial ---")
print(df_rfm.head())

# Criando as notas (Scores) de 1 a 5
# Para Recência: QUANTO MENOR, MELHOR (nota alta para quem comprou há pouco tempo)
df_rfm['R_Score'] = pd.qcut(df_rfm['Recencia'], 5, labels=[5, 4, 3, 2, 1])

# Para Frequência e Monetário: QUANTO MAIOR, MELHOR (nota alta para quem compra muito e gasta muito)
# Usamos rank(method='first') para evitar erros se houver muitos valores repetidos (como clientes que compraram só 1 vez)
df_rfm['F_Score'] = pd.qcut(df_rfm['Frequencia'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
df_rfm['M_Score'] = pd.qcut(df_rfm['Monetario'], 5, labels=[1, 2, 3, 4, 5])

# Criando um Score Geral (Soma ou concatenação)
df_rfm['RFM_Score'] = df_rfm['R_Score'].astype(str) + df_rfm['F_Score'].astype(str) + df_rfm['M_Score'].astype(str)

print("Notas atribuídas com sucesso!")
print(df_rfm.head())

# Função para classificar o cliente com base no Score de Recência e Frequência
def segmentar_cliente(df):
    r = int(df['R_Score'])
    f = int(df['F_Score'])
    
    if r >= 4 and f >= 4:
        return 'Campeões (VIP)'
    elif r >= 3 and f >= 3:
        return 'Clientes Leais'
    elif r >= 4 and f <= 2:
        return 'Novos Clientes'
    elif r <= 2 and f >= 4:
        return 'Clientes em Risco (Eram bons)'
    elif r <= 2 and f <= 2:
        return 'Clientes Perdidos / Hibernando'
    else:
        return 'Potencialmente Fiéis'

# Aplicando a segmentação
df_rfm['Segmento'] = df_rfm.apply(segmentar_cliente, axis=1)

# Verificando quantos clientes temos em cada grupo
print("\n--- Distribuição dos Segmentos ---")
print(df_rfm['Segmento'].value_counts())

import matplotlib.pyplot as plt
import seaborn as sns
# Se der erro no squarify, rode no terminal: pip install squarify
import squarify 

# 1. Preparando os dados para o gráfico
df_segmentos = df_rfm['Segmento'].value_counts().reset_index()
df_segmentos.columns = ['Segmento', 'Quantidade']

# 2. Configurando o visual
plt.figure(figsize=(15, 8))
colors = sns.color_palette('RdYlGn', len(df_segmentos)) # Gradiente do Vermelho ao Verde

# 3. Criando o Treemap
squarify.plot(sizes=df_segmentos['Quantidade'], 
              label=df_segmentos['Segmento'], 
              alpha=0.8, 
              color=colors,
              value=df_segmentos['Quantidade'])

plt.title("Distribuição dos Segmentos de Clientes (RFM)", fontsize=18)
plt.axis('off')
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(data=df_rfm, x='Segmento', y='Monetario', estimator=sum, palette='viridis')
plt.title('Receita Total por Segmento de Cliente')
plt.xticks(rotation=45)
plt.ylabel('Soma do Valor Pago (R$)')
plt.show()