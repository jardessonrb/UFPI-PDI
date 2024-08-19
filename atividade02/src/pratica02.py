# Site de converção de RBG para HSV: https://www.peko-step.com/pt/tool/hsvrgb.html
from PIL import Image
import os
import math

def salvar_imagem(imagem: Image, pasta: str, nome_imagem: str):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens\\"+pasta, nome_imagem)
    imagem.save(caminho_imagem)

def obter_arquivo_imagem(nome_imagem: str) -> Image :
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagem = os.path.join(diretorio_atual, "imagens\\entrada", nome_imagem)

    return Image.open(caminho_imagem)

def calcular_hue(delta, max_intensidade, r_linha, g_linha, b_linha):
    mod = 6
    angulo = 60

    if(delta == 0):
        return 0

    if(max_intensidade == r_linha):
        return (angulo * (((g_linha - b_linha) / delta) % mod))
    
    if(max_intensidade == g_linha):
        return (angulo * (((b_linha - r_linha) / delta) + 2))
    
    if(max_intensidade == b_linha):
        return (angulo * (((r_linha - g_linha) / delta) + 4))

def calcular_saturation(delta_intensidade, max_intensidade):
    return (0 if (max_intensidade == 0)  else (delta_intensidade / max_intensidade))

def calcular_porcentagem_para_valor(porcentagem):
    return round(255 * porcentagem)

def calcular_valor_para_porcentagem(valor):
    return round(((100 * valor) / 255) / 100)



def rgb_to_hsv(r: int, g: int, b:int) -> tuple:
    valor_maximo_intensidade = 255
    r_linha = r/valor_maximo_intensidade
    g_linha = g/valor_maximo_intensidade
    b_linha = b/valor_maximo_intensidade

    max_intensidade = max(r_linha, g_linha, b_linha)
    min_intensidade = min(r_linha, g_linha, b_linha)

    delta_intensidade = max_intensidade - min_intensidade

    h_hue = calcular_hue(delta_intensidade, max_intensidade, r_linha, g_linha, b_linha)
    s_saturation = calcular_saturation(delta_intensidade, max_intensidade)
    v_value = max_intensidade

    return (round(h_hue), calcular_porcentagem_para_valor(s_saturation), calcular_porcentagem_para_valor(v_value))

def calcular_rgb_linha(intensidade_x, intensidade_c, h_hue):
    if(h_hue >= 0 and h_hue < 60):
        return (intensidade_c, intensidade_x, 0)
    elif(h_hue >= 60 and h_hue < 120):
        return (intensidade_x, intensidade_c, 0)
    elif(h_hue >= 120 and h_hue < 180):
        return (0, intensidade_c, intensidade_x)
    elif(h_hue >= 180 and h_hue < 240):
        return (0, intensidade_x, intensidade_c)
    elif(h_hue >= 240 and h_hue < 300):
        return (intensidade_x, 0, intensidade_c)
    else:
        return (intensidade_c, 0, intensidade_x)


def hsv_to_rgb(h, s, v):
    angulo = 60
    valor_maximo = 255
    s = calcular_valor_para_porcentagem(s)
    v = calcular_valor_para_porcentagem(v)

    valor_intensidade_c = v * s
    valor_intensidade_x = (valor_intensidade_c * (1 - abs((h / angulo) % 1)))
    valor_intensidade_m = v - valor_intensidade_c

    r_linha, g_linha, b_linha = calcular_rgb_linha(valor_intensidade_x, valor_intensidade_c, h)

    r = ((r_linha + valor_intensidade_m) * valor_maximo)
    g = ((g_linha + valor_intensidade_m) * valor_maximo)
    b = ((b_linha + valor_intensidade_m) * valor_maximo)

    return (math.floor(r), math.floor(g), math.floor(b))

def transformar_modelo_colorido_para_preto_branco(r: int, g:int, b:int) -> tuple[int, int, int]:
    intensidade: int = round((r + g + b) / 3)

    return (intensidade, intensidade, intensidade)

def separar_canal_cor(r: int, g:int, b:int) -> dict[str, tuple[int, int, int]]:
    canais: dict[str, tuple[int, int, int]] = {}

    canais["r"] = (r, 0, 0)
    canais["g"] = (0, g, 0)
    canais["b"] = (0, 0, b)

    return canais

def separar_imagem_em_canais_cores(nome_imagem: str):
    imagem_origem: Image = obter_arquivo_imagem(nome_imagem)
    largura, altura = imagem_origem.size

    imagem_canal_r: Image = Image.new("RGB", imagem_origem.size)
    imagem_canal_g: Image = Image.new("RGB", imagem_origem.size)
    imagem_canal_b: Image = Image.new("RGB", imagem_origem.size)
    matriz_pixels_imagem_origem = imagem_origem.load()
    for l in range(largura):
        for a in range(altura):
            r, g, b = matriz_pixels_imagem_origem[l, a]
            canais: dict[str, tuple[int, int, int]] = separar_canal_cor(r, g, b)
            imagem_canal_r.putpixel((l, a), canais["r"])
            imagem_canal_g.putpixel((l, a), canais["g"])
            imagem_canal_b.putpixel((l, a), canais["b"])

    salvar_imagem(imagem_canal_r, "canais", "imagem_canal_r_"+nome_imagem)
    salvar_imagem(imagem_canal_g, "canais", "imagem_canal_g_"+nome_imagem)
    salvar_imagem(imagem_canal_b, "canais", "imagem_canal_b_"+nome_imagem)

def trasnformar_imagem_para_preto_branco(nome_imagem: str):
    imagem_origem: Image = (obter_arquivo_imagem(nome_imagem)).convert("RGB")
    largura, altura = imagem_origem.size

    imagem_preto_branco: Image = Image.new("RGB", imagem_origem.size)
    matriz_pixels_imagem_origem = imagem_origem.load()
    for l in range(largura):
        for a in range(altura):
            r, g, b = matriz_pixels_imagem_origem[l, a]
            cor_preto_branco: tuple[int, int, int] = transformar_modelo_colorido_para_preto_branco(r, g, b)
            imagem_preto_branco.putpixel((l, a), cor_preto_branco)
            
    salvar_imagem(imagem_preto_branco, "preto_branco", "imagem_preto_branco_"+nome_imagem)

def main():
    # rgb = (255,0,16)
    # hsv = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    # print(f'valor rgb = {rgb} => hsv = {hsv}')
    # print('\n')
    # novo_rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    # print(f'valor hsv = {hsv} => rgb = {novo_rgb}')

    # separar_imagem_em_canais_cores("flores.png")
    trasnformar_imagem_para_preto_branco("flores.png")
main()