from typing import Dict, List, Tuple

PetKey = Tuple[str, str, int]
PetsDB = Dict[PetKey, List[object]]

TIPOS_VALIDOS = ("CC", "GT", "MM", "AV", "RP", "OT")

# EXERCÍCIO 1-a: Função checaCadastroPET

# O objetivo desta função é não deixar passar nenhum ID bagunçado. A gente recebe o ID, 
# vê se ele tem o tamanho certo (11 caracteres se não tiver hífen) e analisa 3 coisas:
# 1. Os 2 primeiros dígitos (o tipo de animal).
# 2. Os 5 dígitos do meio (que é o registro sequencial e não pode começar do zero).
# 3. Os 4 últimos dígitos (que formam o ano de nascimento).
# Se passar em tudo, a gente adiciona no dicionário. Se der ruim, devolvemos como estava!


def checaCadastroPET(
    cadastro: PetsDB,
    id_pet: str,
    dados_pet: List[object]
) -> PetsDB:
    if not isinstance(id_pet, str):
        return cadastro
        
    # Primeiro, vamos ver como esse ID chegou para a gente e dar uma limpada nele (tiando os espaços e etc....
    if len(id_pet) == 13:
        if id_pet[2] != "-" or id_pet[8] != "-":
            return cadastro
        id_normalizado = id_pet.replace("-", "")
    elif len(id_pet) == 11:
        if "-" in id_pet:
            return cadastro
        id_normalizado = id_pet
    else:
        return cadastro
        
    # depois de limpar se ele não tiver exatamente 11 caracteres, a gente trava ele!
    if len(id_normalizado) != 11:
        return cadastro

    # Corta a string para pegar cada pedaço da informação..
    tipo = id_normalizado[:2]
    registro = id_normalizado[2:7]
    ano_texto = id_normalizado[7:11]

    # Checando se o tipo de animal existe na nossa lista de tipos validos 
    if tipo not in TIPOS_VALIDOS:
        return cadastro

    # O registro precisa ter cinco dígitos e começar do 1 (assim evita que comece com 00000)
    if not registro.isdigit() or int(registro) < 1:
        return cadastro

    # O ano tem que ser so número e ter 4 dígitos
    if not ano_texto.isdigit() or len(ano_texto) != 4:
        return cadastro

    chave: PetKey = (tipo, registro, int(ano_texto))

    # Se esse pet já existe na nossa base, a gente recusa pra não duplicar.
    if chave in cadastro:
        return cadastro

    # Tudo certo! Adicionamos os dados e devolvemos o dicionário atualizado.
    cadastro[chave] = dados_pet
    return cadastro
#===================================================================================================================

# EXERCÍCIO 1-b: Bloco de Testes da função de validação

# Esse "if __name__ == '__main__':" é um truque bem legal do Python. Ele diz:
# "Só rode esses testes de mentirinha se eu executar ESSE arquivo direto". 
# Se outro arquivo importar ele (como o principal.py), isso aqui fica escondidinho e não roda nada dele.

if __name__ == "__main__":
    
    # Dicionário inicial que pediu pra gente usar de cobaia
    db_pets = {
        ("CC", "00001", 2024): ['Max', 'Cachorro', 2024],
        ("GT", "00002", 2018): ['Miau', 'Gato', 2018],
    }

    # Dados falsos pra gente testar se a função
    dados_teste1 = ['Lulu', 'Cachorro', 2020]
    id_teste1 = "CC-00001-2023" # ID formatado para teste 1

    dados_teste2 = ['Loro', 'Ave', 2025]
    id_teste2 = "AV-00003-2025" # ID formatado para teste 2

    print("--- Testando checaCadastroPET ---")
    print("\nDicionário ANTES dos testes (olha quem já tava aí):")
    print(db_pets)

    # Executando Teste 1
    print("\nExecutando Teste 1 (Será que a Lulu entra?):")
    db_pets = checaCadastroPET(db_pets, id_teste1, dados_teste1)
    
    # Executando Teste 2
    print("\nExecutando Teste 2 (Será que o Loro entra?):")
    db_pets = checaCadastroPET(db_pets, id_teste2, dados_teste2)

    print("\nDicionário DEPOIS dos testes (Vê quem ficou no final):")
    print(db_pets)