import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import re  # Biblioteca para usar expressões regulares

# Conecte-se ao banco de dados e leia os dados
conn = sqlite3.connect('dinossauros.db')
query = "SELECT * FROM dino_data"
df = pd.read_sql_query(query, conn)
conn.close()

# Pré-processamento dos dados

# 1. Limpeza da coluna 'length'
# Extrai o valor numérico da coluna 'length' (ex: "8.0m" vira 8.0)
df['length'] = df['length'].str.replace('m', '').astype(float)

# 2. Limpeza da coluna 'period'
# Extrai o ano médio do período.
# Usamos uma expressão regular para encontrar os anos.
def get_avg_year(period_str):
    years = re.findall(r'\d+', period_str)
    if len(years) >= 2:
        return (int(years[0]) + int(years[1])) / 2
    elif len(years) == 1:
        return int(years[0])
    return 0

df['period_numeric'] = df['period'].apply(get_avg_year)

# 3. Preparar os dados para o modelo
# Agora incluímos a nova coluna numérica 'period_numeric' e 'length'
features = ['period_numeric', 'length', 'lived_in', 'type']
target = 'diet'

# Preencha valores ausentes (NaN) na coluna 'length' com a média
df['length'] = df['length'].fillna(df['length'].mean())

# Converta dados de texto em números usando LabelEncoder
le = LabelEncoder()
for col in ['lived_in', 'type', 'diet']:
    df[col] = le.fit_transform(df[col])

# Separe os dados em treino e teste
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Crie e treine o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Faça previsões e verifique a precisão do modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"A precisão do modelo é: {accuracy:.2f}")