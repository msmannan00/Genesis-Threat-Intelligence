# Local Imports
from CrawlerInstance.classModels.indexModel import indexModel
from CrawlerInstance.iCrawlController.htmlParser import htmlParser


class parseManager:
    __m_html_parser = None

    def on_parse_html(self, p_html, p_base_url):
        m_title, m_description, m_correct_keyword, m_incorrect_keyword, m_validity_score = self.__on_html_parser_invoke(p_base_url, p_html)

        return indexModel(p_title=m_title, p_description=m_description, p_url = p_base_url,
                          p_validity_score=m_validity_score, p_keyword=m_correct_keyword + m_incorrect_keyword)

    def __on_html_parser_invoke(self, p_base_url, p_html):

        m_html_parser = htmlParser(p_base_url, p_html)
        m_html_parser.feed(p_html)
        return m_html_parser.get_parsed_html()
