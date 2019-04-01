
def addTheCompany():
    retry = True
    while(retry==True):
        print("-----Add company details-----\n-----------------------------")
        code = input('Enter the yahoo code : ')
        name = input('Enter the name of the company : ')
        typeComp = input('Enter the type of company\n\
        --Banking, IT, FMCG, Energy, Automobile--\nChoice : ')
        cap = input('--Small, Mid, Large--\nEnter market capitalization : ')

        types=['Banking', 'IT', 'FMCG', 'Energy', 'Automobile']
        caps = ['Small','Mid','Large']
        flag = True

        if not (typeComp in types):
            flag = False

        if not (cap in caps):
            flag = False

        if(flag == True):
            print("Details Added\n-----------------------------")
        else:
            print("There is some error, no changes made")
            if not (input('To try again? [y/n] : ')=="y"):
                print('-----------------------------')
                retry = False
                break
            continue

        txt = "\n\""+code+"\","+"\""+name+"\","+"\""+typeComp+"\","+"\""+cap+"\""
        with open('Companies.txt','a') as csvFile:
            csvFile.write(txt)

def main():
    addTheCompany()

if __name__ == '__main__':
    main()
