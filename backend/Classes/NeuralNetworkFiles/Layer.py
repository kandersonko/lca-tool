class Layer:
    def __init__(self, name, display_name, definition, parameters):
        self.name = name
        self.display_name = display_name
        self.definition = definition
        self.parameters = parameters
    
    def getName(self):
        return self.name

    def getDisplayName(self):
        return self.display_name

    def getDefinition(self):
        return self.definition

    def getParameters(self):
        return self.parameters
