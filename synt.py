from lex import lex
from lex import tableOfSymb

lex()   # Викликаємо функцію лексичного аналізу
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)

numRow = 1  # Викликаємо функцію лексичного аналізу
len_tableOfSymb = len(tableOfSymb)  # Обчислюємо довжину таблиці символів
print(('len_tableOfSymb', len_tableOfSymb))

# Функція для виведення повідомлення про помилку та завершення програми з вказаним кодом помилки
def failParse(message, details, error_code=1):
    numLine, lex, tok = details
    print(f"Parser ERROR in line {numLine-1}: {message} - Current token: ({lex}, {tok})")
    exit(error_code)


def getSymb():
    global numRow
    if numRow > len_tableOfSymb:  # Якщо досягли кінця таблиці символів, повертаємо None для всіх значень
        return None, None, None
    numLine, lexeme, token, _ = tableOfSymb[numRow] # Інакше повертаємо поточний символ
    return numLine, lexeme, token

# Функція для аналізу токенів. Перевіряє, чи відповідає поточний токен очікуваному.
def parseToken(expected_lexeme, expected_token, error_message=None):
    global numRow
    numLine, lex, tok = getSymb()   # Отримуємо поточний символ
    if (lex, tok) == (expected_lexeme, expected_token):# Якщо поточний символ відповідає очікуваному
        numRow += 1 #збільшуємо лічильник рядка
        return True
    else: # Інакше використовуємо загальне повідомлення про невідповідність токенів
        if error_message:# Якщо є конкретне повідомлення про помилку, використовуємо його
            failParse(error_message, (numLine, lex, tok) )
        else:
            failParse("Token mismatch", (numLine, lex, tok, expected_lexeme, expected_token))
        return False


def parseProgram():
    print("Parsing Program...")
    parseDeclarList()  # Аналізуємо список оголошень
    parseStatementList() # Аналізуємо список інструкцій
    print("Parser: Syntax analysis completed successfully") # Повідомлення про успішне завершення аналізу
    return True


#rabotaet

def parseDeclarList():
    print("Parsing Declaration List...")
    while True:
        if not parseDeclaration():
            break
        numLine, lex, tok = getSymb()
        if lex == ";":  # Якщо крапка з комою
            parseSeparator()  # Аналіз роздільника
    return True

def parseSeparator():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Separator: {lex, tok}...")
    if lex == ";":
        numRow += 1
        return True
    else:
        failParse("Expected separator ';'", (numLine, lex, tok), error_code=12)
        return False


def parseDeclaration():# Функція для аналізу окремого оголошення
    print("Parsing Declaration...")
    numLine, lex, tok = getSymb() # Отримуємо поточний символ
    if lex is None:             # Якщо символ відсутній, завершуємо аналіз
        return False
    if lex in ("int", "double", "boolean"):# Перевіряємо, чи є поточний символ типом даних
        parseType()                         # Аналізуємо тип даних
        parseIdentList()            # Аналізуємо список ідентифікаторів
        return True
    else:
        return False

# Функція для аналізу типу даних
def parseType():
    global numRow
    numLine, lex, tok = getSymb() # Отримуємо поточний символ
    print(f"Parsing Type: {lex, tok}...") # Повідомлення про початок аналізу типу даних
    if lex in ("int", "double", "boolean"): # Перевіряємо, чи є поточний символ типом даних
        numRow += 1
        return True
    else: # Якщо поточний символ не є типом даних, виводимо повідомлення про помилку
        failParse("Unexpected token in Type", (numLine, lex, tok), error_code=2)
        return False

# Функція для аналізу списку ідентифікаторів
def parseIdentList():
    global numRow
    numLine, lex, tok = getSymb()# Отримуємо поточний символ
    print(f"Parsing Identifier List: {lex, tok}...")
    if tok == "ident":  # Перевіряємо, чи є поточний символ ідентифікатором
        numRow += 1
        while True:
            numLine, lex, tok = getSymb()  # Отримуємо наступний символ
            if lex == ",":                  # Якщо це кома, аналізуємо наступний ідентифікатор
                numRow += 1
                numLine, lex, tok = getSymb()
                if tok == "ident":
                    numRow += 1
                else: # Якщо після коми відсутній ідентифікатор, виводимо повідомлення про помилку
                    failParse("Expected identifier after comma", (numLine, lex, tok), error_code=3)
                    return False
            else:
                break
        return True
    else: # Якщо поточний символ не є ідентифікатором, виводимо повідомлення про помилку
        failParse("Expected identifier in IdentList", (numLine, lex, tok), error_code=4)
        return False

#rabotaet-----------


def parseStatementList():
    print("Parsing Statement List...")
    while True:
        if not parseStatement():
            break
        numLine, lex, tok = getSymb() # Отримуємо поточний символ
        if lex == ";":  # Якщо крапка з комою
            parseSeparator()  # Аналіз роздільника
        if lex is None or lex == "}":  # Якщо символ відсутній або це закриваюча дужка, завершуємо аналіз
            break
    return True

def parseStatement():
    numLine, lex, tok = getSymb() # Отримуємо поточний символ
    print(f"Parsing Statement: {lex, tok}...")
    # Перевіряємо тип інструкції та аналізуємо її
    if tok == "ident":
        next_numLine, next_lex, next_tok, _ = tableOfSymb[numRow + 1] if numRow + 1 <= len_tableOfSymb else (None, None, None, None)
        if next_lex == "=":
            next_next_numLine, next_next_lex, next_next_tok, _ = tableOfSymb[
                numRow + 2] if numRow + 2 <= len_tableOfSymb else (None, None, None, None)
            if next_next_lex == "readLine":
                parseInp()
                return True
            else:
                parseAssign()
                return True
        else:
            failParse("Unexpected token after identifier", (next_numLine, next_lex, next_tok), error_code=5)
    elif lex == 'println':
        parseOut()
        return True
    elif lex == 'for':
        parseForStatement()
        return True
    elif lex == 'while':
        parseWhileStatement()
        return True
    elif lex == 'do':
        parseDoWhileStatement()
        return True
    elif lex == 'if':
        parseIfStatement()
        return True
    elif lex == 'switch':
        parseSwitchStatement()
        return True
    elif lex == 'break':
        parseBreak()
        return True
    else:
        failParse("Unexpected token in Statement", (numLine, lex, tok))
        return False

def parseAssign():
    print("Parsing Assign Statement...")
    parseIdent() # Аналізуємо ідентифікатор
    parseToken("=", "assign_op", "Expected assignment operator '=' after identifier") # Перевіряємо наявність оператора присвоєння
    parseExpression() # Аналізуємо вираз

def parseIdent():
    global numRow
    numLine, lex, tok = getSymb() # Отримуємо поточний символ
    print(f"Parsing Identifier: {lex, tok}...")
    if tok == "ident": # Перевіряємо, чи є поточний символ ідентифікатором
        numRow += 1
        return True
    else: # Якщо поточний символ не є ідентифікатором, виводимо повідомлення про помилку
        failParse("Expected identifier", (numLine, lex, tok), error_code=6)
        return False


def parseExpression():
    numLine, lex, tok = getSymb()
    print(f"Parsing Expression: {lex, tok}...")
    if tok in ("intnum", "realnum", "ident") or lex in ("(", "-", "+"):# Визначаємо тип виразу (арифметичний чи булевий) та аналізуємо його
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
    if tok == "ident": # Перевіряємо, чи є поточний символ ідентифікатором
        parseIdent() # Аналізуємо ідентифікатор
    elif tok in ("intnum", "realnum"):# Перевіряємо, чи є поточний символ числовою константою (ціле або дійсне число)
        parseArithmConst()# Аналізуємо числову константу
    elif lex == "(":# Перевіряємо, чи є поточний символ відкриваючою дужкою
        numRow += 1# Переходимо до наступного символу
        parseArithmExpression()# Аналізуємо арифметичний вираз всередині дужок
        if not parseToken(")", "bracket","Expected closing bracket ')'"): # Перевіряємо, чи є наступний символ закриваючою дужкою
            return False
        return True
    else: # Якщо поточний символ не відповідає жодному з вищезазначених варіантів
        failParse('невідповідність у Expression.Factor ' 'Expected int, double, ident або \'(\' Expression \')\'',
                  (numLine, lex, tok ), error_code=7)
    return True

def parseArithmConst():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Arithmetic Constant: {lex, tok}...")
    if tok in ("intnum", "realnum"):
        numRow += 1
        return True
    else:
        failParse("Expected arithmetic constant", (numLine, lex, tok), error_code=8)
        return False

def parseSign(optional=False):
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Sign: {lex, tok}...")
    if  lex == "-":
        numRow += 1
        return True
    elif optional: # Якщо знак є необов'язковим і його немає, повертаємо False
        return False
    else:# Якщо знак відсутній, виводимо помилку
        failParse("Expected sign", (numLine, lex, tok), error_code=9)
        return False

def parseRelOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Relational Operator: {lex, tok}...")
    if tok == "rel_op":
        numRow += 1
        return True
    else:
        failParse("Expected relational operator", (numLine, lex, tok), error_code=10)
        return False

def parseAddOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Additive Operator: {lex, tok}...")
    if tok == "add_op":
        numRow += 1
        return True
    else:
        failParse("Expected additive operator", (numLine, lex, tok), error_code=10)
        return False

def parseMultOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Multiplicative Operator: {lex, tok}...")
    if tok == "mult_op":
        numRow += 1
        return True
    else:
        failParse("Expected multiplicative operator", (numLine, lex, tok), error_code=10)
        return False

def parsePowerOp():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Power Operator: {lex, tok}...")
    if lex == "**":
        numRow += 1
        return True
    else:
        failParse("Expected power operator", (numLine, lex, tok), error_code=10)
        return False

#---------------------------------------------
def parseOut():
    print("Parsing Out Statement...")
    parseToken('println', "keyword")
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'println'")
    numLine, lex, tok = getSymb()
    if tok == 'text':
        parseText()
    else:
        parseExpression()
    parseToken(')', 'bracket', "Expected closing bracket ')'")
    return True

def parseText():
    global numRow
    numLine, lex, tok = getSymb()
    print(f"Parsing Text: {lex, tok}...")
    if tok == 'text':
        numRow += 1
        return True
    else:
        failParse("Expected text", (numLine, lex, tok), error_code=11)
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
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'for'")
    parseInit()
    parseToken(';', 'punct', "Expected ';'")
    parseBoolExpr()
    parseToken(';', 'punct', "Expected ';'")
    parseUpdate()
    parseToken(')', 'bracket', "Expected closing bracket ')'")
    parseToken('{', 'brace', "Expected opening brace '{'")
    parseStatementList()
    parseToken('}', 'brace', "Expected closing brace '}' ")
    return True

def parseInit():
    print("Parsing Init...")
    parseIdent()
    parseToken('=', 'assign_op', "Expected assignment operator '=' after identifier")  # Парсинг оператора присваивания
    parseArithmExpression()
    return True

def parseUpdate():
    print("Parsing Update...")
    parseIdent()
    parseToken('=', 'assign_op', "Expected assignment operator '=' after identifier")  # Парсинг оператора присваивания
    parseArithmExpression()
    return True
#---------------------------------------------
def parseWhileStatement():
    print("Parsing While Statement...")
    parseToken('while', "keyword")
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'while'")
    parseBoolExpr()
    parseToken(')', 'bracket', "Expected closing bracket ')'")
    parseToken('{', 'brace', "Expected opening brace '{'")
    parseStatementList()
    parseToken('}', 'brace', "Expected closing brace '}' ")
    return True

#---------------------------------------------
def parseDoWhileStatement():
    print("Parsing Do-While Statement...")
    parseToken('do', "keyword")
    parseToken('{', 'brace',"Expected opening bracket '(' after 'do'")
    parseStatementList()
    parseToken('}', 'brace', "Expected closing brace '}'")
    parseToken('while', "keyword")
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'while'")
    parseBoolExpr()
    parseToken(')', 'bracket', "Expected closing bracket ')'")
    return True

#---------------------------------------------
def parseIfStatement():
    print("Parsing If Statement...")
    parseToken('if', "keyword")
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'if'")
    parseBoolExpr()
    parseToken(')', 'bracket', "Expected closing bracket ')'")
    parseToken('{', 'brace')
    parseStatementList()
    parseToken('}', 'brace', "Expected closing brace '}'")

    # Проверка на наличие опциональной части 'else'
    numLine, lex, tok = getSymb()
    if lex == 'else':
        parseToken('else', "keyword")
        parseToken('{', 'brace')
        parseStatementList()
        parseToken('}', 'brace')
    return True

#---------------------------------------------
def parseSwitchStatement():
    print("Parsing Switch Statement...")
    parseToken('switch', "keyword")
    parseToken('(', 'bracket', "Expected opening bracket '(' after 'switch'")
    parseExpression()
    parseToken(')', 'bracket', "Expected closing bracket ')'")
    parseToken('{', 'brace')
    parseCaseList()

    # Проверка на наличие опциональной части 'default'
    numLine, lex, tok = getSymb()
    if lex == 'default':
        parseDefaultCase()

    parseToken('}', 'brace')
    return True


def parseCaseList():
    print("Parsing Case List...")
    while True:
        numLine, lex, tok = getSymb()
        if lex == 'case':
            parseCaseStatement()
        elif lex == 'default':
            parseDefaultCase()
            break
        else:
            break



def parseCaseStatement():
    print("Parsing Case Statement...")
    parseToken('case', "keyword")
    parseExpression()
    parseToken(':', 'punct', "Expected ':'")
    while True:
        numLine, lex, tok = getSymb()
        if lex in ['case', 'default', '}']:
            break
        parseStatement()



def parseDefaultCase():
    print("Parsing Default Case...")
    parseToken('default', "keyword")
    parseToken(':', 'punct', "Expected ':'")
    parseStatementList()
    return True

def parseBreak():
    print("Parsing Break Statement...")
    parseToken('break', "keyword")
    return True

parseProgram()
