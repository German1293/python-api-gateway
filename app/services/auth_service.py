from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Usuario mock (luego DB)
fake_user = {
    "username": "admin",
    "email": "admin@example.com",
    "hashed_password": pwd_context.hash("admin123"),
}

def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return None
    if not pwd_context.verify(password, fake_user["hashed_password"]):
        return None
    return fake_user