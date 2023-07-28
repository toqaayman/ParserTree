from treelib import Tree
import sys
import random

token_index=1                             #token stream token_index
parse_tree = Tree()                       #made tree
parse_tree.create_node('BEGIN', parse_tree.root) #root node named 'root'
ban=[]                              #tokens that wont be read. filled later
mul='*/'
addop='+-'
compare=['<=','>=','==','!=','<','>']
num=['Identifier','Constant']
integer=['0123456789']
rules = {
  'PROGRAM': ['Identifier','Semicolon'],          # PROGRAM -> PROGRAM Identifier ;
  'PROCEDURE': ['Identifier','Semicolon'],        # PROCEDURE -> PROGRAM Identifier ;
  'DECLARE':['Datatype','Identifier','Semicolon'],# DECLARE -> Datatype Identifier ;
  'PARAMETERS':['Datatype','Identifier','Semicolon'],# DECLARE -> Datatype Identifier ;
  'READ':['Identifier','Semicolon'],    # Read -> Read Identifier ;
  'WRITE':['Identifier','Semicolon'],    # WRITE -> WRITE Identifier ;
  'SET':['Identifier','Relational_Operator','Semicolon'],
  'CALL':['Identifier','L_Bracket','ARGLIST','R_Bracket'],
  'IF':['Identifier','Relational_Operator','Constant','THEN', 'ELSE','ENDIF'],
  'WHILE':['Identifier','Relational_Operator','Constant','DO', 'ENDWHILE'],
  'UNTIL':['Identifier','Relational_Operator','Constant','DO', 'ENDUNTIL']
}

tokens=[
'PROGRAM','PROGRAM',
'EvalFormula','Identifier',
';','Semicolon',

'DECLARE','DECLARE',

'INTEGER','Datatype',
'a','Identifier',
';','Semicolon',

'REAL','Datatype',
'b','Identifier',
';','Semicolon',

'PROCEDURE','PROCEDURE',

'FindFormula','Identifier',
';','Semicolon',

'PARAMETERS','PARAMETERS',

'INTEGER','Datatype',
'x','Identifier',
';','Semicolon',

'REAL','Datatype',
'y','Identifier',
';','Semicolon',

'BEGIN','BEGIN',

'WHILE','WHILE',
'x','Identifier',
'!','Relational_Operator',
'0','Constant',
'DO','DO',

'IF','IF',
'x','Identifier',
'<','Relational_Operator',
'0','Constant',
'THEN','THEN',
'SET','SET',
'y','Identifier',
'=','Relational_Operator',
'10','Constant',
'-','Relational_Operator',
'4.5','Constant',
'*','Relational_Operator',
'x','Identifier',
';','Semicolon',

'ELSE','ELSE',
'SET','SET',
'y','Identifier',
'=','Relational_Operator',
'4.5','Constant',
'*','Relational_Operator',
'x','Identifier',
'+','Relational_Operator',
'10','Constant',
';','Semicolon',

'ENDIF','ENDIF',
';','Semicolon',

'WRITE','WRITE',
'y','Identifier',
';','Semicolon',

'READ','READ',
'x','Identifier',
';','Semicolon',

'ENDWHILE','ENDWHILE',
';','Semicolon',

'BEGIN','BEGIN',

'READ','READ',
'a','Identifier',
';','Semicolon',

'CALL','CALL',
'FindFormula','Identifier',
'(','L_Bracket',
'ARGLIST','ARGLIST',
')','R_Bracket',

'WRITE','WRITE',
'b','Identifier',
';','Semicolon',

'END','END'
]

def parse(token_index, rule, _parent):
    for i in range(len(rules[rule])):
        if tokens[token_index] != rules[rule][i]:
            sys.exit(f"Invalid token sequence. Token '{tokens[token_index]}' is not '{rules[rule][i]}'. Error at token_index {token_index}")
        if tokens[token_index-1] not in ['REAL', 'INTEGER']:
            if tokens[token_index] == 'Relational_Operator' and tokens[token_index-1] == '=':
                token_index = expresion(token_index, _parent)
                token_index -= 2
            elif tokens[token_index] == 'THEN':
                token_index = stmt(token_index, 'ELSE')
            elif tokens[token_index] in ['ELSE', 'DO']:
                token_index = stmt(token_index, 'ENDIF' if tokens[token_index] == 'ELSE' else 'ENDWHILE' if rule == 'WHILE' else 'ENDUNTIL')
            parse_tree.create_node(tokens[token_index-1], parent=_parent)
        token_index += 2
    return token_index

def DPP_parse(token_index, target_token):
    if tokens[token_index] == target_token:
        ban.append(target_token)
    token_index += 2
    if tokens[token_index] != 'Datatype':
        print("WARNING! Empty declare section. Please remove it or add to it")
        return token_index
    parse_tree.create_node(target_token, target_token, parent=parse_tree.root)
    while tokens[token_index] == 'Datatype':
        new_parent = tokens[token_index-1] + str(random.random())[2:]
        parse_tree.create_node(tokens[token_index-1], new_parent, parent=target_token)
        token_index = parse(token_index, target_token, new_parent)
    return token_index

def stmt(token_index,ending):
    safety=0
    allowed=['READ','WRITE','SET','CALL','IF','WHILE','UNTIL']
    while(tokens[token_index]!=ending and safety<1000):#loops between BEGIN to END
        safety+=1
        if(tokens[token_index] in allowed):
            x=tokens[token_index-1]+str(random.random())[2:]
            parse_tree.create_node(tokens[token_index],x,parent=parse_tree.root)
            token_index+=2
            token_index=parse(token_index,tokens[token_index-2],x)
        else:
            token_index+=2
    return token_index-2

def switch_inlist(category,stuff):
    counter=0
    while (counter<len(stuff) and counter<1000):
            if (stuff[counter] in category):
                temp=stuff[counter]
                stuff[counter]=stuff[counter-1]
                stuff[counter-1]=temp
            counter+=1

def exp_parse(counter,arr,_parent):
    while (counter<len(arr) and counter<1000):
        if (arr[counter] not in addop and arr[counter] not in mul):
            parse_tree.create_node(arr[counter],parent=_parent)
        elif (arr[counter] in addop):
            new_parent=arr[counter]+str(random.random())[2:]
            parse_tree.create_node(arr[counter],new_parent,_parent)
            _parent=new_parent
        elif (arr[counter] in mul):
            new_parent=arr[counter]+str(random.random())[2:]
            parse_tree.create_node(arr[counter],new_parent,_parent)
            new_parent2=new_parent
            counter+=1
            while(counter<len(arr) and arr[counter] not in addop and counter<1000):
                if (arr[counter] not in mul):
                    parse_tree.create_node(arr[counter],parent=new_parent2)
                else:
                    new_parent=arr[counter]+str(random.random())[2:]
                    parse_tree.create_node(arr[counter],new_parent,new_parent2)
                    new_parent2=new_parent
                counter+=1
        counter+=1
        
def expresion(point,parent_node):
    stuff=[]
    point-=1
    saftey=0
    while (tokens[point]!=';' and saftey<1000):
        stuff.append(tokens[point])
        point+=2
        saftey+=1
        
    counter=0
    while (counter<len(stuff) and counter<1000):
            if stuff[counter] in mul:
                if counter==len(stuff)-1:
                    stuff[counter-1:] = [','.join(stuff[counter-1:])]
                else:
                    stuff[counter-1:counter+2] = [','.join(stuff[counter-1:counter+2])]
                counter-=3
            counter+=1
    
    switch_inlist(addop,stuff)
    temp=[]
    
    for i in stuff:
        temp+=(i.split(","))
    stuff=temp
    switch_inlist(mul,stuff)
    exp_parse(0,stuff,parent_node)
    return point+1

if tokens[token_index]!= 'PROGRAM':          #if program dosnt start withe PROGRAM
    sys.exit('First token is not the program name.')

parse_tree.create_node(tokens[token_index-1], 'program', parent=parse_tree.root)
token_index+=2
token_index=parse(token_index,'PROGRAM','program')
safety=0
targets=['PROCEDURE','DECLARE']

while(tokens[token_index]!='BEGIN' and len(targets)>0 and safety<1000):
    if tokens[token_index] not in targets:
        sys.exit('ERROR! Recived '+tokens[token_index]+', were expecting tokens BEGIN or '+str(targets))
    elif (tokens[token_index]=='DECLARE'):
        targets.remove('DECLARE')
        token_index=DPP_parse(token_index,'DECLARE')
    
    elif (tokens[token_index]=='PROCEDURE'):
        targets.remove('PROCEDURE')
        targets.append('PARAMETERS')
        parse_tree.create_node(tokens[token_index-1], 'procedure', parent=parse_tree.root)
        token_index+=2
        token_index=parse(token_index,'PROCEDURE','procedure')
        
    elif (tokens[token_index]=='PARAMETERS'):
        targets.remove('PARAMETERS')
        token_index=DPP_parse(token_index,'PARAMETERS')
    safety+=1

if 'PARAMETERS' in targets:
    sys.exit('ERROR! PROCEDURE declared without PARAMETERS')

if tokens[token_index]!='BEGIN':
    sys.exit('ERROR! Recived '+tokens[token_index]+', were expecting tokens BEGIN or '+str(targets))
stmt(token_index,'END')
print('\nparse_tree:')
print(parse_tree.show())