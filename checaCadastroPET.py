from typing import Dict, List, Tuple

PetKey = Tuple[str, str, int]
PetsDB = Dict[PetKey, List[object]]

TIPOS_VALIDOS = ("CC", "GT", "MM", "AV", "RP", "OT")

def checaCadastroPET(
    cadastro: PetsDB,
    id_pet: str,
    dados_pet: List[object]
) -> PetsDB:
    if not isinstance(id_pet, str):
        return cadastro
    #diferencia e validar os dois formatos.
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
    #ID deve ter exatamente 11 caracteres.
    if len(id_normalizado) != 11:
        return cadastro

    tipo = id_normalizado[:2]
    registro = id_normalizado[2:7]
    ano_texto = id_normalizado[7:11]

    # Checa o tipo usando uma referência.
    if tipo not in TIPOS_VALIDOS:
        return cadastro

    # Registro cinco dígitos e iniciado em 1, não em 0.
    if not registro.isdigit() or int(registro) < 1:
        return cadastro

    # Ano- quatro dígitos numéricos.
    if not ano_texto.isdigit() or len(ano_texto) != 4:
        return cadastro

    chave: PetKey = (tipo, registro, int(ano_texto))

    # Se a chave já existir, recusa o cadastro.
    if chave in cadastro:
        return cadastro

    cadastro[chave] = dados_pet
    return cadastro

if __name__ == "__main__":
    # Dicionário inicial exigido no PDF
    db_pets = {
        ("CC", "00001", 2024): ['Max', 'Cachorro', 2024],
        ("GT", "00002", 2018): ['Miau', 'Gato', 2018],
    }

    # Dados de teste exigidos
    dados_teste1 = ['Lulu', 'Cachorro', 2020]
    id_teste1 = "CC-00001-2023" # ID formatado para teste 1

    dados_teste2 = ['Loro', 'Ave', 2025]
    id_teste2 = "AV-00003-2025" # ID formatado para teste 2

    print("--- Testando checaCadastroPET ---")
    print("\nDicionário ANTES dos testes:")
    print(db_pets)

    # Executando Teste 1
    print("\nExecutando Teste 1 (cadastroTeste1):")
    db_pets = checaCadastroPET(db_pets, id_teste1, dados_teste1)
    
    # Executando Teste 2
    print("\nExecutando Teste 2 (cadastroTeste2):")
    db_pets = checaCadastroPET(db_pets, id_teste2, dados_teste2)

    print("\nDicionário DEPOIS dos testes:")
    print(db_pets)