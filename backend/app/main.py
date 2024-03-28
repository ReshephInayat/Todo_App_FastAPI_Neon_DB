# Here We are Importing fastapi From FastAPI
# Dependencies: It is just a function that can take all the same parameters that a path operation function can take -- # https://fastapi.tiangolo.com/tutorial/dependencies/
# HttpException sub class od exception and  a class from starlette.exceptions that we will use to handle exceptions in our API
from fastapi import FastAPI, Depends, HTTPException

# If you check, the function is decorated with an @asynccontextmanager.
# That converts the function into something called an "async context manager"
# A context manager in Python is something that you can use in a with statement, for example, open() can be used as a context manager:
from contextlib import asynccontextmanager


# Importing sqlmodel from SQlmodel: SQLModel is based on Python type annotations, and powered by Pydantic and SQLAlchemy
# Field: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/# define-the-fields-columns
# Session: https://sqlmodel.tiangolo.com/tutorial/select/?h=session#sqlmodels-sessionexec
# https://sqlmodel.tiangolo.com/tutorial/select/?h=session#create-a-session
# select: https://sqlmodel.tiangolo.com/tutorial/select/h=session#create-a-select-statement
# create_engine: It is an object that handles the communication with the database.If you have a server database (for example PostgreSQL or MySQL), the engine will hold the network connections to that database.
from sqlmodel import SQLModel, Field, Session, select, create_engine


# importing Optional Type from typing python typing package
# Annotated: https://fastapi.tiangolo.com/tutorial/dependencies #share-annotated-dependencies
from typing import Annotated, Optional


# importing setting modules
from app import settings


app: FastAPI = FastAPI()


# The name of each of these variables will be the name of the column in the table.And the type of each of them will also be the type of table column:
# primary_key: Now let's review the id field. This is the primary key of the table.So, we need to mark id as the primary key.To do that, we use the special Field function from sqlmodel and set the argument primary_key=True:
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)


# only needed for psycopg 3
# Replacing postgresql with postgresql+psycopg2
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


# The pool_recycle=300 option is an “optimistic” approach to prevent the pool from using a connection that has passed a certain age. In this case, we are setting the value to 5 minutes to correspond with the default compute auto-suspend in Neon.
# https://docs.sqlalchemy.org/en/20/core/pooling.html#setting-pool-recycle
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300, echo=True
)
# Creating the engine is very simple, just call create_engine() with a URL for the database to use
# in this case we stored the database url in a variable called connection_string and passed it as an argument
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#create-the-engine


# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#calling-create_all
# This MetaData object at SQLModel.metadata has a create_all() method.
# It takes an engine and uses it to create the database and all the tables registered in this MetaData object.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
# A context manager in Python is something that you can use in a with statement
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# with Session(engine) as session: This establishes a database session using some database engine (probably SQLAlchemy) defined in engine. The with statement ensures proper session management, automatically closing the session when the block exits.
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_main():
    return {"Response": "Todo App"}


@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
    print(f"Added Todo {todo}")
    # session.add(todo): This adds the provided todo object to the session. This action stages the object for insertion into the database.
    session.add(todo)
    # session.commit(): This commits the transaction to the database, effectively persisting the changes (adding the new todo) to the database.
    session.commit()
    # session.refresh(todo): This refreshes the state of the todo object from the database. This might be necessary if there are any database triggers or defaults that are applied upon insertion.
    session.refresh(todo)
    return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
    return todos

# with Session(engine) as session: Similar to the create_todo function, this establishes a database session using the provided database engine.
# - todos = session.exec(select(Todo)).all(): This executes a SELECT query on the Todo table (assuming Todo is a SQLAlchemy model) and retrieves all todo items from the database. It uses the select construct to create a SELECT statement, and all() fetches all results.
# return todos: Finally, the retrieved todo items are returned as the response to the client. This is typically returned as a JSON array.


@app.get("/todos/{todo_id}", response_model=Todo)
def read_single_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# @app.delete("/todos/", response_model=Todo)
# async def delete_all_todos(session: Annotated[Session, Depends(get_session)]):
#     """Deletes all todos from the database"""
#     # Use query.delete() for deletion
#     session.query(Todo).delete()
#     session.commit()
#     return {"message": "Deleted all todos"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"200 OK": "Todo Deleted Successfully"}


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_data = todo.model_dump(exclude_unset=True)
        db_todo.sqlmodel_update(todo_data)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
