##########################
# Import libraries/modules
##########################

from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_selector as selector
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, precision_score, recall_score

##########################
# Preprocessor Pipeline
##########################

def make_preprocessor(data):
    numerical_columns_selector = selector(dtype_exclude=object)
    numerical_columns = numerical_columns_selector(data) 
    numerical_preprocessor = SimpleImputer(strategy="most_frequent")
    preprocessor = make_column_transformer([numerical_preprocessor, numerical_columns], remainder="passthrough")
    return preprocessor

#############################
# Dummy classifier Pipeline
#############################

class DummyPipe:
    title = "Dummy Classifier Pipeline"
    def __init__(self):
        self.model = DummyClassifier(strategy='most_frequent', random_state=0)
    def pipe (self, data):
        preprocessor = make_preprocessor(data)
        pipeline = make_pipeline(preprocessor, self.model)
        return pipeline
 
###############################
# Logistic Regression Pipeline
###############################
    
class LogPipe:
    title = "Logistic Regression Pipeline"
    def __init__(self):
        self.model = LogisticRegression(max_iter=500)
    def pipe (self, data):
        preprocessor = make_preprocessor(data)
        pipeline = make_pipeline(preprocessor, self.model)
        return pipeline
    
###############################
# Model Evaluation
###############################

def evaluate(target_test, predictions):
    accuracy = accuracy_score(target_test, predictions)
    bal_accuracy = balanced_accuracy_score(target_test, predictions)
    precision = precision_score(target_test, predictions, pos_label=1)
    recall = recall_score(target_test, predictions, pos_label=1)
    return accuracy, bal_accuracy, precision, recall