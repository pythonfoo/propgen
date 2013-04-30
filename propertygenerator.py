#!/usr/bin/python3
import XMLproperty
import sys
import propgen
import os
"""
Dateien aus dem Unterverzeichnis Props einlesen und daraus Propertys generieren
"""


# PropertyHandler Kopf schreiben
# Der PropertyClassHandler wird gebraucht um die automatisch 
# generierten Klassen zu kennen bzw. aufrufen zu können
genproperty = propgen.genproperty()
classheader = genproperty.appendHandlerHeader()
datei2 = open('./propertysDir/propsHandler.py', 'w')
for line in classheader:
    print(line, file=datei2)
datei2.close()

# in Unterverzeichnis props abgelegte Dateinamen in fileList array ablegen 
dirList = os.listdir('./propertysDesign')

for filename in dirList:
    if filename.endswith('.xml'):
        # xml einlesen und daraus ein Propertydatei in Python generieren
        propname = filename.replace('.xml', '') # hier muss noch das .xml geloescht werden
        xmlgenerator = XMLproperty.xmlPropertyGenerator()
        genproperty = propgen.genproperty()

        print("+++ Propertygenerator generator starts for: " + filename + " +++\n")

        # Einlesen der Datei, die als Parameter angehaengt wurde
        proppath = "./propertysDesign/" + filename
        proparray = xmlgenerator.read_dict(proppath)
    
        # Eingangsparameter als Arrays leer erstellen
        propinit = []
        propper = []

        # Header der Propertyclasse erstellen
        propheader = genproperty.appendHeader( [], propname)

        # macht aus den aus xml gelesenen Parametern den PropertyCode
        for prop in proparray:
            if prop.editable == 1:
                propinit, propper = genproperty.appendPropReadWrite( propinit, propper, prop.name )
            elif prop.editable == 0:
                propinit, propper = genproperty.appendPropRead( propinit, propper, prop.name )
        newfilename = 'propertysDir/' + propname + '.py'
        
        # Erstellt die PropertyHandlerMethode
        propHandlerMethod = genproperty.appendPropHandlerMethod(proparray, propname)

        # Schreibt die PropertyClasse in einen File
        datei = open(newfilename, 'w')
        for line in propheader:
            print(line, file=datei)
        for line in propinit:
            print(line, file=datei)
        for line in propper:
            print(line, file=datei)
        for line in propHandlerMethod:
            print(line, file=datei)
        datei.close()
        # hier wird der Handler fuer alle Tabellen mit der Info fuer die
        # aktuelle Tabelle aufgefuellt
        propHandler = genproperty.appendHandlerPropCall(propname)

        datei2 = open('./propertysDir/propsHandler.py', 'a')
        for line in propHandler:
            print(line, file=datei2) 
        datei2.close() 
        print("Generator ends with no Errors")
    else:
        print("No .xml in props/ Directory. Ends with no Work to do.")

if len(dirList) == 0:
    print("No File in props/Directory. Ends with no Work to do.")



            
