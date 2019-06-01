from search_engine import SearchEngine
from tkinter import *
import os
import json
import webbrowser

class Search_UI:
    def __init__(self):
        self.query = ""
        self.db = json.load(open(os.path.join(".", "InvertedIndex.json")), encoding="utf-8")
        self.snippet_dict = json.load(open(os.path.join(".", "snippet.json")), encoding="utf-8")
        self.tk = Tk()
        self.tk.title("Best Search Engine")
    
    def show_content(self,event):
        url_index= event.widget.cget("text").find("  Its snippet:")
        url = event.widget.cget("text")[0:url_index]
        webbrowser.open_new((r"http://"+url))
        
    def build_UI(self):
        self.tk.geometry('600x600')
        label = Label(self.tk, text= "Input the query:")
        label.place(relx=.3,rely=.5, anchor=  "center")
        self.entry = Entry(self.tk,width=50)
        
        self.entry.place(relx=.5,rely=.5, anchor=  "center")
        search_button = Button(self.tk, text= "Search", command=self.print_result)
        search_button.place(relx=.84,rely=.5, anchor=  "center")
        quit_button = Button(self.tk, text= "QUIT", command=self.tk.destroy)
        quit_button.place(relx=.5,rely=.8, anchor=  "center")
        self.tk.mainloop()
    def print_result(self):
        self.query = self.entry.get()
        My_search_engine = SearchEngine(self.db)
        self.top_level = Toplevel(self.tk)
        self.top_level.geometry("500x500")
        self.top_level.title("The Result")
        result = My_search_engine.print_results(self.query)
        return_doc = My_search_engine.get_return_doc()
        if len(self.query) == 0:
            label = Label(self.top_level,text="Please enter your text again")
        elif len(result) == 0:
            label = Label(self.top_level,text="No result found")
        else:
            label = Label(self.top_level,text="These are the top 20 results for query "+ self.query+ ": ")
        label.pack()
        i=0
        for single_result in result:
            single_link_and_snippet = Label(self.top_level, text=single_result+"  Its snippet: "+ self.snippet_dict[return_doc[i]]+"...", fg="blue",cursor="hand2")
            single_link_and_snippet.pack()
            #single_snippet = Label(self.top_level, text="its snippet: "+ self.snippet_dict[return_doc[i]])
            i+=1
            single_link_and_snippet.bind("<Button-1>",  self.show_content)
if __name__ == "__main__":
    
    search_ui = Search_UI()
    search_ui.build_UI()
    