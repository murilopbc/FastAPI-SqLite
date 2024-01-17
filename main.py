from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import *
from models import *
from typing import List

# Inicializar FastAPI

app = FastAPI()


# Função GET para Acessar todos os funcionários cadastrados

@app.get('/get_all_users', response_model=List[UserRead])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users 

# Função GET para acessar informações do funcionário de acordo com o ID

@app.get('/user/{user_id}', response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(user_id == UserDB.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# Função PUT para editar/atualizar informações do funcionário

@app.put('/update_user/{user_id}', response_model=UserRead)
async def update_user(user_id: int, upd_user: UserUpdate, db: Session = Depends(get_db)):
    
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail='Item Not Found')

    for key, value in upd_user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# Função POST para Adiconar/Criar informações de um funcionário 

@app.post('/user/', response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = UserDB(**user.dict())
    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

# Função DELETE para deletar as informações de um funcionário

@app.delete('/delete_user/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if db_user:
        db.delete(db_user)
        db.commit()
        
        return {'message': f'User with id "{user_id}" deleted', 'Deleted_user': db_user}
    else:
        raise HTTPException(status_code=404, detail='User Not Found')
