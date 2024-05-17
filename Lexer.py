import re

# Регулярные выражения для различных типов чисел
hex_pattern = re.compile(r'^[0-9A-Fa-f]+[Hh]$')  # Шестнадцатеричные числа, оканчивающиеся на маркер 'H' или 'h'
oct_pattern = re.compile(r'^[0-7]+[Oo]$')        # Восьмеричные числа, оканчивающиеся на маркер 'O' или 'o'
bin_pattern = re.compile(r'^[01]+[Bb]$')         # Двоичные числа, оканчивающиеся на маркер 'B' или 'b'
dex_pattern = re.compile(r'^\d+$')               # Десятичные числа

# Системные символы и операторы
sys_list = "ABCDEFabsdef HhOo"  # Список допустимых символов
operator = ['NE', 'EQ', 'LT', 'LE', 'GT', 'GE', 'and', 'or', '~']  # Логические операторы
arithmetic_operator = ['plus', 'min', 'mult', 'div']  # Арифметические операторы
type_of_data = ['integer', 'real', 'boolean']  # Типы данных
for_data = ['for', 'to', 'do']  # Ключевые слова для цикла for
if_data = ['if', 'then', 'else']  # Ключевые слова для условного оператора if
while_data = ['while', 'do']  # Ключевые слова для цикла while
keywords = type_of_data + for_data + if_data + while_data + ['begin', 'end', 'readln', 'writeln', 'dim']  # Все ключевые слова

def search_token(program_string):
    flag_of_mistake = False  # Флаг ошибки
    current_token = ""  # Текущий токен
    current_token_list = []  # Список токенов
    current_program_string = program_string.split('\n')  # Разделение строки программы на строки
    flag_enterence = False  # Флаг входа в программу
    flag_output = False  # Флаг выхода из программы
    o_flag = True  # Флаг для проверки скобок

    # Проверка на наличие точки входа в программу
    for current_string in current_program_string:
        if current_string.strip() == '{':
            flag_enterence = True
        elif current_string.strip() in ["}end", "} end"]:
            flag_output = True
            break

    if not flag_enterence:
        print("Ошибка #0051: Не найдена точка входа в программу")
        return flag_of_mistake

    # Обработка каждой строки программы
    for current_string in current_program_string:
        current_string += ' '  # Добавление пробела в конец строки для корректной обработки последнего токена
        current_token = ""  # Сброс текущего токена
        token_flag = 0  # Флаг токена

        # Обработка каждого символа в строке
        for current_sim in current_string:
            if current_sim == '\n':
                if current_token:
                    current_token_list.append(current_token)
                current_token = ""
                token_flag = 0
            elif current_sim == '-':
                current_token += current_sim
                token_flag = 2
            elif current_sim.isalpha():
                if token_flag == 2 and len(current_token) == 1 and current_token in sys_list:
                    print("Ошибка")
                    return flag_of_mistake
                current_token += current_sim
                token_flag = 2
            elif current_sim.isdigit():
                current_token += current_sim
                token_flag = 2
            elif current_sim in ['.', '~', '(', ')']:
                if token_flag == 2:
                    current_token += current_sim
                else:
                    if token_flag != 0:
                        current_token_list.append(current_token)
                    current_token = ""
                    current_token_list.append(current_sim)
            elif current_sim == '[':
                current_token_list.append(current_sim)
                current_token = ""
                o_flag = False
            elif current_sim == ']':
                current_token_list.append(current_sim)
                current_token = ""
                o_flag = True
            elif current_sim == ',':
                if current_token:
                    current_token_list.append(current_token)
                current_token = ""
                current_token_list.append(current_sim)
            elif current_sim == ' ' or token_flag == 0:
                if len(current_token) == 0:
                    continue
                if token_flag == 2:
                    if not any(pattern.match(current_token) for pattern in [hex_pattern, oct_pattern, bin_pattern, dex_pattern]):
                        print("Ошибка")
                        return flag_of_mistake
                current_token_list.append(current_token)
                current_token = ""
                token_flag = 0

    # Проверка на наличие точки выхода из программы
    if not flag_output:
        print("Ошибка #0010: Неожиданный конец файла")
        return flag_of_mistake

    # Проверка на корректность скобок
    if not o_flag:
        print("Ошибка")
        return flag_of_mistake

    # Добавление начального и конечного токенов
    current_token_list.insert(0, '{')
    current_token_list.append('}')
    current_token_list.append('end')

    return current_token_list
