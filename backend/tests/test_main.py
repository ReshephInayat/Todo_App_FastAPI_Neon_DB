# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency
# https://fastapi.tiangolo.com/tutorial/testing/
# https://realpython.com/python-assert-statement/
# https://understandingdata.com/posts/list-of-python-assert-statements-for-unit-tests/


from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app, get_session, Todo
from app import settings


# ===================================================================================================
def test_read_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Response": "Todo App"}


def test_read_main_2():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() != {"message": "Hello World"}


# ===================================================================================================


# ===================================================================================================
def test_create_todo():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        # override the dependencies of main.py

        client = TestClient(app=app)
        todo_content = "Buy Milky Bread"
        response = client.post("/todos/", json={"content": todo_content})
        data = response.json()
        assert response.status_code == 200
        assert data["content"] == todo_content


def test_create_todo_2():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)
        todo_content = 1
        response = client.post("/todos/", json={"content": todo_content})
        data = response.json()
        assert response.status_code == 200
        assert data["content"] != todo_content


# ===================================================================================================


# ===================================================================================================
def test_read_todos():

    connection_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app=app)
        response = client.get("/todos/")
        assert response.status_code == 200

#                   W o r ki n g      on    This

# def test_read_todos_2():
#     connection_string = str(settings.TEST_DATABASE_URL).replace(
#         "postgresql", "postgresql+psycopg"
#     )
#     engine = create_engine(
#         connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
#     )
#     SQLModel.metadata.create_all(engine)
#     with Session(engine) as session:
#         def get_session_override():
#             return session
#         app.dependency_overrides[get_session] = get_session_override
#         client = TestClient(app=app)
#         result = {"content": "Buy groceries"}
#         response = client.get("/todos/", json={"content": result["content"]})
#         data = response.json()
#         assert response.status_code == 200
#         # assert data["id"] == JSON.id
#         assert data["content"] == result.content

# # ===================================================================================================


# Test Get Single Todo Pending.......


# Test Delete Todo Pending.......


# Test Update Todo Pending.......
