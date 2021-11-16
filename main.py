import requests
import re
from bs4 import BeautifulSoup as bs
import zipfile
import os
import hashlib
from pprint import pprint


# Задание №1
# директория извлечения файлов архива
directory_to_extract_to = 'for_unzip'
# путь к архиву
arch_file = 'tiff-4.2.0_lab1.zip'

# Создать новую директорию, в которую будет распакован архив
try:
    os.mkdir(directory_to_extract_to)
except FileExistsError:
    pass

# С помощью модуля zipfile извлечь содержимое архива в созданную директорию
with zipfile.ZipFile(arch_file) as zip_file:
    zip_file.extractall(directory_to_extract_to)

# # Задание №2.1
# Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to.
# Сохранить полученный список в txt_files
txt_files = []

for r, _, f in os.walk(directory_to_extract_to):

    for file in f:
        file_path = f'{r}\{file}'

        if file_path.endswith('.txt'):
            txt_files.append(file_path)

# Задание №2.2
# Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.
for file_path in txt_files:

    with open(file_path, 'rb') as file:
        hash_ = hashlib.md5(file.read()).hexdigest()
       # print(hash_)


# Задание №3
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла

# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to
hash_list = {}
for r, _, f in os.walk(directory_to_extract_to):
    for file_name in f:
        target_file = f'{r}\{file_name}'

        with open(target_file, 'rb') as file:
            target_file_data = file.read()
            hash_ = hashlib.md5(target_file_data).hexdigest()

        if hash_ == target_hash:
            break
    if hash_ == target_hash:
        break

# Отобразить полный путь к искомому файлу и его содержимое на экране
    #print(target_file)
    #print(target_file_data)


# Задание №4
# Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений. Возможно выполнение этого задания иным способом (например, с помощью сторонних модулей).
response = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

# парсим строки таблицы
soup = bs(response.content, 'html.parser').html.body
rows = soup.select("[class^=Table-module_row]")#CSS селектор

# парсим заголовки
headers = [header.text for header in rows[0].select('[class^=Table-module_cell]')]

for row in rows[1:-1]:
    # достаём значения, чистим данные
    row_values = [row_value.text.split('(')[0]
                                .replace("\xa0", '')
                                .replace("*", '')
                                .replace('_', '-1')
                                .strip()
                  for row_value in row.select('[class^=Table-module_cell]')]
    # отрезаем первую часть названия
    row_values[0] = " ".join(row_values[0].split(' ')[2:])

    # Запись извлеченных данных в словарь
    result_dct[row_values[0]] = {}
    result_dct[row_values[0]][headers[1]] = int(row_values[1])
    result_dct[row_values[0]][headers[2]] = int(row_values[2])
    result_dct[row_values[0]][headers[3]] = int(row_values[3])
    result_dct[row_values[0]][headers[4]] = int(row_values[4])
    pprint(result_dct)

# Задание №5
# Запись данных из полученного словаря в файл
with open('data.csv', 'w') as file:
    # пишем заголовки
    file.write(f'Страна,{",".join(headers[1:])}\n')
    # пишем строки
    for key in result_dct.keys():
        file.write(f'{key},'
                   f'{result_dct[key][headers[1]]},'
                   f'{result_dct[key][headers[2]]},'
                   f'{result_dct[key][headers[3]]},'
                   f'{result_dct[key][headers[4]]}\n')

# Задание №6
# Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
print(f'{headers[1]}: {result_dct[target_country][headers[1]]}\n'
      f'{headers[2]}: {result_dct[target_country][headers[2]]}\n'
      f'{headers[3]}: {result_dct[target_country][headers[3]]}\n'
      f'{headers[4]}: {result_dct[target_country][headers[4]]}')
