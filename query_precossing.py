# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 21:22:13 2016

@author: nancy
"""

import sys
import nltk_wordnet
import query_parsing
from tkinter import *

class CustomListbox(Listbox):
    def __contains__(self, str):
        return str in self.get(0, "end")
        
def passQuery():
    mtext = queryTerms.get()
    query_terms = query_parsing.queryParsing(mtext)
    print("Printing mtext:")
    print(mtext)
    print("Printing query terms...")
    print(query_terms)

def fetchSynonyms(key):
    mtext = queryTerms.get()
    if key.char == " ":
        strArray = mtext.split()
        if len(strArray)!= 0:
            if len(strArray) == 1:
                s = mtext
            if len(strArray) > 1:
                s = strArray[len(strArray)-1]
            simWords = nltk_wordnet.getSynonyms(s)
            for item in simWords:
                if item not in mlist:
                    mlist.insert(END,item)

    if mtext == "":
        mlist.delete(0, END)

def onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    mentry.insert(END, " ")
    mentry.insert(END, value)

mGui = Tk()
queryTerms = StringVar()

mGui.geometry('800x800+500+300')
mGui.title('My window')
#mlabel = Label(mGui,text='My Label', fg='red').place(x=10,y=10)
mlabel = Label(mGui,text='Query', fg='blue').place(x=10,y=10)

mentry = Entry(mGui,textvariable = queryTerms)
mentry.bind("<Key>", fetchSynonyms)
mentry.place(x=70,y=10, width=600)

mlist = CustomListbox(mGui)
mlist.bind("<<ListboxSelect>>", onSelect)
mlist.place(x=70,y=40)

mbutton = Button(mGui, text='Submit', command = passQuery).place(x=70,y=220)

mGui.mainloop()