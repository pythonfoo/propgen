#!/usr/bin/python3
import XMLproperty
import os

"""
Erzeugen einer XML-Datei, die die Propertyparameter aufnimmt.
Der Name der Datei soll nachher der Classenname der Property sein.
"""
print("Propety Generator\n\n")
filenamewithoutpath = input("input Filename: ")
filename = "./props/"+filenamewithoutpath

proparray = []
xmlgenerator = XMLproperty.xmlPropertyGenerator()
i="y"
while i == "y":
    prop = XMLproperty.XMLpropertyParameter()

    clear = os.system('clear')
    print("Eine neue Property \n \n")
    prop.name = input("Enter the Propertyname: ")
    print("1 - int \n2 - float\n3 - string\n4 - bool\n5 - object\n6 - ?")
    prop.typinf = input("Select the Property Typ: ")
    iniskey = input("is Key 0=No 1=yes [0 default]:")
    if iniskey == 0:
        prop.isKey = 0
    else:
        prop.isKey = 1
    ineditable = input("is editable 0=No 1=yes [1 default]:")
    if ineditable == 0:
        prop.editable = 0
    else:
        prop.editable = 1
    
    proparray.append(prop)
    i = input("Noch eine Property (y):")

xmlgenerator.write_property(proparray, filename)
