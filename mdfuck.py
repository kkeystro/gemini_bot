import re

import markdown2
from bs4 import BeautifulSoup


def clean_html(html_text):
    # Список поддерживаемых HTML тегов в aiogram
    supported_tags = ['b', 'strong', 'i', 'em', 'u', 's', 'strike', 'del', 'ins', 'a', 'code', 'pre']

    # Сначала защитим выражения вроде "if a <b and b>c"
    protected_expressions = []

    def protect_expression(match):
        protected_expressions.append(match.group())
        return f"PROTECTED_EXPRESSION_{len(protected_expressions) - 1}"

    html_text = re.sub(r'\b\w+\s*[<>]\s*\w+(\s+(and|or)\s+\w+\s*[<>]\s*\w+)*', protect_expression, html_text)

    # Парсим HTML
    soup = BeautifulSoup(html_text, 'html.parser')

    # Удаляем неподдерживаемые теги, сохраняя их содержимое
    for tag in soup.find_all():
        if tag.name not in supported_tags:
            tag.unwrap()

    # Преобразуем обратно в строку
    cleaned_html = str(soup)

    # Восстанавливаем защищенные выражения
    for i, expr in enumerate(protected_expressions):
        cleaned_html = cleaned_html.replace(f"PROTECTED_EXPRESSION_{i}", expr)

    return cleaned_html


def escape_markdown_v2(md_text):
    # Convert Markdown to HTML
    html = markdown2.markdown(md_text, extras=["markdown-in-html"])

    # Clean HTML by removing unsupported tags
    cleaned_html = clean_html(html)

    return cleaned_html
