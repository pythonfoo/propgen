#!/usr/bin/python3

import sys
class genproperty(object):
    """
    propinit ist der initialisierungsteil __init der Propertyklasse
    propper ist die eigentliche Deffinition für die Propertys
    """

    def appendHeader(self, propheader, classname):
        propheader.append("class " + classname + "(object):")
        propheader.append("    def __init__(self):")
        return propheader
    def appendPropRead(self, propinit, propper, propname):
        propinit.append("        self._" + propname + " = None ")
        propper.append("    @property")
        propper.append("    def " + propname + "(self):")
        propper.append("        return self._" + propname)
        return propinit, propper
    def appendPropReadWrite(self, propinit, propper, propname):
        propinit.append("        self._" + propname + " = None ")
        propper.append("    @property")
        propper.append("    def " + propname + "(self):")
        propper.append("        return self._" + propname)
        propper.append("    @" + propname +".setter")
        propper.append("    def " + propname + "(self, value):")
        propper.append("        self._" + propname + " = value")
        propper.append(" ")
        return propinit, propper
    
    def appendPropReadWriteKey(self, propinit, propper, propname):
        return none 
    def appendPropReadKey(self, propinit, propper, propname):
        return none
    # Beginning With PropertyReturnerCode
    # Neu Neu Neu !!! 25.06.2012 noch nicht fertig !!!
    def appendHandlerHeader(self):
        # Erstellt den Kopf des PropertyClassHandlers 
        # Der PropertyClassHandler wird gebraucht um die automatisch 
        # generierten Klassen zu kennen bzw. aufrufen zu können
        prophandler = []
        prophandler.append(" ")
        prophandler.append("class propsHandler(object):")
        prophandler.append("    def __init__(self):")
        prophandler.append("        pass")
        prophandler.append("    def getProperty_byName(self, propname): ")
        return prophandler
    def appendHandlerPropCall(self, propname):
        propHandlerPropCall = []
        propHandlerPropCall.append(" ")
        propHandlerPropCall.append("        # Tabelle: " + propname + "----------")
        propHandlerPropCall.append('        if propname == "' + propname + '" :')
        propHandlerPropCall.append("            import propertysDir." + propname + " as " + propname)
        propHandlerPropCall.append("            tmp = " + propname + "." + propname + "()" )
        propHandlerPropCall.append("            return tmp" )
        propHandlerPropCall.append("        else:" )
        propHandlerPropCall.append("            return False" )

        return propHandlerPropCall 

    def appendPropHandlerMethod(self, proparray, propname):
        proper = []
        proper.append(" ")
        proper.append("    def getElement(self, elementDataArray):")
        proper.append("        element = " + propname + "()")
        i = 0
        # propinfoArray Sollte nur die namen der einzelnen Propertys enthalten
        for prop in proparray:
            proper.append("        element." + prop.name + " = elementDataArray[" + str(i) + "]")
            i += 1
        proper.append("        return element")
        return proper
