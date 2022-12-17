import pandas as pd
from logger import data_variable


def string_format(phone_dict):
    # вывод таблицей - построчный (из словаря)
    print('\n')
    data = pd.DataFrame(phone_dict)
    print(data)


def column_format(phone_list):
    # вывод в столбец с разделением пустой строкой (из списка)
    print('\n')
    for i in range(len(phone_list)):
        for j in range(len(data_variable.title)):
            print(f'{data_variable.title[j]}: {phone_list[i][j]}')
        print()
