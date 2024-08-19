from PIL import Image
import os
from enum import Enum
import matplotlib.pyplot as plotador_grafico

flores_colorida = "flores.png"
flor_microscopica = "flor_microscopica.png"

max_intensidade_rgb = 255

class CanalCor(Enum):
    R = 1
    G = 2
    B = 3

class TipoChave(Enum):
    INTENSIDADE_VALOR = 1
    VALOR_INTENSIDADE = 2

def salvar_imagem(imagem: Image, pasta: str, nome_imagem: str):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens\\"+pasta, nome_imagem)
    imagem.save(caminho_imagem)

def obter_arquivo_imagem(nome_imagem: str) -> Image :
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens\\entrada", nome_imagem)

    return Image.open(caminho_imagem)

def plotar_grafico(intensidades):
    chaves = list(intensidades.keys())
    valores = list(intensidades.values())
    cont = 0
    for valor in valores:
        cont += valor
    # print(cont)

    fig, aux = plotador_grafico.subplots()

    aux.bar(chaves, valores)
    plotador_grafico.title('Histograma')
    plotador_grafico.xlabel('Intensidade')
    plotador_grafico.ylabel('Ocorrências')
    
    plotador_grafico.show()

def inicializar_registro_frenquencias() -> dict:
    frequencias: dict = {}
    for i in range(0, 256):
        frequencias[i] = 0
    return frequencias

def especificar_histograma(quantidade_pixels: int) -> dict:
    frequencias_intensidades: dict = inicializar_registro_frenquencias()
    cont = 0
    while(cont < 256 and quantidade_pixels > 0):
        print(f'Restam {quantidade_pixels} pixels para distribuição')
        while(True):
            intensidade = int(input("Digite a intensidade [0, 255]: "))
            frequencia = int(input(f'Digite a frequência [0, {quantidade_pixels}]: '))

            if (intensidade < 0 or intensidade > 255) or (frequencia < 0 or frequencia > quantidade_pixels):
                print("Valores digitados incorretamente. Digite novamente!")
            else:
                if intensidade not in frequencias_intensidades:
                    frequencias_intensidades[intensidade] = frequencia
                else:
                    frequencias_intensidades[intensidade] = frequencias_intensidades[intensidade] + frequencia
                
                quantidade_pixels -= frequencia
                break
        cont += 1
    
    return frequencias_intensidades

def calcular_distribuicao_normalizada(frequencias_intensidades: dict, quantidade_pixels: int, max_intensidade: int) -> dict:
    distribuicao_acumulada = 0
    registro_distribuicao_comulativa: dict = {}
    for chave, valor in frequencias_intensidades.items():
        distribuicao_acumulada += valor
        valor_distribuicao = distribuicao_acumulada / quantidade_pixels
        cdf_normalizado = round(valor_distribuicao * max_intensidade)
        registro_distribuicao_comulativa[chave] = cdf_normalizado

    return registro_distribuicao_comulativa

def criar_imagem_equalizada_em_canal_cor(imagem_original: Image, equalizacao: dict, canalCor: CanalCor) -> Image:
    imagem_equalizada = Image.new('RGB', imagem_original.size)
    matriz_imagem_origem = imagem_original.convert("RGB").load()
    largura, altura = imagem_original.size

    for l in range(largura):
        for a in range(altura):
            r, g, b = matriz_imagem_origem[l, a]

            if canalCor == CanalCor.R:
                if r in equalizacao:
                    imagem_equalizada.putpixel((l, a), (equalizacao[r], g, b))
                else:
                    imagem_equalizada.putpixel((l, a), (r, g, b))
            if canalCor == CanalCor.G:
                if g in equalizacao:
                    imagem_equalizada.putpixel((l, a), (r, equalizacao[g], b))
                else:
                    imagem_equalizada.putpixel((l, a), (r, g, b))
            if canalCor == CanalCor.B:
                if b in equalizacao:
                    imagem_equalizada.putpixel((l, a), (r, g, equalizacao[b]))
                else:
                    imagem_equalizada.putpixel((l, a), (r, g, b))

    return imagem_equalizada

def calcular_valores_intensidade_em_canal_cor(imagem: Image, canalCor: CanalCor) -> tuple[int, dict, int, int]:
    matriz_pixels = imagem.convert("RGB").load()
    largura = imagem.size[0]
    comprimento = imagem.size[1]
    valores_intensidade = inicializar_registro_frenquencias()
    quantidade_pixels = largura * comprimento
    max_intensidade = 0
    min_intensidade = 255
    for l in range(0, largura):
        for c in range(0, comprimento):
            r, g, b = matriz_pixels[l, c]
            intensidade = -1
            if canalCor == CanalCor.R:
                intensidade = r
            if canalCor == CanalCor.G:
                intensidade = g
            if canalCor == CanalCor.B:
                intensidade = b

            max_intensidade = max(max_intensidade, intensidade)
            min_intensidade = min(min_intensidade, intensidade)

            valores_intensidade[intensidade] = (valores_intensidade[intensidade] + 1)
    return (quantidade_pixels, valores_intensidade, min_intensidade, max_intensidade)

def criar_imagem_com_equalizacao_especificada_em_canal_cor(imagem_original: Image, equalizacao: dict, histograma_especificado: dict, canalCor: CanalCor) -> Image:
    imagem_equalizada = Image.new('RGB', imagem_original.size)
    matriz_imagem_origem = imagem_original.load()
    largura, altura = imagem_original.size

    for l in range(largura):
        for a in range(altura):
            r, g, b = matriz_imagem_origem[l, a]
            #Define qual o canal selecionado para a intensidade.  -1 por que não é uma intensidade
            intensidade = -1
            if canalCor == CanalCor.R:
                intensidade = r

            if canalCor == CanalCor.G:
                intensidade = g

            if canalCor == CanalCor.B:
                intensidade = b

            valor_mapeado = -1
            if intensidade in equalizacao:
                if equalizacao[intensidade] in histograma_especificado:
                    valor_mapeado = histograma_especificado[equalizacao[intensidade]]

            if valor_mapeado != -1 and canalCor == CanalCor.R:
                imagem_equalizada.putpixel((l, a), (valor_mapeado, g, b))

            elif valor_mapeado != -1 and canalCor == CanalCor.G:
                imagem_equalizada.putpixel((l, a), (r, valor_mapeado, b))
            
            elif valor_mapeado != -1 and canalCor == CanalCor.B:
                imagem_equalizada.putpixel((l, a), (r, g, valor_mapeado))
            else:
                imagem_equalizada.putpixel((l, a), (r, g, b))

    return imagem_equalizada

def criar_mapeamento_intensidade(intensidades_mapeadas: dict, quantidade_pixels: int, tipoChave: TipoChave, max_intensidade: int):
    mapeamento_intensidades: dict = {}
    quantidade_pixels_acumulados = 0
    for chave, valor in intensidades_mapeadas.items():
        quantidade_pixels_acumulados += valor
        valor_mapeado = round((quantidade_pixels_acumulados / quantidade_pixels) * max_intensidade)

        if tipoChave == TipoChave.INTENSIDADE_VALOR and quantidade_pixels_acumulados != 0:
            mapeamento_intensidades[chave] = valor_mapeado
        elif tipoChave == TipoChave.VALOR_INTENSIDADE and quantidade_pixels_acumulados != 0:
            mapeamento_intensidades[valor_mapeado] = chave
    return mapeamento_intensidades

def main():
    canalCorEscolhido = CanalCor.B
    nomeImagemEscolhida = flor_microscopica

    imagem_original: Image = obter_arquivo_imagem(nomeImagemEscolhida)
    quantidade_pixels, intensidades, min_intensidade, max_intensidade = calcular_valores_intensidade_em_canal_cor(imagem_original, canalCorEscolhido)
    intensidades_normalizadas = calcular_distribuicao_normalizada(intensidades, quantidade_pixels, max_intensidade)

    imagem_equalizada_em_canal_cor = criar_imagem_equalizada_em_canal_cor(imagem_original, intensidades_normalizadas, canalCorEscolhido)
    # pratica01.salvar_imagem(imagem_equalizada_em_canal_cor, "equalizada_canal_cor", "imagem_equalizada_canal_cor_"+canalCorEscolhido.name+"_"+nomeImagemEscolhida)
    
    salvar_imagem(imagem_equalizada_em_canal_cor, "equalizada_canal_cor", "imagem_equalizada_em_canal_cor_"+canalCorEscolhido.name+"_"+nomeImagemEscolhida)
    # intensidades_mapeadas_imagem_original = criar_mapeamento_intensidade(intensidades, quantidade_pixels, TipoChave.INTENSIDADE_VALOR, max_intensidade)
    # # print(len(intensidades_mapeadas_imagem_original))
    # for chave, valor in intensidades_mapeadas_imagem_original.items():
    #     print(f'{chave} = {valor}')
    
    # histograma_especificado = especificar_histograma(quantidade_pixels)

    # intensidades_mapeadas_imagem_especificada = criar_mapeamento_intensidade(histograma_especificado, quantidade_pixels, TipoChave.VALOR_INTENSIDADE, max_intensidade)
    # for chave, valor in intensidades_mapeadas_imagem_especificada.items():
    #     print(f'{chave} = {valor}')

    # imagem_especificada_em_canal_de_cor: Image = criar_imagem_com_equalizacao_especificada_em_canal_cor(imagem_original, intensidades_mapeadas_imagem_original, intensidades_mapeadas_imagem_especificada, canalCorEscolhido)
    quantidade_pixels_es, intensidades_es, min_intensidade_es, max_intensidade_es = calcular_valores_intensidade_em_canal_cor(imagem_original, canalCorEscolhido)
    # salvar_imagem(imagem_especificada_em_canal_de_cor, "especificada_canal_cor", "imagem_especificada_em_canal_cor_"+canalCorEscolhido.name+"_"+nomeImagemEscolhida)

    plotar_grafico(intensidades)
    plotar_grafico(intensidades_es)

main()