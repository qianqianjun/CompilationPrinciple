def isTerminal(k):
    if (k[0] >= 'a' and k[0] <= 'z') or \
            (k[0] >= '0' and k[0] <= '9') or \
            k[0] == 'ε' or \
            k[0] == '(' or \
            k[0] == ')' or \
            k[0] == '+' or \
            k[0] == '-' or \
            k[0] == '*' or \
            k[0] == '/' or \
            k[0] == '=':
        return True
    return False