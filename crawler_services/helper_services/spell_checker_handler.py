# Local Imports
import re

from native_services.helper_method.helper_method import helper_method
from crawler_services.native_services.log_manager.log_enums import ERROR_MESSAGES
from crawler_services.constants.constant import CLASSIFIER_PATH_CONSTANT

class spell_checker_handler:
    __instance = None
    __spell_check = None

    # Initializations
    @staticmethod
    def get_instance():
        if spell_checker_handler.__instance is None:
            spell_checker_handler()
        return spell_checker_handler.__instance

    def __init__(self):
        if spell_checker_handler.__instance is not None:
            raise Exception(ERROR_MESSAGES.S_SINGLETON_EXCEPTION)
        else:
            self.__spell_check = set(open(CLASSIFIER_PATH_CONSTANT.S_DICTIONARY_PATH).read().split())
            spell_checker_handler.__instance = self

    def init_dict(self):
        self.__spell_check = set(open(CLASSIFIER_PATH_CONSTANT.S_DICTIONARY_MINI_PATH).read().split())

    # List Word Validator - Divides the list into 2 list of valid and invalid words
    def validation_handler(self, p_word_list):
        invalid = []
        valid = []

        if len(p_word_list) > 1:
            for word in set(p_word_list):
                if helper_method.is_stop_word(word) is False:
                    if word in self.__spell_check and word not in valid:
                        valid.append(word)
                    elif word not in invalid:
                        invalid.append(word)
            return list(invalid), list(valid)
        else:
            return p_word_list,p_word_list

    # List Word Validator - Divides the list into 2 list of valid and invalid words along with stopwords if any
    def invalid_word_validation_handler(self, p_word):
        p_words = re.sub('[^A-Za-z0-9]+', ' ', p_word)
        m_word_list = p_words.split()
        valid = []

        for word in m_word_list:
            if helper_method.is_stop_word(word) is False:
                if word in self.__spell_check and word not in valid:
                    valid.append(word)
        return list(valid)
