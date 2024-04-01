import os
from PIL import Image

class IdentificaroVizinhaca:
    cor_pixels_fronteira = (0, 0, 0, 255)
    cor_fundo = (255, 255, 255, 255)
    cor_pixel_vizinho = (94, 14, 102, 255)
    
    def __init__(self, nome_imagem: str) -> None:
        self.nome_imagem = nome_imagem
        self.imagem_para_processamento: Image = self.obter_arquivo_imagem()
        self.largura = self.imagem_para_processamento.size[0]
        self.comprimento = self.imagem_para_processamento.size[1]
        self.imagem_final = Image.new("RGB", (self.largura, self.comprimento), self.cor_fundo)
    
    def obter_arquivo_imagem(self) -> Image :
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "imagens\\q1", self.nome_imagem)

        return Image.open(caminho_imagem)

    def salvar_imagem(self, nome_imagem: str):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "imagens\\q3", nome_imagem)

        self.imagem_final.save(caminho_imagem)

    def is_pixel_fronteira(self, pixel) -> bool:
        r, g, b = pixel
        r2, g2, b2, alpha = self.cor_pixels_fronteira

        return (r == r2 and g == g2 and b == b2)

    def colorir_vizinho_4(self, x: int, y: int, matriz_imagem_final):
        dx = [0, 1, 0, -1]
        dy = [-1, 0, 1, 0]
        for i in range(0, 4):
            linha = x + dx[i]
            coluna = y + dy[i]
            if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
                matriz_imagem_final[linha, coluna] = self.cor_pixel_vizinho

    def colorir_vizinho_d(self, x: int, y: int, matriz_imagem_final):
        dx = [-1, 1, -1, 1]
        dy = [-1, -1, 1, 1]
        for i in range(0, 4):
            linha = x + dx[i]
            coluna = y + dy[i]
            if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
                matriz_imagem_final[linha, coluna] = self.cor_pixel_vizinho

    def colorir_vizinho_8(self, x: int, y: int, matriz_imagem_final):
        dx = [0, 1, 0, -1, -1, 1, -1, 1]
        dy = [-1, 0, 1, 0, -1, -1, 1, 1]
        for i in range(0, 8):
            linha = x + dx[i]
            coluna = y + dy[i]
            if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
                matriz_imagem_final[linha, coluna] = self.cor_pixel_vizinho

    def definir_vizinhos_k(self, nome_imagem_final, tipo: str):
        matriz_pixels_imagem_final = self.imagem_final.load()
        matriz_pixels_imagem_processamento = self.imagem_para_processamento.load()
        for x in range(0, self.largura):
            for y in range(0, self.comprimento):
                pixel_atual = matriz_pixels_imagem_processamento[x, y]
                if self.is_pixel_fronteira(pixel_atual):
                    if tipo == '4':
                        self.colorir_vizinho_4(x, y, matriz_pixels_imagem_final)
                    elif tipo == 'd':
                        self.colorir_vizinho_d(x, y, matriz_pixels_imagem_final)
                    elif tipo == '8':
                        self.colorir_vizinho_8(x, y, matriz_pixels_imagem_final)

        self.salvar_imagem(nome_imagem_final)

def main():
    imagens = ["aviao_adjacencia_4.png", "aviao_adjacencia_8.png", "aviao_adjacencia_m.png", "folha_adjacencia_4.png", "folha_adjacencia_8.png", "folha_adjacencia_m.png"]
    vizinhacas = ["4", "8", "d"]

    for imagem in imagens:
        for vizinhaca in vizinhacas:
            split_nome_imagem = imagem.split(".")
            identificaroVizinhaca = IdentificaroVizinhaca(imagem)
            identificaroVizinhaca.definir_vizinhos_k(split_nome_imagem[0]+"_vizinha_"+vizinhaca+".png", vizinhaca)
            

if __name__ == "__main__":
    main()