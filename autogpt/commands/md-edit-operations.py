#!/usr/bin/env python3

import subprocess
import re
import sys

DOCLINK = ""
bold = "\033[1m"
normal = "\033[0m"
regular_bar = "-" * 52
bold_bar = "=" * 52
error_bar = "!**************************************************!"

file_list = subprocess.check_output(["git", "diff", "--diff-filter=d", "--cached", "--name-only"]).decode().splitlines()
md_file_list = list(filter(lambda x: x.endswith(".md"), file_list))

if md_file_list:
    errors = 0
    print("\n", "The following files were changed:")
    for file in md_file_list:
        print(f" - {file}")
    print(bold_bar)

    print("\n", regular_bar)
    print(f"{bold}Spell check{normal}")
    print(regular_bar)
    spell_passed = subprocess.call(["npx", "mdspell", "-r", "-a", "-n", "--en-us"] + md_file_list)
    
    print("\n", regular_bar)
    print(f"{bold}Link check{normal}")
    print(regular_bar)
    links_passed = subprocess.call(["npx", "markdown-link-check", "-q", "-p"] + md_file_list)

    print("\n", regular_bar)
    print(f"{bold}Formatting check{normal}")
    print(regular_bar)
    format_passed = subprocess.call(["npx", "markdownlint-cli2"] + md_file_list)

    error_descr = ""

    if links_passed != 0:
        error_descr += "\n- Broken links."
        errors = 1
    if spell_passed != 0:
        error_descr += "\n- Spelling errors."
        errors = 1
    if format_passed != 0:
        error_descr += "\n- Markdown formatting errors."
        errors = 1

    if errors == 1:
        print("\n", error_bar)
        print(f"{bold}ERRORS FOUND{normal}")
        print("There are some problems with your commit:")
        print(error_descr)
        print("\n", "For details on how to fix these errors, see")
        print(f"{DOCLINK}.")
        print(error_bar, "\n")
        sys.exit(1)
    else:
        print("\n", regular_bar)
        print(f"{bold}No errors were found!{normal}")
        sys.exit(0)

else:
    print("\n", regular_bar)
    print("No markdown files were changed in this commit.")
    print("Skipping checks...")
    print(regular_bar, "\n")
    sys.exit(0)
