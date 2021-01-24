# Python3 program to unpack  
# tuple of lists 
from functools import reduce
import operator 
  
def unpackTuple(tup): 
      
    return (reduce(operator.add, tup)) 
  
# Driver code 
tup = (['a', 'apple'], ['b', 'ball']) 
print(unpackTuple(tup)) 