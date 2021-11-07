# Local Imports
import copy
from json import JSONEncoder

from CrawlerInstance.classModels.subhostModel import subHostModel
from CrawlerInstance.constants import constants, strings


class backupModel:
    # Local Variables
    __m_parsed = False
    __m_host = strings.S_SPACE
    __m_catagory = constants.S_THREAD_CATEGORY_GENERAL
    __m_url_data = []

    # Initializations
    def __init__(self, p_host, p_sub_host, p_depth, p_catagory):
        self.__m_parsed = False
        self.__m_host = p_host
        self.__m_catagory = p_catagory
        self.__m_url_data.clear()
        self.__m_url_data.append(subHostModel(p_sub_host, p_depth))

    def get_category(self):
        return self.__m_catagory

class urlObjectEncoder(JSONEncoder):
    def default(self, o):
        m_dict = copy.deepcopy(o.__dict__)

        # skip objects for server processing to reduce request load
        if 'm_sub_url' in m_dict:
            del m_dict['m_sub_url']

        return m_dict