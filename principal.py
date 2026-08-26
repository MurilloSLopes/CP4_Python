from cadastroPET import petCreate, petRead, petDelete, petUpdate, petList

from petsDB import db_pets

def exibir_menu() -> None:
    """Exibe as opções do sistema."""
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


def main() -> None:
    """Executa o menu principal até o usuário escolher a opção Sair."""
    while True:
        exibir_menu()

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 6.")
            continue

        if opcao == 1:
            petList(db_pets)

        elif opcao == 2:
            id_pet = input("Digite o ID do PET: ").strip()
            petRead(db_pets, id_pet)

        elif opcao == 3:
            try:
                nome = input("Nome do PET: ").strip()
                tipo = input(
                    "Tipo (Cachorro, Gato, Mamífero, Ave, Réptil ou Outro): "
                ).strip()
                ano = int(input("Ano de nascimento: "))
                petCreate(db_pets, tipo, ano, nome)
            except ValueError as erro:
                print(f"Erro no cadastro: {erro}")

        elif opcao == 4:
            id_pet = input("Digite o ID do PET que deseja remover: ").strip()
            petDelete(db_pets, id_pet)

        elif opcao == 5:
            id_pet = input("Digite o ID do PET que deseja atualizar: ").strip()
            petUpdate(db_pets, id_pet)

        elif opcao == 6:
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida. Escolha um número de 1 a 6.")


if __name__ == "__main__":
    main()
