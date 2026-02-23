import numpy as np
import cv2
from skimage import util
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import filedialog, messagebox

# ------------------------------
# GERAR MULTILOOK
# ------------------------------
def aplicar_multilook(img, ruido="gaussian", n_looks=5):
    looks = []

    for i in range(n_looks):
        if ruido == "gaussian":
            noisy = util.random_noise(img, mode="gaussian", var=0.01)

        elif ruido == "speckle":
            noisy = util.random_noise(img, mode="speckle")

        elif ruido == "s&p":
            noisy = util.random_noise(img, mode="s&p", amount=0.05)

        elif ruido == "poisson":
            noisy = util.random_noise(img, mode="poisson")

        elif ruido == "uniform":
            noise = np.random.uniform(-0.1, 0.1, img.shape)
            noisy = np.clip(img + noise, 0, 1)

        else:
            noisy = img.copy()

        looks.append(noisy)

    return np.array(looks)


# ------------------------------
# TENDÊNCIA CENTRAL
# ------------------------------
def calcular_tendencias(looks):
    mean_img = np.mean(looks, axis=0)
    median_img = np.median(looks, axis=0)

    # Otimização da moda (evita lentidão)
    looks_int = (looks * 255).astype(np.uint8)
    mode_img = stats.mode(looks_int, axis=0, keepdims=False)[0] / 255.0

    return mean_img, median_img, mode_img


# ------------------------------
# GUI
# ------------------------------
img = None


def selecionar_imagem():
    global img

    caminho = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )

    if caminho:
        img = cv2.imread(caminho)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0

        messagebox.showinfo("Imagem carregada", f"{caminho}")


# ------------------------------
# APLICAR EFEITOS (COM NAVEGAÇÃO)
# ------------------------------
def aplicar_efeitos():
    global img

    if img is None:
        messagebox.showwarning("Aviso", "Nenhuma imagem selecionada!")
        return

    tipos_ruido = [
        ("gaussian", "Gaussiano (Aditivo)"),
        ("speckle", "Speckle (Multiplicativo)"),
        ("s&p", "Salt & Pepper"),
        ("poisson", "Poisson"),
        ("uniform", "Uniforme")
    ]

    messagebox.showinfo("Processando", "Gerando simulações... Aguarde.")

    resultados = []

    for tipo, nome in tipos_ruido:
        looks = aplicar_multilook(img, ruido=tipo, n_looks=5)
        mean_img, median_img, mode_img = calcular_tendencias(looks)

        # Corrige o erro (normalização)
        diff = np.abs(img - mean_img)
        if diff.max() != 0:
            diff = diff / diff.max()

        resultados.append({
            "nome": nome,
            "ruido": looks[0],
            "media": mean_img,
            "mediana": median_img,
            "moda": mode_img,
            "erro": diff
        })

    estado = {"indice": 0}

    fig, axs = plt.subplots(2, 3, figsize=(15, 8))

    im_original = axs[0, 0].imshow(img)
    axs[0, 0].set_title("Original")
    axs[0, 0].axis("off")

    im_ruido = axs[0, 1].imshow(resultados[0]["ruido"])
    axs[0, 1].set_title("Ruído")
    axs[0, 1].axis("off")

    im_media = axs[0, 2].imshow(resultados[0]["media"])
    axs[0, 2].set_title("Média")
    axs[0, 2].axis("off")

    im_mediana = axs[1, 0].imshow(resultados[0]["mediana"])
    axs[1, 0].set_title("Mediana")
    axs[1, 0].axis("off")

    im_moda = axs[1, 1].imshow(resultados[0]["moda"])
    axs[1, 1].set_title("Moda")
    axs[1, 1].axis("off")

    im_erro = axs[1, 2].imshow(resultados[0]["erro"], cmap='gray')
    axs[1, 2].set_title("Erro (o quanto mudou da original)")
    axs[1, 2].axis("off")

    def atualizar():
        r = resultados[estado["indice"]]

        im_ruido.set_data(r["ruido"])
        im_media.set_data(r["media"])
        im_mediana.set_data(r["mediana"])
        im_moda.set_data(r["moda"])
        im_erro.set_data(r["erro"])

        fig.suptitle(f"{r['nome']} ({estado['indice']+1}/{len(resultados)})", fontsize=14)

        fig.canvas.draw_idle()

    def on_key(event):
        if event.key == "right":
            estado["indice"] = (estado["indice"] + 1) % len(resultados)
            atualizar()

        elif event.key == "left":
            estado["indice"] = (estado["indice"] - 1) % len(resultados)
            atualizar()

    fig.canvas.mpl_connect("key_press_event", on_key)

    #  Corrige sobreposição do título
    fig.tight_layout(rect=[0, 0, 1, 0.92])

    plt.show()


# ------------------------------
# INTERFACE
# ------------------------------
root = tk.Tk()
root.title("Simulação Multilook")
root.geometry("900x700")

btn_select = tk.Button(root, text="Selecionar Imagem", command=selecionar_imagem)
btn_select.pack(pady=10)

btn_apply = tk.Button(root, text="Aplicar Efeitos", command=aplicar_efeitos)
btn_apply.pack(pady=10)

root.mainloop()