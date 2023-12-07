# Берём список нецензурных слов из файла OBSCENE_LIST.txt
# Все нехорошие слова которые мы хотим, чтобы отсеивались, заливаем туда
# Каждое новое слово обязательно на новой строке!
f = open('OBSCENE_LIST.txt', 'r', encoding='utf8')
OBSCENES = tuple(f.read().lower().split("\n"))
f.close()


# делаем преобразование нецензурных слов в формате из "Дурак" в "Д****"
def search_obscene(str, tuple=OBSCENES):
    list_str = str.split()  # Строку разбиваем на список
    for obscene in tuple:  # Проходим по кортежу нехороших слов
        for i in range(len(list_str)):  # Проходим по списку слов нашего текста
            while list_str[i].lower().find(obscene) >= 0:  # Если нехорошее слово входит в элемент списка, идём в цикл
                a = list_str[i].lower().find(obscene)
                len_word = len(obscene)
                # Если после нехорошего слова нет больше символов, то сохраняем первую букву, остальное заменяем "*"
                if a+len_word > len(list_str[i]):
                    list_str[i] = list_str[i][:a+1] + "*" * (len_word-1)
                else:  # Иначе дописываем в конец ещё символы
                    list_str[i] = list_str[i][:a+1] + "*" * (len_word-1) + list_str[i][a + len_word:]
    return " ".join(list_str)  # Возвращаем список объединенный в единое предложение в формате текста


a = 'asdfasdfsd askd fh sdfjks fj hdfsj дурак авыол. Членпридурок! Шлюха!'
print(search_obscene(a))