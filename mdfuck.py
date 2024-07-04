import markdown2
from bs4 import BeautifulSoup


def clean_html(html_text):
    supported_tags = ['b', 'strong', 'i', 'em', 'u', 's', 'strike', 'del', 'ins', 'a', 'code', 'pre']

    soup = BeautifulSoup(html_text, 'html.parser')

    for tag in soup.find_all():
        if tag.name not in supported_tags:
            tag.unwrap()

    cleaned_html = str(soup)

    return cleaned_html


def escape_markdown_v2(md_text):
    html = markdown2.markdown(md_text, extras=["markdown-in-html"])

    cleaned_html = clean_html(html)

    return cleaned_html
