import json
import os
import re

import requests

from GetAimToken import GetAimToken


def TranslateOnceString(texts, IAM_TOKEN):
    folder_id = 'b1gsnj5934aaighejk5g'
    target_language = 'ru'
    translatedString = ""
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
        "sourceLanguageCode": "zh"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }
    # print("Начинаем перевод фразы " + texts)
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    if response.status_code == 200:
        data = response.text
        json_dec = json.loads(data)
        translatedString = json_dec['translations'][0]['text']
    else:
        print("Что то пошло не так, попробуйте позже")
        print(response.text)
    return translatedString


def TranslateWTS(path, mapName):
    print("Открываем war3map.wts из папки " + path)
    if not os.path.exists(path):
        print("Переводить нечего!, завершаем работу")
        return False
    clearWTS(path + '\\war3map.wts')
    GetCleanText(path, mapName)


def ExtractMap(map):
    path = "Folder_" + map
    if os.path.exists(map):
        if not os.path.exists(path):
            print("Распаковываем карту " + path)
            print("mpqtool extract " + "\"" + map + "\"" + " -o " + "\"" + "./" + path + "\"")
            os.system("mpqtool extract " + "\"" + map + "\"" + " -o " + "\"" + "./" + path + "\"")
        else:
            print(path + " уже существует, распаковка не требуется")
    else:
        print("Файл " + map + " не существует")
    return path


def FindAllMaps(fileDir):
    print("Ищем все карты внутри внутри кампании " + fileDir)
    fileExt = r".w3x"
    list = []
    for i in os.listdir(fileDir):
        if i.endswith(fileExt):
            list.append(i)
    print("Найдено карт для перевода " + str(len(list)))
    return list


def StarProgram():
    # IAM_TOKEN = GetAimToken()
    AllMaps = FindAllMaps(WORK_FOLDER)
    k = 0
    for mapName in AllMaps:
        if k >= 0:
            print("Начинаем работу с " + mapName)
            path = ExtractMap(WORK_FOLDER + "\\" + mapName)
            TranslateWTS(path, mapName)
        k = k + 1


def clearWTS(wts):
    print("Очищаем файл " + wts + " от комментариев")
    f = open(wts, 'r', encoding='utf-8', errors='ignore')
    contents = f.read()
    text = re.sub(r'//.*\n', "", contents)
    f.close()
    print("Перезаписываем файл " + wts)
    f = open(wts, 'w', encoding='utf-8')
    f.write(str(text))
    f.close()
    print("файл очищен")
    # print(contents)


def getStringNumber(contents):
    regex = r'STRING .*\n'
    text = re.findall(regex, contents)
    list1 = []
    list2 = []
    result = [[], []]
    for i in text:
        list1.append(i[6:len(i) - 1])
    # print(list1)
    regex = r'\{\n.*\n\}'
    text = re.findall(regex, contents)
    for i in text:
        list2.append(i[2:len(i) - 2])
    # print(list2)
    result[0] = list1
    result[1] = list2
    k = 5
    # print(result[0][k], result[1][k]) # пример получения элемента k
    return result


def GetCleanText(path, mapName):
    print("Дробим и очищаем строки")
    f = open(path + '\\war3map.wts', 'r', encoding='utf-8', errors='ignore')
    contents = f.read()
    wtsText = getStringNumber(contents)
    # print(contents)
    IAM_TOKEN = GetAimToken()
    newWTS = ""
    k = 0
    for i in wtsText[1]:
        translatedString = TranslateOnceString(i, IAM_TOKEN)
        cleanString = translatedString.replace('/', '|')
        print(cleanString)
        newWTS = newWTS + "STRING" + wtsText[0][k] + "\n" + "{\n" + cleanString + "\n}\n"
        k = k + 1
    # print(newWTS)
    file = open(path + '\\war3map#0419.wts', 'w+', encoding='utf-8')
    file.write(str(newWTS))
    file.close()
    print("Перепаковываем карту обратно")
    os.system("mpqtool new ./" + "\"" + "" + path + "\"" + " " + "\"" + "Translated\\" + mapName + "\"")


# path = ExtractMap("1.w3x")
# TranslateWTS(path)
# clearWTS("Folder_ChinaCampaings\FB02.w3x\war3map.wts")
WORK_FOLDER = "ChinaCampaings"  # имя папки

StarProgram()
# TranslateWTS("Folder_ChinaCampaings\CAMERA B.w3x", "CAMERA B.w3x")
# GetCleanText("Folder_ChinaCampaings\PAGE02.w3x","Folder_ChinaCampaings\PAGE02.w3x\war3map.wts")
