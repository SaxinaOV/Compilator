from random import choice, random

type_ = 1
adjectives = ["красивый", "большой", "маленький", "весёлый", "умный", "интересный", "важный"]
verbs = ["ходил", "читал", "ел", "покупал", "делал", "думал", "ждал", "смотрел", "рисовал", "видел", "писал", "брал"]
nouns = ["мальчик", "учитель", "ворон", "карась", "мужчина", "школьник", "отец", "слон"]
where = ["в парке", "в магазине", "дома", "на улице", "в школе", "на работе"]
when = ["в субботу", "раньше", "в выходные", "вечером", "в понедельник", "вчера", "утром", "ночью"]
nouns2 = ["журнал", "фильм", "обед", "проект", "велосипед", "портрет", "билет"]
Q = ["когда", "зачем", "почему"]
s = []
error = False
first_word = True
new_c = ''
adv_count = 0
attr2_count = 0
max_adv_count = 2
max_attr2_count = 3

def check_int(n, bot=0, top=10000000):
    n = n.strip()
    while not n.isdigit() or int(n) > top or int(n) < bot:
        print('Неверный ввод.')
        n = input()
    return int(n)

class Node:
    def __init__(self, v):
        self.value = v
        self.children = []

    def addChild(self, child):
        self.children.append(child)

def read(c):
    global s, error, first_word
    if type_ == 0 and error == False:
        try:
            if s[0] == c :
                s = s[1:]
                if first_word and c[0] != c[0].upper():
                    print("\nошибка: вместо '{}' ожидалось '{}'".format(c, c[0].upper()+c[1:]))
                    error = True
                    return None
            else:
                print("\nошибка: вместо '{}' ожидалось '{}'".format(s[0], c))
                error = True
                return None
        except:
            error = True
            return None
    else:
        s.append(c)
    return True
        
def Sentence():
    global error, new_c, first_word, adv_count, attr2_count, s
    error = False
    first_word = True
    adv_count = attr2_count = 0
    res = Node("Sentence")
    if type_ == 1:
        c = choice(adjectives + nouns + Q)
        new_c = c
    else: 
        c = s[0]
    if c.lower() in adjectives + nouns:
        res.addChild(Subj())
        res.addChild(Pred())
        res.addChild(Adv())
        res.addChild('.')
        n = read('.')
        if n == 0:
            print("\nошибка: вместо '{}' ожидалось '.''".format(c))
    elif c.lower() in Q:
        res.addChild(Quest())
        res.addChild(Subj())
        res.addChild(Pred())
        res.addChild('?')
        n = read('?')
        if n == 0:
            print("\nошибка: вместо '{}' ожидалось '?''".format(c))
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, adjectives + nouns + Q))
        error = True
    if type_ == 0:
        if error == True or s:
            return None
    return res

def Subj():
    global error, new_c
    res = Node("Subj")
    if type_ == 1:
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in adjectives:
        res.addChild(Attr1())
        new_c = choice(nouns)
        res.addChild(Noun())
        res.addChild(Attr2())
    elif c.lower() in nouns:
        res.addChild(Noun())
        res.addChild(Attr2())
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, adjectives + nouns))
        error = True
    return res  

def Pred():
    global error, new_c
    res = Node("Pred")
    if type_ == 1:
        c = choice(verbs)
        new_c = c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in verbs:
        res.addChild(Verb())
        res.addChild(WWW())    
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, verbs))
        error = True
    return res   

def Adv():
    global error, new_c, adv_count, max_adv_count
    res = Node("Adv")
    if type_ == 1:
        if adv_count < max_adv_count:
            r = random()
            if r > 0.4:
                c = choice((", когда", ", пока"))
                adv_count += 1
            else:
                c = ""
        else:
            c = ""
        new_c = c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c == ", когда" or c ==  ", пока":
        res.addChild(c)
        read(c)
        new_c = choice(nouns+adjectives)
        res.addChild(Subj())
        res.addChild(Pred()) 
        res.addChild(Adv()) 
    return res  

def Attr1():
    global error, new_c
    res = Node("Attr1")
    if type_ == 1:
        '''
        r = random()
        if r > 0.1:
            new_c = ""
        else:
            n = new_c
            while n == new_c:
                n = choice(adjectives)
            new_c = n
        '''
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in adjectives:
        res.addChild(Adj())  
        res.addChild(Attr1())  
    elif c == "":
        return res  
    return res   

def Noun():
    global error, new_c, first_word, attr2_count, max_attr2_count
    res = Node("Noun")
    if type_ == 1:
        c = new_c
        if first_word:
            c = c[0].upper() + c[1:]
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in nouns:
        read(c)
        if first_word:
            first_word = False
        res.addChild(c) 
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, nouns))
        error = True
    if type_ == 1:
        if attr2_count < max_attr2_count:
            r = random()
            if r < 0.3:
                new_c = ", который"
                attr2_count += 1
            else:
                new_c = choice(verbs)
            c = new_c
        else:
           c = new_c = choice(verbs)
    return res   

def Attr2():
    global error, new_c, attr2_count, max_attr2_count
    res = Node("Attr2")
    if type_ == 1:
        '''
        if attr2_count < max_attr2_count:
            r = random()
            if r > 0.1:
                c = ", который"
                attr2_count += 1
            else:
                c = ""
            new_c = c
        else:
           c = new_c = "" 
        '''
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c == ", который":
        res.addChild(c) 
        read(c)
        res.addChild(Pred()) 
        res.addChild(',') 
        read(',')
    if type_ == 1:
        new_c = choice(verbs)
    return res  

def Attr3():
    global error, new_c, attr2_count, max_attr2_count
    res = Node("Attr3")
    if type_ == 1:
        if attr2_count < max_attr2_count:
            r = random()
            if r > 0.1:
                c = ", который"
                attr2_count += 1
            else:
                c = ""
            new_c = c
        else:
           c = new_c = "" 
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c == ", который":
        res.addChild(c) 
        read(c)
        res.addChild(Pred()) 
    return res  

def Verb():
    global error, new_c
    res = Node("Verb")
    if type_ == 1:
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in verbs:
        res.addChild(c)
        read(c)
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, verbs))
        error = True
    if type_ == 1:
        new_c = choice(adjectives + nouns2 + where + when + [""])
    return res

def WWW():
    global error, new_c
    res = Node("WWW")
    if type_ == 1:
        #new_c = choice(adjectives + nouns2 + where + when + [""])
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in nouns2 + adjectives:
        res.addChild(What())
    elif c.lower() in where:
        res.addChild(Where())
    elif c.lower() in when:
        res.addChild(When())
    return res

def Adj():
    global error, new_c, first_word
    res = Node("Adj")
    if type_ == 1:
        c = new_c
        if first_word:
            c = c[0].upper() + c[1:]
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in adjectives:
        res.addChild(c)
        if first_word:
            first_word = False
        read(c)
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, adjectives))
        error = True
    if type_ == 1:
        r = random()
        if r > 0.1:
            new_c = ""
        else:
            n = new_c
            while n == new_c:
                n = choice(adjectives)
            new_c = n
    return res

def What():
    global error, new_c
    res = Node("What")
    if type_ == 1:
        c = choice(adjectives + nouns2)
        new_c = c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c in adjectives:
        res.addChild(Attr1())
        new_c = choice(nouns2)
        res.addChild(Noun2())
        res.addChild(Attr3())
    elif c in nouns2:
        res.addChild(Noun2())
        res.addChild(Attr3())
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, adjectives + nouns2))
        error = True
    return res

def Where():
    global error, new_c
    res = Node("Where")
    if type_ == 1:
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c in where:
        res.addChild(c)
        read(c)
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, where))
        error = True
    return res

def When():
    global error, new_c
    res = Node("When")
    if type_ == 1:
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c in when:
        res.addChild(c)
        read(c)
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, when))
        error = True
    return res

def Noun2():
    global error, new_c
    res = Node("Noun2")
    if type_ == 1:
        c = new_c
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c in nouns2:
        res.addChild(c)
        read(c)
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, nouns2))
        error = True
    return res

def Quest():
    global error, new_c, first_word
    res = Node("Quest")
    if type_ == 1:
        c = new_c
        if first_word:
            c = c[0].upper() + c[1:]
    else: 
        try:
            c = s[0]
        except:
            c = ""
    if c.lower() in Q:
        read(c)
        if first_word:
            first_word = False
        res.addChild(c)
    else:
        print("\nошибка: вместо '{}' ожидалось слово из {}".format(c, Q))
        error = True
    if type_ == 1:
        new_c = choice(adjectives+nouns)
    return res

def parse(s):
    if len(s)>1:
        i = 0
        while i < len(s):
            if i != len(s)-1: 
                if s[i][-1] == ',':
                    if "который" in s[i+1] or "когда" in s[i+1] or "пока" in s[i+1]:
                        s[i] = s[i][:-1]
                        s[i+1] = ', ' + s[i+1]
                    else:
                        s.insert(i+1, ',')
                        s[i] = s[i][:-1]
                        i += 1
                if 'в' == s[i] or 'на' == s[i]:
                    s[i+1] = s[i] + ' ' + s[i+1] 
                    s.pop(i)
                    i -= 1
            if s[i][-1] == '?':
                s[i] = s[i][:-1]
                s.append('?')
                break
            if s[i][-1] == '.':
                s[i] = s[i][:-1]
                s.append('.')
                break
            i += 1
    return s

def tree_to_sentence(t, s=""):
    if isinstance(t, Node):
       for child in t.children:
            s = tree_to_sentence(child, s)
    else:
        if t != None:
            if t[0] != ',' and t[0] != '?' and t[0] != '.':
                s += ' '
            s += t
    return s
    



while(True):
    print("1. Проверка предложения\n2. Генерация предложения\n")
    n = check_int(input(), 1, 2)
    if n == 1:
        type_ = 0
        print("Введите предложение")
        st = input()
        if st == '':
            s_list = st.split(' ')
            s = s_list
            s = parse(s)
            res = Sentence()
            if res != None:
                print("\nПредложение корректно\n")
            else:
                print("\nПредложение некорректно\n")
        else:
            s_list = st.split(' ')
            s = s_list
            s = parse(s)
            res = Sentence()
            if res != None:
                print("\nПредложение корректно\n")
            else:
                print("\nПредложение некорректно\n")
    elif n == 2:
        type_ = 1
        res = Sentence()
        sent = tree_to_sentence(res, "")[1:] 
        print(sent+'\n')
        '''
        type_ = 0
        s_list = sent.split(' ')
        s = s_list
        s = parse(s)
        res = Sentence()
        if res != None:
            print("Предложение корректно\n")
        else:
            print("\nПредложение некорректно\n")
        '''
    first_word = True
input()
