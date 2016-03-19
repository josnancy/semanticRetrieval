
import nltk_wordnet
import query_parsing, executing_search
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class CustomListbox(Listbox):
    def __contains__(self, str):
        return str in self.get(0, "end")


class SemanticSearch(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Semantic Search")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SearchPage, ResultsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SearchPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        controller.geometry('800x800+500+300')
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text="Search Page", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        self.queryTerms = StringVar()

        # mlabel = Label(mGui,text='My Label', fg='red').place(x=10,y=10)
        mlabel = Label(self, text='Query', fg='blue').place(x=10, y=10)

        self.mentry = ttk.Entry(self, textvariable=self.queryTerms)
        self.mentry.bind("<Key>", self.fetchSynonyms)
        self.mentry.place(x=70, y=10, width=600)

        self.mlist = CustomListbox(self)
        self.mlist.bind("<<ListboxSelect>>", self.onSelect)
        self.mlist.place(x=70, y=40)

        self.mbutton = ttk.Button(self, text='Submit', command=lambda: self.passQuery(controller)).place(x=70, y=220)

    def passQuery(self,controller):
        print("inside passQuery")
        mtext = self.mentry.get()
        query_terms = query_parsing.queryParsing(mtext)
        print("Printing query terms...")
        print(query_terms)

        # Vectorizing query terms
        indexTerms = np.load('IndexTerms.npy')
        queryVector = np.zeros(indexTerms.size)
        for qterm in query_terms:
            cntr = 0
            for term in np.nditer(indexTerms):
                if qterm == term:
                    queryVector[cntr] = 1
                cntr = cntr + 1
        print("query vector")
        print(queryVector.T)
        np.save("queryVector", queryVector.T)
        executing_search.execute_search(queryVector.T)
        controller.show_frame(ResultsPage)


    def fetchSynonyms(self,key):
        mtext = self.mentry.get()
        if key.char == " ":
            strArray = mtext.split()
            if len(strArray) != 0:
                if len(strArray) == 1:
                    s = mtext
                if len(strArray) > 1:
                    s = strArray[len(strArray) - 1]
                simWords = nltk_wordnet.getSynonyms(s)
                for item in simWords:
                    if item not in self.mlist:
                        self.mlist.insert(END, item)

        if mtext == "":
            self.mlist.delete(0, END)


    def onSelect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.mentry.insert(END, " ")
        self.mentry.insert(END, value)

class SearchPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Search Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back To Search", command=lambda: controller.show_frame(ResultsPage))
        button1.pack()


class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Showing Results", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back To Search", command=lambda: controller.show_frame(SearchPage))
        button1.pack()

        m = PanedWindow(self,orient=HORIZONTAL)
        m.pack(fill=BOTH, expand=1)

        f1 = ttk.Labelframe(m, text='Pane1', width=100, height=100)
        f2 = ttk.Labelframe(m, text='Pane2', width=100, height=100)   # second pane
        m.add(f1)
        m.add(f2)


app = SemanticSearch()
app.mainloop()
