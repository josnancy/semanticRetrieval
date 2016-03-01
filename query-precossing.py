# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 21:22:13 2016

@author: nancy
"""

import sys
import nltk_wordnet
from tkinter import *

def passQuery():
    mtext = queryTerms.get()
    print(mtext)

def fetchSynonyms(key):
    mtext = queryTerms.get()
    if key.char == " ":
        simWords = nltk_wordnet.getSynonyms(mtext)
        for item in simWords:
            idx=1    
            mlist.insert(idx,item)
            idx = idx + 1
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

mlist = Listbox(mGui)
mlist.bind("<<ListboxSelect>>", onSelect)
mlist.place(x=70,y=40)

mbutton = Button(mGui, text='Submit', command = passQuery).place(x=70,y=220)

mGui.mainloop()