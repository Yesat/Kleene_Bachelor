#Basic algebraic function just to simplify a few things.

def kS(a):
    return a+'*'

def prodExp(a,b):
    if (a=='0' or b=='0'):
        return '0'
    elif (a == 'eps'):
        return b
    elif (b == 'eps'):
        return a
    else:
        return a+b
#brackrts

def addExp(a,b):
    if (a == '0'):
        return b
    elif (b == '0'):
        return a
    else:
        return a+'+'+b


#Working on the regular language as string to do basic stuff.

def wfk(mat,size):

    M_=[]
    s = range(size)
    M_.append(mat)


    for Z in s:
        M_.append([[None]*size]*size)
        for X in s:
            for Y in s:
                c = prodExp(prodExp(M_[Z][Y][Z],kS(M_[Z][Z][Z])),M_[Z][Z][Y])
                M_[Z+1][X][Y]=addExp(M_[Z][X][Y],c)

    #This is not working...
    result = M_[Z+1]
    print(result)
    for X in s:
        result[X][X] = addExp(M_[Z+1][X][X],'esp') #This doesn't return the right matrix, need to check
        print(result[X][X])
    print(result)
    return result


#Testing
M=[['a','b'],['0','0']]
size = 2
result2 = wfk(M,size)

#X = [['a','0','b'],['a','b','0'],['0','0','a+b+c']]
#size = 3
#result3 = wfk(X,size)