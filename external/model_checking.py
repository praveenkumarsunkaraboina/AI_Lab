import itertools
def main():
    N=int(input("Enter the number of variables:\n"))
    possibilities=list(itertools.product([True,False],repeat=N))
    temp=False

    if N==3:
        for i in range(len(possibilities)):
            A=possibilities[i][0]
            B=possibilities[i][1]
            C=possibilities[i][2]

            condition1 = A or B
            condition2 = (not A) == (not B or C)
            condition3 = not A or not B or C

            if condition1 and condition2 and condition3:
                temp=True
                print("KB is Satisfied")
                print(f"{A}, {B},{C}")
    elif N==4:
        for i in range(len(possibilities)):
            A = possibilities[i][0]
            B = possibilities[i][1]
            C = possibilities[i][2]
            D = possibilities[i][3]

            condition1 = C == (B or D)
            condition2 = not A or (not B and not D)
            condition3 = (B and not C) or A
            condition4 = D or C
            if condition1 and condition2 and condition3 and condition4:
                temp=True
                print("KB is Satisfied.")
                print(f"({A},{B},{C},{D})")
    
    if not temp:
        print("No matter how we assign truth values to variables no satifiable assignment is obtained....")

if __name__ == "__main__":
    main()

            
