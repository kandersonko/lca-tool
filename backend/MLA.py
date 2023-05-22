
# File contains all information pertaining to the Machine Learning Algortihms.

# Classification
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier

# clustering
from sklearn.cluster import KMeans

class MLA:
    def __init__(self, name, definition, parameters):
        self.name = name
        self.definition = definition
        self.parameters = parameters
    
    def getName(self):
        return self.name

    def getDefinition(self):
        return self.definition

    def getParameters(self):
        return self.parameters

list_MLAs = []

# KNN
Name = "KNN"
Definition = ["KNN info"]
Parameter_0 = {"Name":"n_neighbors", 
               "Type": ["int"], 
               "Default":5, 
               "Possible":["int"], 
               "Definition":"Number of neighbors to use by default for kneighbors queries."}
Parameter_1 = {"Name":"weights", "Type": ["option"], "Default":"uniform", "Possible":["uniform","distance"], 
                "Definition":"Weight function used in prediction. Possible values:\n\n‘uniform’ : uniform weights. All points in each neighborhood are weighted equally.\n‘distance’ : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away.\n[callable] : a user-defined function which accepts an array of distances, and returns an array of the same shape containing the weights."}
Parameter_2 = {"Name":"algorithm", "Type": ["option"], "Default":"auto", "Possible":["ball_tree","kd_tree","brute","auto"],
              "Definition":"Algorithm used to compute the nearest neighbors:\n\n'ball_tree’ will use BallTree\n‘kd_tree’ will use KDTree\n‘brute’ will use a brute-force search.\n‘auto’ will attempt to decide the most appropriate algorithm based on the values passed to fit method."}
Parameter_3 = {"Name":"leaf_size", "Type": ["int"], "Default":30, "Possible":["int"],
              "Definition":"Leaf size passed to BallTree or KDTree. This can affect the speed of the construction and query, as well as the memory required to store the tree. The optimal value depends on the nature of the problem."}
Parameter_4 = {"Name":"p", "Type": ["int"], "Default":"2", "Possible":["int"],
              "Definition":"Power parameter for the Minkowski metric. When p = 1, this is equivalent to using manhattan_distance (l1), and euclidean_distance (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
                  "Parameter_4":Parameter_4}

knn_algorithm = MLA(Name, Definition, Parameters)

list_MLAs.append(knn_algorithm)

# SVM
Name = "SVM"
Definition = ["SVM info"]
Parameter_0 = {"Name":"C", "Type": ["float"], "Default":1.0, "Possible":["float"], 
               "Definition":"Regularization parameter. The strength of the regularization is inversely proportional to C. Must be strictly positive. The penalty is a squared l2 penalty."}
Parameter_1 = {"Name":"kernel", "Type": ["option"], "Default":"rbf", "Possible":["linear","poly","rbf","sigmoid","precomputed"], 
                "Definition":"Specifies the kernel type to be used in the algorithm. If none is given, ‘rbf’ will be used. If a callable is given it is used to pre-compute the kernel matrix from data matrices; that matrix should be an array of shape (n_samples, n_samples)."}
Parameter_2 = {"Name":"degree", "Type": ["int"], "Default":3, "Possible":["int"],
              "Definition":"Degree of the polynomial kernel function (‘poly’). Must be non-negative. Ignored by all other kernels."}
Parameter_3 = {"Name":"gamma", "Type": ["option"], "Default":"scale", "Possible":["scale","auto","float"],
              "Definition":"Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.\n\nif gamma='scale' (default) is passed then it uses 1 / (n_features * X.var()) as value of gamma,\nif ‘auto’, uses 1 / n_features\nif float, must be non-negative."}
Parameter_4 = {"Name":"coef0", "Type": ["float"], "Default":0.0, "Possible":["float"],
              "Definition":"Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’."}
Parameter_5 = {"Name":"shrinking", "Type": ["bool"], "Default":True, "Possible":[True,False],
              "Definition":"Whether to use the shrinking heuristic."}
Parameter_6 = {"Name":"probability", "Type": ["bool"], "Default":False, "Possible":[True,False],
              "Definition":"Whether to enable probability estimates. This must be enabled prior to calling fit, will slow down that method as it internally uses 5-fold cross-validation, and predict_proba may be inconsistent with predict."}
Parameter_7 = {"Name":"tol", "Type": ["float"], "Default":0.003, "Possible":["float"],
              "Definition":"Tolerance for stopping criterion."}
Parameter_8 = {"Name":"cache_size", "Type": ["float"], "Default":200, "Possible":["float"],
              "Definition":"Specify the size of the kernel cache (in MB)."}
Parameter_9 = {"Name":"cache_weight", "Type": ["option"], "Default":None, "Possible":["balanced", None],
              "Definition":"Specify the size of the kernel cache (in MB)."}
Parameter_10 = {"Name":"verbose", "Type": ["bool"], "Default":False, "Possible":[True,False],
              "Definition":"Enable verbose output. Note that this setting takes advantage of a per-process runtime setting in libsvm that, if enabled, may not work properly in a multithreaded context."}
Parameter_11 = {"Name":"max_iter", "Type": ["int"], "Default":-1, "Possible":["int"],
              "Definition":"Hard limit on iterations within solver, or -1 for no limit."}
Parameter_12 = {"Name":"decision_function_shape", "Type": ["option"], "Default":"ovr", "Possible":["ovo","ovr"],
              "Definition":"Whether to return a one-vs-rest (‘ovr’) decision function of shape (n_samples, n_classes) as all other classifiers, or the original one-vs-one (‘ovo’) decision function of libsvm which has shape (n_samples, n_classes * (n_classes - 1) / 2). However, note that internally, one-vs-one (‘ovo’) is always used as a multi-class strategy to train models; an ovr matrix is only constructed from the ovo matrix. The parameter is ignored for binary classification."}
Parameter_13 = {"Name":"break_ties", "Type": ["bool"], "Default":False, "Possible":[True,False],
              "Definition":"If true, decision_function_shape='ovr', and number of classes > 2, predict will break ties according to the confidence values of decision_function; otherwise the first class among the tied classes is returned. Please note that breaking ties comes at a relatively high computational cost compared to a simple predict."}
Parameter_14 = {"Name":"random_state", "Type": ["int_or_null"], "Default":None, "Possible":["int"],
              "Definition":"Controls the pseudo random number generation for shuffling the data for probability estimates. Ignored when probability is False. Pass an int for reproducible output across multiple function calls."}


Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
             "Parameter_4":Parameter_4,"Parameter_5":Parameter_5,"Parameter_6":Parameter_6,
             "Parameter_7":Parameter_7,"Parameter_8":Parameter_8,"Parameter_9":Parameter_9,
             "Parameter_10":Parameter_10,"Parameter_11":Parameter_11,"Parameter_12":Parameter_12,
             "Parameter_13":Parameter_13, "Parameter_14":Parameter_14}

svm_algorithm = MLA(Name, Definition, Parameters)

list_MLAs.append(svm_algorithm)


## This is clustering algorithm not classification.
# K-Means
Name = "K-Means"
Definition = ["K-Means clustering."]
Parameter_0 =  {"Name":"n_clusters", "Type": ["int"], "Default":8, "Possible":["int"], 
               "Definition":"The number of clusters to form as well as the number of centroids to generate."}
Parameter_1 =  {"Name":"initialization", "Type": ["option"], "Default":"k-means++", "Possible":["k-means++", "random"], 
               "Definition":"Method for initialization:<br\><br\>‘k-means++’ : selects initial cluster centroids using sampling based on an empirical probability distribution of the points’ contribution to the overall inertia. This technique speeds up convergence. The algorithm implemented is “greedy k-means++”. It differs from the vanilla k-means++ by making several trials at each sampling step and choosing the best centroid among them.<br\><br\>‘random’: choose n_clusters observations (rows) at random from data for the initial centroids.<br\><br\>If an array is passed, it should be of shape (n_clusters, n_features) and gives the initial centers.<br\><br\>If a callable is passed, it should take arguments X, n_clusters and a random state and return an initialization."}
Parameter_2 =  {"Name":"n_int", "Type": ["int"], "Default":10, "Possible":["int"], 
               "Definition":"Number of times the k-means algorithm is run with different centroid seeds. The final results is the best output of n_init consecutive runs in terms of inertia. Several runs are recommended for sparse high-dimensional problems (see Clustering sparse data with k-means).<br\><br\>When n_init='auto', the number of runs depends on the value of init: 10 if using init='random', 1 if using init='k-means++'."}
Parameter_3 =  {"Name":"max_iter", "Type": ["int"], "Default":300, "Possible":["int"], 
               "Definition":"Maximum number of iterations of the k-means algorithm for a single run."}
Parameter_4 =  {"Name":"tol", "Type": ["float"], "Default":0.0001, "Possible":["float"], 
               "Definition":"Relative tolerance with regards to Frobenius norm of the difference in the cluster centers of two consecutive iterations to declare convergence."}
Parameter_5 =  {"Name":"verbose", "Type": ["int"], "Default":0, "Possible":["int"], 
               "Definition":"Verbosity mode."}
Parameter_6 =  {"Name":"random_state", "Type": ["int_or_null"], "Default":None, "Possible":["int"], 
               "Definition":"Determines random number generation for centroid initialization. Use an int to make the randomness deterministic."}
Parameter_7 =  {"Name":"copy_x", "Type": ["bool"], "Default":True, "Possible":[True,False], 
               "Definition":"When pre-computing distances it is more numerically accurate to center the data first. If copy_x is True (default), then the original data is not modified. If False, the original data is modified, and put back before the function returns, but small numerical differences may be introduced by subtracting and then adding the data mean. Note that if the original data is not C-contiguous, a copy will be made even if copy_x is False. If the original data is sparse, but not in CSR format, a copy will be made even if copy_x is False."}
Parameter_8 =  {"Name":"algorithm", "Type": ["option"], "Default":"lloyd", "Possible":["lloyd", "elkan", "auto", "full"], 
               "Definition":'K-means algorithm to use. The classical EM-style algorithm is "lloyd". The "elkan" variation can be more efficient on some datasets with well-defined clusters, by using the triangle inequality. However it’s more memory intensive due to the allocation of an extra array of shape (n_samples, n_clusters).<br\><br\>"auto" and "full" are deprecated and they will be removed in Scikit-Learn 1.3. They are both aliases for "lloyd".'}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
             "Parameter_4":Parameter_4,"Parameter_5":Parameter_5,"Parameter_6":Parameter_6,
             "Parameter_7":Parameter_7,"Parameter_8":Parameter_8}

k_mean_algorithm = MLA(Name, Definition, Parameters)

#list_MLAs.append(k_mean_algorithm)

# Decision Trees
Name = "DecisionTreeClassifier"
Definition = ["A decision tree classifier."]
Parameter_0 =  {"Name":"criterion", "Type": ["option"], "Default":"gini", "Possible":["gini", "entropy", "log_loss"], 
               "Definition":"The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “log_loss” and “entropy” both for the Shannon information gain."}
Parameter_1 =  {"Name":"splitter", "Type": ["option"], "Default":"best", "Possible":["best","random"], 
               "Definition":"The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split."}
Parameter_2 =  {"Name":"max_depth", "Type": ["int_or_null"], "Default":None, "Possible":["int"], 
               "Definition":"The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples."}
Parameter_3 =  {"Name":"min_samples_split", "Type": ["int"], "Default":2, "Possible":["int"], 
               "Definition":"The minimum number of samples required to split an internal node:<br\><br\>If int, then consider min_samples_split as the minimum number.<br\><br\>If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the minimum number of samples for each split."}
Parameter_4 =  {"Name":"min_samples_leaf", "Type": ["int"], "Default":1, "Possible":["int"], 
               "Definition":"The minimum number of samples required to be at a leaf node. A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches. This may have the effect of smoothing the model, especially in regression.<br\><br\>If int, then consider min_samples_leaf as the minimum number.<br\><br\>If float, then min_samples_leaf is a fraction and ceil(min_samples_leaf * n_samples) are the minimum number of samples for each node."}
Parameter_5 =  {"Name":"min_weight_fraction_leaf", "Type": ["float"], "Default":0.0, "Possible":["float"], 
               "Definition":"The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node. Samples have equal weight when sample_weight is not provided."}
Parameter_6 =  {"Name":"max_features", "Type": ["int_or_null"], "Default":None, "Possible":["int"], 
               "Definition":"The number of features to consider when looking for the best split:<br\><br\>If int, then consider max_features features at each split.<br\><br\>If float, then max_features is a fraction and max(1, int(max_features * n_features_in_)) features are considered at each split.<br\><br\>If “auto”, then max_features=sqrt(n_features).<br\><br\>If “sqrt”, then max_features=sqrt(n_features).<br\><br\>If “log2”, then max_features=log2(n_features).<br\><br\>If None, then max_features=n_features."}
Parameter_7 =  {"Name":"random_state", "Type": ["int_or_null"], "Default":None, "Possible":["int"], 
               "Definition":'Controls the randomness of the estimator. The features are always randomly permuted at each split, even if splitter is set to "best". When max_features < n_features, the algorithm will select max_features at random at each split before finding the best split among them. But the best found split may vary across different runs, even if max_features=n_features. That is the case, if the improvement of the criterion is identical for several splits and one split has to be selected at random. To obtain a deterministic behaviour during fitting, random_state has to be fixed to an integer.'}
Parameter_8 =  {"Name":"max_leaf_nodes", "Type": ["int_or_null"], "Default":None, "Possible":["int"], 
               "Definition":"Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes."}
Parameter_9 =  {"Name":"min_impurity_decrease", "Type": ["float"], "Default":0.0, "Possible":["float"], 
               "Definition":"A node will be split if this split induces a decrease of the impurity greater than or equal to this value.<br\><br\>The weighted impurity decrease equation is the following:<br\><br\>N_t / N * (impurity - N_t_R / N_t * right_impurity - Nt_L / N_t * left_impurity)<br\><br\>where N is the total number of samples, N_t is the number of samples at the current node, N_t_L is the number of samples in the left child, and N_t_R is the number of samples in the right child.<br\><br\>N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed."}
Parameter_10 =  {"Name":"class_weight", "Type": ["int_or_null"], "Default":None, "Possible":["int"], 
               "Definition":"Weights associated with classes in the form {class_label: weight}. If None, all classes are supposed to have weight one. For multi-output problems, a list of dicts can be provided in the same order as the columns of y.<br\><br\>Note that for multioutput (including multilabel) weights should be defined for each class of every column in its own dict. For example, for four-class multilabel classification weights should be [{0: 1, 1: 1}, {0: 1, 1: 5}, {0: 1, 1: 1}, {0: 1, 1: 1}] instead of [{1:1}, {2:5}, {3:1}, {4:1}].<br\><br\>The “balanced” mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as n_samples / (n_classes * np.bincount(y))<br\><br\>For multi-output, the weights of each column of y will be multiplied.<br\><br\>Note that these weights will be multiplied with sample_weight (passed through the fit method) if sample_weight is specified."}
Parameter_11 =  {"Name":"ccp_alpha", "Type": ["float"], "Default":0.0, "Possible":["float"], 
               "Definition":"Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen. By default, no pruning is performed."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
             "Parameter_4":Parameter_4,"Parameter_5":Parameter_5,"Parameter_6":Parameter_6,
             "Parameter_7":Parameter_7,"Parameter_8":Parameter_8,"Parameter_9":Parameter_9,
             "Parameter_10":Parameter_10,"Parameter_11":Parameter_11}

decision_tree_classifiier_algorithm = MLA(Name, Definition, Parameters)

list_MLAs.append(decision_tree_classifiier_algorithm)


# Stocastic Gradient Decent

def getMLAs():
    return list_MLAs



# Method to pull all parameters from a given method
def getParameters(algorithm_Name):
    Parameters = {}
    for algorithm in list_MLAs:
        if algorithm.getName() == algorithm_Name:
            Parameters = algorithm.getParameters()
    return Parameters

# get settings to fill the model parameters.
def getSettings(data, Parameters):
    settings = {}
    settings["Parameter_Length"] = len(Parameters)

    # Cycle through parameters
    for i in range(len(Parameters)):
        temp = Parameters["Parameter_" + str(i)]["Name"]+"_checked"

        # get name
        settings["Parameter_" + str(i) + "_Name"] = Parameters["Parameter_" + str(i)]["Name"]

        # get default
        if data[Parameters["Parameter_" + str(i)]["Name"]+"_checked"] == "false":
            settings["Parameter_" + str(i)] = Parameters["Parameter_" + str(i)]["Default"]
            # convert to acceptable type
            settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"])

        elif data[Parameters["Parameter_" + str(i)]["Name"]+"_checked"] == "true":
            settings["Parameter_" + str(i)] = data[Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
            settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"])

    return settings


def convertToType(value, Type):
    if Type[0] == "int":
        return int(value)
    elif Type[0] == "float":
        return float(value)
    elif Type[0] == "bool":
        if value == "true" or value == True:
            return True
        elif value == "false" or value == False:
            return False
    elif Type[0] == "int_or_null":
        if value == "null" or value == "None":
            return None
        elif value != None:
            return int(value)
        else:
            return value
    else:
        return value



# Method to create the model based on given form data.
def createModel(data):
    Parameters = getParameters(data["MLalgorithm"])
    settings = getSettings(data, Parameters)

    # Check which alorithm to create
    if data["MLalgorithm"] == "KNN": 
       # Fill the model information, note that the parameters are in the same order as writen above.
        model = KNeighborsClassifier(n_neighbors=settings['Parameter_0'],
                                     weights=settings['Parameter_1'],
                                     algorithm=settings['Parameter_2'],
                                     leaf_size=settings['Parameter_3'],
                                     p=settings['Parameter_4']
                                     )
        

    elif data["MLalgorithm"] == "SVM": 
        model = SVC(C=settings['Parameter_0'],
                    kernel=settings['Parameter_1'],
                    degree=settings['Parameter_2'],
                    gamma=settings['Parameter_3'],
                    coef0=settings['Parameter_4'],
                    shrinking=settings['Parameter_5'],
                    probability=settings['Parameter_6'],
                    tol=settings['Parameter_7'],
                    cache_size=settings['Parameter_8'],
                    class_weight=settings['Parameter_9'],
                    verbose=settings['Parameter_10'],
                    max_iter=settings['Parameter_11'],
                    decision_function_shape=settings['Parameter_12'],
                    break_ties=settings['Parameter_13'],
                    random_state=settings['Parameter_14'])

    elif data["MLalgorithm"] == "K-Means":
        model = KMeans(n_clusters=settings['Parameter_0'],
                    init=settings['Parameter_1'],
                    n_init=settings['Parameter_2'],
                    max_iter=settings['Parameter_3'],
                    tol=settings['Parameter_4'],
                    verbose=settings['Parameter_5'],
                    random_state=settings['Parameter_6'],
                    copy_x=settings['Parameter_7'],
                    algorithm=settings['Parameter_8'])

    elif data["MLalgorithm"] == "DecisionTreeClassifier":
        model = DecisionTreeClassifier(criterion=settings['Parameter_0'],
                    splitter=settings['Parameter_1'],
                    max_depth=settings['Parameter_2'],
                    min_samples_split=settings['Parameter_3'],
                    min_samples_leaf=settings['Parameter_4'],
                    min_weight_fraction_leaf=settings['Parameter_5'],
                    max_features=settings['Parameter_6'],
                    random_state=settings['Parameter_7'],
                    max_leaf_nodes=settings['Parameter_8'],
                    min_impurity_decrease=settings['Parameter_9'],
                    class_weight=settings['Parameter_10'],
                    ccp_alpha=settings['Parameter_11'])
        
    return model, settings