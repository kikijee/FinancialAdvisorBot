import tkinter 

class GUI:

    def __init__(self, root):
        # base window attributes
        self.master = root
        self.master.title("Financial Advisor Bot")
        self.master.geometry("800x600")
        self.master.maxsize(800,600)
        self.master.config(bg="#1c1c1f")
     
        self.canvas = tkinter.Canvas(self.master,width=775,height=400,bg="#393b40")
        self.canvas.grid(row=0,column=0,padx=10,pady=5)

        self.frame_bot_text = tkinter.Frame(self.master,width=750,height=375,bg="black").grid(row=0,column=0)
        self.frame_user_ui = tkinter.Frame(self.master,width=750,height=135,bg="#1c1c1f").grid(row=1,column=0,pady=5)

        self.bot_output = tkinter.Text(self.frame_bot_text,width=740,height=365,state=tkinter.DISABLED,bg="#393b40",fg="#92c7d1",bd=5)

        self.input_text = tkinter.Text(self.frame_user_ui,width=40,height=2,bg="#393b40",fg="#92c7d1",bd=5)
        self.input_text.grid(row=1,column=0)

        self.quit_button = tkinter.Button(self.frame_user_ui,text="ask",command=self.get_line,bg="#92c7d1")
        self.quit_button.grid(row=2,column=0)

    def get_line(self):
        if(self.input_text.get('1.0',"1.0 lineend") != ""):
            input = self.input_text.get("1.0","1.0 lineend")
            self.input_text.delete("1.0","1.0 lineend")

            input = input.strip()
            print(input)


    def print_line(self,string):
        self.bot_output.delete("1.0",tkinter.END)
        self.bot_output.config(state=tkinter.NORMAL)
        self.bot_output.insert(tkinter.END,string)

        # for x in arr:
        #     self.output_lex.insert(str(self.line_num_out)+'.0','<'+str(x[0])+','+str(x[1])+'>'+'\n\n')
        #     self.line_num_out += 2
        self.bot_output.config(state=tkinter.DISABLED)

    




        