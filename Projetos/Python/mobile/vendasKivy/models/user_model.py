class User:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        """Converte o objeto User para um dicionário."""
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
