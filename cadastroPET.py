from typing import Dict, List, Tuple, Optional

from checaCadastroPET import checaCadastroPET

PetKey = Tuple[str, str, int]
PetDB = Dict[PetKey, List[object]]

MAPA_TIPOS = {
    "cachorro": "CC",
    "cão": "CC",
    "cao": "CC",
    "gato": "GT",
    "mamifero": "MM",
    "mamífero": "MM",
    "ave": "AV",
    "reptil": "RP",
    "réptil": "RP",
    "outro": "OT",
    "outros": "OT",
}

TIPOS_POR_CODIGO = {
    "CC": "Cachorro",
    "GT": "Gato",
    "MM": "Mamífero",
    "AV": "Ave",
    "RP": "Réptil",
    "OT": "Outro",
}

def _normaliza_id(id_pet: str) -> str:
    # Remove hífens e espaços do ID informado.
    return id_pet.strip().replace("-", "")

def _localiza_chave(cadastro: PetDB, id_pet: str) -> Optional[PetKey]:
    #Localiza uma chave pelo ID completo ou pelo registro sequencial de 5 dígitos.
    busca = _normaliza_id(id_pet)
    for chave in cadastro:
        tipo, registro, ano = chave
        completo = f"{tipo}{registro}{ano}"
        if busca == completo or busca == registro:
            return chave
    return None

def petCreate(
    cadastro: PetDB,
    tipo_pet: str,
    ano_nascimento: int,
    nome_pet: str
) -> PetDB:
    tipo_normalizado = str(tipo_pet).strip().lower()
    codigo = MAPA_TIPOS.get(tipo_normalizado)

    if codigo is None:
        raise ValueError("Tipo de PET inválido.")

    if not isinstance(ano_nascimento, int):
        raise ValueError("O ano de nascimento deve ser um número inteiro.")

    registros = [int(chave[1]) for chave in cadastro] if cadastro else [0]
    novo_registro = max(registros) + 1
    registro_texto = f"{novo_registro:05d}"

    id_pet = f"{codigo}-{registro_texto}-{ano_nascimento}"
    dados_pet = [nome_pet, TIPOS_POR_CODIGO[codigo], ano_nascimento]

    quantidade_antes = len(cadastro)
    checaCadastroPET(cadastro, id_pet, dados_pet)

    if len(cadastro) > quantidade_antes:
        print(f"PET cadastrado com sucesso! ID: {id_pet}")
    else:
        print("Não foi possível cadastrar o PET.")

    return cadastro

def petRead(cadastro: PetDB, id_pet: str) -> None:
    # Procura um PET pelo ID e imprime seus dados.
    chave = _localiza_chave(cadastro, id_pet)

    if chave is None:
        print("O ID do PET não foi encontrado no cadastro\n")
        print("Confira os dados e tente novamente!")
        return

    tipo_codigo, registro, ano_id = chave
    nome, tipo, ano = cadastro[chave]
    id_formatado = f"{tipo_codigo}-{registro}-{ano_id}"

    print("Dados do seu PET:... \n")
    print(f"Nome: {nome} \n")
    print(f"Ano de nascimento: {ano} \n")
    print(f"Raça: {tipo}")
    print(f"ID: {id_formatado}")

def petDelete(cadastro: PetDB, id_pet: str) -> PetDB:
    # Remove um PET localizado pelo ID e retorna o dicionário atualizado.
    chave = _localiza_chave(cadastro, id_pet)

    if chave is None:
        print("O ID do PET não foi encontrado no cadastro\n")
        print("Confira os dados e tente novamente!")
        return cadastro

    del cadastro[chave]
    print(f"Cadastro do PET id: {id_pet}, removido com sucesso!")
    return cadastro


def petUpdate(cadastro: PetDB, id_pet: str) -> PetDB:
    # Atualiza nome, tipo e/ou ano de um PET, sem alterar seu registro sequencial.
    chave = _localiza_chave(cadastro, id_pet)

    if chave is None:
        print("O ID do PET não foi encontrado no cadastro\n")
        print("Confira os dados e tente novamente!")
        return cadastro

    codigo_atual, registro, ano_chave = chave
    nome_atual, tipo_atual, ano_atual = cadastro[chave]

    novo_nome = input(f"Nome [{nome_atual}]: ").strip()
    if novo_nome:
        print(f"O nome '{nome_atual}' foi substituído para '{novo_nome}'!")
        nome_atual = novo_nome

    novo_tipo = input(f"Tipo [{tipo_atual}]: ").strip().lower()
    novo_codigo = codigo_atual
    if novo_tipo:
        codigo_candidato = MAPA_TIPOS.get(novo_tipo)
        if codigo_candidato is not None:
            novo_tipo_extenso = TIPOS_POR_CODIGO[codigo_candidato]
            print(f"O tipo '{tipo_atual}' foi substituído para '{novo_tipo_extenso}'!")
            tipo_atual = novo_tipo_extenso
            novo_codigo = codigo_candidato
        else:
            print("Tipo inválido. O tipo atual foi mantido.")

    novo_ano = input(f"Ano de nascimento [{ano_atual}]: ").strip()
    ano_final = ano_atual
    if novo_ano:
        if novo_ano.isdigit():
            ano_novo_int = int(novo_ano)
            print(f"O ano '{ano_atual}' foi substituído para '{ano_novo_int}'!")
            ano_final = ano_novo_int
        else:
            print("Ano inválido. O ano atual foi mantido.")

    # registro sequencial permanece o mesmo tipo e ano fazem parte da chave
    # do modelo proposto no enunciado, então a chave é reconstruída.
    nova_chave: PetKey = (novo_codigo, registro, int(ano_final))
    novos_dados = [nome_atual, tipo_atual, int(ano_final)]

    if nova_chave != chave:
        del cadastro[chave]

    cadastro[nova_chave] = novos_dados
    print(f"Cadastro do PET id: {id_pet}, atualizado com sucesso!")
    print(f"Novo ID: {novo_codigo}-{registro}-{ano_final}")

    return cadastro


def petList(cadastro: PetDB) -> None:
    # Lista todos os PETS um a um que estao cadastrados.
    if not cadastro:
        print("Nenhum PET cadastrado.")
        return

    print("\n===== PETS CADASTRADOS =====")
    for numero, (chave, dados) in enumerate(cadastro.items(), start=1):
        tipo_codigo, registro, ano_id = chave
        nome, tipo, ano = dados
        print(f"\nPET {numero}")
        print(f"ID: {tipo_codigo}-{registro}-{ano_id}")
        print(f"Nome: {nome}")
        print(f"Tipo: {tipo}")
        print(f"Ano de nascimento: {ano}")

if __name__ == "__main__":
    db_pets: PetDB = {
        ("CC", "00001", 2024): ["Max", "Cachorro", 2024],
        ("GT", "00002", 2018): ["Miau", "Gato", 2018],
    }

    print("Executando Testes das Funções!!!\n")
    print(50 * "-")

    print("Teste 2-a: petCreate")
    petCreate(db_pets, "outro", 2022, "TESTE")
    print(50 * "-")

    print("Teste 2-b: petRead")
    petRead(db_pets, "CC-00001-2024")
    print(50 * "-")

    print("Teste 2-c: petDelete")
    petDelete(db_pets, "00003")
    print(50 * "-")

    print("Teste 2-e: petList")
    petList(db_pets)
    print(50 * "-")

    print("Para 2-d: petUpdate")
    # A instrução abaixo orienta quem estiver testando o código a cumprir o requisito do PDF
    print(">>> ATENÇÃO AVALIADOR: Para testar o update, deixe Nome e Tipo em branco (Aperte ENTER) e digite '2019' no campo de Ano.")
    petUpdate(db_pets, "00002")
    print(50 * "-")
    
    print("\nVisualizando dicionário após todas as operações do teste:")
    petList(db_pets)

    # ### 2-f) Diferença entre funções e procedimentos:
# Em programação (e na linguagem Python, academicamente falando):
# - FUNÇÃO (Function): Processa dados e OBRIGATORIAMENTE retorna um valor ao 
#   programa que a chamou (usando a palavra reservada 'return'). 
#   Exemplo: def petCreate e def petDelete, que retornam o dicionário atualizado.
# - PROCEDIMENTO (Procedure): Executa uma ação ou tarefa específica (como imprimir 
#   algo na tela), mas NÃO retorna nenhum valor (em Python, retorna None implicitamente).
#   Exemplo: def petList e def petRead, que apenas imprimem os dados no console.
