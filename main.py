"""""""""
Ceci est un programme avec pour objectif de créer et entretenir un dictionnaire personnalisé.
 --> N'oubliez plus les mots que vous avez appris
"""""""""

# On importe les modules requis pour le projet
from os import listdir
from os import rename, remove
from os.path import isfile, join
from colorama import Fore

# On crée une liste contenant tous les fichiers avec l'extension '.txt' car ils correspondent à des dictionnaires
dir_files = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".txt")]
print(Fore.MAGENTA + "Vos dictionnaires sont :", ', '.join(dir_files) + Fore.RESET)


# On définit une fonction pour créer / supprimer des dictionnaires
def file_manager(opt):
    # On sépare le nom du dictionnaire (si présent) de l'option choisie par l'utilisateur
    option = opt.split("/")

    # On crée un nouveau fichier et on le renomme selon les langues qu'il contient
    if opt == "new":
        open(opt, "x")
        f_name = input("Entrez la langue à traduire : ") + " - " + input("Entrez la langue de traduction : ") + '.txt'
        rename(opt, f_name)
        print(Fore.GREEN + f"Le fichier {f_name} a bien été créé !!" + Fore.RESET)
    # On supprime le fichier indiqué par l'utilisateur s'il existe
    elif option[-1] == "delete":
        try:
            remove(option[0])
            print(Fore.GREEN + f"Le fichier {option[0]} a bien été supprimé !" + Fore.RESET)
        except FileNotFoundError:
            print(Fore.YELLOW + f"Le fichier {option[0]} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
            pass
    return


# On définit une fonction pour lire le contenu d'un dictionnaire
def read_file(file):
    # On récupère le nom du fichier
    dictionary = file.split("/")[0]
    # On vérifie que le fichier existe
    try:
        f = open(dictionary, "r")
    except FileNotFoundError:
        print(Fore.YELLOW + f"Le fichier {dictionary} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
        return

    clean_files(dir_files)

    word = input('Entrez le mot que vous cherchez dans une des deux langues ou "/all" pour afficher tout le dictionnaire : ')

    # On affiche la ligne contenant le mot en question ou alors on affiche la totalité du dictionnaire
    if word == "/all":
        for line in f.readlines():
            expression = line.split(";")
            try:
                expression.remove('\n')
            except ValueError:
                pass
            # print(expression)
            print(''.join(expression))
    else:
        word = word + ";"
        for line in f.readlines():
            if word in line:
                expression = line.split(";")
                try:
                    expression.remove('\n')
                except ValueError:
                    pass
                # print(expression)
                print(''.join(expression))
    return


# On définit une fonction pour ajouter des mots à un dictionnaire
def append_to_file(file):
    # On récupère le nom du fichier
    dictionary = file.split("/")[0]
    # On vérifie que le fichier existe
    try:
        f = open(dictionary, "r")
    except FileNotFoundError:
        print(Fore.YELLOW + f"Le fichier {dictionary} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
        return

    f = open(dictionary, "a")

    to_translate = input("Entrez le mot dans la langue à traduire : ").lower()
    if "/" in to_translate:
        words = to_translate.split("/")
        print(words)
        part_one = ""
        for word in words:
            word = word + ";"
            part_one += word
        print(part_one)
        part_one = part_one[:-1]
        part_one = part_one.replace(";", ";/", 1)
        to_translate = part_one
        print(to_translate)
    translated = input("Entrez le mot dans la langue traduite : ").lower()
    if "/" in translated:
        translations = translated.split("/")
        part_two = ""
        for word in translations:
            word = word + ";"
            part_two += word
        part_two = part_two[:-1]
        part_two = part_two.replace(";", ";/", 1)
        translated = part_two

    # On modifie la syntaxe des expressions pour pouvoir utiliser la fonction "split" sur les ";" plus tard
    line = to_translate + "; = " + translated + ";" + '\n'

    f.write(line)
    print(Fore.GREEN + f"Le mot {to_translate} et sa traduction {translated} ont bien été ajouté au dictionnaire !" + Fore.RESET)

    sort_files(dir_files)
    return


# On définit une fonction pour retirer des expressions d'un dictionnaire
def remove_from_file(file):
    # On récupère le nom du fichier
    dictionary = file.split("/")[0]
    # On vérifie que le fichier existe
    try:
        f = open(dictionary, "r")
    except FileNotFoundError:
        print(Fore.YELLOW + f"Le fichier {dictionary} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
        return

    lines = f.readlines()

    remove_word = input("Quel mot souhaitez-vous retirer du dictionnaire ? ")
    removable_lines = []
    # On ajoute à la liste tous les mots qui contiennent la suite de caractères recherchée
    for line in lines:
        if remove_word in line:
            removable_lines.append(line)

    # On montre à l'utilisateur les expressions trouvées afin qu'il indique celle à supprimer
    for line in removable_lines:
        expression = line.split(";")
        try:
            expression.remove('\n')
        except ValueError:
            pass
        # print(expression)
        print(''.join(expression) + Fore.BLUE + f" index : {removable_lines.index(line)}" + Fore.RESET)

    to_remove = int(input("Entrez l'index de la ligne à retirer : "))
    to_remove = removable_lines[to_remove]

    # On supprime toutes les lignes avant de les écrire à nouveau sauf pour l'expression à supprimer
    with open(dictionary, "w") as f:
        for line in lines:
            if line.strip("\n") != to_remove.rstrip():
                f.write(line)

    print(Fore.GREEN + "L'expression a bien été retirée de votre dictionnaire !" + Fore.RESET)
    return


def sort_files(files):
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
            lines.sort()
        with open(file, 'w') as f:
            for line in lines:
                f.write(line)
    return


def clean_files(files):
    for file in files:
        uniqlines = set(open(file).readlines())
        cleaned_file = open(file, "w").writelines(uniqlines)
    return


sort_files(dir_files)
clean_files(dir_files)

while True:

    opts = input("Entrez <nom>/append pour ajouter des mots à un dictionnaire; <nom>/remove pour retirer un mot d'un dictionnaire; <nom>/read pour en ouvrir un; 'new' pour en créer un nouveau et '<nom>/delete' pour en effacer un. "
                 "Vous pouvez aussi taper \"exit\" pour fermer le programme : ")

    # Pour laisser un espace avant les print de la fonction (je sais plus si le "\n" décale la réponse de l'utilisateur d'une ligne aussi).
    print("")

    # On vérifie l'option choisie par l'utilisateur
    if "append" in opts:
        append_to_file(opts)
    elif "remove" in opts:
        remove_from_file(opts)
    elif "read" in opts:
        read_file(opts)
    elif "new" in opts or "delete" in opts:
        file_manager(opts)
    elif opts == "exit":
        print("A bientôt !")
        exit()

    dir_files = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".txt")]
    print("\n" + Fore.MAGENTA + "Vos dictionnaires sont :", ', '.join(dir_files) + Fore.RESET)
