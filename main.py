import customtkinter as ctk
from app.application import Application

if __name__ == '__main__':
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')
    Application().run()
