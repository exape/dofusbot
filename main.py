from src import miningModule

mining = miningModule.Mining()

# main()
# Dofusbot entry point
def main():
    print("Saisir la ressource souhaitée:")
    print("1 pour le minage")
    print("2 pour sortir du programme")
    choice = input("Choix: ")
    match choice:
        case "2":
            exit(0)
        case "1":
            mining.setupMining()
        case _:
            print("Erreur de saisie. Veuillez vérifier la syntaxe et ré-essayer.")
            exit(1)
main()