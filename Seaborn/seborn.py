import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Conecte-se ao banco de dados e leia os dados
conn = sqlite3.connect('dinossauros.db')
df = pd.read_sql_query("SELECT * FROM dino_data", conn)
conn.close()

# 1. Pré-processamento e limpeza dos dados
period_order = [
    'Early Triassic', 'Mid Triassic', 'Late Triassic',
    'Early Jurassic', 'Mid Jurassic', 'Late Jurassic',
    'Early Cretaceous', 'Mid Cretaceous', 'Late Cretaceous'
]

def clean_period(text):
    for p in period_order:
        if p in text:
            return p
    return 'Other'

df['cleaned_period'] = df['cleaned_period'] = df['period'].apply(clean_period)
df_sorted = df[df['cleaned_period'].isin(period_order)].copy()
df_sorted['cleaned_period'] = pd.Categorical(df_sorted['cleaned_period'], categories=period_order, ordered=True)

# 2. Criar a tabela cruzada completa
period_type_crosstab = pd.crosstab(df_sorted['cleaned_period'], df_sorted['type'])
sorted_types = period_type_crosstab.sum().sort_values(ascending=False).index
period_type_crosstab = period_type_crosstab[sorted_types]

# 3. Criar a lista de quadros para a animação
frames = []
growth_steps = 10
for i, period in enumerate(period_order):
    for step in range(growth_steps + 1):
        frames.append({'period_index': i, 'growth_factor': step / growth_steps})

# Adiciona quadros extras para congelar a animação no final
end_period_index = len(period_order) - 1
for _ in range(30):  # Adiciona 30 quadros do estado final
    frames.append({'period_index': end_period_index, 'growth_factor': 1.0})

# 4. Preparar o gráfico para animação
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(16, 10))
max_count = period_type_crosstab.sum(axis=1).max()

def update(frame_data):
    ax.clear()
    
    current_period_index = frame_data['period_index']
    growth_factor = frame_data['growth_factor']
    
    # Filtra os dados para os períodos atuais
    df_current_periods = period_type_crosstab.iloc[:current_period_index + 1, :].copy()
    
    # Ajusta a altura da barra do período atual com o fator de crescimento
    df_current_periods.iloc[-1] *= growth_factor

    df_current_periods.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')

    for container in ax.containers:
        labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in container]
        ax.bar_label(container, labels=labels, label_type='center', fontsize=10, color='white')

    ax.set_title('Evolução dos Tipos de Dinossauros', fontsize=22, pad=20)
    ax.set_xlabel('Período Histórico', fontsize=14)
    ax.set_ylabel('Número de Dinossauros', fontsize=14)
    
    ax.set_ylim(0, max_count * 1.1)
    
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    
    ax.legend(title='Tipo de Dinossauro', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.tight_layout()

# Cria a animação
ani = FuncAnimation(fig, update, frames=frames, repeat=False)

# SALVAR A ANIMAÇÃO
ani.save('dino_animated_final.gif', writer='pillow', fps=5)

print("Animação salva como 'dino_animated_final.gif' na sua pasta de projeto!")