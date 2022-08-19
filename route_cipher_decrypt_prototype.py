ciphertext = '16 12 8 4 0 1 5 9 13 17 18 14 10 6 2 3 7 11 15 19'
# разбить элементы на слова, не на буквы
cipherlist = list(ciphertext.split())
# инициализировать переменные
COLS = 4
ROWS = 5
key = '-1 2 -3 4'  # отрицательное число означает чтение ВВЕРХ столбца, а не ВНИЗ

translation_matrix = [None] * COLS
plaintext = ''
start = 0
stop = ROWS

# превратить key_int в список целых чисел
key_int = [int(i) for i in key.split()]
# превратить столбцы в элементы списка списков
for k in key_int:
    if k < 0: # читать в столбце снизу вверх
        col_items = cipherlist[start:stop]
    elif k > 0: # читать в столбце сверху вниз
        col_items = list((reversed(cipherlist[start:stop])))
    translation_matrix[abs(k) - 1] = col_items
    start += ROWS
    stop += ROWS

print(f'пшифротекст = {ciphertext}')
print(f'ппереводная матрица = {translation_matrix} ', sep='\n')
print(f'пдлина ключа = {len(key_int)}')

# обойти в цикле вложенные списки, передавая последний элемент
# в новый список

for i in range(ROWS):
    for col_items in translation_matrix:
        word = str(col_items.pop())
        plaintext += word + ' '
print(f'поткрытый текст = {plaintext}')


