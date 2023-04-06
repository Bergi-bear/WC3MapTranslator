import os
import re


def GetAimToken():
    print("Получаем aim токен")
    os.system("yc iam create-token > CurrentAimToken.txt")
    f = open('CurrentAimToken.txt', 'r', encoding='utf-8')
    content = f.read()
    content=re.sub(r'\n', r'', content)
    #print(content)
    print("Токен получен")
    return content


#GetAimToken()
