#!pip install emoji
import emoji
import html
import logging
import re
from typing import List

prefix_list = [
    "ال",
    "و",
    "ف",
    "ب",
    "ك",
    "ل",
    "لل",
    "\u0627\u0644",
    "\u0648",
    "\u0641",
    "\u0628",
    "\u0643",
    "\u0644",
    "\u0644\u0644",
    "س",
]
suffix_list = [
    "ه",
    "ها",
    "ك",
    "ي",
    "هما",
    "كما",
    "نا",
    "كم",
    "هم",
    "هن",
    "كن",
    "ا",
    "ان",
    "ين",
    "ون",
    "وا",
    "ات",
    "ت",
    "ن",
    "ة",
    "\u0647",
    "\u0647\u0627",
    "\u0643",
    "\u064a",
    "\u0647\u0645\u0627",
    "\u0643\u0645\u0627",
    "\u0646\u0627",
    "\u0643\u0645",
    "\u0647\u0645",
    "\u0647\u0646",
    "\u0643\u0646",
    "\u0627",
    "\u0627\u0646",
    "\u064a\u0646",
    "\u0648\u0646",
    "\u0648\u0627",
    "\u0627\u062a",
    "\u062a",
    "\u0646",
    "\u0629",
]
other_tokens = ["[رابط]", "[مستخدم]", "[بريد]"]

# the never_split list is ussed with the transformers library
prefix_symbols = [x + "+" for x in prefix_list]
suffix_symblos = ["+" + x for x in suffix_list]
never_split_tokens = list(set(prefix_symbols + suffix_symblos + other_tokens))

url_regexes = [
    r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    r"@(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS",
    r"http[s]?://[a-zA-Z0-9_\-./~\?=%&]+",
    r"www[a-zA-Z0-9_\-?=%&/.~]+",
    r"[a-zA-Z]+\.com",
    r"(?=http)[^\s]+",
    r"(?=www)[^\s]+",
    r"://",
]
user_mention_regex = r"@[\w\d]+"
email_regexes = [r"[\w-]+@([\w-]+\.)+[\w-]+", r"\S+@\S+"]
redundant_punct_pattern = (
    r"([!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ【»؛\s+«–…‘]{2,})"
)

regex_tatweel = r"(\D)\1{2,}"
multiple_char_pattern = re.compile(r"(\D)\1{2,}", re.DOTALL)

rejected_chars_regex = r"[^0-9\u0621-\u063A\u0640-\u066C\u0671-\u0674a-zA-Z\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘]"
rejected_chars_regexv2 = r"[^0-9\u0621-\u063A\u0641-\u066C\u0671-\u0674a-zA-Z\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘/]"

regex_url_step1 = r"(?=http)[^\s]+"
regex_url_step2 = r"(?=www)[^\s]+"
regex_url = r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
regex_mention = r"@[\w\d]+"
regex_email = r"\S+@\S+"

chars_regex = r"0-9\u0621-\u063A\u0640-\u066C\u0671-\u0674a-zA-Z\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘"
chars_regexv2 = r"0-9\u0621-\u063A\u0640-\u066C\u0671-\u0674a-zA-Z\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘/"

white_spaced_double_quotation_regex = r'\"\s+([^"]+)\s+\"'
white_spaced_single_quotation_regex = r"\'\s+([^']+)\s+\'"
white_spaced_back_quotation_regex = r"\`\s+([^`]+)\s+\`"
white_spaced_em_dash = r"\—\s+([^—]+)\s+\—"

left_spaced_chars = r" ([\]!#\$%\),\.:;\?}٪’،؟”؛…»·])"
right_spaced_chars = r"([\[\(\{“«‘*\~]) "
left_and_right_spaced_chars = r" ([\+\-\<\=\>\@\\\^\_\|\–]) "

hindi_nums = "٠١٢٣٤٥٦٧٨٩"
arabic_nums = "0123456789"
hindi_to_arabic_map = str.maketrans(hindi_nums, arabic_nums)

def _remove_non_digit_repetition(text: str) -> str:
    """
    :param text:  the input text to remove elongation
    :return: delongated text
    """
    text = multiple_char_pattern.sub(r"\1\1", text)
    return text

def _remove_redundant_punct(text: str) -> str:
    text_ = text
    result = re.search(redundant_punct_pattern, text)
    dif = 0
    while result:
        sub = result.group()
        sub = sorted(set(sub), key=sub.index)
        sub = " " + "".join(list(sub)) + " "
        text = "".join(
            (text[: result.span()[0] + dif], sub, text[result.span()[1] + dif :])
        )
        text_ = "".join(
            (text_[: result.span()[0]], text_[result.span()[1] :])
        ).strip()
        dif = abs(len(text) - len(text_))
        result = re.search(redundant_punct_pattern, text_)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def simple_clean(text: str,
                 keep_user=False,
                 replace_urls_emails_mentions=True,
                 remove_html_markup=True,
                 map_hindi_numbers_to_arabic=True,
                 remove_non_digit_repetition=True,
                 lower=True,
                 split_hashtags=True,
                 drop_urls_emails=True,
                 keep_emojis=True) -> str:
    
    text = str(text).replace("…","...")
    text = html.unescape(text)
    
    if lower:
        text = text.lower()

    if replace_urls_emails_mentions:
        # replace all possible URLs
        for reg in url_regexes:
            text = re.sub(reg, " URL ", text)
        # REplace Emails with [بريد]
        for reg in email_regexes:
            text = re.sub(reg, " EMAIL ", text)
        # replace mentions with [مستخدم]
        if keep_user:
            text = re.sub(user_mention_regex, " USER ", text)
        else:
            text = re.sub(user_mention_regex, " ", text)
            
    if drop_urls_emails:
        text = text.replace("URL","").replace("EMAIL","")
        
    if remove_html_markup:
        # remove html line breaks
        text = re.sub("<br />", " ", text)
        # remove html markup
        text = re.sub("</?[^>]+>", " ", text)

    if map_hindi_numbers_to_arabic:
        text = text.translate(hindi_to_arabic_map)

    # remove repeated characters >2
    if remove_non_digit_repetition:
        text = _remove_non_digit_repetition(text)


    # remove unwanted characters
    if keep_emojis:
        emoji_regex = "".join(list(emoji.UNICODE_EMOJI["en"].keys()))
        rejected_chars_regex2 = "[^%s%s]" % (chars_regex, emoji_regex)
        text = re.sub(rejected_chars_regex2, " ", text)
    else:
        text = re.sub(rejected_chars_regex, " ", text)
    #text = text.replace("..","...")
    
    if split_hashtags:
        text = " ".join([a for a in re.split('([A-Z][a-z]+)', text) if a])
    
    text = text.replace("  "," ").replace("؟","?").replace("..","...").replace('[مستخدم]','').replace('[رابط]','').replace(" _ ","").replace('"',"").replace("\n"," ").replace("  "," ").strip()
    return text


"""
import re
import string
import numpy as np
import pandas as pd
url_regexes = [
    r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    r"@(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS",
    r"http[s]?://[a-zA-Z0-9_\-./~\?=%&]+",
    r"www[a-zA-Z0-9_\-?=%&/.~]+",
    r"[a-zA-Z]+\.com",
    r"(?=http)[^\s]+",
    r"(?=www)[^\s]+",
    r"://",
]
user_mention_regex = r"@[\w\d]+"
email_regexes = [r"[\w-]+@([\w-]+\.)+[\w-]+", r"\S+@\S+"]
redundant_punct_pattern = (
    r"([!\"\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ【»؛\s+«–…‘]{2,})"
)
regex_tatweel = r"(\w)\1{2,}"
rejected_chars_regex = r"[\"\$%\'\(\)\*\+,\.;\-<=·>@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘]"

regex_url_step1 = r"(?=http)[^\s]+"
regex_url_step2 = r"(?=www)[^\s]+"
regex_url = r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
regex_mention = r"@[\w\d]+"
regex_email = r"\S+@\S+"

chars_regex = r"0-9\u0621-\u063A\u0640-\u066C\u0671-\u0674a-zA-Z\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ»؛\s+«–…‘"

def simple_clean(text):
    text = text.replace("@ ","@").replace('؟','?').replace('\n\n','. ').replace('\n','. ').replace("'",'').strip()
    text = re.sub(user_mention_regex, "USER", text)
    # replace all possible URLs
    for reg in url_regexes:
        text = re.sub(reg, "URL", text)
    # REplace Emails with [بريد]
    for reg in email_regexes:
        text = re.sub(reg, "EMAIL", text)
    # replace mentions with [مستخدم]
    # remove html line breaks
    text = re.sub("<br />", " ", text)
    # remove html markup
    text = re.sub("</?[^>]+>", " ", text)
    text = re.sub(rejected_chars_regex, " ", text)
    text = text.replace('[مستخدم]','').replace('[رابط]','').replace(" _ ","").replace('"',"").strip()
    text = re.sub(' +',' ',text)
    return text
"""