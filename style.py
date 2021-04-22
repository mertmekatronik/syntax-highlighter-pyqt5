from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers
from pygments import highlight
from pygments import lexers
from bs4 import BeautifulSoup
from externals.cssParser import parse


class Style:

    @staticmethod
    def get_all_styles():
        return list(get_all_styles())

    @staticmethod
    def get_all_lexers():
        return get_all_lexers()

    def highlight_code(self, code, language,circles:bool,autoresize:bool, style="default"):
        formatter = HtmlFormatter(style=style, noclasses=True)
        lex = lexers.get_lexer_by_name(language)
        html_code = highlight(code, lex, formatter)

        return self.refactor_html_code(html_code,circles,autoresize)




    @staticmethod
    def refactor_html_code(html_code,circles:bool,autoresize:bool):
        moreHTML = '''<div style="text-align: left; padding-left: 20px; padding-top: 20px;">
<span style="height: 12px; width: 12px; background-color: #ff5f56; border-radius: 50%; display: inline-block;"></span>&nbsp; &nbsp;
<span style="height: 12px; width: 12px; background-color: #ffbd2e; border-radius: 50%; display: inline-block;"></span>&nbsp; &nbsp; 
<span style="height: 12px; width: 12px; background-color: #27c93f; border-radius: 50%; display: inline-block;"></span>
</div>
'''
        
        soup = BeautifulSoup(html_code, 'html.parser')
        
        div = soup.find("div", attrs={"class": "highlight"})
        
        bground = div['style']
        style = parse(div["style"])
        div['style'] = div['style'] + ";border-radius: 12px;over;"

        
        pre = div.find('pre')
        pre['style'] = pre['style'] + f'background : {style["background"]};margin: 5px, 20px; border-radius: 12px; padding: 20px;'
        
        if circles:
            div.insert(0,BeautifulSoup(moreHTML, 'html.parser'))
        if autoresize:
            div['style'] = div['style'] + "display: inline-block;"

        pre['style'] = pre['style'] +" border:0px;"
            
        
        
          

        return str(soup.prettify()), bground



