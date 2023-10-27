from lex import lex
from lex import tableOfSymb

lex()
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)

numRow = 1
len_tableOfSymb = len(tableOfSymb)
print(('len_tableOfSymb', len_tableOfSymb))

def failParse(message, details):
    print(f"Parser ERROR: {message} - {details}")
    exit(1)

def getSymb():
    global numRow
    if numRow > len_tableOfSymb:
        return None, None, None
    numLine, lexeme, token, _ = tableOfSymb[numRow]
    return numLine, lexeme, token

def parseToken(expected_lexeme, expected_token, error_message=None):
    global numRow
    numLine, lex, tok = getSymb()
    if (lex, tok) == (expected_lexeme, expected_token):
        numRow += 1
        return True
    else:
        if error_message:
            failParse(error_message, (numLine, lex, tok))
        else:
            failParse("Token mismatch", (numLine, lex, tok, expected_lexeme, expected_token))
        return False

# def parseProgram():
#     global numRow
#     print("Parsing Program...")
#     parseDeclarList()
#     while numRow <= len_tableOfSymb:
#         parseStatement()
#     if numRow != len_tableOfSymb + 1:
#         failParse("Unexpected tokens at the end of the program", numRow)
#     print("Parser: Syntax analysis completed successfully")
#     return True
def parseProgram():
    print("Parsing Program...")
    parseDeclarList()
    parseStatementList()
    print("Parser: Syntax analysis completed successfully")
    return True


#rabotaet

def parseDeclarList():
    print("Parsing Declaration List...")
    while True:
        if not parseDeclaration():
            break
    return True

def parseDeclaration():
    print("Parsing Declaration...")
    numLine, lex, tok = getSymb()
    if lex is None:
        return False
    if lex in ("int", "double", "boolean"):
        parseType()
        parseIdentList()
        return True
    # elif lex.startswith("//"):  # предполагая, что комментарии начинаются с '//'
    #     parseComment()
    #     return True
    else:
        return False


def parseType():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Type: {lex, tok}...")
    if lex in ("int", "double", "boolean"):
        numRow += 1
        return True
    else:
        failParse("Unexpected token in Type", (numLine, lex, tok))
        return False

def parseIdentList():

    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Identifier List: {lex, tok}...")
    if tok == "ident":
        numRow += 1
        while True:
            numLine, lex, tok = getSymb()
            if lex == ",":
                numRow += 1
                numLine, lex, tok = getSymb()
                if tok == "ident":
                    numRow += 1
                else:
                    failParse("Expected identifier after comma", (numLine, lex, tok))
                    return False
            else:
                break
        return True
    else:
        failParse("Expected identifier in IdentList", (numLine, lex, tok))
        return False

# def parseComment():
#     global numRow
#     numLine, lex, tok = getSymb()
#     if lex.startswith("//"):
#         numRow += 1
#         return True
#     else:
#         failParse("Expected comment", (numLine, lex, tok))
#         return False

#rabotaet-----------


def parseStatementList():
    global numRow
    print("Parsing Statement List...")
    while numRow <= len_tableOfSymb:
        parseStatement()

def parseStatement():
    numLine, lex, tok = getSymb()
    print(f"Parsing Statement: {lex, tok}...")
    if tok == "ident":  # начало инструкции присваивания
        next_numLine, next_lex, next_tok, _ = tableOfSymb[numRow + 1] if numRow + 1 <= len_tableOfSymb else (None, None, None, None)
        if next_lex == "=":
            next_next_numLine, next_next_lex, next_next_tok, _ = tableOfSymb[
                numRow + 2] if numRow + 2 <= len_tableOfSymb else (None, None, None, None)
            if next_next_lex == "readLine":
                parseInp()
            else:
                parseAssign()
        else:
            failParse("Unexpected token after identifier", (next_numLine, next_lex, next_tok))
    elif lex == 'println':
        parseOut()
    if lex == 'for':
        parseForStatement()
    else:
        failParse("Unexpected token in Statement", (numLine, lex, tok))
        return False

def parseAssign():
    print("Parsing Assign Statement...")
    parseIdent()
    parseToken("=", "assign_op")
    parseExpression()

def parseIdent():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Identifier: {lex, tok}...")
    if tok == "ident":
        numRow += 1
        return True
    else:
        failParse("Expected identifier", (numLine, lex, tok))
        return False

def parseAssignOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing AssignOp: {lex, tok}...")
    if lex == "=":  # предполагая, что оператор присваивания это '='
        numRow += 1
        return True
    else:
        failParse("Expected assign operator", (numLine, lex, tok))
        return False

def parseExpression():
    numLine, lex, tok = getSymb()
    print(f"Parsing Expression: {lex, tok}...")
    if tok in ("intnum", "realnum", "ident") or lex in ("(", "-", "+"):
        return parseArithmExpression()
    else:
        return parseBoolExpr()

def parseBoolExpr():
    print("Parsing Boolean Expression...")
    parseArithmExpression()
    parseRelOp()
    parseArithmExpression()

def parseArithmExpression():
    print("Parsing Arithmetic Expression...")
    parseSign(optional=True)
    parseTerm()
    while True:
        numLine, lex, tok = getSymb()
        if lex in ("+", "-"):
            parseAddOp()
            parseTerm()
        else:
            break
    return True

def parseTerm():
    print("Parsing Term...")
    parsePower()
    while True:
        numLine, lex, tok = getSymb()
        if lex in ("*", "/"):
            parseMultOp()
            parsePower()
        else:
            break
    return True

def parsePower():
    print("Parsing Power...")
    parseFactor()
    while True:
        numLine, lex, tok = getSymb()
        if lex == "**":
            parsePowerOp()
            parseFactor()
        else:
            break
    return True

def parseFactor():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Factor: {lex, tok}...")
    if tok == "ident":
        parseIdent()
    elif tok in ("intnum", "realnum"):
        parseArithmConst()
    elif lex == "(":
        numRow += 1
        parseArithmExpression()
        if not parseToken(")", "bracket"):
            failParse("Expected closing bracket in line", ( numLine))
            return False
        return True
    else:
        failParse('невідповідність у Expression.Factor',
                  (numLine, lex, tok, ' int, double, ident або \'(\' Expression \')\''))
    return True

def parseArithmConst():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Arithmetic Constant: {lex, tok}...")
    if tok in ("intnum", "realnum"):
        numRow += 1
        return True
    else:
        failParse("Expected arithmetic constant", (numLine, lex, tok))
        return False

def parseSign(optional=False):
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Sign: {lex, tok}...")
    if lex in ("+", "-"):
        numRow += 1
        return True
    elif optional:
        return False
    else:
        failParse("Expected sign", (numLine, lex, tok))
        return False

def parseRelOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Relational Operator: {lex, tok}...")
    if lex in ("<", ">", "<=", ">=", "==", "!="):
        numRow += 1
        return True
    else:
        failParse("Expected relational operator", (numLine, lex, tok))
        return False

def parseAddOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Additive Operator: {lex, tok}...")
    if lex in ("+", "-"):
        numRow += 1
        return True
    else:
        failParse("Expected additive operator", (numLine, lex, tok))
        return False

def parseMultOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Multiplicative Operator: {lex, tok}...")
    if lex in ("*", "/"):
        numRow += 1
        return True
    else:
        failParse("Expected multiplicative operator", (numLine, lex, tok))
        return False

def parsePowerOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Power Operator: {lex, tok}...")
    if lex == "**":
        numRow += 1
        return True
    else:
        failParse("Expected power operator", (numLine, lex, tok))
        return False

#---------------------------------------------
def parseOut():
    print("Parsing Out Statement...")
    parseToken('println', "keyword")
    parseToken('(', 'bracket')
    numLine, lex, tok = getSymb()
    if tok == 'text':
        parseText()
    else:
        parseExpression()
    parseToken(')', 'bracket')
    return True

def parseText():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Text: {lex, tok}...")
    if tok == 'text':
        numRow += 1
        return True
    else:
        failParse("Expected text", (numLine, lex, tok))
        return False

#----------------------------------
def parseInp():
    print("Parsing Input Statement...")
    parseIdent()  # Парсинг идентификатора
    parseToken('=', 'assign_op', "Expected assignment operator '=' after identifier")  # Парсинг оператора присваивания
    parseToken('readLine', 'keyword', "Expected keyword 'readLine' after '='")  # Парсинг ключевого слова 'readLine'
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'readLine'")  # Парсинг открывающей скобки
    parseToken(')', 'bracket', "Expected closing bracket ')' after opening bracket '('")  # Парсинг закрывающей скобки
    return True
#----------------------------------
def parseForStatement():
    print("Parsing For Statement...")
    parseToken('for', "keyword")
    parseToken('(', 'bracket')
    parseInit()
    parseToken(';', 'punct')
    parseBoolExpr()
    parseToken(';', 'punct')
    parseUpdate()
    parseToken(')', 'bracket')
    parseToken('{', 'brace')
    parseStatementList()
    parseToken('}', 'brace')
    return True

def parseInit():
    print("Parsing Init...")
    parseIdent()
    parseAssignOp()
    parseArithmExpression()
    return True

def parseUpdate():
    print("Parsing Update...")
    parseIdent()
    parseAssignOp()
    parseArithmExpression()
    return True

parseProgram()
