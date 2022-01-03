import eventlet

from crawler_instance.constants.constant import CRAWL_SETTINGS_CONSTANTS
from crawler_instance.constants.strings import GENERIC_STRINGS, ERROR_MESSAGES
from crawler_instance.helper_method.helper_method import helper_method
from crawler_instance.i_crawl_manager.i_crawl_enums import RESPONSE_CODE
from crawler_shared_directory.shared_services.log_manager.log_manager import log
from crawler_services.constants.strings import GENERIC_STRINGS


class web_request_manager:

    # Load URL - used to request url for parsing to actually crawl the hidden web
    def load_url(self, p_url):

        m_request_handler = helper_method.on_create_session()
        try:
            with eventlet.Timeout(1):
                page = m_request_handler.get(p_url, timeout=CRAWL_SETTINGS_CONSTANTS.S_URL_TIMEOUT, allow_redirects=True, )
                m_html = page.content.decode(GENERIC_STRINGS.S_ISO)

            if page.status_code != RESPONSE_CODE.S_SUCCESS.value or page.content == GENERIC_STRINGS.S_EMPTY:
                return p_url, False, None
            else:
                return page.url, True, m_html

        except Exception as e:
            log.g().e("WEB REQUEST E1 : " + ERROR_MESSAGES.S_URL_PROCESSING_ERROR + " : " + p_url + " : " + str(e))
            return p_url, False, None

