from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import json
import random
import os

class PasswordManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.website = TextInput(hint_text="Website", multiline=False)
        self.email = TextInput(hint_text="Email", multiline=False)
        self.password = TextInput(hint_text="Password", multiline=False)

        generate_btn = Button(text="GENERATE PASSWORD")
        generate_btn.bind(on_press=self.generate_password)

        add_btn = Button(text="ADD PASSWORD")
        add_btn.bind(on_press=self.save)

        search_btn = Button(text="SEARCH")
        search_btn.bind(on_press=self.find_password)

        # Add widgets to layout
        self.add_widget(Label(text="Password Manager", font_size=24))
        self.add_widget(self.website)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(generate_btn)
        self.add_widget(search_btn)
        self.add_widget(add_btn)

    def generate_password(self, instance):
        letters = ["a", "bl", "gui", "gdfe", "ge", "e", "egew", "fhaweiu", "dhafh", "z", "xv"]
        numbers = ["1568", "29+8", "579", "654587", "9857942", "234"]
        symbols = ["$^W", ")(*&", "(^&^)", "@!#", "{|}", "[%]"]
        generated = random.choice(letters) + random.choice(numbers) + random.choice(symbols)
        self.password.text = generated

    def save(self, instance):
        website = self.website.text
        email = self.email.text
        password = self.password.text
        if not website or not email or not password:
            self.show_popup("ALERT", "Please do not leave any field empty.")
            return

        json_data = {website: {"email": email, "password": password}}

        try:
            with open("password_data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data.update(json_data)

        with open("password_data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        self.website.text = ""
        self.email.text = ""
        self.password.text = ""
        self.show_popup("Saved", f"Credentials for '{website}' saved successfully.")

    def find_password(self, instance):
        website = self.website.text
        try:
            with open("password_data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            self.show_popup("Error", "No data file found.")
            return

        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            self.show_popup(website, f"Email: {email}\nPassword: {password}")
        else:
            self.show_popup("Not Found", f"No credentials found for '{website}'.")

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup_content.add_widget(Label(text=message))
        close_btn = Button(text="Close", size_hint_y=None, height=40)
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup_content.add_widget(close_btn)
        popup.open()

class PasswordApp(App):
    def build(self):
        return PasswordManager()

if __name__ == '__main__':
    PasswordApp().run()