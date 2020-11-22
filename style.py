from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers
from pygments import highlight
from pygments import lexers
from bs4 import BeautifulSoup


class Style:

    @staticmethod
    def get_all_styles():
        return list(get_all_styles())

    @staticmethod
    def get_all_lexers():
        return get_all_lexers()

    def highlight_code(self, code, language, style="default"):
        formatter = HtmlFormatter(style=style, noclasses=True)
        lex = lexers.get_lexer_by_name(language)
        html_code = highlight(code, lex, formatter)

        return self.refactor_html_code(html_code)

    @staticmethod
    def refactor_html_code(html_code):
        soup = BeautifulSoup(html_code, 'html.parser')
        div = soup.find("div", attrs={"class": "highlight"})
        bground = div['style']
        div['style'] = div['style'] + ";border-radius: 10px;over"
        pre = div.find('pre')
        pre['style'] = pre['style'] + ';margin: 20px, 20px; padding: 20px;'

        return str(soup.prettify()), bground
