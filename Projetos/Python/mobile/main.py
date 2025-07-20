from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.snackbar import Snackbar
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definição do banco de dados
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    profile_type = Column(String, default="cliente")

engine = create_engine('sqlite:///database/app.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Telas
class LoginScreen(Screen):
    pass

class RegistrationScreen(Screen):
    pass

class ProfileScreen(Screen):
    current_profile = "cliente"

    def toggle_profile(self):
        app = MDApp.get_running_app()
        app.switch_profile()

class MainApp(MDApp):
    current_user = None

    def build(self):
        self.title = "Sistema de Login"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        Builder.load_file("screens/login.kv")
        Builder.load_file("screens/registration.kv")
        Builder.load_file("screens/profile.kv")

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegistrationScreen(name="registration"))
        sm.add_widget(ProfileScreen(name="profile"))

        return sm

    def gmail_login(self):
        email = "usuario@gmail.com"
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email)
            session.add(user)
            session.commit()
        self.current_user = user
        self.root.current = "profile"
        self.update_profile_screen()

    def user_login(self, email, password):
        user = session.query(User).filter_by(email=email, password=password).first()
        if user:
            self.current_user = user
            self.root.current = "profile"
            self.update_profile_screen()
        else:
            self.show_alert("Usuário ou senha incorretos.")

    def register_user(self, name, nickname, email, password):
        if not name or not nickname or not email or not password:
            self.show_alert("Preencha todos os campos!")
            return
        if session.query(User).filter_by(email=email).first():
            self.show_alert("Email já registrado.")
            return
        user = User(name=name, nickname=nickname, email=email, password=password)
        session.add(user)
        session.commit()
        self.current_user = user
        self.root.current = "profile"
        self.update_profile_screen()

    def update_profile_screen(self):
        screen = self.root.get_screen("profile")
        user = self.current_user
        screen.ids.profile_name.text = f"Nome: {user.name or 'N/A'}"
        screen.ids.profile_email.text = f"Email: {user.email}"
        screen.ids.profile_type.text = f"Perfil: {user.profile_type.capitalize()}"
        screen.ids.toggle_button.icon = (
            "arrow-left" if user.profile_type == "fornecedor" else "arrow-right"
        )

    def switch_profile(self):
        if self.current_user:
            self.current_user.profile_type = (
                "fornecedor" if self.current_user.profile_type == "cliente" else "cliente"
            )
            session.commit()
            self.update_profile_screen()

    def show_alert(self, message):
        Snackbar(text=message).show()

    def logout(self):
        self.root.current = "login"
        Snackbar(text="Você foi desconectado!").show()

if __name__ == "__main__":
    MainApp().run()
