import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Preparar os dados
data = {
    'time_numeric': [0, 1, 2, 3, 4, 5, 6],
    'dino_count': [0, 2, 4, 13, 17, 14, 6]
}
df_sauropod_animation = pd.DataFrame(data)

X = df_sauropod_animation[['time_numeric']].values
y = df_sauropod_animation['dino_count'].values

poly_features = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)

X_plot = np.linspace(X.min(), 7, 100).reshape(-1, 1)
X_plot_poly = poly_features.transform(X_plot)
y_plot = model.predict(X_plot_poly)

next_period_numeric = np.array([[7]])
next_period_poly = poly_features.transform(next_period_numeric)
prediction = model.predict(next_period_poly)

# 2. Configurar a figura e os eixos
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title('Modelo de Previsão da População de Sauropods')
ax.set_xlabel('Período Geológico')
ax.set_ylabel('Contagem de Dinossauros')
ax.grid(True)
ax.set_xlim(-0.5, 7.5)
ax.set_ylim(-5, 25)

period_names = ['Early Triassic', 'Late Triassic', 'Early Jurassic', 'Middle Jurassic', 
                'Late Jurassic', 'Early Cretaceous', 'Late Cretaceous', 'Próximo Período']
tick_positions = np.arange(len(period_names))
plt.xticks(tick_positions, period_names, rotation=45, ha='right', fontsize=10)

ax.scatter(X, y, color='blue', label='Dados Históricos', zorder=5)

line_trace, = ax.plot([], [], color='red', linewidth=2, label='Curva de Previsão')
line_star, = ax.plot([], [], 'o', color='orange', markersize=8)
prediction_point, = ax.plot([], [], 'go', markersize=10, label=f'Previsão: {prediction[0]:.2f}')

# Adicionar a legenda manualmente para evitar que ela pisque
ax.legend()

# 3. Função de animação
def animate(i):
    # A estrela cadente percorre a curva
    if i < len(X_plot):
        line_trace.set_data(X_plot[:i], y_plot[:i])
        line_star.set_data(X_plot[i:i+1], y_plot[i:i+1])
    else: # Mantém a linha completa e o ponto final visíveis
        line_trace.set_data(X_plot, y_plot)
        line_star.set_data(X_plot[-1:], y_plot[-1:])
        prediction_point.set_data(next_period_numeric, prediction)
    
    # Fazer as anotações aparecerem apenas nos quadros finais
    if i >= len(X_plot) - 1:
        ax.annotate('Dados Históricos:\nA população aumentou, atingiu um pico e depois começou a cair.', 
                    xy=(4, 17), 
                    xytext=(4.1, 19.5),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=10)
        
        ax.annotate('Curva de Previsão:\nO modelo aprendeu a tendência de crescimento e queda.',
                    xy=(2.33, 10), 
                    xytext=(0.5, 12.5),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=10)

        ax.annotate(f'Previsão para o próximo período:\n{prediction[0]:.2f} dinossauros',
                    xy=(7, prediction[0]), 
                    xytext=(7.1, prediction[0] + 5),
                    arrowprops=dict(facecolor='green', shrink=0.05),
                    fontsize=10)
        
    return line_trace, line_star, prediction_point

# 4. Criar e salvar a animação
ani = FuncAnimation(fig, animate, frames=len(X_plot) + 70, interval=50) # Adiciona 30 quadros extras para a pausa
ani.save('estrela_cadente_pausa_final.gif', writer='imagemagick')

plt.tight_layout()
plt.show()