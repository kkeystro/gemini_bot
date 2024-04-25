import markdown2
import re


def clean_html(html):
    # Pattern to identify all HTML tags
    tag_pattern = re.compile(r'<(/?\w+)([^>]*?)>')

    # Supported tags and their allowed formats
    supported_tags = {
        'b': '',
        'strong': '',
        'i': '',
        'em': '',
        'u': '',
        'ins': '',
        's': '',
        'strike': '',
        'del': '',
        'a': ['href'],
        'code': '',
        'pre': '',
        'span': ['class="tg-spoiler"'],
        'tg-spoiler': '',
        'tg-emoji': ['emoji-id']
    }

    # Function to check if tag is supported
    def tag_allowed(tag, attrs):
        if tag not in supported_tags:
            return False
        if isinstance(supported_tags[tag], str):
            return supported_tags[tag] == attrs.strip()
        else:
            attr_pattern = re.compile(r'(\w+)="([^"]+)"')
            for attr, value in attr_pattern.findall(attrs):
                if f'{attr}="{value}"' not in supported_tags[tag]:
                    return False
            return True

    # Replace or keep tags based on whether they're supported
    def replace_tag(match):
        tag, attrs = match.groups()
        tag_name = tag.strip('/')
        if tag_allowed(tag_name, attrs):
            return f'<{tag}{attrs}>'
        return ''

    return tag_pattern.sub(replace_tag, html)


def escape_markdown_v2(md_text):
    # Convert Markdown to HTML
    html = markdown2.markdown(md_text, extras=["markdown-in-html"])

    # Clean HTML by removing unsupported tags
    cleaned_html = clean_html(html)

    return cleaned_html
