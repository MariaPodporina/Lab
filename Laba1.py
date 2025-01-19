with open('laba1.txt', 'r') as f:
    sym=f.readline().split()
    ''' Открытие файла и считывание значений '''
r=[int(i) for i in sym]
n=r[0]
s=r[-1]
r.pop(0)
r.pop(-1)
''' Присвоение значений переменным '''

def combinations(numbers: list[int],goal:int,index:int,summ:int,symbols:str):
    ''' Функция исследует все возможные комбинации чисел с операциями сложения и вычитания '''
    if index==len(numbers):
        if summ==goal:
            return symbols+'='+str(goal)
        return None
    plus=combinations(numbers,goal, index+1, summ + numbers[index], symbols+'+'+str(numbers[index]))
    if plus:
        return plus
    minus=combinations(numbers, goal, index+1, summ-numbers[index], symbols+'-'+str(numbers[index]))
    if minus:
        return minus
    return None

o=combinations(r,s,0,0,'')
''' Приводит в действие функцию '''
if o:
    if o[0]=='+':
        ''' Записывает решение в файл '''
        with open('laba1.txt', 'a') as f:
            f.write(o[1:]+'\n')
    else:
        with open('laba1.txt', 'a') as f:
            f.write(o+'\n')
else:
    with open('laba1.txt', 'a') as f:
        f.write('no solution' + '\n')