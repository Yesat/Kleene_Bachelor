from collections import deque
from to_infix import Calculator
import random
import time

#Current issue: So for a 10 state matrix, I'm currently getting about about 400k terms in M* without checkinf if the addition contains.
# 
# Adding the counter, you get a longer time of generation, but cut down the size to 87k. 
class RegLang(object):
    #ideas: 
    #for communtativity of addition, have it build as a set.
    #non set for multiplcation as it's not communative.
    def __init__(self,data,children):
        self.data = data
        self.children = children

    def add_child(self, node):
        self.children.append(node) 
    
    def get_children(self):
        return self.children

    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children


def unit():
    return RegLang("eps",[])
def zero():
    return RegLang("",[])
        
def multiply(el1, el2):
    if (el1.data == "" or el2.data == ""):
            return(zero())
    elif el1.data == "eps":
            return(el2)
    elif el2.data == "eps":
            return(el1) 
    else:
            c = RegLang("·", [el1, el2])
            return c

def add( el1,  el2):
    #potentially precalculate dft here
    if (el1.data == ''):#could use dft
        return(el2)
    elif el2.data == '':
        return(el1)
    elif isEqual(el1,el2): 
         return(el1)
    elif contains(el1,el2):
        return(el2)
    elif contains(el2,el1):
        return(el1)
    elif el1.data == "eps" and el2.data == "·":
        left = el2.children[0]
        right = el2.children[1]
        if right.data == "*":
            if isEqual(left,right.children[0]):
                return right
    else:
        c = RegLang("+", [el1,el2])
        return c

# def add_dft(el1,el2):
#     a = dft(el1)
#     b = dft(el2)
#     if (a == ['']):
#         return el2
#     elif (b == ['']):
#         return el1
#     elif isEqual_dft(a,b):
#         return el1
#     elif contains_dft(a,b):
#         return el2
#     elif contains_dft(b,a):
#         return el1
#     else:
#         c = RegLang("+", [el1,el2])
#         return c

def closure(el):
    if el.data=="":
        return unit()
    elif el.data == 'eps':
        return unit()
    else:
        return RegLang("*",[el])

#idea, make it as "Disjunction normal forms" addition of multiplciations. 

def dft(root):#Move to to_infix maybe.
    nodes = []
    stack = [root]
    traverse = []
    while stack:
            #Pop left
            cur_node = stack[0]
            stack = stack[1:]
            nodes.append(cur_node)
            for child in cur_node.get_rev_children():
                stack.insert(0,child)
                
    for node in nodes:
        traverse.append(node.data)
    return traverse

# def push(traverse,p)

def isEqual(el1,el2):
    if (el1.data == el2.data and el1.children == el2.children):
        return True
    elif (dft(el1) == dft(el2)):
        print('same thing')
        return True
    else:
        return False

def isEqual_dft(a,b):
    if(a==b):
        return True
    else:
        return False
        
def contains(el1, el2):
    small = dft(el1)
    big = dft(el2)
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return True
    return False

# def contains_dft(small,big)):
#     for i in xrange(len(big)-len(small)+1):
#         for j in xrange(len(small)):
#             if big[i+j] != small[j]:
#                 break
#         else:
#             return True
#     return False
    
def to_string(root):
      cal = Calculator()
      return cal.convert(dft(root))   

def mat_to_string(mat):
    size = len(mat[0])
    return [[to_string(mat[i][j]) for i in range(size)] for j in range(size)]

def operation_test():
    print('(a+b)')
    a = RegLang("a",[])
    b = RegLang("b",[])
    c = RegLang("c",[])
    d = RegLang("d",[])
    e = RegLang("e",[])

    o1 = add(a,b)
    o2 = multiply(c,d)
    o3 = closure(e)
    o4 = add(o2,o3)
    
    root = multiply(o1,o4)
    cal = Calculator()
    travers = dft(root)
    calc=cal.convert(travers)
    print(travers)
    print(calc)


def mat_test(size,alphabet):
    mat = gen_matrix(size,alphabet)
    start = time.perf_counter()
    matstar = wfk(mat,size)
    matstar_calc = time.perf_counter()-start
    print(matstar_calc)
    return(mat,matstar)

def wfk(mat,size):

    M_=[]
    s = range(size)
    M_.append(mat)


    for Z in s:
        M_.append([[None]*size]*size)
        for X in s:
            for Y in s:
                c = multiply(multiply(M_[Z][Y][Z],closure(M_[Z][Z][Z])),M_[Z][Z][Y])
                M_[Z+1][X][Y]=add(M_[Z][X][Y],c)

    #This is not working...
    result = M_[Z+1]

    for X in s:
        result[X][X] = add(M_[Z+1][X][X],unit())
    return result
 
def gen_matrix(size,alphabet):
    alphabet.append("")
    alphabet.append("eps")
    matrix = [[RegLang(random.choice(alphabet),[]) for i in range(size)] for i in range(size)]
    return matrix
        
