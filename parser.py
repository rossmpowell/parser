import re
import sys

#re contains the following useful methods:
#compile
#match
#search
#findall

#and support for groups

inputString = ''
nextToken = ''
progNameFound = False
termlist = ["program", "begin", "end", "read", "write", "if", "then", "else", "while", "do", ":=", ";", ',', '(', ')']

def lex():
    global inputString
    global nextToken
    global progNameFound
    #print (inputString + " this is the input string in lex")

    if (inputString == ''):
        print("Syntax Error: end token expected")
        sys.exit(0)

    if ((inputString == '') & (nextToken == '')):
        print("Syntax Error: inputString is equal to ''")
        sys.exit(0)

    if (nextToken == '<progname>'): #Done just to make sure that a single capital letter variable can still work
        progNameFound = True        #and it will find <variable> instead of <progname>

    p = re.compile('(\d*?) ')  #Constant Finding
    m = p.match(inputString)
    if (m != None):
        nextToken = '<constant>'
        inputString = inputString.replace(m.group(1) + ' ', '', 1)
        return

    p = re.compile('([A-Z].*?) ')  #ProgName Finding
    m = p.match(inputString)
    if ((m != None) & (not progNameFound)):
        nextToken = '<progname>'
        inputString = inputString.replace(m.group(1) + ' ', '', 1)
        return

    p = re.compile('([=<>][>=]?) ')  #Relational Operator Finding
    m = p.match(inputString)
    if (m != None):
        nextToken = '<relational_operator>'
        inputString = inputString.replace(m.group(1) + ' ', '', 1)
        return

    p = re.compile('([*\/]) ')  #Multiplying Operator
    m = p.match(inputString)
    if (m != None):
        nextToken = '<multiplying_operator>'
        inputString = inputString.replace(m.group(1) + ' ', '', 1)
        return

    p = re.compile('([+-]) ')  #Sign or Adding operator
    m = p.match(inputString)
    if (m != None):
        nextToken = '<adding_operator>'
        inputString = inputString.replace(m.group(1) + ' ', '', 1)
        return

    p = re.compile('(.*?) ')  #Terminal
    m = p.match(inputString)
    if (m != None):
        if (m.group(1) in termlist):
            nextToken = m.group(1)
            inputString = inputString.replace(m.group(1) + ' ', '', 1)
            return

    p = re.compile('([a-zA-Z].*?) ') #Variable
    m = p.match(inputString)
    if (m != None):
        nextToken = '<variable>'
        inputString = inputString.replace(m.group(1) + ' ', '', 1)
        return

    print("Syntax Error: Unknown Symbol")
    sys.exit(0)

#Starts the parser
def parser():
    global inputString
    global nextToken
    lex()   #Load nextToken for start of program;
            #call lex within functions whenever possible
    if (nextToken == ''):
        sys.exit(0)
    if (nextToken == 'program'):
        lex()
        if (nextToken == '<progname>'): #function not needed, checked in lex()
            lex()
            compoundStmt()
        else:
            print("Syntax Error: Invalid Program Name")
            sys.exit(0)
    else:
        print("Syntax Error: Missing 'program'")
        sys.exit(0)
    if (len(inputString) != 0):
        print("Syntax Error: Garbage after end")
        sys.exit(0)
    return

#Compound statement function (if we are supposed to be in a compound statement)
def compoundStmt():
    global inputString
    global nextToken
    if (nextToken == 'begin'):
        stmt()
        while (nextToken == ';'):
            stmt()
        if (nextToken != 'end'):
            print("Syntax Error: End of Compound Statement expected!")
            sys.exit(0)
    else:
        print("Syntax Error: Beginning of Compound Statement expected!")
        sys.exit(0)
    return

#Statement function
def stmt():
    global inputString
    global nextToken
    lex()
    if ((nextToken == '<variable>') | (nextToken == 'read') | (nextToken == 'write')):
        simpleStmt()
    elif ((nextToken == 'begin') | (nextToken == 'if') | (nextToken == 'while')):
        structuredStmt()
    else:
        print("Syntax Error: Statement expected")
        sys.exit(0)
    return

#simple statment decides what type of simple statement exists based ff nextToken
def simpleStmt():
    global inputString
    global nextToken
    if (nextToken == '<variable>'):
        assignmentStmt()
    elif (nextToken == 'read'):
        readStmt()
    elif (nextToken == 'write'):
        writeStmt()
    else:
        print("Syntax Error: Assignment Statement or Read Statement or Write Statement expected")
        sys.exit(0)
    return

#structured statment decides what type of structured statement exists based ff nextToken
def structuredStmt():
    global inputString
    global nextToken
    if (nextToken == 'begin'):
        compoundStmt()
    elif (nextToken == 'if'):
        ifStmt()
    elif (nextToken == 'while'):
        whileStmt()
    else:
        print("Syntax Error: compound statement or read statement or write statement expected")
        sys.exit(0)
    return

def assignmentStmt():
    global inputString
    global nextToken
    lex()
    #get to the assignment op
    if(nextToken == ":="):
        lex()
        #then assignment op to expression
        expression()
    else:
        print("Syntax Error: := sign expected")
        sys.exit(0)
    return

def readStmt():
    global inputString
    global nextToken
    lex()
    if (nextToken == '('):
        lex()
        if (nextToken == '<variable>'):
            lex()
            while (nextToken == ','):
                lex()
                if (nextToken == '<variable>'):
                    lex()
                else:
                    print("Syntax Error: variable expected")
                    sys.exit(0)
            if (nextToken == ')'):
                lex()
            else:
                print("Syntax Error: ')' expected")
                sys.exit(0)
        else:
            print("Syntax Error: variable expected")
            sys.exit(0)
    else:
        print("Syntax Error: '(' expected")
        sys.exit(0)
    return

def writeStmt():
    global inputString
    global nextToken
    lex()
    if (nextToken == '('):
        lex()
        expression()
        while (nextToken == ','):
            lex()
            expression()
        if (nextToken == ')'):
            lex()
        else:
            print("Syntax Error: ')' expected")
            sys.exit(0)
    else:
        print("Syntax Error: '(' expected")
        sys.exit(0)
    return

def whileStmt():
    global inputString
    global nextToken
    lex()
    expression()
    if(nextToken == 'do'):
        stmt()
    return


def ifStmt():
    global inputString
    global nextToken
    lex()
    expression()
    if(nextToken == 'then'):
        stmt()
        if(nextToken == 'else'):
            stmt()
    else:
        print("Syntax Error: 'then' expected")
        sys.exit(0)
    return

def expression():
    global inputString
    global nextToken
    simpleExpr()
    if (nextToken == '<relational_operator>'):
        lex()
        simpleExpr()
    #ending an expression, but having another terminal left. These are the only terminals that are necessary
    elif ((nextToken == 'end') | (nextToken == 'else') | (nextToken == 'do') | (nextToken == 'then')):
        return
    else:
        print("Syntax error: relational operator expected")
        sys.exit(0)
    return

def simpleExpr():
    global inputString
    global nextToken
    if (nextToken == '<adding_operator>'):
        lex()
    term()
    while (nextToken == '<adding_operator>'):
        lex()
        term()
    return

def term():
    global inputString
    global nextToken
    factor()
    while(nextToken == '<multiplying_operator>'):
        lex()
        factor()
    return

def factor():
    global inputString
    global nextToken
    if((nextToken == '<variable>') | (nextToken == '<constant>')):
        lex()
    else:
        if (nextToken == '('):
            lex()
            expression()
            if (nextToken == ')'):
                lex()
            else:
                print("Syntax Error: ')' expected")
                sys.exit(0)
        else:
            print("Syntax Error: '(' expected")
            sys.exit(0)
    return

inputString = input("Enter an inputString: ")
parser()
print("The string is syntactically correct!! :<")