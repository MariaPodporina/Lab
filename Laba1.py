file=open('laba1.txt')
sym=file.readline().split()
r=[int(i) for i in sym] #числа
n=r[0] #колич. чисел
s=r[-1] #цель
r.pop(0)
r.pop(-1)
#print(r,n,s)

def F(numbers,goal,index=0,summ=0,symbols=''):
    if index==len(numbers):
        if summ==goal:
            return symbols+'='+str(goal)
        return None
    plus=F(numbers,goal, index+1, summ + numbers[index], symbols+'+'+str(numbers[index]))
    if plus:
        return plus
    minus=F(numbers, goal, index+1, summ-numbers[index], symbols+'-'+str(numbers[index]))
    if minus:
        return minus
    return None

o=F(r,s,0,0,'')
if o:
    if o[0]=='+':
        #print(o[1:])
        with open('laba1.txt', 'a') as file:
            file.write(o[1:]+'\n')
    else:
        #print(o)
        with open('laba1.txt', 'a') as file:
            file.write(o+'\n')
else:
    #print('no solution')
    with open('laba1.txt', 'a') as file:
        file.write('no solution' + '\n')
