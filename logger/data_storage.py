from logger import data_variable


def init_book():  # создание файла телефонной книги при отсутствии
    with open(data_variable.book_file, 'w', encoding='utf-8') as book:
        book.write('')


def number_of_lines(user_file):
    # подсчёт количества записей в телефонной книге
    with open(user_file, 'r', encoding='utf-8') as book:
        return sum(1 for _ in book)


def last_line(user_file):
    # вывод последней строки из файла телефонной книги
    with open(user_file, 'r', encoding='utf-8') as book:
        lines = book.read().splitlines()
        return lines[-1]


def add_new_contact(new_contact):
    # добавление нового контакта в файл телефонной книги
    if number_of_lines(data_variable.book_file) == 0:
        num = 1
    else:
        num = int(last_line(data_variable.book_file).split(data_variable.s_symb)[0]) + 1
    with open(data_variable.book_file, 'a', encoding='utf-8') as book:
        new_contact = str(num) + data_variable.s_symb + new_contact + '\n'
        book.write(new_contact)
    return new_contact


def delete_contact(id):
    cont = data_variable.s_symb.join(choice_by_id(id)) + '\n'
    result_file = ''
    with open(data_variable.book_file, 'r', encoding='utf-8') as book:
        source_file = book.read()
        result_file = source_file.replace(cont, '')
    with open(data_variable.book_file, 'w', encoding='utf-8') as book:
        book.write(result_file)
    return cont[:-2]


def book_to_list():
    # список всех контаков телефонной книги
    with open(data_variable.book_file, 'r', encoding='utf-8') as book:
        str_list = book.read().split('\n')[:-1]
        phone_list = []
        for item in str_list:
            phone_list.append(item.split(data_variable.s_symb))
    return phone_list


def contact_to_list(num, value):
    # список контактов по значению позиции сортировки
    with open(data_variable.book_file, 'r', encoding='utf-8') as book:
        str_list = book.read().split('\n')[:-1]
        contact_list = []
        for item in str_list:
            entry = item.split(data_variable.s_symb)
            if value.lower() == entry[num].lower() or value.lower() in entry[num].lower():
                contact_list.append(entry)
    return contact_list


def choice_by_id(id):
    # вывод контакта в список по заданному id
    phone_list = book_to_list()
    for item in range(len(phone_list)):
        if int(phone_list[item][0]) == id:
            contact_list = phone_list[item]
    return contact_list


def id_to_list():
    # формирование списка id для диалога выбора id контакта
    phone_list = book_to_list()
    id_list = []
    for item in range(len(phone_list)):
        id_list.append(int(phone_list[item][0]))
    return id_list


def name_to_list(num):
    # формирование списка неповторяющихся значений в телефонной книге
    # по заданной позиции поиска из title
    phone_list = book_to_list()
    name_list = [phone_list[0][num]]
    for i in range(1, len(phone_list)):
        if not phone_list[i][num] in name_list:
            name_list.append(phone_list[i][num])
    return name_list


def output_to_string(phone_list):
    # создание словаря из списка для вывода таблицей
    phone_dict = dict()
    for i in range(len(data_variable.title)):
        key = data_variable.title[i]
        column = []
        for j in range(len(phone_list)):
            column.append(phone_list[j][i])
        value = column
        phone_dict[key] = value
    return phone_dict
