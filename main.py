import PIL.Image as Image
import matplotlib.pyplot as plt
import numpy as np

TAUX_COMP = 16

#Calcule du niveau de gris de l'image
def gray_scale(T):

    bw = np.empty_like(T, shape=(T.shape[0], T.shape[1]))
    for i in range(T.shape[0]):
        for j in range(T.shape[1]):
            r, v, b, _ = T[i][j]
            white = int((int(r * 0.2126) + int(v * 0.7152) + int(b * 0.0722))/3)
            bw[i][j] = white

    return bw

#Réduction de la taille de l'image
def compresser(T):

    somme = 0
    if TAUX_COMP == 1:
        div = 1
    else:
        div = 2

    compJ = np.empty_like(T, shape=(T.shape[0], int(T.shape[1]/(TAUX_COMP/div))))
    for i in range(T.shape[0]):
        for j in range(T.shape[1]):

            if j%(TAUX_COMP/2) == 0 and j > 0:

                compJ[i][int((j-(TAUX_COMP/div))/(TAUX_COMP/div))] = int(somme/(TAUX_COMP/div))
                somme = 0

            somme = somme + T[i][j]

    somme = 0

    comp = np.empty_like(compJ, shape=(int(compJ.shape[0]/TAUX_COMP), compJ.shape[1]))
    for j in range(compJ.shape[1]):
        for i in range(compJ.shape[0]):

            if i%TAUX_COMP == 0 and i > 0:

                comp[int((i-TAUX_COMP)/TAUX_COMP)][j] = int(somme/TAUX_COMP)
                somme = 0

            somme += compJ[i][j]

        comp[-1][j] = (somme/TAUX_COMP)

    return comp

#Transformation du niveau de gris en caractère
def gray_char(T):

    char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

    gc = []
    for i in range(T.shape[0]):
        gc.append([])
        for j in range(T.shape[1]):
            gc[i].append([])

    for i in range(T.shape[0]):
        for j in range(T.shape[1]):
            gc[i][j] = char[int(T[i][j] * (len(char)-1) / 255)]

    return gc

#Sauvegarde de l'image en caractère dans un fichier save.txt
def save(T):

    File = open("save.txt", "a")

    for i in range(len(T)):
        for j in range(len(T[i])):
            File.write(T[i][j])
        File.write("\n")

    File.close()

#image a transformer
image = Image.open("./photocorse.png")

imageTab = np.array(image)

#Test qui l'image est bien en RGBA
if image.mode == "RGBA":
    save(gray_char(compresser(gray_scale(imageTab))))
else:
    print("Format d'image incorrect : " + image.mode + " (RGBA attendu !)")
