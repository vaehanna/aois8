size_of_table = 16
FOUR = 4
A_start = 3
B_start = 7
S_start = 11


def from_normal_to_diagonal(table):
    newtable = [[0 for m in range(size_of_table)] for n in range(size_of_table)]
    for j in range(size_of_table):
        column = [table[i][j] for i in range(size_of_table)]
        for i in range(size_of_table):
            string_index = shift_index(i, j)
            newtable[string_index][j] = column[i]
    return newtable


def shift_index(index, shift_number):
    newindex = shift_number + index
    if newindex >= size_of_table:
        return newindex - size_of_table
    else:
        return newindex


def add_new_word(word, standart_table, diagonal_table):
    empty_index = 0
    while standart_table[empty_index] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        empty_index += 1
    standart_table[empty_index] = [word[i] for i in range(size_of_table)]
    for j in range(size_of_table):
        string_index = shift_index(empty_index, j)
        diagonal_table[string_index][j] = word[j]


def read_column(table, index):
    return [table[shift_index(index, i)][i] for i in range(size_of_table)]


def sum(table, standart_table, V):
    for i in range(size_of_table):
        word = read_column(table, i)
        if [word[0], word[1], word[2]] == V:
            A, B = [], []
            S = [0, 0, 0, 0, 0]
            for j in range(FOUR):
                A.append(word[A_start + j])
                B.append(word[B_start + j])
            for j in range(FOUR):
                S[len(S) - j - 1] += A[len(A) - j - 1] + B[len(B) - j - 1]
                if S[len(S) - j - 1] >= 2:
                    S[len(S) - j - 1] -= 2
                    S[len(S) - j - 2] = 1
            for j in range(S_start, size_of_table):
                string_index = shift_index(i, j)
                table[string_index][j] = S[j - S_start]
            standart_table[i] = read_column(table, i)


def f1(first_word, second_word, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_word)):
        if first_word[i] == 1 and second_word[i] == 1:
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_word(rezult, standart_table, diagonal_table)


def f14(first_word, second_word, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_word)):
        if not (first_word[i] == 1 and second_word[i] == 1):
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_word(rezult, standart_table, diagonal_table)


def f3(first_word, standart_table, diagonal_table):
    add_new_word(first_word, standart_table, diagonal_table)


def f12(first_word, standart_table, diagonal_table):
    rezult = []
    for i in range(len(first_word)):
        if first_word[i] == 1:
            rezult.append(1)
        else:
            rezult.append(0)
    add_new_word(rezult, standart_table, diagonal_table)


def compare(first_word, second_word):
    g = 0
    l = 0

    word_first = [bool(first_word[i]) for i in range(len(first_word))]
    word_second = [bool(second_word[i]) for i in range(len(second_word))]

    for i in range(len(first_word)):
        g = g or (not (word_second[i]) and word_first[i] and not (l))
        l = l or (word_second[i] and not (word_first[i]) and not (g))

    if g == 0 and l == 0:
        return '='
    elif g == 1 and l == 0:
        return '>'
    else:
        return '<'


def most_big(mas_word):
    if mas_word == []:
        return None
    copy_mas = mas_word.copy()
    for i in range(len(copy_mas[0])):
        biggest_word = []
        for j in range(len(copy_mas)):
            if copy_mas[j][i] == 1:
                biggest_word.append(copy_mas[j])
        if biggest_word != []:
            copy_mas = biggest_word

    return copy_mas


def most_little(mas_word):
    if mas_word == []:
        return None
    copy_mas = mas_word.copy()
    for i in range(len(copy_mas[0])):
        smallest_word = []
        for j in range(len(copy_mas)):
            if copy_mas[j][i] == 0:
                smallest_word.append(copy_mas[j])
        if smallest_word != []:
            copy_mas = smallest_word

    return copy_mas


def find_down(mas_word, key_word):
    smaller_word = []
    for i in range((len(mas_word))):
        if compare(key_word, mas_word[i]) == '>':
            smaller_word.append(mas_word[i])

    biggest = most_big(smaller_word)
    return biggest


def find_up(mas_word, key_word):
    bigger_word = []
    for i in range((len(mas_word))):
        if compare(key_word, mas_word[i]) == '<':
            bigger_word.append(mas_word[i])

    smallest = most_little(bigger_word)
    return smallest


standart_table = [[0 for i in range(size_of_table)] for j in range(size_of_table)]
diagonal_table = from_normal_to_diagonal(standart_table)
while True:
    operation = input(
        '\n 1 - Добавить новое слово \n 2 - Сложение \n 3 - Чтение столбца \n 4 - Функция f1 \n 5 - Функция f14 \n 6 - Функция f3 \n 7 - Функция f12\n' +
        ' 8 - Поиск ближайшего снизу значения \n 9 - Поиск ближайшего сверху значения \n 10 - Показать таблицы \n')
    match (operation):
        case '1':
            word = input('Введите слово: ')
            word = word.replace(' ', '')
            word = [int(word[i]) for i in range(size_of_table)]
            add_new_word(word, standart_table, diagonal_table)
        case '2':
            V = input('Введите V: ')
            V = V.replace(' ', '')
            V = [int(V[i]) for i in range(len(V))]
            sum(diagonal_table, standart_table, V)
        case '3':
            index = int(input('Введите индекс столбца: '))
            print(read_column(diagonal_table, index))
        case '4':
            first_word_index = int(input('Введите индекс первого слова: '))
            second_word_index = int(input('Введите индекс второго слова: '))
            first_word = read_column(diagonal_table, first_word_index)
            second_word = read_column(diagonal_table, second_word_index)
            f1(first_word, second_word, standart_table, diagonal_table)
        case '5':
            first_word_index = int(input('Введите индекс первого слова: '))
            second_word_index = int(input('Введите индекс второго слова: '))
            first_word = read_column(diagonal_table, first_word_index)
            second_word = read_column(diagonal_table, second_word_index)
            f14(first_word, second_word, standart_table, diagonal_table)
        case '6':
            first_word_index = int(input('Введите индекс первого слова: '))
            second_word_index = int(input('Введите индекс второго слова: '))
            first_word = read_column(diagonal_table, first_word_index)
            f3(first_word, standart_table, diagonal_table)
        case '7':
            first_word_index = int(input('Введите индекс первого слова: '))
            second_word_index = int(input('Введите индекс второго слова: '))
            first_word = read_column(diagonal_table, first_word_index)
            f12(first_word, standart_table, diagonal_table)
        case '8':
            word = input('Введите свое слово: ')
            word = word.replace(' ', '')
            word = [int(word[i]) for i in range(size_of_table)]
            smallest = find_down(standart_table, word)
            if smallest == None:
                print('Нет слова меньше заданного!')
            else:
                for word in smallest:
                    print(word)
        case '9':
            word = input('Введите свое слово: ')
            word = word.replace(' ', '')
            word = [int(word[i]) for i in range(size_of_table)]
            biggest = find_up(standart_table, word)
            if biggest == None:
                print('Нет слова больше заданного!')
            else:
                for word in biggest:
                    print(word)
        case '10':
            print('\nОбычная таблица:')
            for i in range(size_of_table):
                print(standart_table[i])
            print('\nДиагональная таблица:')
            for i in range(size_of_table):
                print(diagonal_table[i])
