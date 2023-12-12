import pandas as pd
import wordfreq as wf
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator


def identify_pos(pos):
    morphy_tag = {'NN': ['n', 'существительное'], 'JJ': ['a', 'прилагательное'],
                  'VBN': ['v', 'глагол'], 'RB': ['r', 'наречие']}
    return morphy_tag.get(pos, ['n', 'существительное'])


def specify_pos(text):
    for word, tag in pos_tag(word_tokenize(text)):
        return identify_pos(tag)[1]


def identify_lemma(text):
    wnl = WordNetLemmatizer()
    for word, tag in pos_tag(word_tokenize(text)):
        return wnl.lemmatize(word.lower(), pos=identify_pos(tag)[0])


def translate_word(text):
    translated = GoogleTranslator('en', 'ru').translate(text)
    return translated


def read_text_file():
    with open('input.txt', 'r') as file:
        data = [line.strip().split() for line in file]
        data = pd.DataFrame(data, columns=['Слово', 'Категория'])
    return data


def create_dictionary():
    data = read_text_file()
    with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        for index, row in data.iterrows():
            word = row['Слово']
            sheet_name = row['Категория']
            freq = wf.word_frequency(word, 'en')
            df_temp = pd.DataFrame(
                {'Слово': [word],
                 'Часть речи': [specify_pos(word)],
                 'Перевод': [translate_word(word)],
                 'Лемма': [identify_lemma(word)],
                 'Частота': [freq]})
            df_temp.to_excel(writer, sheet_name=sheet_name, index=False, header=False,
                             startrow=writer.sheets[sheet_name].max_row)
    return df_temp


def sorted_dictionary():
    create_dictionary()
    with pd.ExcelFile('output.xlsx', engine='openpyxl') as xls:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df.sort_values(by='Частота', inplace=True, ascending=False)
            df['Частота'] = df['Частота'].apply(lambda x: '{:.10f}'.format(x))
            with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False, engine='openpyxl')

    return df
