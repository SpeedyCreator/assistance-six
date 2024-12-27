from src.AssistantSix import*
import requests
import threading as th
import random
from src.CArreraTrigerWord import*
from src.srcSix import*
import signal
from setting.ArreraGazelleUIOld import*
from librairy.arrera_tk import *

VERSION = "I2025-1.00"

class SixGUI :
    def __init__(self,icon:str,jsonConfAssistant:str,jsonUser:str,jsonNeuronNetwork:str,jsonConfSetting:str):
        # var
        self.__emplacementIcon = icon
        self.__nameSoft = "Arrera Six"
        self.__themeNB = int # 0 : white 1 : black
        self.__darkModeEnable = bool
        self.__sixSpeaking = bool
        # Teste de la connextion internet
        try:
            requests.get("https://duckduckgo.com",timeout=5)
            self.__etatConnexion = True
        except requests.ConnectionError :
            self.__etatConnexion = False
        # Demarage d'Arrera TK
        self.__arrTK = CArreraTK()
        # Instantation de l'objet Six
        self.__six = CArreraSix(jsonNeuronNetwork)
        # Instentation de l'objet Arrera Triger
        self.__objTriger = CArreraTrigerWord("6")
        # Instantation de l'objet srcSix
        self.__objSRCSix = SIXsrc(jsonWork(jsonConfAssistant))
        # Objet 
        self.__objetDectOS = OS()
        # Creation du theard Trigger word
        self.__TriggerWorkStop = th.Event()
        # Creation du theard Minuteur Actu 
        self.__thMinuteurActu = th.Thread(target=self.__minuteurActu)
        # initilisation fenetre
        self.__screen = self.__arrTK.aTK(title="Arrera Six",icon=self.__emplacementIcon)
        self.__screen.title(self.__nameSoft)
        self.__screen.geometry("500x400+5+30")
        self.__arrTK.setResizable(False)
        self.__screen.protocol("WM_DELETE_WINDOW",self.__onClose)
        # Declaration de l'objet Arrera Gazelle 
        self.__gazelleUI = CArreraGazelleUIOld(self.__screen,jsonUser,jsonNeuronNetwork,jsonConfAssistant,jsonConfSetting)
        self.__gazelleUI.passQuitFnc(self.__quitParametre)
        # Fichier json
        self.__fileSixConfig = jsonWork(jsonConfAssistant)
        # Teste de de la connection internet
        try:
            requests.get("https://duckduckgo.com",timeout=5)
            self.__etatConnexion = True
        except requests.ConnectionError :
            self.__etatConnexion = False
        # initilisation du menu six
        sixMenu = self.__arrTK.createTopMenu(self.__screen)
        self.__arrTK.addCommandTopMenu(sixMenu,text="Parametre",command=self.__activeParametre)
        self.__arrTK.addCommandTopMenu(sixMenu,text="A propos",command=lambda : self.__arrTK.aproposWindows(nameSoft=self.__nameSoft,
                                                                                                            iconFile=self.__emplacementIcon,
                                                                                                            version=VERSION,
                                                                                                            copyright="Copyright Arrera Software by Baptiste P 2023-2025",
                                                                                                            linkSource="https://github.com/Arrera-Software/Six",
                                                                                                            linkWeb="https://arrera-software.fr/"))
        # widget et canvas
        # canvas

        # Image de fond
        fileImage = ["acceuil.png",#0
                     "triste1.png",#1
                     "triste2.png",#2
                     "sureprit.png",#3
                     "mute1.png",#4
                     "mute2.png",#5
                     "noConnect.png",#6
                     "parole1.png",#7
                     "parole2.png",#8
                     "parole3.png",#9
                     "boot0.png",#10
                     "boot1.png",#11
                     "boot2.png",#12
                     "boot3.png",#13
                     "colere.png",#14
                     "content.png",#15
                     "actu.png",#16
                     "micro.png",#17
                     "microIcon.png",#18
                     "parametreOpen.png"#18
                     ]
        emplacementGUIDark = "asset/IMGinterface/dark/"
        emplacementGUILight = "asset/IMGinterface/white/"

        # Canvas Acceuil
        self.__canvasAcceuil = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[0],
                                                                       imageDark=emplacementGUIDark+fileImage[0],
                                                                       width=500,height=350)
        # Canvas Boot
        self.__canvasBoot0 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[10],
                                                                       imageDark=emplacementGUIDark+fileImage[10],
                                                                       width=500,height=350)
        self.__canvasBoot1 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[11],
                                                                       imageDark=emplacementGUIDark+fileImage[11],
                                                                       width=500,height=350)
        self.__canvasBoot2 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[12],
                                                                       imageDark=emplacementGUIDark+fileImage[12],
                                                                       width=500,height=350)
        self.__canvasBoot3 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[13],
                                                                       imageDark=emplacementGUIDark+fileImage[13],
                                                                       width=500,height=350)
        # Canvas Parole
        self.__canvasParole1 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[7],
                                                                       imageDark=emplacementGUIDark+fileImage[7],
                                                                       width=500,height=350)
        self.__canvasParole2 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[8],
                                                                       imageDark=emplacementGUIDark+fileImage[8],
                                                                       width=500,height=350)
        self.__canvasParole3 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[9],
                                                                       imageDark=emplacementGUIDark+fileImage[9],
                                                                       width=500,height=350)
        # Canvas NoConnect
        self.__canvasNoConnect = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[6],
                                                                       imageDark=emplacementGUIDark+fileImage[6],
                                                                       width=500,height=350)
        # Canvas Emotion
        self.__canvasContent = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[15],
                                                                       imageDark=emplacementGUIDark+fileImage[15],
                                                                       width=500,height=350)
        self.__canvasColere = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[14],
                                                                       imageDark=emplacementGUIDark+fileImage[14],
                                                                       width=500,height=350)
        self.__canvasSurprit = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[3],
                                                                       imageDark=emplacementGUIDark+fileImage[3],
                                                                       width=500,height=350)
        # Canvas Triste
        self.__canvasTriste1 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[1],
                                                                       imageDark=emplacementGUIDark+fileImage[1],
                                                                       width=500,height=350)
        self.__canvasTriste2 = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[2],
                                                                       imageDark=emplacementGUIDark+fileImage[2],
                                                                       width=500,height=350)
        # Canvas Parametre
        self.__canvasParaOpen = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[19],
                                                                       imageDark=emplacementGUIDark+fileImage[19],
                                                                       width=500,height=350)
        # Canvas Actu
        self.__canvasActu = self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                       imageLight=emplacementGUILight+fileImage[16],
                                                                       imageDark=emplacementGUIDark+fileImage[16],
                                                                       width=500,height=350)
        # Canvas Mute
        self.__canvasMute = [self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                     imageLight=emplacementGUILight+fileImage[4],
                                                                     imageDark=emplacementGUIDark+fileImage[4],
                                                                     width=500,height=350),
                             self.__arrTK.createArreraBackgroudImage(self.__screen,
                                                                     imageLight=emplacementGUILight+fileImage[5],
                                                                     imageDark=emplacementGUIDark+fileImage[5],
                                                                     width=500,height=350)]
        # widget 
        self.__entryUser = Entry(self.__screen,font=("Arial","20"),width=25,relief=SOLID)
        self.__labelTextDuringSpeak = Label(self.__canvasParole2,font=("arial","15"),bg="red", bd=0)
        self.__labelTextAfterSpeak = Label(self.__canvasParole3,font=("arial","15"),bg="red", bd=0)
        # Label Micro
        imageMicroTriger=self.__arrTK.createImage(pathLight=emplacementGUILight+fileImage[17],
                                                  pathDark=emplacementGUIDark+fileImage[17],
                                                  tailleX=50,tailleY=50)
        imageMicroRequette=self.__arrTK.createImage(pathLight=emplacementGUILight+fileImage[18],
                                                  pathDark=emplacementGUIDark+fileImage[18],
                                                    tailleX=50,tailleY=50)
        self.__labelTriggerMicro = self.__arrTK.createLabel(self.__screen,width=50,height=50,image=imageMicroTriger,text=" ")
        self.__labelMicroRequette = self.__arrTK.createLabel(self.__screen,width=50,height=50,image=imageMicroRequette,text=" ")
        # Canvas Actu
        self.__labelActu = Label(self.__canvasActu,font=("arial","15"),bg="red", bd=0)
        self.__btnQuitActu = Button(self.__canvasActu,text="Quitter",font=("arial","15"),bg="red",command=self.__quitActu)
        self.__btnReadActu =  Button(self.__canvasActu,text="Lire a voix haute",font=("arial","15"),bg="red")
        self.__btnStopMute = [Button(self.__canvasMute[0],text="Demute",font=("arial","15"),bg="red",command=self.__quitMute),
                             Button(self.__canvasMute[1],text="Demute",font=("arial","15"),bg="red",command=self.__quitMute)]
        self.__btnQuitMute = [Button(self.__canvasMute[0],text="Quitter",font=("arial","15"),bg="red",command=self.__quit),
                             Button(self.__canvasMute[1],text="Quitter",font=("arial","15"),bg="red",command=self.__quit)]   
        # appelle de la methode pour initiliser le gui
        self.__setTheme()
        #Affichage label parole
        self.__labelTextDuringSpeak.place(x=30,y=110)
        self.__labelTextAfterSpeak.place(x=10,y=80)
        self.__labelActu.place(x=70,y=0)
        self.__btnReadActu.place(relx=0, rely=1, anchor='sw')
        self.__btnQuitActu.place(relx=1, rely=1, anchor='se')
        self.__btnStopMute[0].place(relx=0, rely=1, anchor='sw')
        self.__btnQuitMute[0].place(relx=1, rely=1, anchor='se')
        self.__btnStopMute[1].place(relx=0, rely=1, anchor='sw')
        self.__btnQuitMute[1].place(relx=1, rely=1, anchor='se')
        # Mise a place de la touche entree
        if (self.__objetDectOS.osWindows()==True) and (self.__objetDectOS.osLinux()==False) : 
            self.__detectionTouche(self.__envoie,13)
        else :
            if (self.__objetDectOS.osWindows()==False) and (self.__objetDectOS.osLinux()==True) :
                self.__detectionTouche(self.__envoie,36)
    
    def __setTheme(self):

        theme = self.__fileSixConfig.lectureJSON("theme") #Valeur possible "white" et "dark"

        if theme == "white" :
            self.__arrTK.labelChangeColor(self.__labelTextAfterSpeak,bg="#ffffff",fg="#000000")
            self.__arrTK.labelChangeColor(self.__labelActu,bg="#ffffff",fg="#000000")
            self.__arrTK.boutonChangeColor(self.__btnReadActu,bg="#ffffff",fg="#000000")
            self.__arrTK.boutonChangeColor(self.__btnQuitActu,"#ffffff",fg="#000000")
            self.__arrTK.boutonChangeColor(self.__btnStopMute[0],bg="#ffffff",fg="#000000")
            self.__arrTK.boutonChangeColor(self.__btnQuitMute[0],bg="#ffffff",fg="#000000")
            self.__arrTK.boutonChangeColor(self.__btnStopMute[1],bg="#ffffff",fg="#000000")
            self.__arrTK.boutonChangeColor(self.__btnQuitMute[1],bg="#ffffff",fg="#000000")
            self.__arrTK.labelChangeColor(self.__labelTriggerMicro,bg="#ffffff")
            self.__arrTK.labelChangeColor(self.__labelMicroRequette,bg="#ffffff")
            self.__themeNB = 0 
            self.__darkModeEnable = False
        else :
            if theme == "dark" :
                self.__labelMicroRequette.configure(bg="#000000")
                self.__arrTK.labelChangeColor(self.__labelTextAfterSpeak, bg="#000000",fg="#ffffff")
                self.__arrTK.labelChangeColor(self.__labelActu, bg="#000000",fg="#ffffff")
                self.__arrTK.boutonChangeColor(self.__btnReadActu, bg="#000000",fg="#ffffff")
                self.__arrTK.boutonChangeColor(self.__btnQuitActu, bg="#000000",fg="#ffffff")
                self.__arrTK.boutonChangeColor(self.__btnStopMute[0], bg="#000000",fg="#ffffff")
                self.__arrTK.boutonChangeColor(self.__btnQuitMute[0], bg="#000000",fg="#ffffff")
                self.__arrTK.boutonChangeColor(self.__btnStopMute[1], bg="#000000",fg="#ffffff")
                self.__arrTK.boutonChangeColor(self.__btnQuitMute[1], bg="#000000",fg="#ffffff")
                self.__arrTK.labelChangeColor(self.__labelTriggerMicro, bg="#000000")
                self.__arrTK.labelChangeColor(self.__labelMicroRequette, bg="#000000")
                self.__themeNB = 1
                self.__darkModeEnable = True
            else :
                self.__arrTK.labelChangeColor(self.__labelTextAfterSpeak, bg="#ffffff", fg="#000000")
                self.__arrTK.labelChangeColor(self.__labelActu, bg="#ffffff", fg="#000000")
                self.__arrTK.boutonChangeColor(self.__btnReadActu, bg="#ffffff", fg="#000000")
                self.__arrTK.boutonChangeColor(self.__btnQuitActu, "#ffffff", fg="#000000")
                self.__arrTK.boutonChangeColor(self.__btnStopMute[0], bg="#ffffff", fg="#000000")
                self.__arrTK.boutonChangeColor(self.__btnQuitMute[0], bg="#ffffff", fg="#000000")
                self.__arrTK.boutonChangeColor(self.__btnStopMute[1], bg="#ffffff", fg="#000000")
                self.__arrTK.boutonChangeColor(self.__btnQuitMute[1], bg="#ffffff", fg="#000000")
                self.__arrTK.labelChangeColor(self.__labelTriggerMicro, bg="#ffffff")
                self.__arrTK.labelChangeColor(self.__labelMicroRequette, bg="#ffffff")
                self.__themeNB = 0 
                self.__darkModeEnable = False
        self.__labelTextDuringSpeak.configure(bg="#2b3ceb",fg="white")
    

    def active(self):
        theardSequenceBoot = th.Thread(target=self.__sequenceBoot)
        theardSequenceBoot.start()
        self.__screen.mainloop()
    
    def __onClose(self):
        if (askyesno("Atention","Voulez-vous vraiment fermer Six")):
            self.__quit()
    
    def __quit(self):
        if (self.__objetDectOS.osWindows()==True) and (self.__objetDectOS.osLinux()==False) :
            os.kill(os.getpid(), signal.SIGINT)
        else :
            if (self.__objetDectOS.osWindows()==False) and (self.__objetDectOS.osLinux()==True) :
                os.kill(os.getpid(), signal.SIGKILL)
    
    def __sequenceBoot(self):
        self.__canvasBoot0.place(x=0,y=0)
        time.sleep(0.2)
        self.__canvasBoot0.place_forget()
        self.__canvasBoot1.place(x=0,y=0)
        time.sleep(0.2)
        self.__canvasBoot1.place_forget()
        self.__canvasBoot2.place(x=0,y=0)
        time.sleep(0.2)
        self.__canvasBoot2.place_forget()
        self.__canvasBoot3.place(x=0,y=0)
        time.sleep(0.2)
        self.__canvasAcceuil.place(x=0,y=0)
        if (self.__etatConnexion==False):
            self.__canvasAcceuil.place_forget()
            self.__screen.protocol("WM_DELETE_WINDOW",self.__quit)
            self.__canvasNoConnect.place(x=0,y=0)
            self.__screen.update()
        else :
            self.__sequenceParole(self.__six.boot())
            self.__entryUser.pack(side="bottom")
            self.__startingTriggerWord()
    
    def __clearView(self):
        self.__labelTriggerMicro.place_forget()
        self.__canvasAcceuil.place_forget()
        self.__canvasBoot0.place_forget()
        self.__canvasBoot1.place_forget()
        self.__canvasBoot2.place_forget()
        self.__canvasBoot3.place_forget()
        self.__canvasParole1.place_forget()
        self.__canvasParole2.place_forget()
        self.__canvasParole3.place_forget()
        self.__canvasNoConnect.place_forget()
        self.__canvasContent.place_forget()
        self.__canvasColere.place_forget()
        self.__canvasSurprit.place_forget()
        self.__canvasTriste1.place_forget()
        self.__canvasTriste2.place_forget()
        self.__canvasParaOpen.place_forget()
    
    def __sequenceParole(self,texte:str):
        self.__sixSpeaking = True 
        thSpeak = th.Thread(target=paroleSix,args=(texte,))
        self.__clearView()
        self.__canvasParole1.place_forget()
        self.__canvasParole2.place(x=0,y=0)
        self.__labelTextDuringSpeak.configure(text=texte,wraplength=440,justify="left")
        self.__screen.update()
        thSpeak.start()
        thSpeak.join()
        self.__canvasParole2.place_forget()
        self.__canvasParole3.place(x=0,y=0)
        self.__labelTextAfterSpeak.configure(text=texte,wraplength=475,justify="left")
        del thSpeak
        self.__sixSpeaking = False
        
        
    def __sequenceArret(self):
        texte = self.__six.shutdown()
        self.__clearView()
        self.__labelTextDuringSpeak.configure(text=texte,wraplength=320)
        self.__canvasParole2.place(x=0,y=0)
        self.__screen.update()
        paroleSix(texte)
        self.__canvasParole2.place_forget()
        self.__canvasBoot3.place(x=0,y=0)
        self.__screen.update()
        time.sleep(0.2)
        self.__canvasBoot3.place_forget()
        self.__canvasBoot2.place(x=0,y=0)
        self.__screen.update()
        time.sleep(0.2)
        self.__canvasBoot2.place_forget()
        self.__canvasBoot3.place(x=0,y=0)
        self.__screen.update()
        time.sleep(0.2)
        self.__canvasBoot3.place_forget()
        self.__canvasBoot0.place(x=0,y=0)
        self.__screen.update()
        time.sleep(0.2)
        self.__canvasBoot0.place_forget()
        self.__screen.update()

    def __detectionTouche(self,fonc,touche):
        def anychar(event):
            if event.keycode == touche:
                fonc()               
        self.__screen.bind("<Key>", anychar)  
    
    def __envoie(self): 
        if (self.__sixSpeaking==False):
            texte = self.__entryUser.get()
            if ("parametre" in texte ) :
                self.__activeParametre()
            else :
                if (("mute" in texte)or("silence" in texte)or("ta gueule" in texte)):
                    self.__viewMute()
                else :
                    self.__six.neuron(texte)
                    self.__clearView()
                    self.__canvasParole1.place(x=0,y=0)
                    self.__screen.update()
                    nbSortie = self.__six.getNbSortie()
                    if (nbSortie==15):
                        self.__sequenceArret()
                        self.__quit()
                    else :
                        if (nbSortie==11):
                            self.__sequenceParoleReponseNeuron("Désoler, il a un probleme qui m'empeche de vous donner votre résumer")
                        else :
                            listSortie  = self.__six.getListSortie()
                            if (nbSortie==12):
                                self.__sequenceParoleReponseNeuron("Okay voici votre résumer des actualités du jour. J'éspere qui vous sera utile")
                                self.__viewActu(listSortie,1)
                            else :
                                if (nbSortie==3):
                                    self.__sequenceParoleReponseNeuron("Je vous affiche les actualité du moment")
                                    self.__viewActu(listSortie,2)
                                else :
                                    self.__sequenceParoleReponseNeuron(listSortie[0])
            self.__entryUser.delete(0,END)
    
    def __sequenceParoleReponseNeuron(self,text:str):
        self.__canvasParole1.place_forget()
        self.__canvasParole2.place(x=0,y=0)
        self.__labelTextDuringSpeak.configure(text=text,wraplength=440,justify="left")
        self.__screen.update()
        paroleSix(text)
        self.__canvasParole2.place_forget()
        self.__canvasParole3.place(x=0,y=0)
        self.__labelTextAfterSpeak.configure(text=text,wraplength=475,justify="left")

    def __reloadTheme(self):
        self.__setTheme()
        self.__screen.update()
    
    def __activeParametre(self):
        self.__stopingTriggerWord()
        self.__screen.title(self.__nameSoft+" : Parametre")
        self.__screen.maxsize(500,600)
        self.__screen.minsize(500,600)
        self.__screen.update()
        self.__clearView()
        self.__entryUser.pack_forget()
        self.__gazelleUI.active(self.__darkModeEnable)
    
    def __quitParametre(self):
        self.__screen.maxsize(500,400)
        self.__screen.minsize(500,400)
        self.__screen.title(self.__nameSoft)
        self.__screen.update()
        self.__sequenceParole("Les parametre on etais mit a jour")
        self.__startingTriggerWord()
        self.__entryUser.pack(side="bottom")
        self.__reloadTheme()
    
    def __sixTrigerWord(self):
        sortieTriger = int 
        sortieMicro = str
        while not self.__TriggerWorkStop.is_set():
            self.__microTriggerEnable()
            sortieTriger = self.__objTriger.detectWord()
            self.__microTriggerDisable()
            if (sortieTriger == 1 ):
                self.__microRequetteEnable()
                sortieMicro = self.__objSRCSix.micro()
                self.__entryUser.delete(0,END)
                if (sortieMicro!="nothing"):
                    self.__entryUser.insert(0,sortieMicro)
                self.__microRequetteDisable()
                time.sleep(0.2)
                self.__envoie()
    
    def __viewActu(self,listSortie:list,mode:int):
        """
        1 : Resumer 
        2 : actu
        """
        self.__clearView()
        self.__entryUser.pack_forget()
        self.__screen.maxsize(500,600)
        self.__screen.minsize(500,600)
        self.__screen.update()
        self.__canvasActu.place(x=0,y=0)
        match mode :
            case 1 : 
                self.__labelActu.configure(text=listSortie[0]+
                                        "\n"+listSortie[1]+
                                        "\n"+listSortie[2]+
                                        "\n"+listSortie[3]+
                                        "\n"+listSortie[4]+
                                        "\n"+listSortie[5],
                                        justify="left",
                                        wraplength=400)
                self.__btnReadActu.configure(command=lambda:self.__readActu(listSortie[0]+
                                        "."+listSortie[1]+
                                        "."+listSortie[2]+
                                        "."+listSortie[3]+
                                        "."+listSortie[4]+
                                        "."+listSortie[5]))
            case 2 : 
                self.__labelActu.configure(text=listSortie[0]+
                                        "\n"+listSortie[1]+
                                        "\n"+listSortie[2],
                                        justify="left",
                                        wraplength=400)
                self.__btnReadActu.configure(command=lambda:self.__readActu(listSortie[0]+
                                        "."+listSortie[1]+
                                        "."+listSortie[2]))
        self.__stopingTriggerWord()
        self.__thMinuteurActu.start()
    
    def __quitActu(self):
        self.__clearView()
        self.__canvasActu.place_forget()
        self.__screen.maxsize(500,400)
        self.__screen.minsize(500,400)
        self.__screen.update()
        self.__entryUser.pack(side="bottom")
        self.__screen.update()
        self.__sequenceParole("J'éspere que sa vous a étais utile")
        self.__startingTriggerWord()
        del self.__thMinuteurActu
        self.__thMinuteurActu = th.Thread(target=self.__minuteurActu)
    
    def __readActu(self,texte:str):
        thSpeak = th.Thread(target=paroleSix,args=(texte,))
        thSpeak.start()
        thSpeak.join()
        del thSpeak
    
    def __minuteurActu(self):
        time.sleep(60)
        self.__quitActu()
    
    def __viewMute(self):
        self.__sequenceParole("Okay je vous laisse tranquille")
        self.__clearView()
        self.__stopingTriggerWord()
        self.__entryUser.pack_forget()
        self.__screen.maxsize(500,350)
        self.__screen.minsize(500,350)
        self.__screen.update()
        nb = random.randint(0,1)
        self.__canvasMute[nb].place(x=0,y=0)
    
    def __quitMute(self):        
        self.__clearView()
        self.__screen.maxsize(500,400)
        self.__screen.minsize(500,400)
        self.__screen.update()
        self.__canvasMute[0].place_forget()
        self.__canvasMute[1].place_forget()
        self.__entryUser.pack(side="bottom")
        self.__screen.update()
        self.__sequenceParole("Content d'etre de retour")
        self.__startingTriggerWord()
    
    def __microTriggerEnable(self):
        self.__labelTriggerMicro.place(relx=1.0, rely=0.0, anchor='ne')
        self.__screen.update()
    
    def __microTriggerDisable(self):
        self.__labelTriggerMicro.place_forget()
        self.__screen.update()
    
    def __microRequetteEnable(self):
        self.__labelMicroRequette.place(relx=1.0, rely=0.0, anchor='ne')
        self.__screen.update()
    
    def __microRequetteDisable(self):
        self.__labelMicroRequette.place_forget()
        self.__screen.update()
    
    def __startingTriggerWord(self):
        # Création du thread Trigger word
        self.__thTrigger = th.Thread(target=self.__sixTrigerWord)
        self.__TriggerWorkStop.clear()
        self.__thTrigger.start()

    def __stopingTriggerWord(self):
        self.__TriggerWorkStop.set()