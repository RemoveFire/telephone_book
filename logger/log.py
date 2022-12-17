from datetime import datetime as date
import logger.data_variable


def init_log():
    # создание файла логов при отсутствии
    with open(logger.variable.log_file, 'w', encoding='utf-8') as logs:
        logs.write('')


def write_log(log_oper: str):
    # добавление даты и времени операции + запись лога
    global log_file
    operation_time = date.today().strftime('%d.%m.%Y %H:%M:%S')
    log_oper = log_oper + operation_time + logger.variable.s_symb + '\n'
    with open(logger.variable.log_file, 'a', encoding='utf-8') as logs:
        logs.write(log_oper)
