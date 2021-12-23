
import sys

def leading(v):
    if v in lead_dict.keys():
        return lead_dict[v]
    else:
        lead_dict[v]=[]
   
    p=[]
    for production in g:
        if production[0]==v:
            p.append(production[3:])
            
    for pr in p:
        var=False
        if pr[0] in variables:
            var=True
            if pr[0]!=v:
                l=leading(pr[0])
                for each in l:
                    lead_dict[v].append(each)
                lead_dict[v]=list(set(lead_dict[v]))
                
        elif pr[0] in terminals:
            lead_dict[v].append(pr[0])
        
        if var==True and len(pr)>1:
            lead_dict[v].append(pr[1])
        
    lead_dict[v]=list(set(lead_dict[v]))
    return lead_dict[v]

def trailing(v):
    if v in trail_dict.keys():
        return trail_dict[v]
    else:
        trail_dict[v]=[]
    
    p=[]
    for production in g:
        if production[0]==v:
            p.append(production[3:])
    
    for pr in p:
        var=False
        if pr[-1] in variables:
            var=True
            if pr[-1]!=v:
                t=trailing(pr[-1])
                for each in t:
                    trail_dict[v].append(each)
                trail_dict[v]=list(set(trail_dict[v]))
        elif pr[-1] in terminals:
            trail_dict[v].append(pr[-1])
        
        if var==True and len(pr)>1:
            trail_dict[v].append(pr[-2])
    
    trail_dict[v]=list(set(trail_dict[v]))
    return trail_dict[v]

parseDict = {}
def parse(g):
        
    for production in g:
        production = production[3:]
        
        for i in range(len(production)-1):
            first = production[i]
            second = production[i+1]
            
            if first in variables and second in terminals :
                tp = trailing(first)
                col = terminals.index(second)
                for each in tp:
                    row = terminals.index(each)
                    parseDict[(row,col)] = ">"
                    
            elif first in terminals and second in variables :
                tp = leading(second)
                row = terminals.index(first)
                for each in tp:
                    col = terminals.index(each)
                    parseDict[(row,col)] = "<"
    
    t1 = terminals.index("(")
    t2 = terminals.index(")")
    parseDict[(t1,t2)] = "="
    
    keyList = list(parseDict.keys())
    
    print("\nParsing Table \n")
    print("\t", end="")

    for terminal in terminals:
        print(terminal.ljust(20), end="")
    print("$".ljust(20), end="")
    print("\n")
    
    for terminal in terminals:
        temp = []
        print(terminal+"\t", end="")
        v1 = terminals.index(terminal)
        for i in keyList:
            if i[0]==v1:
                temp.append(i)
        temp.sort()
        list2 = []
        for i in temp:
            list2.append(i[1])
        
        for i in range(len(terminals)):
            if i in list2:
                print(parseDict[(v1,i)].ljust(20), end="")
            else:
                print("".ljust(20), end="")

        print(">".ljust(20), end="")
        print("")
    
    print("$\t", end="")
    for terminal in terminals:
        print("<".ljust(20), end="")
    print("Accept".ljust(20), end="")
        
    
def validate(string):
    
    flag = 0   #string is valid
    string+="$"
    stack = []
    stack.append("$")
    stack.append(string[0])
    
    pointer = 1
    
    while len(stack)>0:
        top = stack[len(stack)-1]
        cur_input = string[pointer]
        
        if cur_input=="$" and top=="$":
            break
        
        elif cur_input=="$" and top!="$":
            stack.pop()
            
        elif cur_input!="$" and top=="$":
            stack.append((cur_input))
            pointer+=1
        
        else:
        
            t1 = terminals.index(top)
            t2 = terminals.index(cur_input)
            
            if parseDict[(t1,t2)]=="<" or parseDict[(t1,t2)]=="=":
                stack.append(cur_input)
                pointer+=1
                
            elif parseDict[(t1,t2)]==">":
                stack.pop()
                
            else:
                flag=1
                break
        
    if flag==0:
        print("String is Valid")
    else:
        print("String is Not Valid")
 
    
# main class

file = open("input_grammar.txt", "r")

grammar=[]
while True:
    ll = file.readline().strip()
    if ll=="":
        break
    grammar.append(ll)
print("\n",grammar)

variables =[]
for i in grammar:
    variables.append(i[0])

terminals = []
for i in grammar:
    i = i[3:]
    for j in i:
        if j not in variables and j!="/":
            terminals.append(j)
terminals = list(set(terminals))
g=[]
for production in grammar:
    v=production[0]
    production=production[3:]
    exp=""
    for letter in production:
        if letter!='/':
            exp+=letter
        else:
            g.append(v+"->"+exp)
            exp=""
    if exp!="":
        g.append(v+"->"+exp)

for production in g:
    production=production[3:]
    var=False
    for letter in production:
        if letter in variables and var==False:
            var=True
        elif letter in variables or letter=='@':
            sys.exit("Grammar is not an operator grammar")
        elif letter in terminals:
            var=False
print("\nGrammar is operator grammar\n")

lead_dict={}
trail_dict={}    

print("Variable".ljust(15), "Leading".ljust(25), "Trailing".ljust(25))
for v in variables:
    print(v.ljust(15), str(set(leading(v))).ljust(25), str(set(trailing(v))).ljust(25))

parse(g)
print("\n")

file1 = open("string.txt", "r")
string = file1.readline()
print("Input String : ", string)
validate(string)

