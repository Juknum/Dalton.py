# /--/ Projet BAC - Julien CONSTANT TS1 & Mylene POZAR TS2 - 2018/2019
# /-/ Comment les autres percoivent-ils les couleurs ?
# / Le daltonisme et autres conditions de vue (animaux domestiques notamment)
# v1.1

''' Definition rapide du daltonisme
l'oeil humain comporte trois cônes de couleurs (L, M, S) qui sont respectivement associés aux couleurs (Red, Green, Blue). Le daltonisme est reconnu comme étant une maladie génétique
qui modifie la structure des cônes et par conséquent la perception des couleurs, ainsi la perception d'une des trois couleurs peut être annihilée ou perturbée.
'''

# /-/ liens utiles :
# http://python.jpvweb.com/python/mesrecettespython/doku.php?id=dialogue_tkfiledialog
# coeff des cones pour daltonien :
# https://ixora.io/projects/colorblindness/color-blindness-simulation-research/
# http://vision.psychol.cam.ac.uk/jdmollon/papers/colourmaps.pdf


# /-/ importation des modules nécessaires:

tk = 0

try:
    from tkinter import *
    from tkinter import filedialog
    from tkinter.messagebox import *
except ImportError:
    print("Erreur d'import tkinter")
else:
    print("Importation réussie de tkinter")
    tk = 1

try:
    import os
except ImportError:
    print("Erreur d'import de os")
    if tk == 1:
        win_error = Tk()
        showinfo("Message à caractère informatif", "Le module os ne fonctionne pas")
        win_error.destroy()
else:
    print("Importation réussie de os")

try:
    from PIL import Image
except ImportError:
    print("Erreur d'import de PIL")
    if tk == 1:
        win_error = Tk()
        showinfo("Message à caractère informatif", "Le module PIL ne fonctionne pas")
        win_error.destroy()
else:
    print("Importation réussie de PIL")

# /-/ variables :
# / variables, menu editer l'image

saved_file = ""
open_file = ""

# / variables, checkbox

pic_d_check = False
pic_f_check = False

# /-/ fonctions du menu :
# // fonctions du menu fichier :


def open_file():  # pic_d_.. = pic_default
    global pic_d_pil, pic_d_tk, default_canvas, pic_d_check, pic_d_canvas
    print("Action : open_file")

    pic_d_path = filedialog.askopenfilename(title="Ouverture d'une image", initialdir="fic", multiple=False, filetypes=(("fichier PNG", "*.png"), ("fichier JPEG", "*.jpg"), ("fichier GIF", ".gif"), ("tout les fichiers", "*.*")))
    print(pic_d_path)

    # Convertion en PNG (si JPEG)
    path, ext = os.path.splitext(pic_d_path)
    if ext == ".jpg" or ".gif":  # si l'extension est jpg ou gif
        print("conversion en png")

        # on créer une image png
        pic = Image.open(pic_d_path)
        pic.save(path + ".png")

        # on actualise le chemin d'acces
        pic_d_path = path + ".png"
        pic_d_pil = Image.open(pic_d_path)

    elif ext == ".png":  # si l'extension est png
        print("pas de conversion en png")
        pic_d_pil = Image.open(pic_d_path)
    else:
        showinfo("Message à caractère informatif", "Le fichier n'est pas supporté (extension)")

    # Test RGBA ou P ou RGB :
    pal = pic_d_pil.getbands()
    print(pal)

    if pal == ('R', 'G', 'B', 'A'):
        print("RGBA : oui et conversion en RGB")
        # Convertion RGBA à RGB
        pic_d_pil_rgb = Image.new("RGB", pic_d_pil.size, (255, 255, 255))
        pic_d_pil_rgb.paste(pic_d_pil, mask=pic_d_pil.split()[3])

        pic_d_pil_rgb.save('RGBA_converted_temp.png')

        pic_d_pil = pic_d_pil_rgb

        # Image avec tkinter
        pic_d_tk = PhotoImage(file="RGBA_converted_temp.png")
        real_width = pic_d_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_d_canvas = default_canvas.create_image(real_width // 2, 360, image=pic_d_tk)
        pic_d_check = True

        # suppression du fichier temporaire :
        os.remove("RGBA_converted_temp.png")

        showinfo("Message à caractère informatif", "Le fichier contenait de la transparence et a été converti\n(RGBA → RGB)")

    elif pal == ('P',):  # palette de 256 couleurs uniques
        print("P")

        # Convertion de P à RGB :
        pic_d_pil_rgb = pic_d_pil.convert('RGB')
        pic_d_pil_rgb.save('P_converted_temp.png')
        pic_d_pil = pic_d_pil_rgb

        # Image avec tkinter
        pic_d_tk = PhotoImage(file="P_converted_temp.png")
        real_width = pic_d_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_d_canvas = default_canvas.create_image(real_width // 2, 360, image=pic_d_tk)
        pic_d_check = True

        # suppression du fichier temporaire :
        os.remove("P_converted_temp.png")

        showinfo("Message à caractère informatif", "Le fichier a été converti\n(P → RGB)")

    elif pal == ('R', 'G', 'B'):
        print("RGB")

        # Image avec tkinter
        pic_d_tk = PhotoImage(file=pic_d_path)
        real_width = pic_d_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_d_canvas = default_canvas.create_image(real_width // 2, 360, image=pic_d_tk)
        pic_d_check = True

        showinfo("Message à caractère informatif", "Le fichier a été correctement importé\n(RGB)")

    else:
        showerror("Message à caractère informatif", "Le fichier n'est pas supporté (propriétés)")


def save_as():
    global pic_f_pil, pic_f_check
    print("Action : save_as")

    # on regarde d'abord s'il existe un fichier à sauvegarder
    if pic_f_check is True:
        print("Il existe un fichier à sauvegarder")
        filename = filedialog.asksaveasfilename(title="Enregistrement de l'image", initialdir="fic", filetypes=(("fichier PNG", "*.png"), ("tous les fichiers", "*.*")))
        print("nom du fichier", filename)

        file_path, file_ext = os.path.splitext(filename)
        pic_f_pil.save(file_path + ".png")
    else:
        showerror("Message à caractère informatif", "Aucun fichier à sauvegarder")

def texte_aff(texte):
    global info_texte, result_canvas
    print("Action : texte_aff")

    result_canvas.delete(main_window, info_texte) 
    info_texte = result_canvas.create_text(400, 50 , text=texte, fill="white", font="Times 20 italic bold")
    
    
# // fonctions du menu position :


def pos_pic_d():
    global pic_d_check
    print("Action : pos_pic_d")

    # / vérif de l'existence de l'image
    if pic_d_check is False:
        showinfo("Message à caractère informatif", "Le fichier n'a pas été importé")
    else:
        pos_window = Toplevel(main_window)
        pos_window.title("Choix de la position de l'image importée")

        # / boutons de paramètrages de l'image :

        for tex, com, r, c in [('↖', pos_pic_d_left_up, 1, 1), ('↑', pos_pic_d_up, 1, 2), ('↗', pos_pic_d_right_up, 1, 3),
                               ('←', pos_pic_d_left, 2, 1), ('⤫', pos_window.destroy, 2, 2), ('→', pos_pic_d_right, 2, 3),
                               ('↙', pos_pic_d_left_down, 3, 1), ('↓', pos_pic_d_down, 3, 2), ('↘', pos_pic_d_right_down, 3, 3)]:
            Button(pos_window, text=tex, command=com).grid(row=r, column=c)


# / déplacement de l'image par défaut :
def pos_pic_d_left():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, -10, 0)


def pos_pic_d_right():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, 10, 0)


def pos_pic_d_down():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, 0, 10)


def pos_pic_d_up():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, 0, -10)


def pos_pic_d_right_up():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, 10, -10)


def pos_pic_d_right_down():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, 10, 10)


def pos_pic_d_left_up():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, -10, -10)


def pos_pic_d_left_down():
    global default_canvas, pic_d_canvas
    default_canvas.move(pic_d_canvas, -10, 10)


def pos_pic_f():
    global pic_f_check

    print("Action : pos_pic_f")

    # / vérif de l'existence de l'image
    if pic_f_check is False:
        if pic_d_check is True:
            showinfo("Message à caractère informatif", "Le fichier n'a pas été converti")
        else:
            showinfo("Message à caractère informatif", "Le fichier n'a pas été importé")
    else:
        pos_window = Toplevel(main_window)
        pos_window.title("Choix de la position de l'image importée")

        # / boutons de paramètrages de l'image :

        for tex, com, r, c in [('↖', pos_pic_f_left_up, 1, 1), ('↑', pos_pic_f_up, 1, 2), ('↗', pos_pic_f_right_up, 1, 3),
                               ('←', pos_pic_f_left, 2, 1), ('⤫', pos_window.destroy, 2, 2), ('→', pos_pic_f_right, 2, 3),
                               ('↙', pos_pic_f_left_down, 3, 1), ('↓', pos_pic_f_down, 3, 2), ('↘', pos_pic_f_right_down, 3, 3)]:
            Button(pos_window, text=tex, command=com).grid(row=r, column=c)

# / déplacement de l'image par défaut :


def pos_pic_f_left():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, -10, 0)


def pos_pic_f_right():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, 10, 0)


def pos_pic_f_down():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, 0, 10)


def pos_pic_f_up():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, 0, -10)


def pos_pic_f_right_up():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, 10, -10)


def pos_pic_f_right_down():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, 10, 10)


def pos_pic_f_left_up():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, -10, -10)


def pos_pic_f_left_down():
    global result_canvas, pic_f_canvas
    result_canvas.move(pic_f_canvas, -10, 10)


# // fonctions du menu Monochromate :


def mono_info():
    print("Action : mono_info")
    showinfo('Message à caractère informatif', 'Il s’agit de l’absence totale de perception des couleurs (touche une personne sur 40 000).\nCelui qui est atteint voit le monde en noir et blanc et des nuances de gris. Les cônes de la cornée sont dépourvus des trois pigments habituels qui permettent de voir les couleurs.')


def Monochromate():  # L = R * 299/1000 + G * 587/1000 + B * 114/1000
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    print("Action : Monochromate")

    if pic_d_check is True:

        texte_aff("Vue d'un Monochromate:")
        
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int((R * 299 / 1000) + (G * 587 / 1000) + (B * 114 / 1000))
                pic_f_pil.putpixel((pixel_d), (L, L, L))

        pic_f_pil.save("temp_mono.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_mono.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_mono.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")

# // fonctions du menu Dichotomate :

# / fenêtre d'informations


def dicho_info():
    print("Action : dicho_info")
    showinfo('Message à caractère informatif', 'Dichromate : Absence du gène, donc du pigment, c’est à dire, perception uniquement à partir de deux couleurs primaires. Il existe trois dichromies différentes :\n  - Protanopie : perception du vert et du bleu seulement,\n  - Deuteranopie : perception du rouge et du bleu seulement,\n  - Tritanopie : perception du rouge et du vert seulement.')


def Protanopie():  # Otto -> Protanopie : perception du vert et du bleu seulement
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    print("Action : Protanopie")

    if pic_d_check is True:

        texte_aff("Vue d'un protanope:")

        
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL : A tester
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int(1.05 * G + -0.05 * B)
                pic_f_pil.putpixel((pixel_d), (L, G, B))
        pic_f_pil.save("temp_protanopie.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_protanopie.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_protanopie.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")


def Deuteranopie():  # Deuteranopie : perception du rouge et du bleu seulement
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    print("Action : Deuteranopie")

    if pic_d_check is True:

        texte_aff("Vue d'un Deuteranope:")
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL : A tester
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int(0.95 * R + 0.05 * B)
                pic_f_pil.putpixel((pixel_d), (R, L, B))
        pic_f_pil.save("temp_deuteranopie.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_deuteranopie.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_deuteranopie.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")


def Tritanopie():  # Tritanopie : perception du rouge et du vert seulement.
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    print("Action : Tritanopie")

    if pic_d_check is True:

        texte_aff("Vue d'un Tritanope:")
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL : A tester
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int(-0.6 * R + 2.3 * G)
                pic_f_pil.putpixel((pixel_d), (R, G, L))
        pic_f_pil.save("temp_tritanopie.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_tritanopie.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_tritanopie.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")

# // fonctions du menu Trichromate :

# / fenêtre d'informations


def tricho_info():
    print("Action : tricho_info")
    showinfo('Message à caractère informatif', 'Trichromate : le gène est muté, le pigment a une sensibilité différente : perception de trois couleurs dont une d’intensité anormale. On distingue trois cas de trichomatie :\n  - Protanomal : lacune au niveau de la perception du rouge,\n  - Deuteranomal : faible perception du vert,\n  - Tritanomal : faible perception du bleu.')


# / choix du cone defectueux (choix indirect fais dans le menu déroulant)


def pro():
    how_much('Protanomalie')


def deu():
    how_much('Deuteranomalie')


def tri():
    how_much('Tritanomalie')

# / fonctions de la fenêtre pour choisir le niveau de lacune du cône


def how_much(info):
    print("Action : how_much")
    global choix_rad, choix_text, hm_window

    if pic_d_check is True:
        hm_window = Toplevel(main_window)
        hm_window.title("Niveau de lacune du cône")

        # explications :
        Label(hm_window, text="A quel point le cône doit-il être impacté ?\nVeuillez choisir une valeur parmis ces options:").pack()

        # boutons radio (on ne peut en choisir qu'un)
        choix_rad = DoubleVar(value=0.25)
        for tex, val in [('25 %', 0.25), ('50 %', 0.5), ('75 %', 0.75)]:
            Radiobutton(hm_window, text=tex, value=val, variable=choix_rad).pack()

        # choix personnel
        Label(hm_window, text="0 < Autre : < 100").pack()
        choix_text = Entry(hm_window, bd=2)
        choix_text.pack()

        # commande de lancement (en fonction du choix indirect précédent)
        if info == 'Protanomalie':
            print("Protanomalie")
            Button(hm_window, text="Lancer la conversion\n(Protanomalie)", command=Protanomal).pack()

        if info == 'Deuteranomalie':
            print("Deuteranomalie")
            Button(hm_window, text="Lancer la conversion\n(Deuteranomalie)", command=Deuteranomal).pack()
        

        if info == 'Tritanomalie':
            print("Tritanomalie")
            Button(hm_window, text="Lancer la conversion\n(Tritanomalie)", command=Tritanomal).pack()

        # bouton pour fermer la fenêtre
        Button(hm_window, text="⤫", command=hm_window.destroy).pack()
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")


def Protanomal():
    print("Action : Protanomal")
    global info_texte, choix_rad, choix_text, hm_window, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas

    val = choix_text.get()
    # si une valeur est rentrée
    if val != "":
        print("saisie manuelle détectée et annalyse")

        # on regarde si la valeur entrée est correcte:
        try:
            float(val)
        # si la saisie est erronée (n'est pas un float->réel)
        except ValueError:
            print("saisie invalide")
            showerror("Message à caractère informatif", "La saisie n'est pas valide, veuillez recommencer")
            # on recréer la fenêtre de choix pour effacer le texte erronée:
            hm_window.destroy()
            how_much('Protanomalie')
        # une fois que la vérification est bonne on vérifie si ce n'est pas trop grand:
        else:
            if 0 <= float(val) <= 100:
                print("saisie acceptée")
                per_invert = float(val) / 100
            # si c'est le cas on recommence:
            else:
                print("saisie trop grande ou trop petite")
                showerror("Message à caractère informatif", "La saisie est trop grande ou trop petite, veuillez recommencer")
                # on recréer la fenêtre de choix pour effacer le texte erronée:
                hm_window.destroy()
                how_much('Protanomalie')
    # si rien n'est rentré on prend la valeur du bouton radio coché
    else:
        print("un bouton a été choisi:")
        per_invert = choix_rad.get()

    per = 1 - per_invert
    print("pourcentage final choisi:", per)

    texte_aff("Vue d'un protanope avec une déficience de {}%:".format((1-per)*100))

    # conversion de l'image selon le pourcentage:

    width = pic_d_tk.width()
    height = pic_d_tk.height()

    pic_f_pil = Image.new('RGB', pic_d_pil.size)

    print("taille:", width, height)

    # Conversion de l'image avec PIL : A tester
    for y in range(height):
        for x in range(width):
            pixel_d = (x, y)
            R, G, B = pic_d_pil.getpixel(pixel_d)
            L = int((R * per) + ((1.05 * G + -0.05 * B) * per_invert))
            pic_f_pil.putpixel((pixel_d), (L, G, B))
    pic_f_pil.save("temp_protanomalie.png")

    # Image avec tkinter
    pic_f_tk = PhotoImage(file="temp_protanomalie.png")
    real_width = pic_f_tk.width() + 20

    # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
    pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

    # supression du fichier temporaire
    os.remove("temp_protanomalie.png")

    pic_f_check = True


def Deuteranomal():
    print("Action : Deuteranomal")
    global info_texte, choix_rad, choix_text, hm_window, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas

    val = choix_text.get()
    # si une valeur est rentrée
    if val != "":
        print("saisie manuelle détectée et annalyse")

        # on regarde si la valeur entrée est correcte:
        try:
            float(val)
        # si la saisie est erronée (n'est pas un float->entier)
        except ValueError:
            print("saisie invalide")
            showerror("Message à caractère informatif", "La saisie n'est pas valide, veuillez recommencer")
            # on recréer la fenêtre de choix pour effacer le texte erronée:
            hm_window.destroy()
            how_much('Deuteranomalie')
        else:
            # une fois que la vérification est bonne on vérifie si ce n'est pas trop grand:
            if 0 <= float(val) <= 100:
                print("saisie acceptée")
                per_invert = float(val) / 100
            # si c'est le cas on recommence:
            else:
                print("saisie trop grande ou trop petite")
                showerror("Message à caractère informatif", "La saisie est trop grande ou trop petite, veuillez recommencer")
                # on recréer la fenêtre de choix pour effacer le texte erronée:
                hm_window.destroy()
                how_much('Deuteranomalie')
    # si rien n'est rentré on prend la valeur du bouton radio coché
    else:
        print("un bouton a été choisi:")
        per_invert = choix_rad.get()

    per = 1 - per_invert
    print("pourcentage final choisi:", per)

    texte_aff("Vue d'un deuteranope avec une déficience de {}%:".format((1-per)*100))

    # conversion de l'image selon le pourcentage:

    width = pic_d_tk.width()
    height = pic_d_tk.height()

    pic_f_pil = Image.new('RGB', pic_d_pil.size)

    print("taille:", width, height)

    # Conversion de l'image avec PIL : A tester
    for y in range(height):
        for x in range(width):
            pixel_d = (x, y)
            R, G, B = pic_d_pil.getpixel(pixel_d)
            L = int((G * per) + ((0.95 * R + 0.05 * B) * per_invert))
            pic_f_pil.putpixel((pixel_d), (R, L, B))
    pic_f_pil.save("temp_deuteranomalie.png")

    # Image avec tkinter
    pic_f_tk = PhotoImage(file="temp_deuteranomalie.png")
    real_width = pic_f_tk.width() + 20

    # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
    pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

    # supression du fichier temporaire
    os.remove("temp_deuteranomalie.png")

    pic_f_check = True


def Tritanomal():
    print("Action : Tritanomal")
    global info_texte, info_texte, choix_rad, choix_text, hm_window, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas

    val = choix_text.get()
    # si une valeur est rentrée
    if val != "":
        print("saisie manuelle détectée et annalyse")

        # on regarde si la valeur entrée est correcte:
        try:
            float(val)
        # si la saisie est erronée (n'est pas un float->entier)
        except ValueError:
            print("saisie invalide")
            showerror("Message à caractère informatif", "La saisie n'est pas valide, veuillez recommencer")
            # on recréer la fenêtre de choix pour effacer le texte erronée:
            hm_window.destroy()
            how_much('Tritanomalie')
        # une fois que la vérification est bonne on vérifie si ce n'est pas trop grand:
        else:
            if 0 <= float(val) <= 100:
                print("saisie acceptée")
                per_invert = float(val) / 100
            # si c'est le cas on recommence:
            else:
                print("saisie trop grande ou trop petite")
                showerror("Message à caractère informatif", "La saisie est trop grande ou trop petite, veuillez recommencer")
                # on recréer la fenêtre de choix pour effacer le texte erronée:
                hm_window.destroy()
                how_much('Tritanomalie')
    # si rien n'est rentré on prend la valeur du bouton radio coché
    else:
        print("un bouton a été choisi:")
        per_invert = choix_rad.get()

    per = 1 - per_invert
    print("pourcentage final choisi:", per)

    texte_aff("Vue d'un tritanope avec une déficience de {}%:".format((1-per)*100))

    # conversion de l'image selon le pourcentage:

    width = pic_d_tk.width()
    height = pic_d_tk.height()

    pic_f_pil = Image.new('RGB', pic_d_pil.size)

    print("taille:", width, height)

    # Conversion de l'image avec PIL : A tester
    for y in range(height):
        for x in range(width):
            pixel_d = (x, y)
            R, G, B = pic_d_pil.getpixel(pixel_d)
            L = int((B * per) + ((-0.6 * R + 2.3 * G) * per_invert))
            pic_f_pil.putpixel((pixel_d), (R, G, L))
    pic_f_pil.save("temp_tritanomalie.png")

    # Image avec tkinter
    pic_f_tk = PhotoImage(file="temp_tritanomalie.png")
    real_width = pic_f_tk.width() + 20

    # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
    pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

    # supression du fichier temporaire
    os.remove("temp_tritanomalie.png")

    pic_f_check = True

# // fonctions du menu Autres vues :

def autre_info():
    print("Action : autre_info")
    showinfo('Message à caractère informatif',"Tous les mammifères sont atteints de Protanopie, seulement ils ne perçoivent pas tous un même angle de vue. Ainsi : \n - Le chat a un angle de vue d'environ 200 degrés \n - Le cheval a un angle de vue d'environ 340 degrés \n - Le chien a un angle de vue d'environ 250 degrés.")

def cat_view() :
    print("Action : cat_view")
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    
    if pic_d_check is True:

        texte_aff("Vue d'un chat:")
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL : 
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int(1.05 * G + -0.05 * B)
                pic_f_pil.putpixel((pixel_d), (L, G, B))
        
    
        Left = 80*width/360
        Top = 0
        Width = width-(Left*2)
        Height = height
        box = (Left, Top, Left+Width, Top+Height)
        pic_c_pil = pic_f_pil.crop(box)        
        pic_c_pil.save("temp_cat.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_cat.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_cat.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")

    
def horse_view():
    print("Action : horse_view")
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    
    if pic_d_check is True:

        texte_aff("Vue d'un cheval:")
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL : 
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int(1.05 * G + -0.05 * B)
                pic_f_pil.putpixel((pixel_d), (L, G, B))
        
    
        Left = 10*width/360
        Top = 0
        Width = width-(Left*2)
        Height = height
        box = (Left, Top, Left+Width, Top+Height)
        pic_c_pil = pic_f_pil.crop(box)        
        pic_c_pil.save("temp_horse.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_horse.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_horse.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")


def dog_view():
    print("Action : dog_view")
    global info_texte, pic_d_check, pic_d_pil, pic_d_tk, pic_f_tk, pic_f_pil, result_canvas, pic_f_check, pic_f_canvas
    
    if pic_d_check is True:

        texte_aff("Vue d'un chien:")
        width = pic_d_tk.width()
        height = pic_d_tk.height()

        pic_f_pil = Image.new('RGB', pic_d_pil.size)

        print("taille:", width, height)

        # Conversion de l'image avec PIL : 
        for y in range(height):
            for x in range(width):
                pixel_d = (x, y)
                R, G, B = pic_d_pil.getpixel(pixel_d)
                L = int(1.05 * G + -0.05 * B)
                pic_f_pil.putpixel((pixel_d), (L, G, B))
        
    
        Left = 55*width/360
        Top = 0
        Width = width-(Left*2)
        Height = height
        box = (Left, Top, Left+Width, Top+Height)
        pic_c_pil = pic_f_pil.crop(box)        
        pic_c_pil.save("temp_dog.png")

        # Image avec tkinter
        pic_f_tk = PhotoImage(file="temp_dog.png")
        real_width = pic_f_tk.width() + 20

        # positionnement sur le canvas de l'image ouverte (largeur, hauteur)
        pic_f_canvas = result_canvas.create_image(real_width // 2, 360, image=pic_f_tk)

        # supression du fichier temporaire
        os.remove("temp_dog.png")

        pic_f_check = True
    else:
        showinfo("Message à caractère informatif", "Aucun fichier à modifier")
        
# /--/ fenetre principale :


main_window = Tk()
main_window.title("Fenêtre principale")

valeur = True
main_window.resizable(width=valeur, height=valeur)

default_canvas = Canvas(main_window, relief=GROOVE, height=900, width=800, bg='gray7')
default_canvas.grid(row=0, column=0)
result_canvas = Canvas(main_window, relief=GROOVE, height=900, width=800, bg='gray7')
result_canvas.grid(row=0, column=1)
info_texte = result_canvas.create_text(100, 25 , text='', fill="white")


# /-/ pannel deroulant :

# / creation de la barre des menus :
menu_list = Menu(main_window)


# / creation du menu fichier
menu_file = Menu(menu_list, tearoff=0)
for lab, com in[('Ouvrir un fichier', open_file), ('Sauvegarder sous', save_as)]:
    menu_file.add_command(label=lab, command=com)

# / creation du menu autres vues
menu_vue = Menu(menu_list, tearoff=0)
for lab, com in[('Chat', cat_view), ('Cheval', horse_view), ('Chien', dog_view), ('À propos', autre_info)]:
    menu_vue.add_command(label=lab, command=com)

# / creation du menu position
menu_pos = Menu(menu_list, tearoff=0)
for lab, com in[('Image importée', pos_pic_d), ('Image obtenue', pos_pic_f)]:
    menu_pos.add_command(label=lab, command=com)

# / creation du menu monochromate
menu_monochromate = Menu(menu_list, tearoff=0)
for lab, com in[('Monochromatie', Monochromate), ('À propos', mono_info)]:
    menu_monochromate.add_command(label=lab, command=com)

# / creation du menu dichromate
menu_dichromate = Menu(menu_list, tearoff=0)
for lab, com in[('Protanopie', Protanopie), ('Deuteranopie', Deuteranopie), ('Tritanopie', Tritanopie), ('À propos', dicho_info)]:
    menu_dichromate.add_command(label=lab, command=com)

# / creation du menu trichromate
menu_trichromate = Menu(menu_list, tearoff=0)
for lab, com in[('Protanomalie', pro), ('Deuteranomalie', deu), ('Tritanomalie', tri), ('À propos', tricho_info)]:
    menu_trichromate.add_command(label=lab, command=com)

# / ajout des menu a la barre de menu
for lab, men in[('Fichier', menu_file), ('Position', menu_pos), ('Monochromate', menu_monochromate), ('Dichromate', menu_dichromate), ('Trichromate', menu_trichromate), ('Autres Visions', menu_vue)]:
    menu_list.add_cascade(label=lab, menu=men)

main_window.config(menu=menu_list)

# /-/ Met la fenêtre en attente

main_window.mainloop()












