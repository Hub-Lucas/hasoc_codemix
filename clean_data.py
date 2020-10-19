# coding=utf-8
# data processing
# by LucasHub 2020-08-12
import nltk
import pandas as pd
import re, string
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from ekphrasis.classes.segmenter import Segmenter
from ekphrasis.classes.spellcorrect import SpellCorrector

text_processor = TextPreProcessor(
    # terms that will be normalized
    normalize=['url', 'email', 'percent', 'money', 'phone', 'user',
               'time', 'url', 'date', 'number'],
    # terms that will be annotated
    annotate={"hashtag", "allcaps", "elongated", "repeated",
              'emphasis', 'censored'},
    fix_html=False,  # fix HTML tokens

    # corpus from which the word statistics are going to be used
    # for word segmentation
    segmenter="twitter",

    # corpus from which the word statistics are going to be used
    # for spell correction
    corrector="twitter",

    unpack_hashtags=True,  # perform word segmentation on hashtags
    unpack_contractions=True,  # Unpack contractions (can't -> can not)
    spell_correct_elong=False,  # spell correction for elongated words

    # select a tokenizer. You can use SocialTokenizer, or pass your own
    # the tokenizer, should take as input a string and return a list of tokens
    tokenizer=SocialTokenizer(lowercase=True).tokenize,
    remove_tags=False,
    # list of dictionaries, for replacing tokens extracted from the text,
    # with other expressions. You can pass more than one dictionaries.
    dicts=[emoticons]
)


# Convert labels to numbers （malayalam，Tamil）
def standardize_label_to_number(df, label):
    # df[label] = df[label].str.replace('not-malayalam', '0')
    df[label] = df[label].str.replace('not-Tamil', '0')

    df[label] = df[label].str.replace('Negative', '1')

    df[label] = df[label].str.replace('Positive', '2')
    df[label] = df[label].str.replace('unknown_state', '3')
    df[label] = df[label].str.replace('Mixed_feelings', '4')
    return df
Mixed_feelings Positive unknown_state Negative not-Tamil not-malayalam

mom = []


def standardize_text(df, text_field):
    sent0 = df[text_field].astype(str).tolist()
    seg_eng = Segmenter(corpus="twitter")
    sp = SpellCorrector(corpus="english")
    puncttok = nltk.WordPunctTokenizer().tokenize
    social_tokenizer = SocialTokenizer(lowercase=False).tokenize

    for i in sent0:
        tok_text = text_processor.pre_process_doc(i)
        mom.append(' '.join(tok_text))
        # id,sent0,label
    df = pd.DataFrame({'id': df['id'], 'sent0': mom, 'label': df['label']})
    return df


# Convert emoji to text
def standardize_meme(df, text_field):
    df[text_field] = df[text_field].str.replace(r"🤩", " <Star eyes grinning face> ")
    df[text_field] = df[text_field].str.replace(r"🥰", " <Smiley smiling eyes and three hearts> ")
    df[text_field] = df[text_field].str.replace(r"🤪", " <Fool> ")
    df[text_field] = df[text_field].str.replace(r"🤝", " <Shake hands> ")
    df[text_field] = df[text_field].str.replace(r"🤦", " <Man covering face with palm> ")
    df[text_field] = df[text_field].str.replace(r"🤑", " <Spit money> ")
    df[text_field] = df[text_field].str.replace(r"🤣", " <Flying bird> ")
    df[text_field] = df[text_field].str.replace(r"🤗", " <Hug> ")
    df[text_field] = df[text_field].str.replace(r"🤔", " <Thinking> ")
    df[text_field] = df[text_field].str.replace(r"🤘", " <Rock> ")
    df[text_field] = df[text_field].str.replace(r"🤐", " <Zipper mouth> ")
    df[text_field] = df[text_field].str.replace(r"🤙", " <Call me> ")
    df[text_field] = df[text_field].str.replace(r"🤚", " <Back of the hand> ")
    df[text_field] = df[text_field].str.replace(r"🥡", " <Takeaway box> ")
    df[text_field] = df[text_field].str.replace(r"🤭", " <Cover your mouth> ")
    df[text_field] = df[text_field].str.replace(r"🤓", " <Nerd> ")
    df[text_field] = df[text_field].str.replace(r"🤲", " <Both hands palm up> ")
    df[text_field] = df[text_field].str.replace(r"🧐", " <Single glasses survey> ")
    df[text_field] = df[text_field].str.replace(r"🤡", " <Clown face> ")
    df[text_field] = df[text_field].str.replace(r"🤜🤛", " <Fist left hand Fist right hand> ")
    df[text_field] = df[text_field].str.replace(r"🤜", " <Fist left hand> ")
    df[text_field] = df[text_field].str.replace(r"🤛", " <Fist right hand> ")
    df[text_field] = df[text_field].str.replace(r"🤨", " <Raise eyebrows> ")
    df[text_field] = df[text_field].str.replace(r"🥳", " <Party> ")
    df[text_field] = df[text_field].str.replace(r"🥺", " <Plead> ")
    df[text_field] = df[text_field].str.replace(r"🤮", " <Vomiting> ")
    df[text_field] = df[text_field].str.replace(r"🤬", " <Symbol covers mouth> ")
    df[text_field] = df[text_field].str.replace(r"🤯", " <Explosive head> ")
    df[text_field] = df[text_field].str.replace(r"🧨", " <Firecrackers> ")
    df[text_field] = df[text_field].str.replace(r"🤞‍‍‍", " <Fingers crossed> ")
    df[text_field] = df[text_field].str.replace(r"🤢‍‍‍", " <disgusting> ")
    df[text_field] = df[text_field].str.replace(r"🦁‍‍‍", " <Lion face> ")
    df[text_field] = df[text_field].str.replace(r"🤟‍‍‍", " <I love you> ")
    df[text_field] = df[text_field].str.replace(r"🧡‍‍‍", " <red heart> ")
    df[text_field] = df[text_field].str.replace(r"‍"‍‍‍, " <zwj> ")


    df[text_field] = df[text_field].str.replace(r"1st ", "first")
    df[text_field] = df[text_field].str.replace(r" 1 st ", "first")
    df[text_field] = df[text_field].str.replace(r"2nd", "second")
    df[text_field] = df[text_field].str.replace(r"2 nd", "second")
    df[text_field] = df[text_field].str.replace(r"3rd", "third")
    df[text_field] = df[text_field].str.replace(r"3 rd", "third")
    df[text_field] = df[text_field].str.replace(r"4th", "fourth")
    df[text_field] = df[text_field].str.replace(r"4 th", "fourth")
    df[text_field] = df[text_field].str.replace(r"5th", "fifth")
    df[text_field] = df[text_field].str.replace(r"5 th", "fifth")
    df[text_field] = df[text_field].str.replace(r"6th", "sixth")
    df[text_field] = df[text_field].str.replace(r"6 th", "sixth")

    df[text_field] = df[text_field].str.replace(r"@", " at ")
    df[text_field] = df[text_field].str.replace(r"&", " and ")
    df[text_field] = df[text_field].str.replace(r"$", " dollar ")
    df[text_field] = df[text_field].str.replace(r":-)", " Express a smile ")
    df[text_field] = df[text_field].str.replace(r"-_-", " Sorry ")
    df[text_field] = df[text_field].str.replace(r"(y)", " Sorry ")
    df[text_field] = df[text_field].str.replace(r"&&", " and ")
    df[text_field] = df[text_field].str.replace(r"@", " at ")
    df[text_field] = df[text_field].str.replace(r"#", " ")
    df[text_field] = df[text_field].str.replace(r"> <", " ")
    df[text_field] = df[text_field].str.replace(r"*", " ")
    df[text_field] = df[text_field].str.replace(r"[", " ")
    df[text_field] = df[text_field].str.replace(r"]", " ")

    df[text_field] = df[text_field].str.replace(r"(", " ")
    df[text_field] = df[text_field].str.replace(r")", " ")
    df[text_field] = df[text_field].str.replace(r"_", " ")
    df[text_field] = df[text_field].str.replace(r"  ", " ")
    df[text_field] = df[text_field].str.replace(r"  ", " ")
    df[text_field] = df[text_field].str.replace(r"  ", " ")
    df[text_field] = df[text_field].str.replace(r"  ", " ")
    df[text_field] = df[text_field].str.replace(r"  ", " ")
    return df


# Convert 5 categories to 2 categories. 0 is not malayalam/Tamil, 1 is malayalam/Tamil
def standardize_label_tow(df, label):
    df[label] = df[label].replace(0, "0")

    df[label] = df[label].replace(1, "1")

    df[label] = df[label].replace(2, "1")
    df[label] = df[label].replace(3, "1")
    df[label] = df[label].replace(4, "1")

    return df


# Eliminate samples with label 0, and return labels in the form of 0, 1, 2, 3
def eliminate_context_label_zero(df, label):
    df = df.drop(df[df.label == 0].index, inplace=False)
    df[label] = df[label].replace(1, "0")
    df[label] = df[label].replace(2, "1")
    df[label] = df[label].replace(3, "2")
    df[label] = df[label].replace(4, "3")
    return df




def drop_column_data(df, label):
    df = df.drop(label, axis=1)
    return df


