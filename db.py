from sqlmodel import create_engine,SQLModel,Session, true

database_url='sqlite:///db.sqlite'

engine=create_engine(database_url,echo=True)

def init_db():
   SQLModel.metadata.create_all(engine)
   
def get_session():
   with Session(engine) as session:
      yield session
    