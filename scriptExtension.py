from src.voice import*
"""
    Fichier qui vous permez de developer vos propre extension
    
"""
def Extension(var,genre,user):
    if "test" in var: #Var correspond au micro 
        speak("Sa marche"+genre+" "+user) # Permet de faire parler l'assistant / genre corespond au genre en court uttiliser dans l'assistant / user corespont au nom 