import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter
from PIL import Image

# Tamanho do tabuleiro e dos quadrados
board_size = 40
square_size = 5

# Intensidades dos quadrados
gray_intensity = 8
black_intensity = 0

# Criação da imagem do tabuleiro
board = np.zeros((board_size, board_size))

for i in range(0, board_size, square_size):
    for j in range(0, board_size, square_size):
        if (i // square_size + j // square_size) % 2 == 0:
            board[i:i+square_size, j:j+square_size] = gray_intensity
        else:
            board[i:i+square_size, j:j+square_size] = black_intensity

# Aplicação do filtro de média
filtered_board = uniform_filter(board, size=3)

# Cálculo dos histogramas
hist_original, bins_original = np.histogram(board, bins=np.arange(10))
hist_filtered, bins_filtered = np.histogram(filtered_board, bins=np.arange(10))

# Salvar as imagens
original_image = Image.fromarray((board * 32).astype(np.uint8))  # Multiplicar por 32 para aumentar a intensidade para a faixa 0-255
filtered_image = Image.fromarray((filtered_board * 32).astype(np.uint8))

original_image.save("original_board.png")
filtered_image.save("filtered_board.png")

# Plot dos histogramas
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].bar(bins_original[:-1], hist_original, width=1, edgecolor='black')
ax[0].set_title('Histograma Original')
ax[0].set_xlabel('Intensidade')
ax[0].set_ylabel('Frequência')

ax[1].bar(bins_filtered[:-1], hist_filtered, width=1, edgecolor='black')
ax[1].set_title('Histograma Filtrado')
ax[1].set_xlabel('Intensidade')
ax[1].set_ylabel('Frequência')

plt.tight_layout()
plt.show()
