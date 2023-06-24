#Лабораторная работа N8, построить и проверить программную модель ассоциативной памяти с диагональной адресацией на основе сумматора.
#поиск ближайшего значения сверху или снизу.
size_of_table = 16
FOUR = 4
A_start = 3
B_start = 7
S_start = 11
import random
from copy import deepcopy
from itertools import combinations
from functools import reduce
def from_normal_to_diagonal(table):
    newtable = [[0 for m in range(size_of_table)] for n in range(size_of_table)]
    for j in range(size_of_table):
        column = [table[i][j] for i in range(size_of_table)]
        for i in range(size_of_table):
            string_index = shift_index(i, j)
            newtable[string_index][j] = column[i]
    return newtable

def merge(formula, arguments_number):
    merged = []
    unmerged = []
    used = [False for i in range(len(formula))]
    for i in range(arguments_number):
        for j in range(len(formula) - 1):
            for k in range(j + 1, len(formula)):
                if from_normal_to_diagonal(formula[j], formula[k], i, arguments_number):
                    used[j] = True
                    used[k] = True
                    merged.append(formula[j].copy())
                    merged[-1].pop(i)
                    merged[-1].insert(i, -1)
                    break
    for i in range(len(used)):
        if not (used[i]):
            unmerged.append(formula[i])
    return merged, unmerged


def substitute(values, formula):
    for i in range(len(values)):
        if values[i] == -1:
            missed_value = i
    for i in range(len(formula)):
        if formula[i] != -1 and i != missed_value:
            existing_arg = i
    res = []
    res.append(formula[missed_value])
    if formula[existing_arg] == values[existing_arg]:
        res.append(1)
    else:
        res.append(0)
    return res


def delete_excess(formula):
    new_formula = formula.copy()
    no_change = 1
    i = 0
    while i < len(new_formula):
        res = []
        for other in new_formula:
            if new_formula[i] != other:
                sub = substitute(new_formula[i], other)
                if sub[1] == no_change:
                    res.append(sub[0])
        pos, neg = False, False
        for arg in res:
            if arg == 0: neg = True
            if arg == 1: pos = True
        if pos and neg:
            new_formula.pop(i)
        else:
            i += 1
    return new_formula


def delete_identical(formula):
    i = 0
    while i < len(formula) - 1:
        same = False
        for j in range(i + 1, len(formula)):
            if formula[i] == formula[j]:
                same = True
        if same:
            formula.pop(i)
        else:
            i += 1
    return formula

def shift_index(index, shift_number):
    newindex = shift_number + index
    if newindex >= size_of_table:
        return newindex - size_of_table
    else:
        return newindex


def add_new_term(term, standart_table, diagonal_table):
    empty_index = 0
    while standart_table[empty_index] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        empty_index += 1
    standart_table[empty_index] = [term[i] for i in range(size_of_table)]
    for j in range(size_of_table):
        string_index = shift_index(empty_index, j)
        diagonal_table[string_index][j] = term[j]


def show(table, index):
    return [table[shift_index(index, i)][i] for i in range(size_of_table)]


def sum(table, standart_table, V):
    for i in range(size_of_table):
        term = show(table, i)
        if [term[0], term[1], term[2]] == V:
            A, B = [], []
            S = [0, 0, 0, 0, 0]
            for j in range(FOUR):
                A.append(term[A_start + j])
                B.append(term[B_start + j])
            for j in range(FOUR):
                S[len(S) - j - 1] += A[len(A) - j - 1] + B[len(B) - j - 1]
                if S[len(S) - j - 1] >= 2:
                    S[len(S) - j - 1] -= 2
                    S[len(S) - j - 2] = 1
            for j in range(S_start, size_of_table):
                string_index = shift_index(i, j)
                table[string_index][j] = S[j - S_start]
            standart_table[i] = show(table, i)


def f1(first_term, second_term, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_term)):
        if first_term[i] == 1 and second_term[i] == 1:
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_term(rezult, standart_table, diagonal_table)


def f14(first_term, second_term, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_term)):
        if not (first_term[i] == 1 and second_term[i] == 1):
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_term(rezult, standart_table, diagonal_table)


def f3(first_term, standart_table, diagonal_table):
    add_new_term(first_term, standart_table, diagonal_table)


def f12(first_term, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_term)):
        if first_term[i] == 1:
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_term(rezult, standart_table, diagonal_table)


def compare(first_term, second_term):
    g = 0
    l = 0

    term_first = [bool(first_term[i]) for i in range(len(first_term))]
    term_second = [bool(second_term[i]) for i in range(len(second_term))]

    for i in range(len(first_term)):
        g = g or (not (term_second[i]) and term_first[i] and not (l))
        l = l or (term_second[i] and not (term_first[i]) and not (g))

    if g == 0 and l == 0:
        return '='
    elif g == 1 and l == 0:
        return '>'
    else:
        return '<'


def most_big(mas_term):
    if mas_term == []:
        return None
    copy_mas = mas_term.copy()
    for i in range(len(copy_mas[0])):
        biggest_term = []
        for j in range(len(copy_mas)):
            if copy_mas[j][i] == 1:
                biggest_term.append(copy_mas[j])
        if biggest_term != []:
            copy_mas = biggest_term

    return copy_mas


def most_little(mas_term):
    if mas_term == []:
        return None
    copy_mas = mas_term.copy()
    for i in range(len(copy_mas[0])):
        smallest_term = []
        for j in range(len(copy_mas)):
            if copy_mas[j][i] == 0:
                smallest_term.append(copy_mas[j])
        if smallest_term != []:
            copy_mas = smallest_term

    return copy_mas

def gluing(SNF):

    nf = []
    for i in range(len(SNF)):  # Run through the SNF in search of implicants
        for j in range(i + 1, len(SNF)):
            summand1 = set(SNF[i])
            summand2 = set(SNF[j])
            implicant = list(summand1 & summand2)
            implicant.sort(key=lambda x: x[-1])
            if len(implicant) == 2:  # If the implicant fits, then add it to NF
                nf.append(implicant)
    return nf


def meth(function, key=None):

    mnf = deepcopy(function)
    for index, _ in enumerate(mnf):  # Checking every implicant, if it is extra
        dict_of_variables = {}
        mnf_copy = deepcopy(mnf)
        verifiable_implicant = mnf_copy.pop(index)  # Remove checked implicant from the list
        for j in verifiable_implicant:
            dict_of_variables[j] = True if key == "1" else False
        for i in mnf_copy:
            for index, j in enumerate(i):  # substitution of values ​​of the checked implicant
                if j in dict_of_variables.keys():
                    i[index] = dict_of_variables[j]
                elif j[-1] in dict_of_variables.keys():
                    i[index] = not dict_of_variables[j[-1]]
                elif f"!{j}" in dict_of_variables.keys():
                    i[index] = not dict_of_variables[f"!{j}"]
        for i in range(len(mnf_copy)):
            for j in range(i + 1, len(mnf_copy)):
                result = set(mnf_copy[i]).symmetric_difference(set(mnf_copy[j]))
                if len(result) == 2 and 1 not in result:
                    mnf.remove(verifiable_implicant)
                    meth(mnf, key)
    return mnf


def calculation_tabular_method(nf, SNF, key=None):

    mnf, table, filled_columns, verifiable_implicants = [], [], [], []
    for i in nf:
        table.append([len(set(i) & set(j)) == 2 for j in SNF])
    filled_columns = [False for _ in range(len(table[0]))]
    for i in range(len(table[0])):
        verifiable_column = [j[i] for j in table]
        if verifiable_column.count(True) == 1:
            implicant = nf[verifiable_column.index(True)]
            if implicant not in mnf:
                mnf.append(implicant)
            filled_columns = list(map(
                lambda x: x[0] or x[1],
                zip(filled_columns, table[verifiable_column.index(True)])
            ))
    verifiable_implicants = [i for i in nf if i not in mnf]
    if False in filled_columns:
        min_amount = 256
        for amount in range(1, len(verifiable_implicants) + 1):
            for subset in combinations(verifiable_implicants, amount):
                set_of_verifiable_implicants = [table[nf.index(i)] for i in subset]
                set_of_verifiable_implicants = reduce(
                    lambda x, y: [i or j for i, j in zip(x, y)],
                    set_of_verifiable_implicants
                )
                if False not in list(map(
                        lambda x: x[0] or x[1],
                        zip(set_of_verifiable_implicants, filled_columns)
                )) and len(set_of_verifiable_implicants) < min_amount:
                    min_amount = len(set_of_verifiable_implicants)
        mnf.extend(subset)
    print("        ", end="")
    for i in SNF:
        sign = "*" if key == "s1" else "+"
        print(f"|   {sign.join(i).ljust(10, ' ')}", end="")
    print()
    for index, i in enumerate(table):
        print(f" {sign.join(nf[index]).rjust(6, ' ')} ", end="")
        for j in i:
            if j:
                print('', end="")
            else:
                print(" ", end="")
        print()
    return mnf


def tabular_method(SNF):

    SNF_binary_list, karno_kart, mnf = [], [], []
    meanings = [
        [""],
        [""],
    ]
    for i in SNF:
        SNF_binary_list.append([str(int(not j.startswith("!"))) for j in i])
    for i in meanings:
        karno_kart.append([j.split() in SNF_binary_list for j in i])
    print("      |  00  |  01  |  11  |  10  ")
    for index, i in enumerate(karno_kart):
        print(f"  {index}   ", end="")
        for j in i:
            print(f"|  {int(j)}   ", end="")
        print()
    if karno_kart[0].count(True) % 2 == 1:
        for i in range(len(karno_kart[0])):
            verifiable_column = [j[i] for j in karno_kart]
            if all(verifiable_column):
                for index, j in enumerate(SNF_binary_list):
                    if j == meanings[0][i].split():
                        mnf.append(SNF[index][1:])
                        for k in karno_kart:
                            k[i] = False
    for index, karno_kart_string in enumerate(karno_kart):
        for iterator in range(len(karno_kart_string)):
            for iterator_for_comparison in range(iterator + 1, len(karno_kart_string)):
                if karno_kart_string[iterator] and karno_kart_string[iterator_for_comparison]:
                    check = meanings[index][iterator].split()[:-1]
                    for index_, SNF_bin_item in enumerate(SNF_binary_list):
                        if SNF_bin_item[:-1] == check:
                            mnf.append(SNF[index_][:-1])
                            karno_kart_string[iterator] = karno_kart_string[iterator_for_comparison] = False
                            break
    return mnf


def check(checked_function, key=None):
    checked_function = deepcopy(checked_function)
    test_1 = checked_function.count("(") == checked_function.count(")")
    test_3 = checked_function.count("a") == checked_function.count("b") == checked_function.count("c")
    if key == "1":
        checked_function = [i.split("*") for i in checked_function.split(" + ")]
    elif key == "2":
        checked_function = [i.split("+") for i in checked_function[1:-1].split(") * (")]
    for i in checked_function:
        test_2 = len(i) == 3
        if not test_2:
            break
    test_4 = type(checked_function) == str
    if key == "1":
        test_5 = checked_function.count("a") - checked_function.count(" + ") == 1
    elif key == "2":
        test_5 = checked_function.count("a") - checked_function.count(" * ") == 1

    return all([test_1, test_2, test_3])

def print_m1(m1):
    m1_output = ""
    for i in m1:
        m1_output += f"{'*'.join(i)}+"
    print(f"M1: {m1_output[:-1]}")


def print_m2(m2):
    m2_output = ""
    for i in m2:
        m2_output += f"({'+'.join(i)})*"
    print(f"M2: {m2_output[:-1]}")


def main():
    try:
        S1 = ()
        print(S1)
        S2 = ()
        print(S2)
        if check(S1, "1") and check(S2, "2"):
            S1 = [i.split("*") for i in S1.split(" + ")]
            S2 = [i.split("+") for i in S2[1:-1].split(") * (")]
            m1 = meth(1, "1")
            m2 = meth(2, "2")
            print_m1(m1)
            print_m2(m2)

            print("method:")
            m1 = calculation_tabular_method(1, S1, "s1")
            print_m1(m1)
            m2 = calculation_tabular_method(2, S2, "s2")
            print_m2(m2)

            print("method:")
            m1 = tabular_method(S1)
            print_m1(m1)
            m2 = tabular_method(S2)
            print_m2(m2)
        else:
            print("mistake(")
    except Exception:
        print("!!!something went wrong!!!")
def find_down(mas_term, key_term):
    smaller_term = []
    for i in range((len(mas_term))):
        if compare(key_term, mas_term[i]) == '>':
            smaller_term.append(mas_term[i])

    biggest = most_big(smaller_term)
    return biggest

def find(s):
    max_match = 0
    match_indices = []

    for i, item in enumerate():
        match_count = 0

        for j in range(len(s)):
            if s[j] == item[j]:
                match_count += 1

        if match_count > max_match:
            max_match = match_count
            match_indices = [i]
        elif match_count == max_match:
            match_indices.append(i)


def recurrent_sort(data, ascending=True):
    if len(data) <= 1:
        return data

    pivot = data[random.randint(0, len(data) - 1)]
    lesser = [x for x in data if x < pivot]
    equal = [x for x in data if x == pivot]
    greater = [x for x in data if x > pivot]

    if ascending:
        return recurrent_sort(lesser) + equal + recurrent_sort(greater)
    else:
        return recurrent_sort(greater) + equal + recurrent_sort(lesser)
def find_up(mas_term, key_term):
    bigger_term = []
    for i in range((len(mas_term))):
        if compare(key_term, mas_term[i]) == '<':
            bigger_term.append(mas_term[i])

    smallest = most_little(bigger_term)
    return smallest


standart_table = [[0 for i in range(size_of_table)] for j in range(size_of_table)]
diagonal_table = from_normal_to_diagonal(standart_table)
while True:
    operation = input(
        '\n 1 - add word \n 2 - sum \n 3 - read \n 4 - function f1(Берет два слова, выполняет побитовую операцию И между ними и добавляет результат в таблицы.) \n 5 - function f14(Берет два слова, выполняет логическую операцию НЕ-И между ними и добавляет результат в таблицы.) \n 6 - function f3( Берет одно слово и добавляет его в таблицы.) \n 7 - function f12(Берет одно слово, оставляет его без изменений и добавляет в таблицы.)\n' +
        ' 8 - nearest low\n 9 - nearest up \n 10 - show tables \n')
    match (operation):
        case '1':
            term = input('Enter a word: ')
            term = term.replace(' ', '')
            term = [int(term[i]) for i in range(size_of_table)]
            add_new_term(term, standart_table, diagonal_table)
        case '2':
            V = input('Enter V: ')
            V = V.replace(' ', '')
            V = [int(V[i]) for i in range(len(V))]
            sum(diagonal_table, standart_table, V)
        case '3':
            index = int(input('Enter column index: '))
            print(show(diagonal_table, index))
        case '4':
            first_term_index = int(input('Enter 1st word index: '))
            second_term_index = int(input('Enter 2nd word index: '))
            first_term = show(diagonal_table, first_term_index)
            second_term = show(diagonal_table, second_term_index)
            f1(first_term, second_term, standart_table, diagonal_table)
        case '5':
            first_term_index = int(input('Enter 1st word index: '))
            second_term_index = int(input('Enter 2nd word index: '))
            first_term = show(diagonal_table, first_term_index)
            second_term = show(diagonal_table, second_term_index)
            f14(first_term, second_term, standart_table, diagonal_table)
        case '6':
            first_term_index = int(input('Enter 1st word index: '))
            second_term_index = int(input('Enter 2nd word index: '))
            first_term = show(diagonal_table, first_term_index)
            f3(first_term, standart_table, diagonal_table)
        case '7':
            first_term_index = int(input('Enter 1st word index: '))
            second_term_index = int(input('Enter 2nd word index: '))
            first_term = show(diagonal_table, first_term_index)
            f12(first_term, standart_table, diagonal_table)
        case '8':
            term = input('Enter a word: ')
            term = term.replace(' ', '')
            term = [int(term[i]) for i in range(size_of_table)]
            smallest = find_down(standart_table, term)
            if smallest == None:
                print('No word smaller!')
            else:
                for term in smallest:
                    print(term)
        case '9':
            term = input('Enter a word: ')
            term = term.replace(' ', '')
            term = [int(term[i]) for i in range(size_of_table)]
            biggest = find_up(standart_table, term)
            if biggest == None:
                print('No word bigger!')
            else:
                for term in biggest:
                    print(term)
        case '10':
            print('\nNormal table:')
            for i in range(size_of_table):
                print(standart_table[i])
            print('\nDiagonal table:')
            for i in range(size_of_table):
                print(diagonal_table[i])
