'''
Este programa toma un texto en inglés (open, read) y:
a) Lo separa por palabras (split)
b) Le elimina los sufijos y signos de puntuación y lo pone todo en minúsculas (normalización)
c) Elimina las palabras de la lista de stopwords (con la función remove_stopwords)
d) Cuenta la frecuencia de cada palabra en un diccionario (count_words, word_probability y )

Las funciones remove_punctuation y remove_apostrophe son funciones de práctica
previas a remove_suffixes. 
'''

import csv

alice_read = open("alice.txt", "r", encoding="utf-8-sig")
alice_text = alice_read.read()
alice_read.close()

english_read = open("english.txt", "r", encoding="utf-8-sig")
english_stopwords = english_read.read()
english_read.close()

# Sustituyo guiones por espacios para que separe palabras compuestas
alice_text = alice_text.replace("—", " ").split()
# Sustituyo el apostrofe por el apostrofe específico que usa el texto de Alice para que se filtren correctamente las stopwords
english_stopwords = english_stopwords.replace("'", "’").split()


stopwords_set = set(english_stopwords)


def remove_stopwords(string_list, set_stopwords):
    # return filter(lambda word: word not in set_stopwords, string_list) --> Ez solution
    text_no_stopwords = []
    for word in string_list:
        if word not in set_stopwords:
            text_no_stopwords.append(word)
    return text_no_stopwords


def remove_punctuation(string):
    symbols = [".", ",", ";"]
    new_string = ""
    if symbols in string:
        for letter in string:
            if letter not in symbols:
                new_string += letter
    else:
        new_string = string
    return new_string


def remove_apostrophe(string):
    apostrophe = "'s"
    new_string = ""
    if apostrophe in string:
        new_string = string.replace(apostrophe, "")
    else:
        new_string = string
    return new_string


'''
# Esta sería mi función si también considerase el caso de contracciones
tales como '/'ts/'nt/'m/'re/'d/'ll
def remove_apostrophe(string):
    apostrophe_variations = ["'s", "'ts", "'nt", "'m", "'re", "'d", "'ll", "'"]
    new_string = ""
    if apostrophe_variations[-1] in string: # Si no tiene apóstrofe simple, no tiene ninguno
        for variation in apostrophe_variations:
            if variation in string:
                new_string = string.replace(variation, "")
    else:
        new_string = string
    return new_string
'''


def remove_suffix(string):
    suffixes = ["!", "'", ",", ";", ".", "?", "”", "—",
                "_", "(", ")", "’", "“", ":", "‘", "[", "]"]
    apostrophe_s = "’s"
    new_string = ""
    # Este condicional quita sólo "'s" y deja los "'" que estén solos
    # Si lo pusiera después del for, el for me quitaría todos los "'" y
    # no habría "'s" posible, y se me colarían en la palabra eses que no quiero
    if apostrophe_s in string:
        string = string.replace(apostrophe_s, "")
    for letter in string:
        if letter not in suffixes:
            new_string += letter
    return new_string


def normalize(string_list):
    new_list = list(
        map(lambda string: remove_suffix(string).lower(), string_list))
    new_list = filter(lambda string: string != "", new_list)
    return new_list


def count_words(string_list):
    # Esto también podría resolverse con una dict comprehension:
    #dict = {string:string_list.count(string) for string in string_list}
    # Que en 1 línea itera por la string_list y cuenta todas las ocurrencias de cada string
    dict = {}
    for string in string_list:
        if string in dict:
            dict[string] += 1
        else:
            dict[string] = 1
    return dict


def word_probability(dict, words_len):
    new_dict = {}
    for key in dict.keys():
        new_dict[key] = dict[key] / words_len
    return new_dict
    # Se podría hacer con un map, pero le veo poco sentido. Habría que pasarle
    # al map los dict.values() para que devuelva una lista con el cálculo de los values
    # y luego tendría que iterar con un bucle for por todo el dict
    # para asignar a cada clave el correspondiente valor ya calculado
    # así que es mejor hacer un solo bucle donde hago todo de una vez
    # (el cálculo y la asignación)


def display_histogram(dict):
    max_blocks_percentage = 50
    max_space_word = 0
    full_block = "▰ "
    empty_block = "▱ "

    # Guardo la longitud de la palabra más larga para poder espaciar correctamente la palabra de la representación
    for key in dict.keys():
        if len(key) > max_space_word:
            max_space_word = len(key)


    full_text = ""
    for key, value in dict.items():
        percentage = round(value * max_blocks_percentage)

        new_line = key + " " * (max_space_word + 1 - len(key)) + full_block * percentage + empty_block * (max_blocks_percentage - percentage) + " (" + str(round(value * 100, 3)) + "%)"
        full_text += f"\n{new_line}"

        print(new_line)
    
    # Devuelve el texto completo para poder más tarde guardarlo en un archivo txt
    return(full_text)
            

# Llamada a todas las funciones para cumplir nuestro objetivo:


# Primero lo normalizo, es decir, le quito signos de puntuación y sufijos y pongo en minúscula
alice_text_normalized = normalize(alice_text)

# Ahora le quito las stopwords
alice_text_no_swords = remove_stopwords(alice_text_normalized, stopwords_set)

# Ahora cuento las ocurrencias de cada palabra
alice_text_wcount = count_words(alice_text_no_swords)

# Ahora calculo la probabilidad de ocurrencia en porcentaje
alice_text_wprob = word_probability(
    alice_text_wcount, len(alice_text_no_swords))

# Ahora imprimo en barras de progreso la probabilidad en base 50 de cada palabra
#alice_text_histogram = display_histogram(alice_text_wprob)

'''
Aunque no lo pide el ejercicio, muestro los porcentajes de aparición de cada palabra
ordenado de menos común a más común.

En conclusión, las palabras más frecuentes son: alice, queen, time, king, turtle, mock, 
hatter, gryphon, head, voice... 
'''

# Ordena un diccionario en función de sus valores
def sort_percentages(dict):
    sorted_dict = {}
    sorted_keys = sorted(dict, key=dict.get)

    for k in sorted_keys:
        sorted_dict[k] = dict[k]
    return sorted_dict


def display_sort_percentages(dict):
    global alice_text_no_swords
    max_space_word = 0

    for key in dict.keys():
        if len(key) > max_space_word:
            max_space_word = len(key)

    full_text = ""
    for key in dict.keys():
        spacing = " " * (max_space_word + 1 - len(key))
        new_line = f"{key}: {spacing} {round(dict[key] / len(alice_text_no_swords) * 100, 4)}% \t\t {dict[key]} / {len(alice_text_no_swords)}"
        full_text += f"{new_line}\n"
        print(new_line)

    # Devuelve el texto completo para poder más tarde guardarlo en un archivo txt
    return full_text



order_by_percentage = sort_percentages(alice_text_wcount)
# display_sort_percentages(order_by_percentage)

# Histograma sorteado
#alice_text_wprob = word_probability(order_by_percentage, len(alice_text_no_swords))
#alice_text_histogram = display_histogram(alice_text_wprob)

'''
El siguiente código funciona para extraer el diccionario a un archivo CSV y poder
poner en práctica lo que aprendí en el workshop de Data Analysis de Le Wagon
'''

# Tengo que transformar el diccionario en una lista de diccionarios donde la clave y el valor están por separado
column_names = ["Word", "Count", "Length"]
dict_list = []
for key, value in alice_text_wcount.items():
    dict_list.append({"Word": key, "Count": value, "Length": len(key)})

with open('alicia_tabla.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=column_names)
    writer.writeheader()
    writer.writerows(dict_list)

# Permite guardar el output de las funciones en un txt para poder leerlo más comodamente que en la consola, ya que si el output es muy largo
# a veces la consola lo corta
def save_to_file(text, name):
    text_write = open(f"outputs/{name}.txt", "w", encoding="utf-8-sig")
    text_write.write(text)
    text_write.close()

    print(f"\nYou can check the full output at outputs/{name}.txt")


# Permite elegir la forma de mostrar los datos
while True:
    response = input("\nChoose between normal histogram (1) and sorted histogram (2) or just percentages (3) ")
    if (response == "1"):
        alice_text_histogram = display_histogram(alice_text_wprob)

        save_to_file(alice_text_histogram, "histogram")
    elif (response == "2"):
        alice_text_wprob = word_probability(order_by_percentage, len(alice_text_no_swords))
        alice_text_histogram = display_histogram(alice_text_wprob)

        save_to_file(alice_text_histogram, "histogram_sorted")
    elif (response == "3"):
        alice_text_percentages = display_sort_percentages(order_by_percentage)

        save_to_file(alice_text_percentages, "percentages_sorted")
    else:
        print("Please, choose between 1, 2 and 3")
