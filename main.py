from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
import uvicorn
import time

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int



dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {}

@app.post('/post')
def get_post() -> Timestamp:
    new_post = Timestamp(id=len(post_db), timestamp=int(time.time()))
    post_db.append(new_post)
    return new_post
    
@app.get('/dog')
def get_dogs(kind: DogType = None) -> list[Dog]:
    if kind is None:
        return [dogs_db[i] for i in dogs_db.keys()]
    else:
        # Not very clever but works
        all_dogs = [dogs_db[i] for i in dogs_db.keys()]
        result = []
        for dog in all_dogs:
            if dog.kind == kind:
                result.append(dog)
        return result
    
@app.post('/dog')
def create_dog(dog: Dog) -> Dog:
    if dogs_db.get(dog.pk, None) is None:
        dogs_db[dog.pk] = dog
        return dogs_db[dog.pk]
    else:
        raise HTTPException(
            status_code=405,
            detail=str(f'There is a dog with pk {dog.pk}.')
        )
    
@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int) -> Dog:
    dog = dogs_db.get(pk, None)
    if dog is not None:
        return dog
    else:
        raise HTTPException(
            status_code=404,
            detail=str(f'There is no dog with pk {pk}.')
        )
    
@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog) -> Dog:
    # Is there a dog with this pk?
    old_dog = dogs_db.get(pk, None)
    if old_dog is None:
        raise HTTPException(
            status_code=404,
            detail=str(f'There is no dog with pk {pk}, consider using POST dog.')
        )
    # May be assert pk == dog.pk? 
    # No info in doc
    dogs_db[pk] = dog
    return dogs_db[pk]
    
if __name__ == '__main__':
    uvicorn.run(app, port=51001)
    