def orient(x,y,width,height):
    a1=width//x
    b1=width//y
    b2=height//x
    a2=height//y
    return [a1*a2, a1, a2, "stejne"] if a1*a2 >= b1*b2 else (b1*b2, b2, b1,"otoceno")


x=int(input("Sirka uzitku: "))
y=int(input("Vyska uzitku: "))
width=int(input("Sirka archu: "))
height=int(input("Vyska archu: "))
print(orient(x,y,width,height)[0])
