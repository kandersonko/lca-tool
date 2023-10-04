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

# Returns the name convention for the Preoptimization
def getName():
    return "Layer"

## list of options for common enteries for layers
# Activations
activations = ["relu","sigmoid","softmax","softplus","softsign","tanh","selu","elu","exponential","None"]

def getActivations():
    return activations

# Initializers
Initializers = ["normal","uniform","random_normal","random_uniform","truncated_normal","zeros","ones","glorot_normal","glorot_uniform","he_normal","he_uniform","identity","orthogonal","constant","variance_scaling"]

def getInitializers():
    return Initializers

# Regularizers.
Regularizers = ["l1","l2","l1_l2","None"]

def getRegularizers():
    return Regularizers

# Constraints
## Note: option to adjust is removed till later as this would add another layer of complexity to adjust the parameters of each constraint method first before choosing.
Constraints = ["max_norm","min_max_norm","non_neg","unit_norm","radial_constraint","None"]

def getConstraints():
    return Constraints

