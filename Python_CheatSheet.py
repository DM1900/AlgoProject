# Comment
"""
https://docs.python.org/3.8/
"""

# numbers
a = 1
b = 2
a, b = 1, 2
c = a+b

# arithmetic 
100-(2+2-((3*7)/2**3))
5/2
9//2
5==8
5!=6
5>=3
"test"=="Test" 

# assignent operators
var = 10
var = var + 10
var += 10
var **= 2 # number to the power of x
# bitwise operators
a = 0b11110000 # binary
print(bin(a))
b = 0x4f5da # hex
print(bin(a) + "\n" + hex(b))
#operators
a, b, c = 6, 7, 13
(a<b) or (b>c) # or, only one needs to be true
(a<b) and (b<c) # and, both need to be true
not((a<b) and (b<c)) # not reverses the rule
a is be
a is not b
list = [123,665,'test',88701.66]
n1 = "test"
n1 in list

# strings
a = 'Text'
b = "text2"

print(a[0:5])
print(a[2:])

# lists
list1 = [123, 'testnumber 1', 67]
print(list1[2])
print(list1 + list2)

list1[0] = 1234

# tuples (an uneditabel list)
myTuple = (1562, 59894, 5156)
print(myTuple[2])
del myTuple

# dictionaries
dict = {'Name': 'Dan', 'Age': 20}
print(dict)
print(dict['Name'])

# while for loops
count = 10
while(count > 0):
    print("*" * count)
    count -= 1
x = 0
while(x < 9):
    print(x)
    x += 1

for i in range(1,10):
    if i == 8:
        print("stop!")
        break
    print(i)

a = 10
b = " "
c = "*"
for i in range(a):
    print((a*b)+(c))
    a -= 1
    c += "**"
a = 10
b = " "
c = "*"
while(a != 0):
    print((a*b)+(c))
    a -= 1
    c += "**"

# if elif else
L = 10
a = 5
for test in range(L): # then check the range against the value
    print(test, " is ", end='')
    if test > a:
        print("More")
    elif test == a:
        print("Equal")
    else:
        print("Less")


def nameOfFunction(a,b,c,d):
    return a + b + c + d
a,b,c,d = 5,8,-41,55
res = nameOfFunction(a,b,c,d)
print(res)

res + res



#Boolean Operators
#The not Operation
#Sometimes we want to know the opposite boolean value for something. To do this, we use the unary operators not:

not True
not False

#The or Operation
#The boolean or operator works the same way that the bitwise OR operator did if we are only considering one bit. The bit of 1 is equivalent to True and 0 is equivalent to False

True or True
True or False

False or False
False or True

#The and Operation
#The and operator is the opposite of or, and both of the operands need to be true.

True and True
True and False

False and False
False and True
