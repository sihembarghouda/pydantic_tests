from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Liste d'éléments pour stocker les tâches
items = []

# Modèle Pydantic pour valider les données d'entrée
class Item(BaseModel):
    text: str
    is_done: bool = False

# Modèle de réponse pour exclure le champ 'is_done'
class ItemResponse(BaseModel):
    text: str

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Bienvenue sur l'API FastAPI !"}

@app.post("/items", response_model=ItemResponse)
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    try:
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Item non trouvé")

@app.get("/items/", response_model=List[ItemResponse])
def list_items(limit: int = 10):
    return items[:limit]
