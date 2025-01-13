from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from controllers.user_controller import UserController
#from kivymd.toast import toast
class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_controller = UserController()
       
    def build(self):
         # Carregar os arquivos KV dentro do método build, após a inicialização do app
        """try:
            Builder.load_file("views/login_screen.kv")
            Builder.load_file("views/register_screen.kv")
        except Exception as e:
            print(f"Erro ao carregar arquivos KV: {e}")"""

        # Configurar o ScreenManager e adicionar telas
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        return self.sm


    def change_screen(self, screen_name):
        """Altera a tela exibida."""
        self.sm.current = screen_name

    def login_user(self, email, password):
        """Realiza o login do usuário."""
        message = self.user_controller.login_user(email, password)
        self.show_message(message)
        if "Bem-vindo" in message:
            self.change_screen("home")  # Tela "home" será implementada posteriormente

    def register_user(self, name, email, password):
        """Registra um novo usuário."""
        message = self.user_controller.register_user(name, email, password)
        self.show_message(message)
        if "sucesso" in message:
            self.change_screen("login")

    def show_message(self, message):
        """Exibe uma mensagem ao usuário."""
        
       # toast(message)

if __name__ == "__main__":
    MainApp().run()
