from typing import Dict, List, Tuple

PetKey = Tuple[str, str, int]
PetsDB = Dict[PetKey, List[object]]

# Este arquivo atua como o nosso "banco de dados" falso inicial. 
# Quando o sistema rodar, ele vai importar essa variável (db_pets)
# vamos trabalhar manipulando ela

db_pets: PetsDB = {
    ("CC", "00001", 2024): [
        "Max",
        "Cachorro",
        2024,
    ],
    ("GT", "00002", 2018): [
        "Miau",
        "Gato",
        2018,
    ],
}