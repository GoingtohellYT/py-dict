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

if not "settings.txt" in dir_files:
    with open("settings.txt", 'x') as config:
        config.write("language : default\ndisplay : column")
else:
    dir_files.remove('settings.txt')

# On récupère les paramètres choisis pour le programme
config_f = open("settings.txt", 'r')
setting_lines = config_f.readlines()
prog_display = setting_lines[1].split(':')[1].lstrip().rstrip()
prog_language = setting_lines[0].split(':')[1].lstrip().rstrip()
# print(prog_language)

if prog_language == "default" or prog_language == "fr":
    print(Fore.MAGENTA + "Vos dictionnaires sont :", ', '.join(dir_files) + Fore.RESET)
elif prog_language == "eng":
    print(Fore.MAGENTA + "Your dictionaries are:", ', '.join(dir_files) + Fore.RESET)


# On définit une fonction pour modifier le fichier de configuration du programme
def modify_config():
    parameters = ["lang", "display"]
    languages = ["fr", "eng", "default"]
    displays = ["line", "column"]

    if prog_language == "default" or prog_language == "fr":
        print(Fore.BLUE + "Voici les paramètres que vous pouvez modifier : " + ", ".join(parameters) + Fore.RESET)
        parameter = input("Quel paramètre souhaitez-vous modifier ? : ")
    elif prog_language == "eng":
        print(Fore.BLUE + "Here are the settings you can modify: " + ", ".join(parameters) + Fore.RESET)
        parameter = input("What setting do you wish to modify? : ")

    # On modifie le paramètre de langue
    if parameter == "lang":
        if prog_language == "default" or prog_language == "fr":
            usr_lang = input(f"Choisissez une langue parmi {', '.join(languages)} :")
        elif prog_language == "eng":
            usr_lang = input(f"Chose a language between {', '.join(languages)}:")

        # On s'assure que la langue demandée est supportée avant de d'appliquer la modification
        if usr_lang in languages:
            config = open("settings.txt", 'r')
            lines = config.readlines()

            # On modifie la ligne qui correspond au paramètre en question
            lines[0] = 'language : ' + usr_lang + "\n"

            # On applique la modification
            with open("settings.txt", 'w') as config:
                for line in lines:
                    config.write(line)

        else:
            if prog_language == "default" or prog_language == "fr":
                print(Fore.YELLOW + "Cette langue n'est pas supportée" + Fore.RESET)
            elif prog_language == "eng":
                print(Fore.YELLOW + "This language is not supported" + Fore.RESET)

    # On modifie le paramètre d'affichage
    elif parameter == "display":
        if prog_language == "default" or prog_language == "fr":
            usr_display = input(f"Choisissez un mode d'affichage parmi {', '.join(displays)} : ")
        elif prog_language == "eng":
            usr_display = input(f"Chose a display mode mode between {', '.join(displays)}: ")

        # On s'assure que le mode d'affichage demandé est supporté
        if usr_display in displays:
            config = open("settings.txt", "r")
            lines = config.readlines()

            # On modifie la ligne qui correspond au paramètre
            lines[1] = "display : " + usr_display

            # On applique la modification
            with open("settings.txt", 'w') as config:
                for line in lines:
                    config.write(line)
    else:
        if prog_language == "default" or prog_language == "fr":
            print(Fore.YELLOW + "Ce paramètre n'existe pas ou ne peut être modifié" + Fore.RESET)
        elif prog_language == "eng":
            print(Fore.YELLOW + "This setting does not exist or cannot be modified" + Fore.RESET)


# On définit une fonction pour créer / supprimer des dictionnaires
def file_manager(opt):
    # On sépare le nom du dictionnaire (si présent) de l'option choisie par l'utilisateur
    option = opt.split("/")

    # On crée un nouveau fichier et on le renomme selon les langues qu'il contient
    if opt == "new":
        open(opt, "x")
        if prog_language == "default" or prog_language == "fr":
            f_name = input("Entrez la langue à traduire : ") + " - " + input(
                "Entrez la langue de traduction : ") + '.txt'
        elif prog_language == "eng":
            f_name = input("Enter the language to be translated: ") + " - " + input(
                "Enter the language of traduction: ") + '.txt'
        rename(opt, f_name)
        if prog_language == "default" or prog_language == "fr":
            print(Fore.GREEN + f"Le fichier {f_name} a bien été créé !!" + Fore.RESET)
        elif prog_language == "eng":
            print(Fore.GREEN + f"The file {f_name} has been created!!")
    # On supprime le fichier indiqué par l'utilisateur s'il existe
    elif option[-1] == "delete":
        try:
            remove(option[0])
            if prog_language == "default" or prog_language == "fr":
                print(Fore.GREEN + f"Le fichier {option[0]} a bien été supprimé !" + Fore.RESET)
            elif prog_language == "eng":
                print(Fore.GREEN + f"The file {option[0]} has been deleted!" + Fore.RESET)
        except FileNotFoundError:
            if prog_language == "default" or prog_language == "fr":
                print(
                    Fore.YELLOW + f"Le fichier {option[0]} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
            elif prog_language == "eng":
                print(
                    Fore.YELLOW + f"The file {option[0]} does not exist. Please try again with an existing dictionary" + Fore.RESET)
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
        if prog_language == "default" or prog_language == "fr":
            print(
                Fore.YELLOW + f"Le fichier {dictionary} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
        elif prog_language == "eng":
            print(
                Fore.YELLOW + f"The file {dictionary} does not exist. Please try again with an existing dictionary" + Fore.RESET)
        return

    clean_files(dir_files)
    sort_files(dir_files)

    if prog_language == "default" or prog_language == "fr":
        word = input(
            'Entrez le mot que vous cherchez dans une des deux langues ou "/all" pour afficher tout le dictionnaire : ')
    elif prog_language == "eng":
        word = input(
            'Enter the word you\'re looking for in one of the two languages or "/all" to print the entire dictionary: ')

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
        if prog_language == "default" or prog_language == "fr":
            print(
                Fore.YELLOW + f"Le fichier {dictionary} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
        elif prog_language == "eng":
            print(
                Fore.YELLOW + f"The file {dictionary} does not exist. Please try with an existing dictionary" + Fore.RESET)
        return

    f = open(dictionary, "a")

    if prog_language == "default" or prog_language == "fr":
        to_translate = input(
            "Entrez le mot dans la langue à traduire (vous pouvez entrer plusieurs mots avec la même traduction en les séparant par un \"/\") : ").lower()
    elif prog_language == "eng":
        to_translate = input(
            "Enter the word in the language to translate (you may enter over one word with the same translation by separating them with a \"/\"): ").lower()

    if "/" in to_translate:
        if prog_display == "line":
            words = to_translate.split("/")
            # print(words)
            part_one = ""
            for word in words:
                word = word + ";"
                part_one += word
            # print(part_one)
            part_one = part_one[:-1]
            part_one = part_one.replace(";", ";/", 1)
            to_translate = part_one
            # print(to_translate)
        if prog_display == "column":
            words = to_translate.split("/")

    if prog_language == "default" or prog_language == "fr":
        translated = input(
            "Entrez le mot dans la langue traduite (vous pouvez entrer plusieurs traductions du même mot en les séparant par un \"/\") : ").lower()
    elif prog_language == "eng":
        translated = input(
            "Enter the word in the translation language (you may enter over one translation of the same word by separating them with a \"/\"): ").lower()

    if "/" in translated:
        if prog_display == "line":
            translations = translated.split("/")
            part_two = ""
            for word in translations:
                word = word + ";"
                part_two += word
            part_two = part_two[:-1]
            part_two = part_two.replace(";", ";/", 1)
            translated = part_two
        elif prog_display == "column":
            translations = translated.split("/")

    # On modifie la syntaxe des expressions pour pouvoir utiliser la fonction "split" sur les ";" plus tard
    if "/" in to_translate and "/" in translated and prog_display == "column":
        for word in words:
            for translation in translations:
                line = word + "; = " + translation + ";" + "\n"
                f.write(line)
    elif "/" in to_translate and "/" not in translated and prog_display == "column":
        for word in words:
            line = word + "; = " + translated + ";" + "\n"
            f.write(line)
    elif "/" not in to_translate and "/" in translated and prog_display == "column":
        for translation in translations:
            line = to_translate + "; = " + translation + ";" + "\n"
            f.write(line)
    else:
        line = to_translate + "; = " + translated + ";" + '\n'
        f.write(line)

    if prog_language == "default" or prog_language == "fr":
        print(
            Fore.GREEN + f"Le mot {to_translate} et sa traduction {translated} ont bien été ajouté au dictionnaire !" + Fore.RESET)
    elif prog_language == "eng":
        print(
            Fore.GREEN + f"The word {to_translate} and its translation {translated} have been added to the dictionary!" + Fore.RESET)

    f.close()
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
        if prog_language == "default" or prog_language == "fr":
            print(
                Fore.YELLOW + f"Le fichier {dictionary} n'existe pas. Veuillez essayer à nouveau avec un dictionnaire valide" + Fore.RESET)
        elif prog_language == "eng":
            print(
                Fore.YELLOW + f"The file {dictionary} does not exist. Please try with an existing dictionary" + Fore.RESET)
        return

    lines = f.readlines()

    if prog_language == "default" or prog_language == "fr":
        remove_word = input("Quel mot souhaitez-vous retirer du dictionnaire ? : ")
    elif prog_language == "eng":
        remove_word = input("Which word do you wish to remove from the dictionary? : ")
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

    if prog_language == "default" or prog_language == "fr":
        to_remove = int(input("Entrez l'index de la ligne à retirer : "))
    elif prog_language == "eng":
        to_remove = int(input("Enter the index of the line to remove: "))
    to_remove = removable_lines[to_remove]

    # On supprime toutes les lignes avant de les écrire à nouveau sauf pour l'expression à supprimer
    with open(dictionary, "w") as f:
        for line in lines:
            if line.strip("\n") != to_remove.rstrip():
                f.write(line)

    if prog_language == "default" or prog_language == "fr":
        print(Fore.GREEN + "L'expression a bien été retirée de votre dictionnaire !" + Fore.RESET)
    elif prog_language == "eng":
        print(Fore.GREEN + "this expression has been removed from your dictionary!" + Fore.RESET)
    return


# On définit une fonction pour classer les mots des dictionnaires dans l'ordre alphabétique
def sort_files(files):
    for file in files:
        with open(file, "r") as fin:
            lines = sorted(fin.readlines())

        with open(file, 'w') as fout:
            fout.writelines(lines)
            fout.close()
    return


# On définit une fonction pour supprimer les doublons dans les dictionnaires
def clean_files(files):
    for file in files:
        uniqlines = set(open(file).readlines())
        cleaned_file = open(file, "w").writelines(uniqlines)
    return


sort_files(dir_files)
clean_files(dir_files)

while True:

    if prog_language == "default" or prog_language == "fr":
        opts = input(
            "Entrez <nom>/append pour ajouter des mots à un dictionnaire; <nom>/remove pour retirer un mot d'un dictionnaire; <nom>/read pour en ouvrir un; \"new\" pour en créer un nouveau et <nom>/delete pour en effacer un. "
            "Vous pouvez aussi taper \"exit\" pour fermer le programme ou \"config\" pour modifier les paramètres du programme : ")
    elif prog_language == "eng":
        opts = input(
            "Enter <name>/append to add words to a dictionary; <name>/remove to remove words from a dictionary; <name>/read to open one, \"new\" to create a new one and <name>/delete to delete a dictionary."
            "Vous may as well enter \"exit\" to end the script or \"config\" to modify the script's settings: ")

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
    elif opts == "config":
        modify_config()
    elif opts == "exit":
        if prog_language == "default" or prog_language == "fr":
            print("A bientôt !")
        elif prog_language == "eng":
            print("See you soon!")
        exit()

    dir_files = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".txt")]
    dir_files.remove("settings.txt")

    if prog_language == "default" or prog_language == "fr":
        print(Fore.MAGENTA + "\nVos dictionnaires sont :", ', '.join(dir_files) + Fore.RESET)
    elif prog_language == "eng":
        print(Fore.MAGENTA + "\nYour dictionaries are:", ', '.join(dir_files) + Fore.RESET)
