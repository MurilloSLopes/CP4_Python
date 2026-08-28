from cadastroPET import petCreate, petRead, petDelete, petUpdate, petList
from petsDB import db_pets

def exibir_menu() -> None:
    # A interface para o usuário escolher o que quer fazer.
    print("\n" + "=" * 40)
    print("       SISTEMA DE CADASTRO DE PETS")
    print("=" * 40)
    print("1 - Listar todos os PETS")
    print("2 - Buscar PET")
    print("3 - Cadastrar PET")
    print("4 - Descadastrar PET")
    print("5 - Atualizar PET")
    print("6 - Sair")
    print("=" * 40)

# ========================================================================================


# EXERCÍCIO 3-a: Módulo Principal
# Aqui usamos um "while True" pra manter o menu 
# aparecendo até a pessoa digitar "6" (Sair).
# Também usamos blocos Try/Except para que o programa não "quebre" se o usuário 
# digitar uma letra quando pedirmos o Ano, por exemplo.

def main() -> None:
    while True:
        exibir_menu()

        try:
            # Capturando o que o usuário quer fazer...
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Entrada inválida! Digita um número de 1 a 6.")
            continue # O continue joga de volta pro topo do While

        if opcao == 1:
            petList(db_pets)

        elif opcao == 2:
            id_pet = input("Digite o ID do PET (ex: CC000012024): ").strip()
            petRead(db_pets, id_pet)

        elif opcao == 3:
            #atenção com Try/Except no cadastro
            try:
                nome = input("Qual o Nome do PET? ").strip()
                tipo = input(
                    "Qual a Espécie (Cachorro, Gato, Mamífero, Ave, Réptil ou Outro)? "
                ).strip()
                ano = int(input("Em que ano ele nasceu? "))
                petCreate(db_pets, tipo, ano, nome)
            except ValueError as erro:
                print(f"Ocorreu um erro no cadastro: {erro}. Tenta preencher novamente!")

        elif opcao == 4:
            id_pet = input("Digite o ID do PET que você quer remover: ").strip()
            petDelete(db_pets, id_pet)

        elif opcao == 5:
            id_pet = input("Digite o ID do PET que você quer atualizar: ").strip()
            petUpdate(db_pets, id_pet)

        elif opcao == 6:
            print("Encerrando o sistema... 🐾")
            break # O break encerra o laço While (e por consequência, o programa)

        else:
            print("Opção inválida. Tem que ser um número de 1 a 6!")


# execute a função main"
if __name__ == "__main__":
    main()