import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from main import MainWindow


app = QApplication([])


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()

    def test_check_line_edits_empty_fields(self):
        # Тест проверяет, что при пустых полях устанавливается текст ошибки
        self.window.check_line_edits()
        error_text = self.window.errorLabel.text()
        self.assertEqual(error_text, 'Не все поля заполнены!')

    def test_check_line_edits_valid_data(self):
        # Тест проверяет, что при корректных данных функция выполняется без ошибок
        self.window.fAxisX_Edit.setText('1')
        self.window.tAxisX_Edit.setText('2')
        self.window.sAxisX_Edit.setText('10')
        self.window.fAxisY_Edit.setText('3')
        self.window.tAxisY_Edit.setText('4')
        self.window.sAxisY_Edit.setText('10')
        self.window.function_Edit.setText('x**2 + y**2')
        with patch('main.MainWindow.create_plot') as mock_create_plot:
            self.window.check_line_edits()
            mock_create_plot.assert_called_once_with(1, 2, 10, 3, 4, 10, 'x**2 + y**2')

    def test_create_plot_valid_data(self):
        # Тест проверяет, что create_plot вызывается с корректными данными
        with patch('matplotlib.pyplot.show') as mock_show:
            self.window.create_plot(1, 2, 10, 3, 4, 10, 'x**2 + y**2')
            mock_show.assert_called_once()

    # Добавьте другие тесты по необходимости

if __name__ == '__main__':
    unittest.main()
