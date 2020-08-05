'''
/ Réécriture propre du précédent programme.
/ Mecredi 5 Aout 2020
/ 
/ Projet BAC - Julien CONSTANT TS1 & Mylene POZAR TS2 - 2018/2019
/ Comment les autres percoivent-ils les couleurs ?
/ Le daltonisme et autres conditions de vue (animaux domestiques notamment)
/
/ v2
'''

# importing modules

from pip._internal import main as pipmain

try:        
    from tkinter            import *
    from tkinter            import filedialog       
    from tkinter.messagebox import *
except ImportError:
    print(  'tkinter : Installing, need restart')
    pipmain(['install', 'tkinter'])
else: print('tkinter : OK')

try: 
    import os
except ImportError:
    print(  'os      : Installing, need restart')
    pipmain(['install', 'os'])
else: print('os      : OK')

try:
    from PIL import Image
except ImportError:
    print(  'pillow  : Installing, need restart')
    pipmain(['install', 'pillow'])
else: print('pillow  : OK')

# Global Variable :

OF_imageLeftCanvas   = 0
OF_imageLeftCanvasTk = 0

OF_ImportedChecked  = False
MCB_ImportedChecked = False
OF_border = 40

getResizableWindow = False

# Tkinter Window :

mainWindow = Tk()
mainWindow.title('Fenêtre Principale')
mainWindow.resizable(width=getResizableWindow, height=getResizableWindow)

frameCanvas = Frame(mainWindow, height=700, width=1600)
frameCanvas.pack(side=TOP)

framePos = Frame(mainWindow, bg='gray7', relief=RIDGE, borderwidth=20)
framePos.pack(side=BOTTOM)

framePosLeft = Frame(framePos, bg='green', relief=RIDGE, borderwidth=5)
framePosLeft.pack(side=LEFT)

framePosRight = Frame(framePos, bg='blue', relief=RIDGE, borderwidth=5)
framePosRight.pack(side=RIGHT)

leftCanvas = Canvas(frameCanvas, height=700, width=800, bg='gray7')
leftCanvas.pack(side=LEFT)

rightCanvas = Canvas(frameCanvas, height=700, width=800, bg='gray7')
rightCanvas.pack(side=RIGHT)

rightCanvasText = rightCanvas.create_text(100, 25, text='', fill='white')


# Fonctions :

def OpenFile():
    print('In OpenFile()')

    global OF_fileOpenedPath, OF_imageOpened
    global leftCanvas, OF_imageLeftCanvas, OF_imageLeftCanvasTk, OF_imageLeftCanvasOnCanvas
    global OF_border, OF_ImportedChecked, OF_imageWidthWithBorder

    # Get user image
    OF_fileOpenedPath = filedialog.askopenfilename(title='Chercher une image', initialdir="fic", multiple=False, filetypes=(("fichier PNG", "*.png"), ("fichier JPEG", "*.jpg"), ("fichier GIF", ".gif"), ("tout les fichiers", "*.*")))
    print(OF_fileOpenedPath)
    # Convert to PNG
    OF_fileOpenedPath = OpenFileConverter(OF_fileOpenedPath)

    # Get Image bands
    OF_imageOpened = Image.open(OF_fileOpenedPath)
    OF_bands = OF_imageOpened.getbands()

    # Convert to RGBA
    if OF_bands != ('R','G','B','A'):
        OF_imageOpened = OF_imageOpened.convert('RGBA')

    # Display Image on mainWindow
    OF_imageLeftCanvasTk = PhotoImage(file=OF_fileOpenedPath)
    OF_imageWidthWithBorder = OF_imageLeftCanvasTk.width() + OF_border

    OF_imageLeftCanvasOnCanvas = leftCanvas.create_image(
        OF_imageWidthWithBorder // 2,
        360,
        image=OF_imageLeftCanvasTk
    )

    OF_ImportedChecked = True

def OpenFileConverter(Path):
    print('In OpenFileConverter()')

    OFC_filePathToName, OFC_fileExt = os.path.splitext(Path)
    OFC_extensionList = ('.jpg', '.JPG', 'JPEG', '.jpeg', 'gif', 'GIF')

    for OFC_extension in OFC_extensionList:
        if OFC_fileExt == OFC_extension:
            os.rename(Path, OFC_filePathToName + '.png')
        if OFC_fileExt == '.png':
            pass
        else:
            print('Wrong file extension')

    Path = OFC_filePathToName + '.png'
    print(Path)
    return Path

def SaveAs():
    print('In SaveAs()')

def UpdateText(Type, Percentage, Cone):
    print('In UpdateText with:',Type,Percentage)

    global rightCanvasText, rightCanvas

    Percentage = Percentage * 100

    rightCanvas.delete(mainWindow, rightCanvasText)
    if Percentage == -1:
        if Type == 'MONO'  :
            rightCanvasText = rightCanvas.create_text(400, 50, text='Monochromatie', fill='white', font="Times 20 italic bold")
        if Type == 'DICHO' :
            if Cone == 'R':
                text = "Vue d'un protanope"
                rightCanvasText = rightCanvas.create_text(400, 50, text=text, fill='white', font="Times 20 italic bold")
            if Cone == 'G':
                text = "Vue d'un deuteranope"
                rightCanvasText = rightCanvas.create_text(400, 50, text=text, fill='white', font="Times 20 italic bold")
            if Cone == 'B':
                text = "Vue d'un triteranope"
                rightCanvasText = rightCanvas.create_text(400, 50, text=text, fill='white', font="Times 20 italic bold")
        if Type == 'CAT' :
            rightCanvasText = rightCanvas.create_text(400, 50, text="Vue d'un chat", fill='white', font="Times 20 italic bold")
        if Type == 'HORSE' :
            rightCanvasText = rightCanvas.create_text(400, 50, text="Vue d'un cheval", fill='white', font="Times 20 italic bold")
        if Type == 'DOG' :
            rightCanvasText = rightCanvas.create_text(400, 50, text="Vue d'un chien", fill='white', font="Times 20 italic bold")
    if Type == 'TRICHO':
        if Cone == 'R':
            text = "Vue atteinte de protanomalie à " + str(Percentage) + "%"
            rightCanvasText = rightCanvas.create_text(400, 50, text=text, fill='white', font="Times 20 italic bold")
        if Cone == 'G':
            text = "Vue atteinte de deuteranomalie à " + str(Percentage) + "%"
            rightCanvasText = rightCanvas.create_text(400, 50, text=text, fill='white', font="Times 20 italic bold")
        if Cone == 'B':
            text = "Vue atteinte de tritanomalie à " + str(Percentage) + "%"
            rightCanvasText = rightCanvas.create_text(400, 50, text=text, fill='white', font="Times 20 italic bold")

def  AskColorBlind(Cone):
    print('In AskColorBlind with:',Cone)    

    global ChoiceRad, ChoiceText, askColorBlindWindow
    global OF_ImportedChecked, mainWindow

    if OF_ImportedChecked is False:
        pass
    else:
        askColorBlindWindow = Toplevel(mainWindow)
        askColorBlindWindow.title('Choix du niveau de lacune du cône')

        Label(askColorBlindWindow, text="A quel point le cône doit-il être impacté ?\nVeuillez choisir une valeur parmis ces options:").pack()

        # Radio Buttons
        ChoiceRad = DoubleVar(value=0.25)
        for Texte, Value in [('25 %', 0.25), ('50 %', 0.5), ('75 %', 0.75)]:
            Radiobutton(askColorBlindWindow, text=Texte, value=Value, variable=ChoiceRad).pack()

        # Personnal Choice
        Label(askColorBlindWindow, text="0 < Autre : < 100").pack()
        ChoiceText = Entry(askColorBlindWindow, bd=2)
        ChoiceText.pack()

        if Cone == 'R':
            Button(askColorBlindWindow, text="Lancer la conversion\n(Protanomalie)",   command= lambda: GetValueAndStart('TRICHO','R')).pack()
        if Cone == 'G':
            Button(askColorBlindWindow, text="Lancer la conversion\n(Deuteranomalie)", command= lambda: GetValueAndStart('TRICHO','G')).pack()
        if Cone == 'B':
            Button(askColorBlindWindow, text="Lancer la conversion\n(Tritanomalie)",   command= lambda: GetValueAndStart('TRICHO','B')).pack()

def GetValueAndStart(Type,Cone):
    print('In GetValueAndStart with:',Type,Cone)

    global askColorBlindWindow
    global ChoiceText, ChoiceRad

    value = ChoiceText.get()
    if value != '':
        try: 
            float(value)
        except ValueError:
            showerror("Message à caractère informatif", "La saisie n'est pas valide, veuillez recommencer")
            askColorBlindWindow.destroy()
            AskColorBlind(Cone)
            return 0
        else:
            if 0 <= float(value) <= 100:
                percentage = float(value) / 100
            else:
                showerror("Message à caractère informatif", "La saisie est trop grande ou trop petite, veuillez recommencer")
                askColorBlindWindow.destroy()
                AskColorBlind(Cone)
                return 0
    else:
        percentage = ChoiceRad.get()

    MakeColorBlind('TRICHO', percentage, Cone)

def MakeColorBlind(Type, Percentage, Cone):
    print('In MakeColorBlind with:',Type,Percentage,Cone)

    global OF_imageLeftCanvasTk, rightCanvas, OF_imageOpened, MCB_imageRightCanvas, MCB_imageRightCanvasTk, MCB_imageRightCanvasOnCanvas
    global OF_ImportedChecked, OF_imageWidthWithBorder, MCB_ImportedChecked

    MCB_width  = OF_imageLeftCanvasTk.width() 
    MCB_height = OF_imageLeftCanvasTk.height()

    MCB_imageRightCanvas = Image.new('RGBA', (MCB_width, MCB_height))

    if OF_ImportedChecked is False:
        pass
    else:
        for y in range(MCB_height):
            for x in range(MCB_width):
                R, G, B, A = OF_imageOpened.getpixel((x,y))

                if Type == 'MONO':
                    L = int((R * 299 / 1000) + (G * 587 / 1000) + (B * 114 / 1000))
                    MCB_imageRightCanvas.putpixel((x,y), (L,L,L,A))

                if Type == 'DICHO':
                    if Cone == 'R':
                        L = int(1.05 * G + -0.05 * B)
                        MCB_imageRightCanvas.putpixel((x,y), (L,G,B,A))
                    if Cone == 'G':
                        L = int(0.95 * R + 0.05 * B)
                        MCB_imageRightCanvas.putpixel((x,y), (R,L,B,A))
                    if Cone == 'B':
                        L = int(-0.6 * R + 2.3 * G)
                        MCB_imageRightCanvas.putpixel((x,y), (R,G,L,A))
                if Type == 'TRICHO':
                    if Cone == 'R':
                        L = int((R * (1 - Percentage)) + ((1.05 * G + -0.05 * B) * (Percentage)))
                        MCB_imageRightCanvas.putpixel((x,y), (L,G,B,A))
                    if Cone == 'G':
                        L = int((G * (1 - Percentage)) + ((0.95 * R + 0.05 * B) * (Percentage)))
                        MCB_imageRightCanvas.putpixel((x,y), (R,L,B,A))
                    if Cone == 'B':
                        L = int((B * (1 - Percentage)) + ((-0.6 * R + 2.3 * G) * (Percentage)))
                        MCB_imageRightCanvas.putpixel((x,y), (R,G,L,A))

        MCB_imageRightCanvas.save('temp.png')

        MCB_imageRightCanvasTk = PhotoImage(file='temp.png')
        
        MCB_imageRightCanvasOnCanvas = rightCanvas.create_image(
            OF_imageWidthWithBorder // 2,
            360,
            image=MCB_imageRightCanvasTk
        )

        os.remove('temp.png')

        if Type == 'MONO':
            UpdateText('MONO', -1, 'NULL')
        if Type == 'DICHO':
            UpdateText('DICHO', -1, Cone)
        if Type == 'TRICHO':
            UpdateText('TRICHO', Percentage, Cone)

        MCB_ImportedChecked = True

def About(Type):
    print("In About with:",Type)

    if Type == 'MONO'  :
        showinfo('Message à caractère informatif', 'Il s’agit de l’absence totale de perception des couleurs (touche une personne sur 40 000).\nCelui qui est atteint voit le monde en noir et blanc et des nuances de gris. Les cônes de la cornée sont dépourvus des trois pigments habituels qui permettent de voir les couleurs.')
    if Type == 'DICHO' :
        showinfo('Message à caractère informatif', 'Dichromate : Absence du gène, donc du pigment, c’est à dire, perception uniquement à partir de deux couleurs primaires. Il existe trois dichromies différentes :\n  - Protanopie : perception du vert et du bleu seulement,\n  - Deuteranopie : perception du rouge et du bleu seulement,\n  - Tritanopie : perception du rouge et du vert seulement.')
    if Type == 'TRICHO':
        showinfo('Message à caractère informatif', 'Trichromate : le gène est muté, le pigment a une sensibilité différente : perception de trois couleurs dont une d’intensité anormale. On distingue trois cas de trichomatie :\n  - Protanomal : lacune au niveau de la perception du rouge,\n  - Deuteranomal : faible perception du vert,\n  - Tritanomal : faible perception du bleu.')
    if Type == 'OTHERS' :
        showinfo('Message à caractère informatif',"Tous les mammifères sont atteints de Protanopie, seulement ils ne perçoivent pas tous un même angle de vue. Ainsi : \n - Le chat a un angle de vue d'environ 200 degrés \n - Le cheval a un angle de vue d'environ 340 degrés \n - Le chien a un angle de vue d'environ 250 degrés.")

# Add Buttons to change pos of images : 


def RightImagePos(Direction):
    #print('In RightImagePos with:',Direction)

    global rightCanvas, MCB_imageRightCanvasOnCanvas 
    global MCB_ImportedChecked

    if MCB_ImportedChecked is False:
        pass
    else:
        if Direction == 'UP' or Direction == 'UP_L' or Direction == 'UP_R':
            rightCanvas.move(MCB_imageRightCanvasOnCanvas , 0, -10)
        if Direction == 'DOWN' or Direction == 'DOWN_L' or Direction == 'DOWN_R':
            rightCanvas.move(MCB_imageRightCanvasOnCanvas , 0, 10)
        if Direction == 'LEFT' or Direction == 'UP_L' or Direction == 'DOWN_L':
            rightCanvas.move(MCB_imageRightCanvasOnCanvas , -10, 0)
        if Direction == 'RIGHT' or Direction == 'UP_R' or Direction == 'DOWN_R':
            rightCanvas.move(MCB_imageRightCanvasOnCanvas , 10, 0)

def LeftImagePos(Direction):
    #print('In LeftImagePos with:',Direction)

    global leftCanvas, OF_imageLeftCanvasOnCanvas
    global OF_ImportedChecked

    if OF_ImportedChecked is False:
        pass
    else:
        if Direction == 'UP' or Direction == 'UP_L' or Direction == 'UP_R':
            leftCanvas.move(OF_imageLeftCanvasOnCanvas, 0, -10)
        if Direction == 'DOWN' or Direction == 'DOWN_L' or Direction == 'DOWN_R':
            leftCanvas.move(OF_imageLeftCanvasOnCanvas, 0, 10)
        if Direction == 'LEFT' or Direction == 'UP_L' or Direction == 'DOWN_L':
            leftCanvas.move(OF_imageLeftCanvasOnCanvas, -10, 0)
        if Direction == 'RIGHT' or Direction == 'UP_R' or Direction == 'DOWN_R':
            leftCanvas.move(OF_imageLeftCanvasOnCanvas, 10, 0)

Button(framePosLeft, text='↑', command= lambda: LeftImagePos('UP'    )).grid(row=0,column=1)
Button(framePosLeft, text='↓', command= lambda: LeftImagePos('DOWN'  )).grid(row=2,column=1)
Button(framePosLeft, text='←', command= lambda: LeftImagePos('LEFT'  )).grid(row=1,column=0)
Button(framePosLeft, text='→', command= lambda: LeftImagePos('RIGHT' )).grid(row=1,column=2)
Button(framePosLeft, text='↖', command= lambda: LeftImagePos('UP_L'  )).grid(row=0,column=0)
Button(framePosLeft, text='↗', command= lambda: LeftImagePos('UP_R'  )).grid(row=0,column=2)
Button(framePosLeft, text='↙', command= lambda: LeftImagePos('DOWN_L')).grid(row=2,column=0)
Button(framePosLeft, text='↘', command= lambda: LeftImagePos('DOWN_R')).grid(row=2,column=2)

Button(framePosRight, text='↑', command= lambda: RightImagePos('UP'    )).grid(row=0,column=1)
Button(framePosRight, text='↓', command= lambda: RightImagePos('DOWN'  )).grid(row=2,column=1)
Button(framePosRight, text='←', command= lambda: RightImagePos('LEFT'  )).grid(row=1,column=0)
Button(framePosRight, text='→', command= lambda: RightImagePos('RIGHT' )).grid(row=1,column=2)
Button(framePosRight, text='↖', command= lambda: RightImagePos('UP_L'  )).grid(row=0,column=0)
Button(framePosRight, text='↗', command= lambda: RightImagePos('UP_R'  )).grid(row=0,column=2)
Button(framePosRight, text='↙', command= lambda: RightImagePos('DOWN_L')).grid(row=2,column=0)
Button(framePosRight, text='↘', command= lambda: RightImagePos('DOWN_R')).grid(row=2,column=2)

# Add Fonctions to menus

menuTab = Menu(mainWindow)

menuFile   = Menu(menuTab, tearoff=0)
menuMono   = Menu(menuTab, tearoff=0)
menuDicho  = Menu(menuTab, tearoff=0)
menuTricho = Menu(menuTab, tearoff=0)
menuOthers = Menu(menuTab, tearoff=0)

menuFile.add_command(label='Ouvrir un fichier', command= lambda: OpenFile())
menuFile.add_command(label='Sauvegarder sous',  command= lambda: SaveAs())

menuMono.add_command(label='Monochromatie', command= lambda: MakeColorBlind('MONO',100,'NULL'))
menuMono.add_command(label='À propos',      command= lambda: About('MONO'))

menuDicho.add_command(label='Protanopie',   command= lambda: MakeColorBlind('DICHO',100,'R'))
menuDicho.add_command(label='Deuteranopie', command= lambda: MakeColorBlind('DICHO',100,'G'))
menuDicho.add_command(label='Tritanopie',   command= lambda: MakeColorBlind('DICHO',100,'B'))
menuDicho.add_command(label='À propos',     command= lambda: About('DICHO'))

menuTricho.add_command(label='Protanomalie',   command= lambda: AskColorBlind('R'))
menuTricho.add_command(label='Deuteranomalie', command= lambda: AskColorBlind('G'))
menuTricho.add_command(label='Tritanomalie',   command= lambda: AskColorBlind('B'))
menuTricho.add_command(label='À propos',       command= lambda: About('TRICHO'))

menuOthers.add_command(label='Chat',     command= lambda: DoAnimalView('CAT'))
menuOthers.add_command(label='Cheval',   command= lambda: DoAnimalView('HORSE'))
menuOthers.add_command(label='Chien',    command= lambda: DoAnimalView('DOG'))
menuOthers.add_command(label='À propos', command= lambda: About('OTHERS'))

for menuName, menu in [
    ('Fichier', menuFile),
    ('Monochromate', menuMono),
    ('Dichromate', menuDicho),
    ('Trichomate', menuTricho),
    ('Autres', menuOthers)
]:
    menuTab.add_cascade(label=menuName, menu=menu)

mainWindow.config(menu=menuTab)
mainWindow.mainloop()