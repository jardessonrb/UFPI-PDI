import os
from enum import Enum
from PIL import Image
import matplotlib.pyplot as plotador_grafico

class TipoChave(Enum):
    INTENSIDADE_VALOR = 1
    VALOR_INTENSIDADE = 2

max_intensidade: int = 255
novo_histograma = []

def evento_click_grafico(evento):
    if evento.inaxes:
        x, y = evento.xdata, evento.ydata
        print(f'Você clicou nas coordenadas x={x}, y={y}')
        novo_valor = (round(x), round(y))
        novo_histograma.append(novo_valor)

def salvar_imagem(imagem: Image, pasta: str, nome_imagem: str):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens\\"+pasta, nome_imagem)
    imagem.save(caminho_imagem)

def plotar_grafico(intensidades):
    chaves = list(intensidades.keys())
    valores = list(intensidades.values())

    fig, aux = plotador_grafico.subplots()

    aux.bar(chaves, valores)
    plotador_grafico.title('Histograma')
    plotador_grafico.xlabel('Intensidade')
    plotador_grafico.ylabel('Ocorrências')

    plotador_grafico.show()

def obter_arquivo_imagem(nome_imagem: str) -> Image :
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens\\entrada", nome_imagem)

    return Image.open(caminho_imagem)

def inicializar_registro_frenquencias() -> dict:
    frequencias: dict = {}
    for i in range(0, 256):
        frequencias[i] = 0
    return frequencias

def calcular_distribuicao_normalizada(frequencias_intensidades: dict, quantidade_pixels: int, max_intensidade: int) -> dict:
    distribuicao_acumulada = 0
    registro_distribuicao_comulativa: dict = {}
    # Cada intensidade com sua distribuição de pixels- chave = intensidade e valor = ocorrências
    for chave, valor in frequencias_intensidades.items():
        distribuicao = (valor + distribuicao_acumulada)
        valor_distribuicao = distribuicao / quantidade_pixels
        cdf_normalizado = round(valor_distribuicao * max_intensidade)
        registro_distribuicao_comulativa[chave] = cdf_normalizado
        distribuicao_acumulada = distribuicao

    return registro_distribuicao_comulativa

def criar_imagem_equalizada(imagem_original: Image, equalizacao: dict) -> Image:
    imagem_equalizada = Image.new('L', imagem_original.size)
    pixels_imagem_original = list(imagem_original.getdata())
    pixels_imagem_equalizada: list = []
    for pixel in pixels_imagem_original:
        r, g, b, a = pixel
        intensidade = round(( r + g + b) / 3)
        if intensidade in equalizacao:
            novo_pixel = int(equalizacao[intensidade])
        else:
            novo_pixel = intensidade
        pixels_imagem_equalizada.append(novo_pixel)
    
    imagem_equalizada.putdata(pixels_imagem_equalizada)

    return imagem_equalizada

def criar_imagem_com_equalizacao_especificada(imagem_original: Image, histograma: dict, histograma_especificado: dict) -> Image:
    imagem_equalizada = Image.new('L', imagem_original.size)
    pixels_imagem_original = list(imagem_original.getdata())
    pixels_imagem_equalizada: list = []
    for pixel in pixels_imagem_original:
        r, g, b, a = pixel
        intensidade = round(( r + g + b) / 3)
        intensidade_pixel = 0
        valor_mapeado = histograma[intensidade]
        if valor_mapeado in histograma_especificado:
            intensidade_pixel = histograma_especificado[valor_mapeado]
        else:
            intensidade_pixel = intensidade
        novo_pixel = int(intensidade_pixel)
        pixels_imagem_equalizada.append(novo_pixel)
    
    imagem_equalizada.putdata(pixels_imagem_equalizada)

    return imagem_equalizada

def calcular_valores_intensidade(imagem: Image) -> tuple[int, dict, int, int]:
    matriz_pixels = imagem.load()
    largura = imagem.size[0]
    comprimento = imagem.size[1]
    valores_intensidade = inicializar_registro_frenquencias()
    quantidade_pixels = largura * comprimento
    max_intensidade = 0
    min_intensidade = 255
    for l in range(0, largura):
        for c in range(0, comprimento):
            intensidade = 0
            if imagem.mode == 'L':
                intensidade = matriz_pixels[l, c]
            else:
                r, g, b, a = matriz_pixels[l, c]
                intensidade = round((r + g + b) / 3)

            max_intensidade = max(max_intensidade, intensidade)
            min_intensidade = min(min_intensidade, intensidade)
            # print(f'R[{r}], G[{g}], B[{b}] = Intensidade[{intensidade}]')

            if intensidade not in valores_intensidade:
                valores_intensidade[intensidade] = 1
            else:
                valores_intensidade[intensidade] = (valores_intensidade[intensidade] + 1)

    return (quantidade_pixels, valores_intensidade, min_intensidade, max_intensidade)

def criar_mapeamento_intensidade(intensidades_mapeadas: dict, quantidade_pixels: int, tipoChave: TipoChave):
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

def especificar_histograma(quantidade_pixels: int, max_intensidade) -> dict:
    frequencias_intensidades: dict = inicializar_registro_frenquencias()

    while(quantidade_pixels > 0):
        print(f'Restam {quantidade_pixels} pixels para distribuição')
        while(True):
            intensidade = int(input(f'Digite a intensidade [0, {max_intensidade}]: '))
            frequencia = int(input(f'Digite a frequência [0, {quantidade_pixels}]: '))

            if (intensidade < 0 or intensidade > max_intensidade) or (frequencia < 0 or frequencia > quantidade_pixels):
                print("Valores digitados incorretamente. Digite novamente!")
            else:
                if intensidade not in frequencias_intensidades:
                    frequencias_intensidades[intensidade] = frequencia
                else:
                    frequencias_intensidades[intensidade] = frequencias_intensidades[intensidade] + frequencia
                
                quantidade_pixels -= frequencia
                break
    
    return frequencias_intensidades


def gerar_intensidades() -> tuple[dict, dict]:
    origem = {
        0: 790,
        1: 1023,
        2: 850,
        3: 656,
        4: 329,
        5: 245,
        6: 122,
        7: 81
    }

    especificado = {
        0: 0,
        1: 0,
        2: 0,
        3: 790,
        4: 1023,
        5: 850,
        6: 985,
        7: 448
    }
    return origem, especificado

def testar_funcoes(intensidades_origem: dict, intensidades_especificada: dict):
    intensidade_original = criar_mapeamento_intensidade(intensidades_origem, 4096, TipoChave.INTENSIDADE_VALOR)
    intensidade_especificada = criar_mapeamento_intensidade(intensidades_especificada, 4096, TipoChave.VALOR_INTENSIDADE)

    for dicionario in intensidade_original.items():
        print(f'original: {dicionario}')

    
    for dicionario in intensidade_especificada.items():
        print(f'especificado: {dicionario}')

def main():
    imagem_flor = "flores_cinza_escurecidas.png"
    imagem_flor_clara = "flores_cinza_clara.png"
    imagem_flor_contraste = "flores_cinza_escurecida_contraste.png"
    imagem_polen = "flor_microscopica_escurecida_cinza.png"
    imagem_polen_clara = "flor_microscopica_cinza_clara.png"
    imagem_polen_contraste = "flor_microscopica_cinza_escurecida_contraste.png"
    imagem_xadrez = "xadrez.png"

    nomeImagemEscolhida = imagem_polen
    imagem_original: Image = obter_arquivo_imagem(nomeImagemEscolhida)
    quantidade_pixels, intensidades, max_intensidade, min_intensidade = calcular_valores_intensidade(imagem_original)

    # print(f'{max_intensidade} e {min_intensidade}')
    # intensidades_normalizadas = calcular_distribuicao_normalizada(intensidades, quantidade_pixels, 255)

    # imagem_equalizada = criar_imagem_equalizada(imagem_original, intensidades_normalizadas)
    # quantidade_pixels_eq, intensidades_eq, max_intensidade_eq, min_intensidade_eq = calcular_valores_intensidade(imagem_equalizada)
    # salvar_imagem(imagem_equalizada, "equalizadas", "equalizada_"+nomeImagemEscolhida)

    plotar_grafico(intensidades)
    # plotar_grafico(intensidades_eq)

    # for chave, valor in novo_histograma:
    #     print(f'Chave: {chave}, Valor: {valor}')

    intensidades_definidas = especificar_histograma(quantidade_pixels, 255)
    intensidades_imagem_original = criar_mapeamento_intensidade(intensidades, quantidade_pixels, TipoChave.INTENSIDADE_VALOR)
    intensidades_mapeadas_especificadas = criar_mapeamento_intensidade(intensidades_definidas, quantidade_pixels, TipoChave.VALOR_INTENSIDADE)
    imagem_especificada: Image = criar_imagem_com_equalizacao_especificada(imagem_original, intensidades_imagem_original, intensidades_mapeadas_especificadas)
    quantidade_pixels_e, intensidades_e, max_intensidade_e, min_intensidade_e = calcular_valores_intensidade(imagem_especificada)

    # plotar_grafico(intensidades)
    plotar_grafico(intensidades_e)

    salvar_imagem(imagem_especificada, "especificadas", "especificadas_"+nomeImagemEscolhida)

    # dict1, dict2 = gerar_intensidades()
    # testar_funcoes(dict1, dict2)

    # cont = 0
    # for chave, valor in intensidades_imagem_original.items():
    #     print(f'[{chave}] = {valor}')
    #     cont += 1
    #     # if  cont == 100:
    #     #     break
    # print(quantidade_pixels)
        
if __name__ == '__main__':
    main()