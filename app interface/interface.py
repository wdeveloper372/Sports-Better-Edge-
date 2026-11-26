from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
script_dir = project_root / "edge calculator script"
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

import sports_bet

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class SingleOddsApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.odds_input = TextInput(hint_text="Enter odds (e.g. -110 or +150)", multiline=False)
        self.result_label = Label(text="Implied Prob: --")

        btn = Button(text="Calculate")
        btn.bind(on_press=self.calculate)

        layout.add_widget(self.odds_input)
        layout.add_widget(btn)
        layout.add_widget(self.result_label)
        return layout

    def calculate(self, instance):
        try:
            odds = float(self.odds_input.text.strip())
            prob = sports_bet.american_to_implied_prob(odds)
            self.result_label.text = f"Implied Prob: {prob:.2f}%"
        except ValueError as err:
            self.result_label.text = f"Error: {err}"


if __name__ == "__main__":
    SingleOddsApp().run()