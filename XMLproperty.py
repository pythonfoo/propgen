#!/usr/bin/python3
# XML-Based Propertyinfo Writer


import xml.dom.minidom as dom
"""
Objekt proParam, dass die einzelnen Parameter für eine einzelne Property aufnimmt
"""
class XMLpropertyParameter(object):
    def __init__(self):
        self._name = None
        self._typinf = 1
        self._isKey = 0
        self._editable = 1

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def typinf(self):
        return self._typinf
    @typinf.setter
    def typinf(self, value):
        self._typinf = value

    @property
    def isKey(self):
        return self._isKey
    @isKey.setter
    def isKey(self, value):
        self._isKey = value

    @property
    def editable(self):
        return self._editable
    @editable.setter
    def editable(self, value):
        self._editable = value

"""
classe, die funktionen zum Generieren von XML Dateien auf basis 
von propParm Objekten bereitstellt
"""
class xmlPropertyGenerator(object):
    # ------ XML Writer Teil ----------------------------------
    # fuegt einzelnen Propertyparameter in den Baum
    def __tag_insert(self, name, proptyp):
        tag_insert = dom.Element(proptyp)
        tag_insert.setAttribute("typ", type(name).__name__)
        text = dom.Text()
        text.data = str(name)
        tag_insert.appendChild(text)
    
        return tag_insert        



    def __tag_main_insert(self, prop):
        # setzt den Zweig fuer eine Property
        tag_eintrag = dom.Element("property")         
        # fuellt die Unterzweige in Property mit den Parametern        
        tag_eintrag.appendChild(self.__tag_insert(prop.name, "name"))
        tag_eintrag.appendChild(self.__tag_insert(prop.typinf, "typinf"))
        tag_eintrag.appendChild(self.__tag_insert(prop.isKey, "isKey"))
        tag_eintrag.appendChild(self.__tag_insert(prop.editable, "editable"))

        return tag_eintrag    


    def write_property(self, properdata, filename):
        # Uebernimmt das Dictionary und Schreibt die Elemente in den Baum
        baum = dom.Document()
        tag_dict = dom.Element("dictionary")

        # fuehgt ein weiteres element in den Baum je schleifendurchlauf
        for XMLpropertyParameter in properdata:
            tag_eintrag = self.__tag_main_insert(XMLpropertyParameter)
            tag_dict.appendChild(tag_eintrag)

        # fuegt den Hauptzweig mit allen Elementen in den XML Baum
        baum.appendChild(tag_dict)

        # schreibt die XMLdaten in die datei
        with open(filename, "w") as f:
            baum.writexml(f, "", "\t", "\n")

    # -------------------  XML Reader Teil -----------------------
    def __readNode(self, knoten):
        return eval("%s('%s')" % (knoten.getAttribute("typ"), knoten.firstChild.data.strip()))



    def read_dict(self, filename):
        d=()
        baum = dom.parse(filename)
        proparray = []

        for propertyentry in baum.firstChild.childNodes:
            prop = XMLpropertyParameter()
            if propertyentry.nodeName == "property":
                schluessel = wert = None
                for knoten in propertyentry.childNodes:
                    if knoten.nodeName == "name":
                        prop.name = self.__readNode(knoten) 
                    elif knoten.nodeName == "typinf":
                        prop.typin = self.__readNode(knoten)
                    elif knoten.nodeName == "isKey":
                        prop.isKey = self.__readNode(knoten)
                    elif knoten.nodeName == "editable":
                        prop.editable = self.__readNode(knoten)
                proparray.append(prop)
        return proparray

"""
# ########################################
# main test
# ########################################

# Propertyklassentest
prop = XMLpropertyParameter()
prop.name = "auto"
prop.typinf = 1

print("Name: " + prop.name + " Typ: " + str(prop.typinf))

# xml-Part Test
proparray = []
proparray.append(prop)
generator = xmlgen()
generator.write_property(proparray, "test.xml")

# XML Reader Test
proparray = generator.read_dict("test.xml")
print("propertyname = " + proparray[0].name)
print(len(proparray))
prop = proparray.pop()
print(len(proparray))
"""
