import datetime as dt
import pymongo
import re

client = pymongo.MongoClient('mongodb://localhost:27017/')
DB = client['pessoal']
collection = DB['Comidas']
opc = { 'sugestões': 's', 'todos': 't', 'sair': 'r', 'adicionar comida': 'a', 'modificar data': 'm' }
sair = False

def atualizar():
    global TODOS, ULTIMOS
    TODOS = [ { item['nome']: item['data'] } for item in collection.find() ]
    ULTIMOS = { }
    for dic in TODOS:
        for key in dic:
            ULTIMOS[dic[key][-1]] = key

def printer(decresc=True):
    if decresc:
        SORTED = { item: ULTIMOS[item] for item in sorted(ULTIMOS, reverse=True) }
    else:
        SORTED = { item: ULTIMOS[item] for item in sorted(ULTIMOS) if item < (dt.datetime.now() - dt.timedelta(days=30)) }

    print()
    print('ID'.rjust(3), 'COMIDA'.rjust(32), 'ÚLTIMA VEZ'.rjust(12))
    print('-' * 59)
    print()
    for num, i in enumerate(SORTED):
        line = str(num).rjust(3) + SORTED[i].rjust(32, '.') + i.strftime('%d/%m/%Y').rjust(14) + '  ' + str((dt.datetime.now() - i).days).ljust(2) + ' dias'
        print(line)
    print('\x1b[0;30;47m', str(len(SORTED)).rjust(2), 'total '.rjust(34), '\x1b[0m'.rjust(24))
    return SORTED

def mod(dic):
    ask = int(input('#: '.rjust(3)))
    if ask > len(dic):
        print('Número maior que o número de comidas')
    else:
        date = input('?: '.rjust(3))
        for num, i in enumerate(dic):
            if num == ask:
                nome = dic[i]

        if date == 'h':
            date = dt.datetime.today()
        else:
            if len(set(re.findall('([^0-9])', date))) > 1:
                print('Uso de separadores inconsistente')
            else:
                sep = re.findall('([^0-9])', date)[0]
                size = len(date.split(sep))
                fields = date.split(sep)
                if size == 2:
                    date = dt.datetime(dt.date.today().year, int(fields[-1]), int(fields[-2]))
                elif size == 3:
                    date = dt.datetime(int(fields[-1]), int(fields[-2]), int(fields[-3]))

        for dic in TODOS:
            for i in dic:
                if i == nome:
                    dic[i].append(date)
                    documento = { i: dic[i] }
                    print('Base de dados atualizada\n', documento)
                    collection.update_one( { "nome": i }, { "$set": { "data": dic[i] } } )
    atualizar()
    return documento

def addFood(comida=False):
    if not comida:
        reg = input('Adicione um dicionário da seguinte forma:\n"caruru" , "17/05/2019"\n')
        reg = reg.split(',')
    else:
#        print(comida)
        if ',' in comida:
            reg  = comida.split(',')
        else:
            reg = list()
            reg.append(comida)

#    print(reg)

    if isinstance(reg, list):
        if len(reg) == 1:
            data = dt.datetime.utcnow()
            reg.append(data)
            reg.append('')
        else:
            data = re.findall('[0-9]+', reg[1])
            reg[1] = dt.datetime(int(data[-1]), int(data[-2]), int(data[-3]))
            if len(reg) < 3:
                reg.append('')

        print(reg)
        collection.insert_one({ "nome": reg[0], "data": [reg[1]], "comentário": reg[2] })
        print('"%s" adicionado!' % reg[0])
    else:
        print('Registro adicionado não tem a forma de uma lista')

def handler():
    global sair
    for item in opc:
        print(opc[item].upper(), item, sep=': ')

    while not sair:
        inp = input('\n :').lower()
        if inp not in opc.values():
            print('Opção não disponível')
        elif inp == 's':
            printer(False)
        elif inp == 't':
            printer(True)
        elif inp == 'm':
            dic = printer(True)
            mod(dic)
        elif inp == 'a':
            addFood()
        elif inp == 'r':
            sair = True

atualizar()
handler()

