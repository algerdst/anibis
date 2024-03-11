with open('1.txt', 'r', encoding='utf-8') as file:
    a=[i.replace('\n','') for i in file if i.startswith('http')]
    print(len(a))