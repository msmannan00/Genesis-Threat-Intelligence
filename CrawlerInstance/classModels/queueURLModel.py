# Non Parsed URL Model
# Model representing information of url to be put in backup queue
from CrawlerInstance.constants import constants
from GenesisCrawlerServices.constants import strings


class queueURLModel:

    # Local Variables
    __m_url = strings.S_EMPTY
    __m_type = strings.S_EMPTY
    __m_depth = constants.S_DEFAULT_DEPTH

    # Initializations
    def __init__(self, p_url, p_depth, p_type):
        self.__m_url = p_url
        self.__m_depth = p_depth
        self.__m_type = p_type

    # Getter Setters
    def get_url(self):
        return self.__m_url

    def get_type(self):
        return self.__m_type

    def get_depth(self):
        return self.__m_depth
