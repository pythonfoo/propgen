 
class propsHandler(object):
    def __init__(self):
        pass
    def getProperty_byName(self, propname): 
 
        # Tabelle: adresse----------
        if propname == "adresse" :
            import propertysDir.adresse as adresse
            tmp = adresse.adresse()
            return tmp
        else:
            return False
