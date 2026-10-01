from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

Window.clearcolor = (0.08, 0.09, 0.12, 1)

OPERATIONS = {"+": "+", "-": "−", "*": "×", "/": "÷"}


def format_number(number):
    if number == int(number) and abs(number) < 1e15:
        return str(int(number))
    return str(round(number, 10))


class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=12, spacing=10, **kwargs)
        self.first = None
        self.operation = None
        self.current = "0"
        self.new_input = True

        self.history = Label(
            text="", font_size=sp(22), color=(0.6, 0.65, 0.75, 1),
            halign="right", valign="bottom", size_hint_y=0.12,
        )
        self.history.bind(size=self.history.setter("text_size"))
        self.display = Label(
            text="0", font_size=sp(52), bold=True,
            halign="right", valign="middle", size_hint_y=0.2,
        )
        self.display.bind(size=self.display.setter("text_size"))
        self.add_widget(self.history)
        self.add_widget(self.display)

        grid = GridLayout(cols=4, spacing=8, size_hint_y=0.58)
        rows = [
            ["C", "DEL", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]
        for row in rows:
            for key in row:
                grid.add_widget(self.make_button(key))
        self.add_widget(grid)

        exit_button = Button(
            text="ВЫХОД", font_size=sp(24), bold=True, size_hint_y=0.1,
            background_normal="", background_color=(0.8, 0.2, 0.25, 1),
        )
        exit_button.bind(on_release=self.exit_app)
        self.add_widget(exit_button)

    def make_button(self, key):
        if key in OPERATIONS or key == "=":
            color = (1, 0.6, 0.1, 1)
        elif key in ("C", "DEL", "%", "+/-"):
            color = (0.35, 0.38, 0.45, 1)
        else:
            color = (0.2, 0.22, 0.28, 1)
        button = Button(
            text=OPERATIONS.get(key, key), font_size=sp(30),
            background_normal="", background_color=color,
        )
        button.bind(on_release=lambda _btn: self.press(key))
        return button

    def show(self):
        self.display.text = self.current
        if self.current == "Ошибка":
            self.history.text = "нельзя делить на ноль"
        elif self.first is not None and self.operation:
            self.history.text = format_number(self.first) + " " + OPERATIONS[self.operation]
        else:
            self.history.text = ""

    def press(self, key):
        if self.current == "Ошибка" and key not in ("C",):
            self.clear()
        if key.isdigit():
            self.add_digit(key)
        elif key == ".":
            self.add_point()
        elif key == "C":
            self.clear()
        elif key == "DEL":
            self.delete()
        elif key == "+/-":
            self.negate()
        elif key == "%":
            self.percent()
        elif key in OPERATIONS:
            self.set_operation(key)
        elif key == "=":
            self.equals()
        self.show()

    def add_digit(self, digit):
        if self.new_input or self.current == "0":
            self.current = digit
            self.new_input = False
        elif len(self.current) < 15:
            self.current += digit

    def add_point(self):
        if self.new_input:
            self.current = "0."
            self.new_input = False
        elif "." not in self.current:
            self.current += "."

    def clear(self):
        self.first = None
        self.operation = None
        self.current = "0"
        self.new_input = True

    def delete(self):
        if self.new_input:
            return
        self.current = self.current[:-1]
        if self.current in ("", "-"):
            self.current = "0"
            self.new_input = True

    def negate(self):
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current

    def percent(self):
        self.current = format_number(float(self.current) / 100)
        self.new_input = True

    def set_operation(self, operation):
        if self.operation and not self.new_input:
            self.equals()
            if self.current == "Ошибка":
                return
        self.first = float(self.current)
        self.operation = operation
        self.new_input = True

    def equals(self):
        if self.operation is None or self.first is None:
            return
        a = self.first
        b = float(self.current)
        if self.operation == "+":
            result = a + b
        elif self.operation == "-":
            result = a - b
        elif self.operation == "*":
            result = a * b
        else:
            if b == 0:
                self.first = None
                self.operation = None
                self.current = "Ошибка"
                self.new_input = True
                return
            result = a / b
        self.first = None
        self.operation = None
        self.current = format_number(result)
        self.new_input = True

    def exit_app(self, *_args):
        App.get_running_app().stop()


class CalculatorApp(App):
    title = "Калькулятор"

    def build(self):
        return Calculator()


if __name__ == "__main__":
    CalculatorApp().run()
