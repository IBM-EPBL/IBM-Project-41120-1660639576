n=int(input("enter the number:"))
n1=0
n2=1
print(n1)
print(n2)

for i in range(3,n+1):
    n3=n2+n1
    print(n3)
    n1=n2
    n2=n3
