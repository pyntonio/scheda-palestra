from pydantic import BaseModel
from typing import Optional

class OroscopoRequest(BaseModel):
    nome: str
    data_nascita: str  # Ad esempio, '1990-01-01'
    ora_nascita: str   # Ad esempio, '15:30'
    luogo_nascita: str # Ad esempio, '45.07, 7.68' (latitudine e longitudine)
    lingua: Optional[str] = "it"  # Linguaggio opzionale, di default "it"
    tipi: Optional[str] = "generico"  # Tipo di oroscopo, di default "generico"
