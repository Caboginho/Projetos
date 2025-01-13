from services.google_sheets import GoogleSheetsService
from models.user_model import User

class UserController:
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.current_user = None

    def register_user(self, name: str, email: str, password: str) -> str:
        """Registra um novo usuário no sistema."""
        if self.sheets_service.user_exists(email):
            return "Usuário já cadastrado."

        user = User(name, email, password)
        self.sheets_service.add_user(user.to_dict())
        return "Usuário cadastrado com sucesso!"

    def login_user(self, email: str, password: str) -> str:
        """Autentica o usuário."""
        user_data = self.sheets_service.get_user(email)
        if not user_data:
            return "Usuário não encontrado."

        user = User.from_dict(user_data)
        if user.password != password:
            return "Senha incorreta."

        self.current_user = user
        return f"Bem-vindo, {user.name}!"

    def logout_user(self) -> str:
        """Desloga o usuário atual."""
        if not self.current_user:
            return "Nenhum usuário está logado."

        self.current_user = None
        return "Logout realizado com sucesso!"

