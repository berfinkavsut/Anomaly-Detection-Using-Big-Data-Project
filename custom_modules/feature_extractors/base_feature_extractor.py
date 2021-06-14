

class BaseFeatureExtractor:

    def __init__(self, param, selected_features):
        """
        :param param: dictionary of model parameters
        :param selected_features: list of selected features to extract features
        """

        self.model = []  # for feature extraction model
        self.param = param  # for model parameters

        # selected columns of data frame for feature extraction
        self.selected_features = selected_features

        # features extracted from the data
        self.features_extracted = []

    def fit(self, X):
        """
        This function takes the input whose features will be extracted and the target values.
        Convert data frame to numpy array.
        Fit and train the model for feature extractor.
        Calculate necessary parameters (e.g. mean) if there exists any.

        :param X: Data Frame input
        :return:
        """

    def transform(self, X):
        """
        This function is called after fit function.
        Convert Data Frame to Numpy array.
        Extract features and return extracted features.

        :param X: data frame input
        :return: data frame extracted features
        """

    def fit_transform(self, X):
        """
        This function both trains the model with the input and extracts features.
        Convert data frame to numpy array.
        Fit and train the model for feature extractor.
        Calculate necessary parameters (e.g. mean) if there exists any.
        Extract features and return extracted features as a data frame.

        :param X: data frame input
        :return: data frame extracted features
        """
