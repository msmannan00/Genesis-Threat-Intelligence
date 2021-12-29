from pathlib import Path


class SHARED_CONSTANT:
    S_PROJECT_PATH = str(Path(__file__).parent.parent.parent)

class CLASSIFIER_PATH_CONSTANT:
    S_CLASSIFIER_FOLDER_PATH = "\\crawler_services\\raw\\classifier_pickled_files"
    S_DATASET_PATH = "\\crawler_services\\raw\\crawled_classifier_websites.csv"
    S_CLASSIFIER_PICKLE_PATH = "\\crawler_services\\raw\\classifier_pickled_files\\web_classifier.sav"
    S_VECTORIZER_PATH = "\\crawler_services\\raw\\classifier_pickled_files\\class_vectorizer.csv"
    S_SELECTKBEST_PATH = "\\crawler_services\\raw\\classifier_pickled_files\\feature_vector.sav"
    S_TRAINING_DATA_PATH = "\\crawler_services\\raw\\classifier_pickled_files\\training_data.csv"
    S_DICTIONARY_PATH = SHARED_CONSTANT.S_PROJECT_PATH + "\\crawler_services\\raw\\dictionary"
    S_DICTIONARY_MINI_PATH = SHARED_CONSTANT.S_PROJECT_PATH + "\\crawler_services\\raw\\dictionary_small"

