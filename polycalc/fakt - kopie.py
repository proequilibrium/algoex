# Python program to find the factorial of a number provided by the user.
import sys
#from datetime import datetime, timedelta
import cProfile
import pstats
import time
# change the value for a different result
num = 1500
t=time.time()
# uncomment to take input from the user
#num = int(input("Enter a number: "))


# check if the number is negative, positive or zero
def fact(num):
        factorial = 1
        if num < 0:
           print("Sorry, factorial does not exist for negative numbers")
        elif num == 0:
           print("The factorial of 0 is 1")
        else:
           for i in range(1,num + 1):
               factorial = factorial*i
           print("The factorial of",num,"is",factorial)

        print(time.time()-t)
        print(sys.getsizeof(factorial))

cProfile.run('fact(10000)', 'profile-faktorial')
p = pstats.Stats('profile-faktorial')
p.sort_stats('time').print_stats(10)
