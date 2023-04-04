def convertToTitle(n):
    if n <= 26:
        return chr(n+64)
    else:
        return convertToTitle((n-1)//26) + chr((n-1)%26+65)