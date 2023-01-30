import customtkinter
from tkinter import *
from ChatBotModel import ChatBot
from StockPredictionModel import*
from tkinter import ttk

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme("dark-blue")
        self.myChatBotModel = ChatBot(self)
        self.button_pressed = StringVar()

        self.geometry("600x470")
        self.title("Financial Advisor Bot 0.0.1")

        self.my_labelframe = customtkinter.CTkFrame(self, corner_radius= 20)
        self.my_labelframe.pack(pady=20)

        self.my_entry = customtkinter.CTkEntry(self.my_labelframe, width=400, height=40, border_width=1,placeholder_text="Ask you advisor",text_color="silver")
        self.my_entry.grid(row=0,column=0,padx=10,pady=10)

        self.my_button = customtkinter.CTkButton(self.my_labelframe, text="Send",command=self.ask)
        self.my_button.grid(row=0,column=1,padx=10)

        self.my_textframe = customtkinter.CTkFrame(self, corner_radius= 20)
        self.my_textframe.pack(pady=10)

        self.my_text = Text(self.my_textframe, height=20,width=67,wrap=WORD,bd=0,bg="#292929",fg="silver",font=('comicsansms',12))

        self.my_text.pack(pady=15,padx=15)
    
    def ask(self):
        self.my_text.delete("1.0","end")
        question = self.my_entry.get()
        self.my_entry.delete(0,END)
        response = self.myChatBotModel.ask(question)
        if response != None: self.my_text.insert(END,response)
                
    def respond(self,response):
        self.my_button.destroy()
        self.my_button = customtkinter.CTkButton(self.my_labelframe, text="respond",command=lambda: self.button_pressed.set("button_pressed"))
        self.my_button.grid(row=0,column=1,padx=10)
        self.my_text.delete("1.0","end")
        self.my_entry.delete(0,END)
        self.my_text.insert(END,response)
        self.my_button.wait_variable(self.button_pressed)
        self.button_pressed = StringVar()
        input = self.my_entry.get()
        self.my_text.delete("1.0","end")
        self.my_entry.delete(0,END)
        self.my_text.insert(END,response)
        return input
        
    def reset_button(self):
        self.my_button.destroy()
        self.my_button = customtkinter.CTkButton(self.my_labelframe, text="Send",command=self.ask)
        self.my_button.grid(row=0,column=1,padx=10)
        self.my_text.delete("1.0","end")
        self.my_entry.delete(0,END)

    def print_to(self,text):
        self.my_text.delete("1.0","end")
        self.my_entry.delete(0,END)
        self.my_text.insert(END,text)
    


        

