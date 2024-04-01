from PIL import Image
import os

class IdentificadorFronteira:
    cor_fundo = (255, 255, 255)
    cor_figura = (0, 0, 0)
    cor_figura_rgba = (0, 0, 0, 255)
    def __init__(self, imagem: str, valorIntensidade: float) -> None:
        self.nome_imagem = imagem
        self.imagemParaProcessamento = self.obter_arquivo_imagem()
        self.largura = self.imagemParaProcessamento.size[0]
        self.comprimento = self.imagemParaProcessamento.size[1]
        self.imagemFinal = Image.new("RGB", (self.largura, self.comprimento), self.cor_fundo)
        self.intensidade = valorIntensidade

    def obter_arquivo_imagem(self) -> Image :
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "imagens", self.nome_imagem)

        return Image.open(caminho_imagem)
    
    def is_intensidade_permitida(self, pixelAtual, pixelVizinho) -> bool:
        r1, g1, b1, a1 = pixelAtual
        r2, g2, b2, a2 = pixelVizinho

        intensidadePixelAtual = (r1 + g1 + b1) / 3
        intensidadePixelVizinho = (r2 + g2 + b2) / 3

        diferencaIntensidade = abs(intensidadePixelAtual - intensidadePixelVizinho)

        return self.intensidade > diferencaIntensidade
    
    def verificar_adjacencia_4(self, x: int, y: int, matriz_imagem) -> bool:
        dx = [0, 1, 0, -1]
        dy = [-1, 0, 1, 0]
        is_fronteira = False
        for i in range(0, 4):
           linha = x + dx[i]
           coluna = y + dy[i]
           if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
               pixelVizinho = matriz_imagem[linha, coluna]
               if not self.is_intensidade_permitida(matriz_imagem[x, y], pixelVizinho):
                   is_fronteira = True
                   break
                   
        return is_fronteira
    
    def definir_adjacencia_4_para_pixel_diagonal(self, x: int, y: int, matriz_imagem):
        dx4 = [0, 1, 0, -1]
        dy4 = [-1, 0, 1, 0]
        adjacencia4 = []
        for i in range(0, 4):
           linha = x + dx4[i]
           coluna = y + dy4[i]
           if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
               adjacencia4.append(matriz_imagem[linha, coluna])

        return adjacencia4
    
    def verificar_adjacencia_m(self, x: int, y: int, matriz_imagem) -> bool:
        dx4 = [0, 1, 0, -1]
        dy4 = [-1, 0, 1, 0]
        is_fronteira = False
        adjacencia4_pixel_principal = []
        for i in range(0, 4):
           linha = x + dx4[i]
           coluna = y + dy4[i]
           if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
               pixelVizinho = matriz_imagem[linha, coluna]
               adjacencia4_pixel_principal.append(pixelVizinho)
               if not self.is_intensidade_permitida(matriz_imagem[x, y], pixelVizinho):
                   is_fronteira = True
                   break
               
        dxd = [-1, 1, -1, 1]
        dyd = [-1, -1, 1, 1]
        for i in range(0, 4):
            linha = x + dxd[i]
            coluna = y + dyd[i]
            if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
                pixel_vizinho_adjacentes_4 = self.definir_adjacencia_4_para_pixel_diagonal(linha, coluna, matriz_imagem)
                for pixel_principal in adjacencia4_pixel_principal:
                    if pixel_principal in pixel_vizinho_adjacentes_4:
                        if not self.is_intensidade_permitida(matriz_imagem[x, y], pixel_principal):
                            is_fronteira = True
                            break               

        return is_fronteira
        
    
    def definir_fronteira_imagem_adjacencia_m(self, nome_imagem: str) -> Image:
        matriz_imagem = self.imagemParaProcessamento.load()
        matriz_imagem_processada = self.imagemFinal.load()
        for x in range(self.largura):
            for y in range(self.comprimento):
                is_fronteira = self.verificar_adjacencia_m(x, y, matriz_imagem)
                if is_fronteira:
                    matriz_imagem_processada[x, y] = self.cor_figura_rgba
        self.salvar_imagem(nome_imagem)
    
    def definir_fronteira_imagem_adjacencia_4(self, nome_imagem: str) -> Image:
        matriz_imagem = self.imagemParaProcessamento.load()
        matriz_imagem_processada = self.imagemFinal.load()
        for x in range(self.largura):
            for y in range(self.comprimento):
                is_fronteira = self.verificar_adjacencia_4(x, y, matriz_imagem)
                if is_fronteira:
                    matriz_imagem_processada[x, y] = self.cor_figura_rgba
        self.salvar_imagem(nome_imagem)
    
    def salvar_imagem(self, nome_imagem: str):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_imagem = os.path.join(diretorio_atual, "imagens\\q1", nome_imagem)

        self.imagemFinal.save(caminho_imagem)

    def verificar_adjacencia_8(self, x: int, y: int, matriz_imagem) -> bool:
        dx = [0, 1, 0, -1, -1, 1, -1, 1]
        dy = [-1, 0, 1, 0, -1, -1, 1, 1]
        is_fronteira = False
        for i in range(0, 8):
           linha = x + dx[i]
           coluna = y + dy[i]
           if coluna >= 0 and coluna < self.largura and linha >= 0 and linha < self.comprimento :
               pixelVizinho = matriz_imagem[linha, coluna]
               if not self.is_intensidade_permitida(matriz_imagem[x, y], pixelVizinho):
                   is_fronteira = True
                   break
        return is_fronteira

    def definir_fronteira_imagem_adjacencia_8(self, nome_imagem: str) -> Image:
        matriz_imagem = self.imagemParaProcessamento.load()
        matriz_imagem_processada = self.imagemFinal.load()
        for x in range(self.largura):
            for y in range(self.comprimento):
                is_fronteira = self.verificar_adjacencia_8(x, y, matriz_imagem)
                if is_fronteira:
                    matriz_imagem_processada[x, y] = self.cor_figura_rgba
        self.salvar_imagem(nome_imagem)
    

def main():
    identificadorFronteiraAdjacencia4 = IdentificadorFronteira("aviao.png", 1.0)
    identificadorFronteiraAdjacencia8 = IdentificadorFronteira("aviao.png", 1.0)
    identificadorFronteiraAdjacenciaM = IdentificadorFronteira("aviao.png", 1.0)

    identificadorFronteiraAdjacencia4.definir_fronteira_imagem_adjacencia_4("aviao_adjacencia_4.png")
    identificadorFronteiraAdjacencia8.definir_fronteira_imagem_adjacencia_8("aviao_adjacencia_8.png")
    identificadorFronteiraAdjacenciaM.definir_fronteira_imagem_adjacencia_m("aviao_adjacencia_m.png")


    identificadorFronteiraAdjacencia4 = IdentificadorFronteira("folha.png", 1.0)
    identificadorFronteiraAdjacencia8 = IdentificadorFronteira("folha.png", 1.0)
    identificadorFronteiraAdjacenciaM = IdentificadorFronteira("folha.png", 1.0)
    
    identificadorFronteiraAdjacencia4.definir_fronteira_imagem_adjacencia_4("folha_adjacencia_4.png")
    identificadorFronteiraAdjacencia8.definir_fronteira_imagem_adjacencia_8("folha_adjacencia_8.png")
    identificadorFronteiraAdjacenciaM.definir_fronteira_imagem_adjacencia_m("folha_adjacencia_m.png")

if __name__ == "__main__":
    main()