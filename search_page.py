
import nltk_wordnet
import query_parsing, executing_search
import numpy as np
from tkinter import *
import tkinter as tk
from tkinter import ttk
from numpy import linalg as LA

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
        controller.geometry('600x600+400+100')
        tk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text="Search Page", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        self.queryTerms = StringVar()

        # mlabel = Label(mGui,text='My Label', fg='red').place(x=10,y=10)
        self.mlabel = Label(self, text='Query', fg='blue').place(x=10, y=10)

        self.mentry = ttk.Entry(self, textvariable=self.queryTerms)
        self.mentry.bind("<Key>", self.fetchSynonyms)
        self.mentry.place(x=70, y=10, width=300)

        self.mlist = CustomListbox(self)
        self.mlist.bind("<<ListboxSelect>>", self.onSelect)
        self.mlist.place(x=70, y=40)

        self.mbutton = ttk.Button(self, text='Submit', command=lambda: self.passQuery(controller)).place(x=70, y=220)

    def passQuery(self, controller):
        mtext = self.mentry.get()
        mtext = mtext.strip()
        print("mtext")
        print(mtext)
        docs =[]
        all_terms =[]

        if mtext != "":
            query_terms = query_parsing.queryParsing(mtext)
            print("Printing query terms...")
            print(query_terms)

            #fetching synonyms from wordnet
            for q in query_terms:
                synonyms = nltk_wordnet.getSynonyms(q)
                for s in synonyms:
                    all_terms.append(s)

            dup_removed_qterms = list(set(all_terms))

            indexTerms = np.load('IndexTerms.npy')

            #finding similar terms form Vt vectors
            termIndexes=[i for i, x in enumerate(indexTerms.tolist()) if any(thing in x for thing in dup_removed_qterms)]
            related_terms = executing_search.findSimilarTerms(termIndexes)

            # vectorizing query terms
            queryVector = np.zeros(indexTerms.size)

            for t in related_terms:
                queryVector[t] = 1

            print("query vector")
            print(queryVector.T)
            np.save("queryVector", queryVector.T)
            if LA.norm(queryVector) != 0:
                docs = executing_search.execute_search(queryVector.T,termIndexes)
            ResultsPage.setDocuments(ResultsPage, docs)
            controller.show_frame(ResultsPage)

    def fetchSynonyms(self, key):
        mtext = self.mentry.get()
        mtext = mtext.strip()
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


class ResultsPage(tk.Frame):
    documentIDs = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ResultsPage.resultsVar = StringVar()
        ResultsPage.label1 = ttk.Label(self, textvariable=ResultsPage.resultsVar, font=LARGE_FONT)
        ResultsPage.label1.pack(pady=10, padx=10)

        ResultsPage.button1 = ttk.Button(self, text="Back To Search", command=lambda: controller.show_frame(SearchPage))
        ResultsPage.button1.pack()
        ResultsPage.resultsList = CustomListbox(self)
        ResultsPage.resultsList.pack(fill=BOTH, expand=YES)

    def setDocuments(self,documents):
        self.resultsVar.set("Here are the matches we found.")
        self.documentIDs = []
        print("in setDocumentIds")
        print(len(documents))
        self.resultsList.delete(0, END)
        if (len(documents) != 0):
            for i in range(0,len(documents)):
                print(documents[i])
                self.documentIDs.append(documents[i])
                self.resultsList.insert(END, documents[i])
        else:
            self.resultsVar.set("No matches found! Try using different terms.")

    def backToSearch(self,controller):
        controller.SearchPage.mlist.delete(0,END)
        controller.SearchPage.queryTerms =""
        controller.show_frame(controller.SearchPage)

app = SemanticSearch()
app.mainloop()