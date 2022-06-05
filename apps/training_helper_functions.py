##########################
# Import libraries/modules
##########################

from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_selector as selector
from sklearn.compose import make_column_transformer


def make_preprocessor(data):
    numerical_columns_selector = selector(dtype_exclude=object)
    numerical_columns = numerical_columns_selector(data) 
    numerical_preprocessor = SimpleImputer(strategy="most_frequent")
    preprocessor = make_column_transformer([numerical_preprocessor, numerical_columns], remainder="passthrough")
    return preprocessor

