# Local Imports
import re
from CrawlerInstance.constants import strings, constants


class indexModel:

    # Local Variables
    __m_title = strings.S_EMPTY
    __m_description = strings.S_EMPTY
    __m_url = strings.S_EMPTY
    __m_content_type = constants.S_THREAD_CATEGORY_GENERAL
    __m_validity_score = 0

    __m_keyword = []
    __m_sub_url = []

    # Initializations
    def __init__(self, p_title=None, p_description=strings.S_EMPTY, p_url=None, p_content_type=None, p_keyword=[], p_validity_score=None):
        self.__m_title = p_title
        self.__m_description = re.sub(' +', strings.S_SPACE, p_description)
        self.__m_url = p_url
        self.__m_keyword = p_keyword
        self.__m_content_type = p_content_type
        self.__m_validity_score = p_validity_score

    # Getter Setters
    def get_validity_score(self):
        return self.__m_validity_score

    def get_sub_url(self):
        return self.__m_sub_url

    def get_url(self):
        return self.__m_url

    def get_title(self):
        return self.__m_title

    def get_description(self):
        return self.__m_description
