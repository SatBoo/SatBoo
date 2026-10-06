# JOGO DA RAPOSA - Passo 7: o gamba (pule por cima dele)
# Computacao Grafica e PDI - ENGCO231N01-SED
# Rode com:  python3 passo7_gamba.py   (setas andam, ESPACO pula, ESC sai)
# Imagens: Sunny Land, de ansimuz (dominio publico). Fonte: Press Start 2P (licenca OFL).
import os, random, shutil, sys
import tkinter as tk
 
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
 
# A fonte .ttf precisa ser instalada antes de abrir a janela
FONTE = os.path.join(PASTA, "PressStart2P-Regular.ttf")
if sys.platform == "win32":
    import ctypes
    ctypes.windll.gdi32.AddFontResourceExW(FONTE, 0x10, 0)
else:
    destino = os.path.expanduser("~/Library/Fonts" if sys.platform == "darwin" else "~/.fonts")
    os.makedirs(destino, exist_ok=True)
    shutil.copy(FONTE, destino)
 
janela = tk.Tk()
janela.title("Raposa e cerejas")
tela = tk.Canvas(janela, width=768, height=480, highlightthickness=0)
tela.pack()
 
# Recortar um pedaco da imagem (x, y, largura, altura), com o dobro do tamanho
def recorta(arquivo, x, y, largura, altura, espelhado=False):
    folha = tk.PhotoImage(file=os.path.join(PASTA, arquivo))
    quadro = tk.PhotoImage()
    lado = -1 if espelhado else 1
    quadro.tk.call(quadro, "copy", folha, "-from", x, y, x + largura, y + altura,
                   "-zoom", 2, 2, "-subsample", lado, 1)
    return quadro
 
corre_dir = [recorta("raposa-corre.png", i * 33, 0, 33, 32) for i in range(6)]
corre_esq = [recorta("raposa-corre.png", i * 33, 0, 33, 32, True) for i in range(6)]
parada_dir = [recorta("raposa-parada.png", i * 33, 0, 33, 32) for i in range(4)]
parada_esq = [recorta("raposa-parada.png", i * 33, 0, 33, 32, True) for i in range(4)]
pulo_dir = [recorta("raposa-pulo.png", i * 33, 0, 33, 32) for i in range(2)]
pulo_esq = [recorta("raposa-pulo.png", i * 33, 0, 33, 32, True) for i in range(2)]
gamba = [recorta("gamba.png", i * 36, 0, 36, 28) for i in range(6)]
cereja = [recorta("cereja.png", i * 21, 0, 21, 21) for i in range(5)]
grama = recorta("chao.png", 16, 16, 16, 16)
terra = recorta("chao.png", 16, 48, 16, 16)
 
# Cenario em camadas: o que e desenhado depois fica na frente
fundo = tk.PhotoImage(file=os.path.join(PASTA, "fundo.png")).zoom(2)
ilha = tk.PhotoImage(file=os.path.join(PASTA, "ilha.png")).zoom(2)
tela.create_image(0, 0, image=fundo, anchor="nw")
tela.create_image(560, 80, image=ilha, anchor="n")
for x in range(0, 768, 32):
    tela.create_image(x, 416, image=grama, anchor="nw")
    tela.create_image(x, 448, image=terra, anchor="nw")
 
CHAO = 352
x, y, vy, olhando, passo, pontos = 100, CHAO, 0, "dir", 0, 0
cx, cy = 500, 330
gx = 800
raposa = tela.create_image(x, y, image=parada_dir[0], anchor="nw")
bicho = tela.create_image(gx, 360, image=gamba[0], anchor="nw")
fruta = tela.create_image(cx, cy, image=cereja[0])
sombra = tela.create_text(22, 22, anchor="nw", font=("Press Start 2P", 16), fill="black")
placar = tela.create_text(20, 20, anchor="nw", font=("Press Start 2P", 16), fill="white")
 
teclas = set()
janela.bind("<KeyPress>", lambda e: teclas.add(e.keysym))
janela.bind("<KeyRelease>", lambda e: teclas.discard(e.keysym))
janela.bind("<Escape>", lambda e: janela.destroy())
 
# O game loop: ler teclas, mover, escolher o quadro, desenhar
def quadro():
    global x, y, vy, olhando, passo, pontos, cx, cy, gx
    andando = False
    if "Right" in teclas:
        x, olhando, andando = x + 6, "dir", True
    if "Left" in teclas:
        x, olhando, andando = x - 6, "esq", True
    if "space" in teclas and y == CHAO:
        vy = -18
    vy = vy + 1.5
    y = min(y + vy, CHAO)
    x = max(0, min(x, 700))
    passo = passo + 1
 
    if y < CHAO:
        lista = pulo_dir if olhando == "dir" else pulo_esq
        imagem = lista[0] if vy < 0 else lista[1]
    elif andando:
        lista = corre_dir if olhando == "dir" else corre_esq
        imagem = lista[passo % 6]
    else:
        lista = parada_dir if olhando == "dir" else parada_esq
        imagem = lista[passo // 3 % 4]
 
    if abs(x + 33 - cx) < 40 and abs(y + 32 - cy) < 40:
        pontos = pontos + 1
        cx, cy = random.randint(60, 700), random.randint(250, 390)
 
    gx = gx - 5
    if gx < -80:
        gx = 800
    if abs(x + 33 - (gx + 36)) < 45 and y > CHAO - 40:
        pontos, gx = 0, 800
 
    tela.coords(bicho, gx, 360)
    tela.itemconfig(bicho, image=gamba[passo // 2 % 6])
    tela.coords(raposa, x, y)
    tela.itemconfig(raposa, image=imagem)
    tela.coords(fruta, cx, cy)
    tela.itemconfig(fruta, image=cereja[passo // 3 % 5])
    tela.itemconfig(sombra, text=f"CEREJAS {pontos}")
    tela.itemconfig(placar, text=f"CEREJAS {pontos}")
    janela.after(33, quadro)
 
quadro()
janela.mainloop()
