import os.path


from logger import data_variable

from logger.log import *
from logger.data_output import *

from logger.data_storage import *


def invalid_number(choice):
    # диалог о выборе действия при некорректном вводе (все диалоги)
    res_choice = 1
    if input(f'Вы ввели некорректное значение: {choice}.\n'
             'Если желаете продолжить, введите "1", '
             'в противном случае введите любой другой символ: ') != '1':
        res_choice = 0
    return res_choice


def choice_and_correct(options: list, message: str):
    # диалог выбора и проверки
    # корректности ввода (все диалоги)
    choice = '-1'
    while not int(choice) in options:
        choice = input(message)
        if not int(choice) in options:
            if invalid_number(choice) == 0:
                choice = 0
                break
    return int(choice)


def input_contact():
    # диалог ввода нового контакта через терминал
    print('Введите новый контакт.')
    contact = ''
    for item in range(1, len(logger.data_variable.title)):
        user_text = ''
        while logger.data_variable.s_symb in user_text or user_text == '':
            user_text = input(f'{logger.data_variable.title[item]}: ')
            if logger.data_variable.s_symb in user_text:
                print(f'Вы использовали системный символ "{logger.data_variable.s_symb}". '
                      'Возможна некорректная работа программы.\n'
                      'Повторите ввод без системного символа.')
        contact = contact + user_text + logger.data_variable.s_symb
    contact[:-2]
    return contact


def search_by_input(num):
    # диалог ввода символов для поиска контакта по позиции поиска
    return input(f'Введите несколько символов для поиска по позиции {logger.data_variable.title[num]}: ')


def when_no_search_results():
    # сообщение для диалога выбора
    # действий при отсутствии контактов по запросу
    print('Контакты, соответствующие Вашему запросу, отсутствуют.\n')
    message = 'Вам доступны следующие действия:\n' + logger.data_variable.mess_actions
    message += 'Введите номер действия: '
    return choice_and_correct(logger.data_variable.actions, message)


def operation_selection():
    # сообщение для диалога выбора типа операции
    message = 'Вам доступны следующие операции:\n' + logger.data_variable.list_oper
    message += 'Введите номер операции: '


def contact_deletion_message():
    # сообщение об удалении контакта
    print('Удаление выбранного контакта выполнено.')


def select_output_format():
    # сообщение для диалога выбора формата вывода данных
    message = 'Вам доступны следующие форматы вывода:\n' + logger.data_variable.out_form
    message += 'Введите номер формата: '
    return choice_and_correct(logger.data_variable.formats, message)


def select_sign(select_list):
    # сообщение для диалога выбора номера позиции поиска из title
    message = 'Поиск в телефонной книге воможен по следующим позициям:\n' + select_list
    message += 'Введите номер позиции: '
    return choice_and_correct(logger.data_variable.sel_position, message)


def id_choice():
    # сообщение для диалога ввода id искомого контакта
    message = 'Введите id искомого контакта: '
    return choice_and_correct(id_to_list(), message)


def get_key(dict, value):
    # возврат ключа по содержимому значения словаря
    for k, v in dict.items():
        if v == value:
            return k


def select_position_title():
    # возврат номера позиции поиска в списке title
    select_list = ''
    for item in range(len(logger.data_variable.sel_position)):
        select_list = select_list + str(logger.data_variable.sel_position[item]) + '. '
        select_list = select_list + logger.data_variable.title[item] + '\n'
    return select_sign(select_list)


def check_availability_data(num, value):
    # проверка наличия контактов по запросу
    list_name = name_to_list(num)
    count = 0
    for item in range(len(list_name)):
        if value.lower() in list_name[item].lower() or value.lower() == list_name[item].lower():
            count += 1
    return count


def print_input_select(contact_list):
    # вывод списка контактов
    choice = select_output_format()
    match choice:
        case 1:
            string_format(output_to_string(contact_list))
            log_f = logger.data_variable.log_form[choice]
        case 2:
            column_format(contact_list)
            log_f = logger.data_variable.log_form[choice]
    return log_f


def input_all():
    return print_input_select(book_to_list())


def input_select():
    sel_pos = select_position_title()
    log_s = logger.data_variable.title[sel_pos] + logger.data_variable.s_symb
    if sel_pos == 0:
        value = str(id_choice())
        log_s = log_s + value + logger.data_variable.s_symb
        log_s = log_s + print_input_select(contact_to_list(0, value)) + logger.data_variable.s_symb
    else:
        av_data = 0
        while av_data == 0:
            value = search_by_input(sel_pos)
            log_s = log_s + value + logger.data_variable.s_symb
            av_data = check_availability_data(sel_pos, value)
            if av_data != 0:
                log_s = log_s + print_input_select(contact_to_list(sel_pos, value)) + logger.data_variable.s_symb
            else:
                act = when_no_search_results()
                if act == 1:
                    av_data = 0
                elif act == 2:
                    name_to_list(sel_pos)
                    next_action = continue_or_exit()
                    if next_action == '1':
                        av_data = 0
                    else:
                        log_s += 'invalid value, the operation was interrupted by the user'
                        av_data = -1
                elif act == 3:
                    log_s += 'invalid value, the operation was interrupted by the user'
                    av_data = -1
    return


def add_contact():
    # ввод нового контакта -> только через терминал с диалогом
    return add_new_contact(input_contact())[:-2]


def del_contact():
    log_d = delete_contact(id_choice())
    contact_deletion_message()
    return log_d


def greetings():
    # приветствие с переходом на диалог выбора дальнейшей работы или завершения
    print('Приветствую Вас в лайтовой программе управления телефонной книгой!')
    return continue_or_exit()


def message_on_empty_book():
    # сообщение при отсутствии записей в тлф.книге
    print('В настоящее время телефонная книга пуста. '
          'Вам доступна только операция добавления нового контакта.')


def farewell():
    # сообщение при завершении работы с программой
    print('Спасибо за пользование программой. До новых встреч!')


def continue_or_exit():  # диалог выбора дальнейшей работы или завершения
    return input('Для продолжения введите "1". \n'
                 'Для завершения - любой другой символ: ')


write_log('program start, ')

if not os.path.isfile(logger.data_variable.log_file):
    # проверка наличия файла логов (из logger.data_variable)
    init_log()
    write_log('init_log_file' + logger.data_variable.s_symb + logger.data_variable.log_file + logger.data_variable.s_symb)
if not os.path.isfile(logger.data_variable.book_file):
    # проверка наличия файла тлф.книги (из logger.data_variable)
    init_book()
    write_log('init_phone_book_file' + logger.data_variable.s_symb + logger.data_variable.book_file + logger.data_variable.s_symb)

next_action = greetings()
while next_action == "1":
    if number_of_lines(logger.data_variable.book_file) == 0:
        # проверка на наличие записей в тлф.книге
        message_on_empty_book()
        if continue_or_exit() == '1':
            opers = get_key(logger.data_variable.log_oper, 'add_contact')
        else:
            break
    else:
        opers = operation_selection()
    match opers:
        case 1:
            log_op = logger.data_variable.log_oper[opers] + logger.data_variable.s_symb
            log_op = log_op + input_all() + logger.data_variable.s_symb
            write_log(log_op)
        case 2:
            log_op = logger.data_variable.log_oper[opers] + logger.data_variable.s_symb
            log_op += input_select()
            write_log(log_op)
        case 3:
            log_op = logger.data_variable.log_oper[opers] + logger.data_variable.s_symb
            log_op += add_contact()
            write_log(log_op)
        case 4:
            log_op = logger.data_variable.log_oper[opers] + logger.data_variable.s_symb
            log_op += del_contact()
            write_log(log_op)
    next_action = continue_or_exit()
farewell()
write_log('program shutdown, ')
