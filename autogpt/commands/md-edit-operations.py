"""Markdown edit operations for AutoGPT"""

from __future__ import annotations

from spellchecker import SpellChecker
import subprocess
import re
import sys
import mistune


def extract_text_from_markdown(markdown):
    # Remove code blocks
    code_block_pattern = r"```.*?```"
    markdown = re.sub(code_block_pattern, "", markdown, flags=re.DOTALL)
    
    # Remove inline code
    inline_code_pattern = r"`.*?`"
    markdown = re.sub(inline_code_pattern, "", markdown)

    # Remove URLs
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    markdown = re.sub(url_pattern, "", markdown)

    # Remove Markdown formatting
    formatting_pattern = r"#|\*|\[|\]|\(|\)|\||>|`|-|_"
    text = re.sub(formatting_pattern, "", markdown)
    return text

def get_md_files_list() -> List:
    file_list = subprocess.check_output(["git", "diff", "--diff-filter=d", "--cached", "--name-only"]).decode().splitlines()
    return list(filter(lambda x: x.endswith(".md"), file_list))

@command("get_mispelled_words", "Check mispelled words", '"filename": "<filename>"')
def get_mispelled_words(filename):
    text = extract_text_from_markdown(filename)
    spell = SpellChecker()
    words = text.split()
    return spell.unknown(words)

def check_markdown_formatting(markdown_content):
    return mistune.markdown(markdown_content)

def broken_links_exist():
    return subprocess.call(["markdown-link-check", "-q", "-p"] + md_file_list)

def format_errors_exist():
    return subprocess.call(["npx", "markdownlint-cli2"] + md_file_list)

def md_files_exist():
    return True if md_file_list else False
