import json
import os
import sys

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FICHIER_JSON = os.path.join(SCRIPT_DIR, "fichier.json")

# Ensure proper encoding for console output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

if os.path.exists(FICHIER_JSON) and os.path.getsize(FICHIER_JSON) > 0:
    with open(FICHIER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f)

def sauvegarder():
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def recherche_en_temps_reel():
    """Recherche dynamique : affiche les résultats au fur et à mesure de la saisie"""
    if not data:
        print("❌ Aucun jeu dans le catalogue. Ajoutez d'abord des jeux.")
        input("Appuyez sur Entrée pour revenir au menu...")
        return

    # Cross-platform key reading
    def get_key():
        if os.name == 'nt':
            import msvcrt
            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):  # Special keys (arrows, etc.)
                key2 = msvcrt.getch()
                return key + key2  # e.g. b'\xe0H' pour Haut
            return key
        else:
            import sys, tty, termios, select
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    # Vérifie s'il s'agit d'une séquence d'échappement (flèche)
                    # ou d'une vraie touche Échap seule
                    if select.select([sys.stdin], [], [], 0.05)[0]:
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[' and select.select([sys.stdin], [], [], 0.05)[0]:
                            ch3 = sys.stdin.read(1)
                            return ('\x1b[' + ch3).encode('utf-8')
                        return (ch + ch2).encode('utf-8')
                    return ch.encode('utf-8')
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return ch.encode('utf-8')

    search_term = ""
    selected_index = 0

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("🔍 RECHERCHE EN TEMPS RÉEL")
            print("Tapez pour rechercher (Entrée pour sélectionner, Échap pour revenir)")
            print(f"Recherche : {search_term}", end="", flush=True)
            print("\n" + "-"*50)

            if search_term:
                filtered = [jeu for jeu in data if
                           search_term.lower() in jeu["nom"].lower() or
                           search_term.lower() in jeu["console"].lower() or
                           search_term.lower() in jeu["genre"].lower()]
            else:
                filtered = data[:]

            if not filtered:
                print("❌ Aucun résultat trouvé")
            else:
                for i, jeu in enumerate(filtered):
                    prefix = "→ " if i == selected_index else "  "
                    print(f"{prefix}{i+1}. {jeu['nom']} | {jeu['console']} | {jeu['genre']}")

            print("\n" + "-"*50)
            print("↑/↓ : Naviguer | Entrée : Sélectionner | Échap : Retour")

            key = get_key()
            if key == b'\x1b':  # Échap
                break
            elif key in (b'\r', b'\n'):  # Entrée
                if filtered and 0 <= selected_index < len(filtered):
                    jeu = filtered[selected_index]
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("✅ JEU SÉLECTIONNÉ")
                    print(f"Nom : {jeu['nom']}")
                    print(f"Console : {jeu['console']}")
                    print(f"Genre : {jeu['genre']}")
                    print("\nAppuyez sur Entrée pour revenir à la recherche...")
                    try:
                        get_key()  # Wait for any key
                    except:
                        break
            elif key in (b'\x08', b'\x7f'):  # Backspace
                if search_term:
                    search_term = search_term[:-1]
                    selected_index = 0
            elif key in (b'\xe0H', b'\x00H', b'\x1b[A'):  # Haut (Windows & Unix)
                if filtered:
                    selected_index = (selected_index - 1) % len(filtered)
            elif key in (b'\xe0P', b'\x00P', b'\x1b[B'):  # Bas (Windows & Unix)
                if filtered:
                    selected_index = (selected_index + 1) % len(filtered)
            elif len(key) == 1 and 32 <= key[0] <= 126:  # Printable ASCII
                search_term += key.decode('utf-8', errors='ignore')
                selected_index = 0
    except KeyboardInterrupt:
        pass
    finally:
        pass  # Settings already restored in get_key for Unix

quit = False
choice = 1
choice_2 = 1
trouve = False
trouve_2 = False

while not quit:
    print("Bienvenue dans votre catalogue de jeux 🕹️")
    print(" ")
    print("1. Afficher le catalogue")
    print("2. Ajouter un jeu")
    print("3. Modifier un jeu")
    print("4. Supprimer un jeu")
    print("5. Recherche en temps réel")
    print("6. Quitter")
    print(" ")

    try:
        choice_input = input("Votre choix : ")
        if not choice_input:
            continue
        choice = int(choice_input)
    except (ValueError, EOFError):
        print("❌ Veuillez entrer un nombre valide !")
        continue

    if choice < 1 or choice > 6:
        print("❌ Veuillez entrer un nombre valide !")
        continue

    print(" ")

    if choice == 1:
        print("Faites un choix :")
        print(" ")
        print("1. Afficher le catalogue par nom")
        print("2. Afficher le catalogue par console")
        print("3. Afficher le catalogue par genre")
        print("4. Retour")
        print(" ")

        try:
            choice_2_input = input("Votre choix : ")
            if not choice_2_input:
                continue
            choice_2 = int(choice_2_input)
        except (ValueError, EOFError):
            print("❌ Veuillez entrer un nombre valide !")
            continue

        if choice_2 < 1 or choice_2 > 4:
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

    elif choice == 2:
        print("➕ AJOUT D'UN NOUVEAU JEU :")
        print(" ")
        try:
            nom = input("Nom du jeu : ")
            if nom is None:
                continue
            console = input("Console : ")
            if console is None:
                continue
            genre = input("Genre : ")
            if genre is None:
                continue
        except EOFError:
            continue

        nouveau_jeu = {
            "nom": nom,
            "console": console,
            "genre": genre,
        }

        data.append(nouveau_jeu)
        sauvegarder()
        print("✅ Votre jeu a été ajouté avec succès !")

    elif choice == 3:
        while True:
            print("🔄️ MODIFIER UN JEU")
            print(" ")
            try:
                game_search = input("Entrez le nom du jeu : ")
                if game_search is None:
                    break
                if not game_search:
                    print("❌ Veuillez entrer un nom de jeu !")
                    continue
            except EOFError:
                break

            print(" ")
            trouve = False
            for i, jeu in enumerate(data):
                if jeu["nom"] == game_search:
                    trouve = True
                    print(f"✅ Jeu trouvé : {jeu['nom']}, {jeu['console']}, {jeu['genre']}")
                    print(" ")
                    print("Laisser vide pour ne pas modifier")
                    print(" ")
                    try:
                        nouveau_nom = input("Nom : ")
                        if nouveau_nom is None:
                            nouveau_nom = ""
                        nouvelle_console = input("Console : ")
                        if nouvelle_console is None:
                            nouvelle_console = ""
                        nouveau_genre = input("Genre : ")
                        if nouveau_genre is None:
                            nouveau_genre = ""
                    except EOFError:
                        break

                    if nouveau_nom:
                        jeu['nom'] = nouveau_nom
                    if nouvelle_console:
                        jeu['console'] = nouvelle_console
                    if nouveau_genre:
                        jeu['genre'] = nouveau_genre
                    sauvegarder()
                    print(" ")
                    print("✅ Jeu modifié avec succès")
                    print(" ")
                    print(f"{jeu['nom']}, {jeu['console']}, {jeu['genre']}")
                    break

            if not trouve:
                print(f"❌ Impossible de trouver {game_search}")
                print(" ")
                try:
                    quitter = input("ENTRER = réessayer, 'quitter' = quitter : ")
                    if quitter is None:
                        break
                    if quitter.lower() == 'quitter':
                        break
                except EOFError:
                    break
                continue
            break

    elif choice == 4:
        while True:
            print("🗑️  SUPPRIMER UN JEU")
            print(" ")
            try:
                game_search_2 = input("Entrez le nom du jeu : ")
                if game_search_2 is None:
                    break
                if not game_search_2:
                    print("❌ Veuillez entrer un nom de jeu !")
                    continue
            except EOFError:
                break

            print(" ")
            trouve_2 = False
            for i, jeu in enumerate(data):
                if jeu["nom"] == game_search_2:
                    trouve_2 = True
                    print(f"✅ Jeu trouvé : {jeu['nom']}, {jeu['console']}, {jeu['genre']}")
                    print(" ")
                    print(f"Voulez-vous vraiment supprimer : {jeu['nom']} ?")
                    try:
                        check = input("ENTRER = OUI, 'non' = NON : ")
                        if check is None:
                            break
                        if check.lower() == 'non':
                            print(" ")
                            break
                    except EOFError:
                        break

                    print(" ")
                    del data[i]
                    sauvegarder()
                    print(" ")
                    print("✅ Jeu supprimé avec succès")
                    print(" ")
                    break

            if not trouve_2:
                print(f"❌ Impossible de trouver {game_search_2}")
                print(" ")
                try:
                    quitter_2 = input("ENTRER = réessayer, 'quitter' = quitter : ")
                    if quitter_2 is None:
                        break
                    if quitter_2.lower() == 'quitter':
                        break
                except EOFError:
                    break
                continue
            break

    elif choice == 5:
        recherche_en_temps_reel()

    elif choice == 6:
        quit = True
        print("Au revoir !")