#!/usr/bin/python3

import sys
import sqlite3
import XMLproperty
#from propsHandler import *
from propertysDir.propsHandler import *
import os
import uuid

"""
install cable update....
hier entstehen erstmal Tests, zum Anbinden von SQLITE an die Propertygenerator
Ziel ist, automatisch die Table ueber die Infos aus den Propertyxml zu generieren
"""

# Tasks:
#
# 1: self.filename Parameteruebergabe an Klasse erstellen (Property ? oder in Funktion)
# 2: Anfuehrungszeichen klaerung in def tablegenerator 
# 3: Joints in Property coden
# 4: Bearbeiten Funktion
# 5: auslese Funktion

class sqlitegen(object):
    def __init__(self, filename, path):
        self._filename = filename
        self._path = path
        self._propsHandler = propsHandler()
        self._propertyInfoArrays = self._get_propertyinformation_arrays()

# hier müssten eigentlich alle proparrays in einem dict nach namen geladen werden
    def _get_propertyinformation_arrays(self):
        xmlgenerator = XMLproperty.xmlPropertyGenerator()
        dirList = os.listdir('./propertysDesign')
        propertyInfoArrays = {}
        for filename in dirList:
            if filename.endswith('.xml'):
                proppath = "./propertysDesign/" + filename
                proparray = xmlgenerator.read_dict(proppath)
                propname = filename.replace('.xml', '')
                propertyInfoArrays[propname] = proparray
        return propertyInfoArrays

    def _get_propertyinformation_array_byName(self, tablename):
        return self._propertyInfoArrays[tablename]

    def _sqliteconnection(self):
        # generates a sqliteconnection by filename
        fullpath = self._path + self._filename
        return sqlite3.connect(fullpath)

    def _sqlitecursor(self):
        # generates a cursor by sqliteconnection
        connection = self._sqliteconnection()
        return connection.cursor(), connection

    def tablegenerator(self, tablename, proparray):
        sqlitecon = self._sqliteconnection()
        # proparray based on propertys by xmlgen.py 
        cursor , connection = self._sqlitecursor()

        # creating a SQL-STRING for TABLEDESIGN in SQLITE
        sqltxt = ""
        i = 2 
        v = len(proparray)
        
        for prop in proparray:
            typ = "TEXT"
            # hier fehlt für alle anderen Datentypen für andere Datenbanken
            # außer string noch die Anagabe
            # im XML ist typinf ein string sollte aber intager sein also fails!!!!
            if prop.typinf == 0: # Has to be UUID.uudi4() or  UUID.uuid3()
                typ = "TEXT"
            elif prop.typinf == 1:
                typ = "INTAGER"
            elif prop.typinf == 2:
                typ = "FLOAT"
            elif prop.typinf == 3:
                typ = "TEXT"   # no SQLite DB's Shorttext
            elif prop.typinf == 4:
                typ = "BOOL"
            elif prop.typinf == 5:
                typ = "OBJECT"
            elif prop.typinf == 6:
                typ = "TEXT"   # no SQLite DB's Longtext
            else :
                raise Exception("Type ID is not defined")
            sqltxt = sqltxt + prop.name + " " + typ 
            if i <= v:
                sqltxt = sqltxt + " ,"
            i += 1
        
        sqltxt = ' CREATE TABLE ' + tablename + ' ( ' + sqltxt + ' ) '
        cursor.execute(sqltxt)    

    def getList(self, tablename, tablecellinfos, whereclose):
        cursor ,connection = self._sqlitecursor()
        proparray = self._get_propertyinformation_array_byName(tablename)
              
        # creating a SQL-STRING for TABLEREAD in SQLITE
        sqltxt = ""
        i = 1
        v = len(proparray)
        for prop in proparray:
            i += 1
            sqltxt = sqltxt + " " + prop.name
            
            if i <= v:
                sqltxt = sqltxt + ","
        # TODO:durty: whereclose Object/Property konstruieren mit sauberer 
        # Prüfung
        if whereclose == "":           
            sqltxt = 'SELECT' + sqltxt + ' FROM ' + tablename  
        else:
            sqltxt = 'SELECT' + sqltxt + ' FROM ' + tablename + ' WHERE ' + whereclose

        cursor.execute(sqltxt)
        data = cursor.fetchall()   # testen, was wenn none in DB 
        
        propdata = []
        
        filledPropClass = []
        i = 0
        for datenzeile in data:
            propClass = self._propsHandler.getProperty_byName(tablename)
            filledPropClass.append(propClass.getElement(datenzeile))
            propdata.append(filledPropClass[i])
            i +=1
        return propdata
        connection.close()

    def updateRowData(self, tablename, RowData): 
        # TODO: PropertyDatenObjekt muss bei Update diese Funktion aufrufen
        # TODO: Update RowData muss im BusinessDaten Objekt liegen genau wie
        # der Key. Die DatenPropertys erben dann diese Eigenschaften
        propClass = self._propsHandler.getProperty_byName(tablename)
        
        cursor ,connection = self._sqlitecursor()
        proparray = self._get_propertyinformation_array_byName(tablename)
        
        sqltxt = ""
        i = 0
        v = len(proparray)
        data = RowData.get_plainData()

        # TODO: Typen müssen noch alle gebaut werden
        for prop in proparray:
            if prop.tyinf == 1:
                sqltxt += prop.name + ' = ' + data[i] + ' ' 
            elif prop.typinf == 2:
                sqltxt += prop.name + ' = "' + data[i] + '" ' 
            
            if i <= v:
                sqltxt = sqltxt + ' '
            else:
                sqltxt += ','

            i += 1

        sqltxt = ' UPDATE ' + tablename + ' SET ' + sqltxt + ' WHERE key = ' + RowData.key
    def delRowData(self, RowData):
        pass 
        # TODO: Delete SQLite Row by UUID out of RowData

    def insertRowData(self, tablename, RowData):
        # Insert muss nur einen leeren Datensatz mit korrektem Key
        # anlegen alle Änderungen werden über Update ausgelöst
        propClass = self._propsHandler.getProperty_byName(tablename)
        
        cursor ,connection = self._sqlitecursor()
        proparray = self._get_propertyinformation_array_byName(tablename)

        # TODO: Key Automatismus muss noch rein (get last Key oder
        # UUID UniqueIdentifyer) wobei letzteres wohl besser wäre
        # creating a SQL-STRING for INSERT in SQLITE
        key = uuid.uuid4()  

        sqltxt = ' '
        i = 1
        v = len(proparray)
        for prop in proparray:
            i += 1
            # TODO: The other Types have to be added
            if prop.typinf == 1:
                sqltxt +=  0 
            elif prop.typinf == 0: # TODO: 0 Must be Key
                sqltxt += key  # TODO: has to be string because of UUID
            else:
                sqltxt += ' " "'
            if i <= v:
                sqltxt += ' '
            else:
                sqltxt += ' , '
        
        sqltxt = 'INSERT INTO ' + tablename + ' VALUES( ' + sqltxt + ' )'

        cursor.execute(sqltxt)
        connection.commit()
        connection.close()
        """  44     def get_plainData(self): in propertys                                                  
         45         data = []                                                             
          46         data.append(self.adresse)                                             
           47         data.append(self.name)                                                
            48         data.append(self.vorname)                                             
             49         data.append(self.key)                                                 
              50         return data      """
