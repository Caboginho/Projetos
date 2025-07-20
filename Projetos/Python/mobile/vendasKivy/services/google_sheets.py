import gspread

class GoogleSheetsService:
    def __init__(self):
        self.client = gspread.service_account(filename="credentials.json")
        self.sheet = self.client.open("TudoDubom").sheet1
        spreadsheets = self.client.openall()
        for sheet in spreadsheets:
            print(sheet.title)
        self.sheet = self.client.open("TudoDubom").sheet1

    def user_exists(self, email: str) -> bool:
        """Verifica se um email já está registrado."""
        records = self.sheet.get_all_records()
        return any(record['email'] == email for record in records)

    def add_user(self, user_data: dict):
        """Adiciona um novo usuário à planilha."""
        self.sheet.append_row(list(user_data.values()))

    def get_user(self, email: str) -> dict:
        """Retorna os dados de um usuário pelo email."""
        records = self.sheet.get_all_records()
        for record in records:
            if record['email'] == email:
                return record
        return None

    def user_exists(self, email: str) -> bool:
        """Verifica se um email já está registrado."""
        records = self.sheet.get_all_records()
        return any(record['email'] == email for record in records)

    def add_user(self, user_data: dict):
        """Adiciona um novo usuário à planilha."""
        self.sheet.append_row(list(user_data.values()))



test = GoogleSheetsService()