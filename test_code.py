import unittest
from unittest.mock import MagicMock
from Main import *

class TestMultilingualApp(unittest.TestCase):
    def test_sqrt_method(self):
        app = MultilingualApp()
        #Корень из нуля
        self.assertEqual(app.sqrt_method(0), "0.0")
        #корень из обычного числа
        self.assertEqual(app.sqrt_method(100), "10.0")
        self.assertEqual(app.sqrt_method(1256, 5), "35.44009")
        #корень из длинного числа
        self.assertEqual(app.sqrt_method(123456789123456789), "351364183.0")
        #корень из комплексного числа
        self.assertEqual(app.sqrt_method(2+5j, 2), "(1.92+1.3i)")

    def test_change_language(self):
        #тест перевода на хинди
        app = MultilingualApp()
        app.load_translations = MagicMock(return_value={"Выберите язык": "Select the language", "Подтвердить": "Confirm",
                                                        "Добавить новый язык": "Add new language", "Значение": "Value",
                                                        "Точность": "Accuracy", "Результат": "Result","Вычислить": "Calculate"})
        app.language_combobox.get = MagicMock(return_value="English")
        app.change_language()
        self.assertEqual(app.language_label.cget("text"), "Select the language")
        self.assertEqual(app.confirm_button.cget("text"), "Confirm")
        self.assertEqual(app.add_language_button.cget("text"), "Add new language")
        self.assertEqual(app.value_label.cget("text"), "Value")
        self.assertEqual(app.accuracy_label.cget("text"), "Accuracy")
        self.assertEqual(app.result_label.cget("text"), "Result")
        self.assertEqual(app.get_result.cget("text"), "Calculate")


if __name__ == '__main__':
    unittest.main()