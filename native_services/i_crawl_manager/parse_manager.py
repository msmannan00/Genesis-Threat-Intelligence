# Local Imports
from services_shared_models.index_model import index_model
from native_services.i_crawl_manager.html_parser import html_parser


class parse_manager:
    __m_html_parser = None

    def on_parse_html(self, p_html, p_base_url, p_content_type):
        m_title, m_description, m_correct_keyword, m_validity_score = self.__on_html_parser_invoke(p_base_url, p_html)

        return index_model(p_title=m_title,p_content_type = p_content_type ,p_description=m_description, p_url = p_base_url,
                           p_validity_score=m_validity_score, p_keyword=m_correct_keyword)

    def __on_html_parser_invoke(self, p_base_url, p_html):

        m_html_parser = html_parser(p_base_url, p_html)
        m_html_parser.feed(p_html)
        return m_html_parser.get_parsed_html()
