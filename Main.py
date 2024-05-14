import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import mpmath
from cmath import sqrt


class MultilingualApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multilingual Sqrt")
        self.geometry("400x300")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#e7e3e8")

        self.current_language = "Russian"
        self.translations = self.load_translations(self.current_language)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="raised", background="#e0e0e0")

        language_frame = tk.Frame(self, bg="#f0f0f0")
        language_frame.pack(pady=10)

        self.language_label = tk.Label(language_frame, text="Выберите язык:", bg="#f0f0f0")
        self.language_label.grid(row=0, column=0, padx=5, pady=5)

        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.language_combobox = ttk.Combobox(language_frame, values=self.get_language_files())
        self.language_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.language_combobox.set("Russian")

        # Frame for buttons
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.confirm_button = ttk.Button(button_frame, text="Подтвердить", command=self.change_language)
        self.confirm_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_language_button = ttk.Button(button_frame, text="Добавить новый язык", command=self.add_language)
        self.add_language_button.grid(row=0, column=1, padx=5, pady=5)

        # Frame for calculation
        calculation_frame = tk.Frame(self, bg="#f0f0f0")
        calculation_frame.pack(pady=10)

        self.value_label = tk.Label(calculation_frame, text=self.translations["Значение"], bg="#f0f0f0")
        self.value_label.grid(row=0, column=0, padx=5, pady=5)

        self.input_entry = tk.Entry(calculation_frame)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        self.accuracy_label = tk.Label(calculation_frame, text="Точность:", bg="#f0f0f0")
        self.accuracy_label.grid(row=1, column=0, padx=5, pady=5)

        self.accuracy_entry = tk.Entry(calculation_frame)
        self.accuracy_entry.grid(row=1, column=1, padx=5, pady=5)

        self.result_label = tk.Label(calculation_frame, text=self.translations["Результат"], bg="#f0f0f0")
        self.result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.get_result = ttk.Button(calculation_frame, text="Вычислить", command=self.calculate_root)
        self.get_result.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def sqrt_method(self, x, accuracy=0):
        if isinstance(x, complex):
            x = sqrt(x)
            return str(round(x.real, accuracy) + round(x.imag, accuracy) * 1j).replace('j', 'i')
        else:
            x = mpmath.sqrt(x)
            len_div = abs(str(x).find('.'))
            return mpmath.nstr(x, n=len_div + accuracy)


    def get_language_files(self):
        language_files = [file.split(".")[0] for file in os.listdir(self.project_dir) if file.endswith(".json")]
        return language_files

    def calculate_root(self):
        value_str = self.input_entry.get()
        accuracy_str = self.accuracy_entry.get()
        try:
            value = int(value_str)
        except ValueError:
            try:
                value = complex(value_str.replace('i', 'j'))
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное числовое значение")
                return

        try:
            accuracy = int(accuracy_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное числовое значение для точности")
            return

        result = self.sqrt_method(value, accuracy)
        self.result_label.config(text=f"Результат: {result}")

    def load_translations(self, language):
        filename = f"{language}.json"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                translations = json.load(file)
            return translations
        except Exception as e:
            return {}

    def change_language(self):
        selected_language = self.language_combobox.get()

        if selected_language != self.current_language:
            self.current_language = selected_language
            self.translations = self.load_translations(selected_language)
            messagebox.showinfo("Успех", f"Язык успешно изменен на {selected_language}")
            self.update_labels()

    def update_labels(self):
        self.value_label.config(text=self.translations["Значение"])
        self.result_label.config(text=self.translations["Результат"])
        self.confirm_button.config(text=self.translations["Подтвердить"])
        self.add_language_button.config(text=self.translations["Добавить новый язык"])
        self.language_label.config(text=self.translations["Выберите язык"])
        self.accuracy_label.config(text=self.translations["Точность"])
        self.get_result.config(text=self.translations["Вычислить"])

    def add_language(self):
        filename = filedialog.askopenfilename(title="Выберите файл с переводом", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                new_language = os.path.basename(filename).split('.')[0]
                current_values = list(self.language_combobox['values'])
                current_values.append(new_language)
                self.language_combobox['values'] = current_values

                shutil.copy(filename, os.path.join(self.project_dir, os.path.basename(filename)))

                messagebox.showinfo("Успех", f"Новый язык '{new_language}' добавлен успешно!")
                self.translations = self.load_translations(new_language)
                self.update_labels()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить новый язык: {e}")


if __name__ == "__main__":
    app = MultilingualApp()
    app.mainloop()
