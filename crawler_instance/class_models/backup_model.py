# Local Imports
import copy
from json import JSONEncoder

from crawler_instance.class_models.sub_host_model import sub_host_model
from crawler_instance.constants import constants, strings


class backup_model:
    # Local Variables
    m_parsed = False
    m_host = strings.S_SPACE
    m_catagory = constants.S_THREAD_CATEGORY_GENERAL
    m_url_data = []

    # Initializations
    def __init__(self, p_host, p_sub_host, p_depth, p_catagory):
        self.m_parsed = False
        self.m_host = p_host
        self.m_catagory = p_catagory
        self.m_url_data.clear()
        self.m_url_data.append(sub_host_model(p_sub_host, p_depth))

class urlObjectEncoder(JSONEncoder):
    def default(self, o):
        m_dict = copy.deepcopy(o.__dict__)

        # skip objects for server processing to reduce request load
        if 'm_sub_url' in m_dict:
            del m_dict['m_sub_url']

        return m_dict