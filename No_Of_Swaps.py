#importing required libraries
import numpy as np

#function to find number of swaps needed
''' Basically the idea is that, for every 1, the number of swaps needed will be equal to the number of zeros present to the right of it. 
For eg, if we consider an array, a = [0,1,0,1,0,1,0]
Here, for the last 1 present at the 6th position(index = 5), there is 1 zero to it's right and so we will have to do 1 swap to bring the 0 to the left. 
Now our array will be a = [0,1,0,1,0,0,1]
Now for the next 1, present at 4th location, number of zeros to it's right is 2, and so 2 swaps have to be done. This process can be continued to get the final array.
This is the logic used. We will add the number of zeros present to the right of every 1, to get the total number of swaps needed'''

def NSwaps(arr,n):
    #defining a new array NofZeros, to store the number of zeros present to the right of each 1
    NofZeros = np.zeros((n,))
    
    NofZeros[n-1] = 1 - arr[n-1]
    for i in range(n-2, -1, -1):
        NofZeros[i] = NofZeros[i+1]
        if arr[i] == 0:
            NofZeros[i] = NofZeros[i] + 1
    swaps = 0
    for j in range(n):
        if arr[j] == 1:
            swaps = swaps + NofZeros[j]

    return swaps

n = input("ENTER THE LENGTH OF YOUR ARRAY: ")
n = int(n)
str_list = input("INPUT YOUR ARRAY SEPARATED BY SPACE: ")
arr_list = str_list.split()

# convert each item to int type
for i in range(n):
    # convert each item to int type
    arr_list[i] = int(arr_list[i])


arr = np.array(arr_list)

print(NSwaps(arr,n))


