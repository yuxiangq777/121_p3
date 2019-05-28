from search_engine import SearchEngine
from tkinter import *
import os
import json
import webbrowser

class Search_UI:
    def __init__(self):
        self.query = ""
        self.db = json.load(open(os.path.join(".", "InvertedIndex.json")), encoding="utf-8")
        self.tk = Tk()
        self.tk.title("Best Search Engine")
    
    def show_content(self,event):
        webbrowser.open_new((r"http://"+event.widget.cget("text")))
        
    def widgets(self):
        self.tk.geometry('600x600')
        label = Label(self.tk, text= "Input the query:")
        label.place(relx=.3,rely=.5, anchor=  "center")
        self.entry = Entry(self.tk)
        self.entry.place(relx=.5,rely=.5, anchor=  "center")
        button_1 = Button(self.tk, text= "Search", command=self.print_result)
        button_1.place(relx=.6,rely=.5, anchor=  "center")
        button_2 = Button(self.tk, text= "QUIT", command=self.tk.destroy)
        button_2.place(relx=.5,rely=.8, anchor=  "center")
        self.tk.mainloop()
    def print_result(self):
        self.query = self.entry.get()
        My_search_engine = SearchEngine(self.db)
        self.top_level = Toplevel(self.tk)
        self.top_level.title("The Result")
        result = My_search_engine.print_results(self.query)
        if len(self.query) == 0:
            label = Label(self.top_level,text="Please enter your text again")
        elif len(result) == 0:
            label = Label(self.top_level,text="No result found")
        else:
            label = Label(self.top_level,text="These are the top 20 results for query "+ self.query+ ": ")
        label.pack()
        for single_result in result:
            single_link = Label(self.top_level, text=single_result,fg="blue", cursor="hand2")
            single_link.pack()
            single_link.bind("<Button-1>",  self.show_content)
if __name__ == "__main__":
    
    search_ui = Search_UI()
    search_ui.widgets()