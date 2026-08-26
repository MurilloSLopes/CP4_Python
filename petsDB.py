from typing import Dict, List, Tuple

PetKey = Tuple[str, str, int]
PetsDB = Dict[PetKey, List[object]]

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