from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from api_folder.api_forms import UserForm
from api_folder.sql_models import DbUser, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Modify this according to your database configuration
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{name}")
async def home(name: str, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == name).first()
    if user: return user.session_token
    return {"Status": "Not implemented"}


@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return [s[0] for s in db.query(DbUser.username).all()]


@app.post("/register")
async def create_user(user_form: UserForm, db: Session = Depends(get_db)):
    user = DbUser()
    user.username = user_form.name
    user.set_password(user_form.password)
    try:
        db.add(user)
        db.commit()
        return {"message": "User created successfully."}
    except Exception:
        raise HTTPException(status_code=409, detail="Username is taken.")


@app.post("/login")
async def login(user_form: UserForm, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.username == user_form.name).first()
    if user and user.check_password(user_form.password):
        try:
            user.generate_random_token()
            db.commit()
            return {"token": str(user.session_token)}
        except Exception:
            raise HTTPException(status_code=500, detail="DB error.")
    raise HTTPException(status_code=409, detail="Couldn't log in.")


if __name__ == "__main__":
    run("api:app", host="0.0.0.0", port=3000, reload=True)
