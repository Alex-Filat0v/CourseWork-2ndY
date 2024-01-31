import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from login_window import Ui_LoginForm
from main_window import Ui_MainWindow
import sqlite3
import bcrypt
import random
import matplotlib.pyplot as plt
from numpy import *
from sympy import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.check_line_edits)

    def check_line_edits(self):
        self.errorLabel.setText('')

        fX_text = self.fAxisX_Edit.text()
        tX_text = self.tAxisX_Edit.text()
        sX_text = self.sAxisX_Edit.text()

        fY_text = self.fAxisY_Edit.text()
        tY_text = self.tAxisY_Edit.text()
        sY_text = self.sAxisY_Edit.text()

        function_text = self.function_Edit.text()

        if not fX_text or not tX_text or not sX_text or not fY_text or not tY_text or not sY_text or not function_text:
            self.errorLabel.setText('Не все поля заполнены!')
        else:
            try:
                fX = int(fX_text)
                tX = int(tX_text)
                sX = int(sX_text)

                fY = int(fY_text)
                tY = int(tY_text)
                sY = int(sY_text)

                self.create_plot(fX, tX, sX, fY, tY, sY, function_text)
            except:
                self.errorLabel.setText('Ошибка, проверьте правильность всех введенных данных!')

    def create_plot(self, fX, tX, sX, fY, tY, sY, function_text):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X = linspace(fX, tX, sX)
        Y = linspace(fY, tY, sY)
        x, y = meshgrid(X, Y)

        x_sym, y_sym = symbols('x y')
        z_sym = sympify(function_text)
        z_func = lambdify((x_sym, y_sym), z_sym, "numpy")

        z = z_func(x, y)

        ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0, antialiased=True, cmap='Spectral')

        plt.title(function_text)

        plt.show()


class LoginForm(QMainWindow, Ui_LoginForm):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.setupUi(self)

        self.login.clicked.connect(self.login_clicked)
        self.registration.clicked.connect(self.registration_clicked)

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()

    def login_clicked(self):
        username = self.loginEdit.text()
        password = self.passwordEdit.text()

        if not username or not password:
            self.label.setText("Введите логин и пароль для входа")
        else:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            user_data = cursor.fetchone()
            conn.close()

            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[0]):
                self.close()
                self.open_main_window()
            else:
                self.label.setText("Не верно введен логин или пароль")
                self.passwordEdit.clear()

    def registration_clicked(self):
        username = self.loginEdit.text()
        password = self.passwordEdit.text()

        if not username or not password:
            self.label.setText("Введите логин и пароль для создания нового аккаунта")
        else:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                self.label.setText("Пользователь с таким логином уже существует")
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                conn.close()

                self.label.setText("Новый аккаунт успешно создан")

            self.loginEdit.clear()
            self.passwordEdit.clear()


if __name__ == '__main__':
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT NOT NULL,
                          password TEXT NOT NULL)''')

    conn.commit()
    conn.close()

    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
