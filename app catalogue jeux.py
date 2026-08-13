import json
import os

if os.path.exists("fichier.json") and os.path.getsize("fichier.json") > 0:
    with open("fichier.json", "r") as f:
        data = json.load(f) 

else:
    data = []
    with open("fichier.json", "w") as f:
              json.dump(data, f)

def sauvegarder():
    with open("fichier.json", "w") as f:
        json.dump(data, f, indent=4)

quit = False
choice = 1
choice_2 = 1
trouve = False
trouve_2 = False

while quit == False:
    print("Bienvenue dans votre catalogue de jeux 🕹️")
    print(" ")
    print("1. Afficher le catalogue")
    print("2. Ajouter un jeu")
    print("3. Modifier un jeu")
    print("4. Supprimer un jeu")
    print("5. Quitter")
    print(" ")

    try:
        choice = int(input("Votre choix : "))
    except ValueError:
        print("❌ Veuillez entrer un nombre valide !")
        continue

    if choice < 1 or choice > 5:
        print("❌ Veuillez entrer un nombre valide !")
        continue

    print(" ")

    if choice == 1 :
        print("Faites un choix :")
        print(" ")
        print("1. Afficher le catalogue par nom")
        print("2. Afficher le catalogue par console")
        print("3. Afficher le catalogue par genre")
        print("4. Retour")
        print(" ")

        try:
            choice_2 = int(input("Votre choix : "))
        except ValueError:
            print("❌ Veuillez entrer un nombre valide !")
            continue
        
        if choice_2 < 1 or choice_2 > 5:
            print("❌ Veuillez entrer un nombre valide !")
            continue
        
        print(" ")

        if choice_2 == 1:
            sorted_data = sorted(data, key=lambda jeu: jeu["nom"])
            for i in range(len(sorted_data)):
                current = sorted_data[i]
                print(f"{i + 1}. {current['nom']}, {current['console']}, {current['genre']}")

        elif choice_2 == 2:
            sorted_data = sorted(data, key=lambda jeu: jeu["console"])
            for i in range(len(sorted_data)):
                current = sorted_data[i]
                print(f"{i + 1}. {current['nom']}, {current['console']}, {current['genre']}")

        elif choice_2 == 3:
            sorted_data = sorted(data, key=lambda jeu: jeu["genre"])
            for i in range(len(sorted_data)):
                current = sorted_data[i]
                print(f"{i + 1}. {current['nom']}, {current['console']}, {current['genre']}")

        elif choice_2 == 4:
            continue


    elif choice == 2 :
        print("➕ AJOUT D'UN NOUVEAU JEU :")
        print(" ")
        nom = input("Nom du jeu : ")
        console = input("Console : ")
        genre = input("Genre : ")

        nouveau_jeu = {
            "nom": nom,
            "console": console,
            "genre": genre,
        }

        data.append(nouveau_jeu)
        sauvegarder()
        print("✅ Votre jeu à été ajouté avec succès !")

    elif choice == 3 :
        while True:
            print("🔄️MODIFIER UN JEU")
            print(" ")
            game_search = input("Entrez le nom du jeu : ")
            print(" ")
            for i, jeu in enumerate(data, 1):
                if jeu["nom"] == game_search:
                    trouve = True
                    print(f"✅ Jeu trouvé : {jeu['nom']}, {jeu['console']}, {jeu['genre']}")
                    print(" ")
                    jeu_modif = data[i - 1]
                    print(f"Modification de : {jeu_modif['nom']}")
                    print("Laiser vide pour ne pas modifier")
                    print(" ")
                    nouveau_nom = input("Nom : ")
                    if nouveau_nom:
                        jeu_modif['nom'] = nouveau_nom
                    nouvelle_console = input("Console : ")
                    if nouvelle_console:
                        jeu_modif['console'] = nouvelle_console
                    nouveau_genre = input("Genre : ")
                    if nouveau_genre:
                        jeu_modif['genre'] = nouveau_genre
                    sauvegarder()
                    print(" ")
                    print("✅ Jeu Modifié avec succès")
                    print(" ")
                    print(f"{jeu_modif['nom']}, {jeu_modif['console']}, {jeu_modif['genre']}")
                    break

            if not trouve:
                print(f"❌Impossible de trouver {game_search}")
                print(" ")
                quitter = input("ENTRER = réessayer, 'quitter' = quitter : ")
                if quitter:
                    print(" ")
                    break
                continue


    elif choice == 4 :
        boucle = True
        while boucle == True:
            print("🗑️  SUPPRIMER UN JEU")
            print(" ")
            game_search_2 = input("Entrez le nom du jeu : ")
            print(" ")
            for i, jeu in enumerate(data, 1):
                if jeu["nom"] == game_search_2:
                    trouve_2 = True
                    print(f"✅ Jeu trouvé : {jeu['nom']}, {jeu['console']}, {jeu['genre']}")
                    print(" ")
                    jeu_suppr = data[i - 1]
                    print(f"Voulez-vous vraiment supprimer : {jeu_suppr['nom']} ?")
                    check = input("ENTRER = OUI, 'non' = NON : ")
                    if check:
                        print(" ")
                        break
                    print(" ")
                    del data[i-1]
                    sauvegarder()
                    print(" ")
                    print("✅ Jeu Supprimé avec succès")
                    print(" ")
                    boucle = False
                    break

            if not trouve_2:
                print(f"❌ Une Erreur est survenue.")
                print(" ")
                quitter_2 = input("ENTRER = réessayer, 'quitter' = quitter : ")
                if quitter_2:
                    print(" ")
                    break
                continue

    elif choice == 5 :
        quit = True 