num = 11
c=0

for i in range(2, int(num/2)+1):
     if (num % i) == 0:
       c+=1
       break
if (c==0):
     print(num, "is a prime number")
else:
     print(num, "is not a prime number")
