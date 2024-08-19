import os
from PIL import Image


def save_list_to_txt(integer_list, filename):
    """
    Grava uma lista de inteiros em um arquivo de texto.

    :param integer_list: Lista de inteiros a ser gravada no arquivo.
    :param filename: Nome do arquivo onde a lista será salva.
    """
    with open(filename, 'w') as file:
        file.write(f"const unsigned char texture_data_2[TEXTURE_WIDTH * TEXTURE_HEIGHT * 3] = {{\n")
        cont = 0
        for number in integer_list:
            file.write(f"{number}, ")
            if cont == 17:
                file.write(f"\n")
                cont = 0
            cont += 1
        file.write(f"}}")


def obter_arquivo_imagem(nome_imagem: str) -> Image :
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens_extracao", nome_imagem)

    return Image.open(caminho_imagem)

def extrair(imagem: Image):
    matriz = imagem.convert("RGB").load()
    largura, altura = imagem.size
    pixels_imagem = []

    for l in range(largura):
        for a in range(altura):
            r, g, b = matriz[l, a]
            pixels_imagem.append(r)
            pixels_imagem.append(g)
            pixels_imagem.append(b)
    # for pixel in pixels_imagem:
    #     print(pixel)

    print(len(pixels_imagem))
    save_list_to_txt(pixels_imagem, "array_text.text")

imagem = obter_arquivo_imagem("parede_madeira.jpg")
extrair(imagem)