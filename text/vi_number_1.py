import re
number_dict = {
    1: 'một',
    2: 'hai',
    3: 'ba',
    4: 'bốn',
    5: 'năm',
    6: 'sáu',
    7: 'bảy',
    8: 'tám',
    9: 'chín',
    0: ''
}
_dot_number_re = re.compile(r"([0-9][0-9\.]+[0-9])")
_decimal_number_re = re.compile(r"([0-9]+\,[0-9]+)")

number_length =['', 'nghìn', 'triệu', 'tỷ', 'nghìn', 'triệu', 'tỷ']

def split_number(number):
    arr = []
    while int(number / 1000) > 0:
        arr.append(number % 1000)
        number = int(number / 1000)
    arr.append(number)
    arr = arr[::-1]
    return arr


def read_3_digit(number, key):
    digit_1 = int(number / 100)
    digit_2 = int((number - digit_1 * 100) / 10)
    digit_3 = number % 10
    if key != 1:
        if digit_2 == 0:
            if digit_1 == 0:
                if digit_3 == 0:
                    return ''
                else:
                    str_3_digit = 'không trăm linh ' + number_dict[digit_3]
            else:
                if digit_3 == 0:
                    return number_dict[digit_1] + ' trăm '
                else:
                    str_3_digit = number_dict[digit_1] + ' trăm linh ' + number_dict[digit_3]
        else:
            if digit_1 == 0:
                if digit_3 == 5:
                    str_3_digit = 'không trăm ' + number_dict[digit_2] + ' mươi lăm '
                else:
                    str_3_digit = 'không trăm ' + number_dict[digit_2] + ' mươi ' + number_dict[digit_3]
            else:
                if digit_3 == 5:
                    str_3_digit = number_dict[digit_1] + ' trăm ' + number_dict[digit_2] + ' mươi lăm '
                else:
                    str_3_digit = number_dict[digit_1] + ' trăm ' + number_dict[digit_2] + ' mươi ' + number_dict[digit_3]
    else:
        if digit_2 == 0:
            if digit_1 == 0:
                str_3_digit = number_dict[digit_3]
            else:
                if digit_3 == 0:
                    return number_dict[digit_1] + ' trăm '
                else:
                    str_3_digit = number_dict[digit_1] + ' trăm linh ' + number_dict[digit_3]
        else:
            if digit_1 == 0:
                if digit_3 == 5:
                    str_3_digit = number_dict[digit_2] + ' mươi lăm '
                else:
                    str_3_digit = number_dict[digit_2] + ' mươi ' + number_dict[digit_3]
            else:
                if digit_3 == 5:
                    str_3_digit = number_dict[digit_1] + ' trăm ' + number_dict[digit_2] + ' mươi lăm '
                else:
                    str_3_digit = number_dict[digit_1] + ' trăm ' + number_dict[digit_2] + ' mươi ' + number_dict[digit_3]
    return str_3_digit.replace('một mươi','mười').replace('mươi một','mươi mốt')


def process_number(number):
    result_string = ''
    array_number = split_number(number)
    key = 1
    for number in array_number:
        if len(read_3_digit(number, key)) > 0:
            result_string = result_string + read_3_digit(number, key) + ' '+number_length[len(array_number) - key] + ' '
        else:
            if len(array_number) >= 5 and key == len(array_number) - 3:
                result_string = result_string + read_3_digit(number, key) + 'tỷ '
            else:
                result_string = result_string + read_3_digit(number, key)
        key += 1
    return result_string.replace("  ", ' ').strip()


def process_number_sign(number_str):
    list_number = re.findall(r"[0-9.]*[0-9]+|%|-|\+|\*|/|\$|kg", number_str)
    if len(list_number) > 0:
        return list_number
    return ''


def _remove_dot(m):
    return m.group(1).replace(".", "")


def _expand_decimal_point(m):
    return m.group(1).replace(",", " phẩy ")


def normalize_number(text):
    text = re.sub(_dot_number_re, _remove_dot, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    return text





