#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import XMLproperty
import sys
import propgen
import os
from proptosqlite import sqlitegen

"""
Hier soll der eigentlich Teilprogrammstart stattfinden, der für die property basierte Datenhaltung ist.
Es sollen z.B. die Tabellen erzeugt werden, falls noch kein SQLite File Existiert. Es sollen die zur Verfügung stehenden Propertys mit ihren Parametern als Information mittesl XML-Auslesung zur Verfügung gestellt werden.
"""

class DataManager(object):
    def __init__(self):
        self._sqliteFileName = "initdata.pro"
        self._sqliteFilePath = "./data/"
        self._tabledict = {}
        # xmldateien in Unterverz. props einlesen und propertyinfos 
        # zur Verfügung stellen
        self._dirlist = os.listdir('./propertysDesign')
        for self._filename in self._dirlist:
            self._xmlgenerator = XMLproperty.xmlPropertyGenerator()
            # Einlesen der Datei, die als Parameter angehängt wurde
            self._proppath = "./propertysDesign/" + self._filename
            self._proparray = self._xmlgenerator.read_dict(self._proppath)
            #print("Test SPLIT for Filename: ", self._filename.split('.', 1))
            tablename = self._filename.split('.',1)[0]
            #print("Tablename is: ", tablename)
            self._tabledict[tablename] = self._proparray
            #for element in self._proparray:   # Helper
            #    print(element.name)           # Helper
            
        print(self._dirlist)
    def getPropParameter(self):
        return self._proparray

    def initSQLITE(self):
        # Erstellen des SQLiteFiles durch aufruf der eigenen 
        # Überladung mit Standardparametern
        self.initSQLITEfilename(self._sqliteFileName, self._sqliteFilePath)
    
    # Überladung von initSQLITEfile mit Angabe des Filename und Path 
    # damit nicht nur eine Standarddatei Möglich ist
    def initSQLITEfilename(self, filename, path):
        # prüfen ob der File schon existiert
        if not os.access(path + filename, os.F_OK):
            # Erstellen des SQLiteFiles 
            self._sqlitegenerator = sqlitegen(filename, path)
            # Anlegen der Tabellen 
            for tablename in self._tabledict:
                tableproparray = self._tabledict[tablename]
                print(tablename)
                self._sqlitegenerator.tablegenerator(tablename, tableproparray)
        else:
            print("File Exists")     

    def getDataList(self, tablename, whereclose):
        # Gibt die Datenliste zurück... zukünftig unabhängig, welcher Datenbanktyp 
        self._sqlitegenerator = sqlitegen(self._sqliteFileName, self._sqliteFilePath)
        for element in self._tabledict:                           # Helper
            print("element in self._tabledict: ", element)        # Helper
        return self._sqlitegenerator.getList( tablename ,self._tabledict[tablename] ,whereclose)
    
# Hauptprogrammteil
class main(object):
    def __init__(self):
        # Testing
        
        print("Programmstart")
        datamanager = DataManager()
        proparray = datamanager.getPropParameter()
        #print(proparray)
        #for prop in proparray:
        #    print(prop,"/n")
        print("Initialize SQLiteFile")    # Helper
        initData = datamanager.initSQLITE()            
        print("Show Data")     # Helper
        data = datamanager.getDataList("adresse", "")
        for element in data:    # Helper
            print("Name: " ,element.name)      # Helper
            print("Vorname: ", element.vorname)      # Helper
            print("Adresse: ", element.adresse)      # Helper
            print("Index: ",element.key)      # Helper
            print("--------- Next ----------")      # Helper

        

# Main Start nur wenn ausgeführt und nicht importiert
if __name__ == "__main__":
    start = main()
       
             



