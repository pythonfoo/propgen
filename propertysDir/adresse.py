class adresse(object):
    def __init__(self):
        self._adresse = None 
        self._name = None 
        self._vorname = None 
        self._key = None 
    @property
    def adresse(self):
        return self._adresse
    @adresse.setter
    def adresse(self, value):
        self._adresse = value
 
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
 
    @property
    def vorname(self):
        return self._vorname
    @vorname.setter
    def vorname(self, value):
        self._vorname = value
 
    @property
    def key(self):
        return self._key
    @key.setter
    def key(self, value):
        self._key = value
 
 
    def getElement(self, elementDataArray):
        element = adresse()
        element.adresse = elementDataArray[0]
        element.name = elementDataArray[1]
        element.vorname = elementDataArray[2]
        element.key = elementDataArray[3]
        return element

    def get_plainData(self):
        data = []
        data.append(self.adresse)
        data.append(self.name)
        data.append(self.vorname)
        data.append(self.key)
        return data
