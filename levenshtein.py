import pandas as pd
import numpy as np

def lev(string1, string2='luca'):
    """
    The definition on https://en.wikipedia.org/wiki/Levenshtein_distance
    is implemented.

    :param string1:
    :param string2:
    :return: Levenshtein distance
    """
    if len(string1) == 0:
        return len(string2)
    elif len(string2) == 0:
        return len(string1)
    elif string1[0] == string2[0]:
        return lev(string1[1:], string2[1:])
    else:
        return 1 + min([lev(string1[1:], string2),
                        lev(string1, string2[1:]),
                        lev(string1[1:], string2[1:])])

def clean_names(string):
    return string.split()[0].strip('"').lower()

if __name__ == '__main__':
    # read and preprocess data
    df = pd.read_csv('./20210103_hundenamen.csv')
    df = df.query('HUNDENAME != "unbekannt"')
    df = df[~df['HUNDENAME'].isnull()]
    df['HUNDENAME'] = df['HUNDENAME'].apply(clean_names)

    # find Levenshtein distance of all entries to "Luca"
    df['LEV'] = df['HUNDENAME'].apply(lev)

    # save unique names with Levenshtein distance of 1.
    res = df.query('LEV == 1')['HUNDENAME'].unique()
    res = list(map(str.capitalize, res))
    with open('./result.csv', 'w') as f:
        for name in res:
            if name == res[-1]:
                f.write(name)
            else:
                f.write(name + ',')