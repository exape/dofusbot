# mining()
# Mining entry point
def mining():
    print("Mining selectionné")
    print("Saisir la méthode de detection par OpenCV:")
    print("1 pour TM_CCOEFF_NORMED")
    print("2 pour TM_CCORR_NORMED")
    print("3 pour sortir du programme")
    choice = input("Choix: ")
    match choice:
        case "3":
            exit(0)
        case "1":
            method = "TM_CCOEFF_NORMED"
        case "2":
            method = "TM_CCORR_NORMED"
        case _:
            print("Erreur de saisie. Veuillez vérifier la syntaxe et ré-essayer.")

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
            mining()
        case _:
            print("Erreur de saisie. Veuillez vérifier la syntaxe et ré-essayer.")

main()