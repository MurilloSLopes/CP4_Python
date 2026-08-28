from typing import Dict, List, Tuple, Optional

from checaCadastroPET import checaCadastroPET

PetKey = Tuple[str, str, int]
PetDB = Dict[PetKey, List[object]]

# Esses mapas ajudam a gente a traduzir o que o usuário digita (ex: "gato") 
# para a sigla certa ("GT") e vice-versa, sem dor de cabeça.

MAPA_TIPOS = {
    "cachorro": "CC", "cão": "CC", "cao": "CC",
    "gato": "GT",
    "mamifero": "MM", "mamífero": "MM",
    "ave": "AV",
    "reptil": "RP", "réptil": "RP",
    "outro": "OT", "outros": "OT",
}

TIPOS_POR_CODIGO = {
    "CC": "Cachorro", "GT": "Gato", "MM": "Mamífero",
    "AV": "Ave", "RP": "Réptil", "OT": "Outro",
}

def _normaliza_id(id_pet: str) -> str:
    # Funçãozinha interna só pra dar uma limpada no ID (tirar hifens e espaços extras)
    return id_pet.strip().replace("-", "")

def _localiza_chave(cadastro: PetDB, id_pet: str) -> Optional[PetKey]:
    # Essa função é nosso "buscador oficial". Ela tenta achar a chave do pet
    # comparando tanto o ID inteiro, quanto apenas aquele registro do meio de 5 dígitos.
    busca = _normaliza_id(id_pet)
    for chave in cadastro:
        tipo, registro, ano = chave
        completo = f"{tipo}{registro}{ano}"
        if busca == completo or busca == registro:
            return chave
    return None

# ========================================================================================



# EXERCÍCIO 2-a: Função petCreate[cite: 12]
# Essa função recebe os dados do animal, converte o tipo dele pra código, 
# descobre qual é o próximo número sequencial disponível e manda pra função de checagem.
# Se der tudo certo, ela devolve o dicionário com o pet novo.

def petCreate(
    cadastro: PetDB,
    tipo_pet: str,
    ano_nascimento: int,
    nome_pet: str
) -> PetDB:
    tipo_normalizado = str(tipo_pet).strip().lower()
    codigo = MAPA_TIPOS.get(tipo_normalizado)

    if codigo is None:
        raise ValueError("Tipo de PET inválido. Tenta outro!")

    if not isinstance(ano_nascimento, int):
        raise ValueError("Ano de nascimento tem que ser um número inteiro!!!")

    # Aqui é a mágica pra descobrir o próximo número sequencial. 
    # Pegamos todos os números cadastrados, achamos o maior e somamos 1!
    registros = [int(chave[1]) for chave in cadastro] if cadastro else [0]
    novo_registro = max(registros) + 1
    registro_texto = f"{novo_registro:05d}" # Coloca os zeros à esquerda pra ficar bonitão tipo a nota que o fabio vai me dar <3 (ex: 00003)

    id_pet = f"{codigo}-{registro_texto}-{ano_nascimento}"
    dados_pet = [nome_pet, TIPOS_POR_CODIGO[codigo], ano_nascimento]

    quantidade_antes = len(cadastro)
    # Chama o "segurança" (nossa função do arquivo checaCadastroPET) pra ver se tá tudo nos certo!
    checaCadastroPET(cadastro, id_pet, dados_pet)

    if len(cadastro) > quantidade_antes:
        print(f"Sucesso! PET cadastrado. O ID dele é: {id_pet}")
    else:
        print("Não foi possível cadastrar o PET!!.")

    return cadastro

# ========================================================================================


# EXERCÍCIO 2-b: Procedimento petRead
# Essa função busca pelo ID (ou só pelo número do meio)
# e imprime tudo arrumadinho pra você na tela. Como não ela nao vai retorna nenhum dado novo (só imprime),


def petRead(cadastro: PetDB, id_pet: str) -> None:
    chave = _localiza_chave(cadastro, id_pet)

    if chave is None:
        print("ID desse PET não foi encontrado no nosso cadastro\n")
        print("Conferia os dados e tente de novo!")
        return

    tipo_codigo, registro, ano_id = chave
    nome, tipo, ano = cadastro[chave]
    id_formatado = f"{tipo_codigo}-{registro}-{ano_id}"

    print("Dados do seu PET:... \n")
    print(f"Nome: {nome} \n")
    print(f"Ano de nascimento: {ano} \n")
    print(f"Raça: {tipo}")
    print(f"ID: {id_formatado}")

# ========================================================================================


# EXERCÍCIO 2-c: Função petDelete[cite: 12]
# Essa é a função se precisar remover um pet do sistema, passa o ID dele aqui.
# Ela apaga a chave do dicionário e te devolve o dicionário sem ele

def petDelete(cadastro: PetDB, id_pet: str) -> PetDB:
    chave = _localiza_chave(cadastro, id_pet)

    if chave is None:
        print("ID desse PET não foi encontrado no nosso cadastro\n")
        print("Confira os dados e tente de novo!")
        return cadastro

    del cadastro[chave] # O comando 'del' é quem faz o trabalho sujo de apagar!
    print(f"Pronto! O cadastro do PET id: {id_pet} foi removido com sucesso!")
    return cadastro

# ========================================================================================


# EXERCÍCIO 2-d: Função petUpdate
# O nome do pet tava errado? Use o Update!
# Essa função deixa você alterar os dados. O truque aqui é que se o usuário apertar só
# ENTER (deixar vazio), a gente mantém o dado antigo.

def petUpdate(cadastro: PetDB, id_pet: str) -> PetDB:
    chave = _localiza_chave(cadastro, id_pet)

    if chave is None:
        print("ID desse PET não foi encontrado no nosso cadastro\n")
        print("Conferia os dados e tente de novo!")
        return cadastro

    codigo_atual, registro, ano_chave = chave
    nome_atual, tipo_atual, ano_atual = cadastro[chave]

    # Atualizando o Nome
    novo_nome = input(f"Nome atual é [{nome_atual}]. Digite o novo (ou ENTER pra manter): ").strip()
    if novo_nome:
        print(f"O nome '{nome_atual}' foi substituído para '{novo_nome}'!")
        nome_atual = novo_nome

    # Atualizando o Tipo
    novo_tipo = input(f"Tipo atual é [{tipo_atual}]. Digite o novo (ou ENTER pra manter): ").strip().lower()
    novo_codigo = codigo_atual
    if novo_tipo:
        codigo_candidato = MAPA_TIPOS.get(novo_tipo)
        if codigo_candidato is not None:
            novo_tipo_extenso = TIPOS_POR_CODIGO[codigo_candidato]
            print(f"O tipo '{tipo_atual}' foi substituído para '{novo_tipo_extenso}'!")
            tipo_atual = novo_tipo_extenso
            novo_codigo = codigo_candidato
        else:
            print("Ops, tipo inválido. Vamos manter o tipo atual!")

    # Atualizando o Ano
    novo_ano = input(f"Ano de nascimento é [{ano_atual}]. Digite o novo (ou ENTER pra manter): ").strip()
    ano_final = ano_atual
    if novo_ano:
        if novo_ano.isdigit():
            ano_novo_int = int(novo_ano)
            print(f"O ano '{ano_atual}' foi substituído para '{ano_novo_int}'!")
            ano_final = ano_novo_int
        else:
            print("O ano tem que ser número. Vamos manter o ano atual!")

    # Como o nosso sistema junta tipo e ano na CHAVE do dicionário, 
    # se o tipo ou ano mudaram, a chave muda! Então temos que criar uma chave nova.
    nova_chave: PetKey = (novo_codigo, registro, int(ano_final))
    novos_dados = [nome_atual, tipo_atual, int(ano_final)]

    # Se a chave mudou mesmo, apagamos a velha.
    if nova_chave != chave:
        del cadastro[chave]

    # Salvamos os dados na chave nova (ou na mesma, se nada mudou de chave)
    cadastro[nova_chave] = novos_dados
    print(f"O Cadastro do PET id: {id_pet} foi atualizado com sucesso!")
    print(f"O Novo ID dele é: {novo_codigo}-{registro}-{ano_final}")

    return cadastro

# ========================================================================================


# EXERCÍCIO 2-e: Procedimento petList
# Uma vitrine de todos os nossos pets cadastrados! 
# Ele varre (usando um for) todo o dicionário imprimindo um por um

def petList(cadastro: PetDB) -> None:
    if not cadastro:
        print("Nenhum PET cadastrado ainda. O sistema tá vazio!")
        return

    print("\n=====  NOSSOS PETS CADASTRADOS  =====")
    # A função enumerate é ótima pra criar um contador (1, 2, 3...) automático.
    for numero, (chave, dados) in enumerate(cadastro.items(), start=1):
        tipo_codigo, registro, ano_id = chave
        nome, tipo, ano = dados
        print(f"\n[ PET {numero} ]")
        print(f"ID: {tipo_codigo}-{registro}-{ano_id}")
        print(f"Nome: {nome} | Tipo: {tipo} | Nasceu em: {ano}")

# ========================================================================================


# EXERCÍCIO 2-g: Bloco de Testes local do CadastroPet
if __name__ == "__main__":
    db_pets: PetDB = {
        ("CC", "00001", 2024): ["Max", "Cachorro", 2024],
        ("GT", "00002", 2018): ["Miau", "Gato", 2018],
    }

    print("Executando Testes das Funções!!!\n")
    print(50 * "-")

    print("Teste 2-a: Criando um novo pet (petCreate)")
    petCreate(db_pets, "outro", 2022, "TESTE")
    print(50 * "-")

    print("Teste 2-b: Lendo dados de um pet (petRead)")
    petRead(db_pets, "CC-00001-2024")
    print(50 * "-")

    print("Teste 2-c: Apagando um pet (petDelete)")
    petDelete(db_pets, "00003")
    print(50 * "-")

    print("Teste 2-e: Listando todos os pets (petList)")
    petList(db_pets)
    print(50 * "-")

    print("Teste 2-d: Atualizando um pet (petUpdate)")

    # A instrução abaixo orienta quem estiver testando o código a cumprir o requisito do PDF!!!
    print(">>> ATENÇÃO: Para testar o update, deixe Nome e Tipo em branco (Aperte ENTER) e digite '2019' no campo de Ano.")
    petUpdate(db_pets, "00002")
    print(50 * "-")
    
    print("\nVisualizando dicionário após todas as operações:")
    petList(db_pets)

# ========================================================================================


# EXERCÍCIO 2-f: Diferença entre funções e procedimentos

# - FUNÇÃO: Ela processa dados, faz os requisitos implementados e OBRIGATORIAMENTE te 
#   devolve um valor (usando a palavra reservada 'return'). 
#   Exemplo: def petCreate e def petDelete, que processam e nos retornam o dicionário atualizado.


# - PROCEDIMENTO: Executa uma ação(ex: imprime alguma coisaa na tela), 
#   mas NÃO te devolve nenhum valor (em Python, a gente diz que retorna 'None' implicitamente).
#   Exemplo: def petList e def petRead, que apenas imprimem os dados no console.
