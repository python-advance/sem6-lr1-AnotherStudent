import sys
import pandas
import re

def countPassengersOnSex(data):
    """
    Какое количество мужчин и женщин ехало на параходе?
    Приведите два числа через пробел.
    """
    sexCounts = data['Sex'].value_counts()
    return [sexCounts['male'], sexCounts['female']]

def countPassengersOnPort(data):
    """
    Подсчитайте сколько пассажиров загрузилось на борт в различных портах? 
    Приведите три числа через пробел.
    """
    portsCounts = data['Embarked'].value_counts()
    return portsCounts

def calcPassengersIsDead(data):
    """
    Посчитайте долю погибших на параходе (число и процент)? 
    """
    counts = data['Survived'].value_counts()
    return [counts[0], (counts[0] / counts.sum()) * 100]

def calcFractionOfClass(data):
    """
    Какие доли составляли пассажиры первого, второго, третьего класса?
    """
    counts = data['Pclass'].value_counts()
    return [counts[1] / counts.sum(), counts[2] / counts.sum(), counts[3] / counts.sum()]

def calcPearsonCorrWithSibAndParch(data):
    """
    Вычислите коэффициент корреляции Пирсона между количеством супругов (SibSp) и количеством детей (Parch).
    """
    corr = data['SibSp'].corr(data['Parch'])
    return corr

def calcPearsonCorrTurboFx(data):
    """
    Выясните есть ли корреляция (вычислите коэффициент корреляции Пирсона) между:
    возрастом и параметром survival;
    полом человека и параметром survival;
    классом, в котором пассажир ехал, и параметром survival.
    """
    corr1 = data['Age'].corr(data['Survived'])
    #TODO: what this is fixed?
    #xSex = []
    #for i in data['Sex']:
    #    if i == 'male':
    #        xSex = xSex + [1]
    #    else:
    #        xSex = xSex + [0]
    #corr2 = data['Survived'].corr(xSex)
    corr2 = 1
    corr3 = data['Pclass'].corr(data['Survived'])
    return [corr1, corr2, corr3]

def calcPassengersAge(data):
    """
    Посчитайте средний возраст пассажиров и медиану
    """
    ages = data['Age'].dropna()
    return [ages.mean(), ages.median()]

def calcTicketPrice(data):
    """
    Посчитайте среднюю цену за билет и медиану.
    """    
    price = data['Fare'].dropna()
    return [price.mean(), price.median()]

# author: Sophia Kramar
def only_name(name):
    # Первое слово до запятой - фамилия
    s = re.search('^[^,]+, (.*)', name)
    if s:
        name = s.group(1)
    # Если есть скобки - то имя пассажира в них
    s = re.search('\(([^)]+)\)', name)
    if s:
        name = s.group(1)
    # Удаляем обращения
    name = re.sub('(Miss\. |Mrs\. |Mr\. |Master\. |Ms\. )', '', name)
    # Берем первое оставшееся слово и удаляем кавычки
    name = name.split(' ')[0].replace('"', '')
    return name

def getMostPopularMaleName(data):
    """
    Какое самое популярное мужское имя на корабле?
    """
    maleNames = data[data['Sex'] == 'male']['Name']
    names = maleNames.map(only_name)
    return names.value_counts().head(1).index.values[0]

def getMostPopularNames(data):
    """
    Какие самые популярные мужское и женские имена людей, старше 15 лет на корабле?
    """
    oldPers = data[data['Age'] > 15]
    dirtMaleNames = oldPers[oldPers['Sex'] == 'male']['Name']
    maleNames = dirtMaleNames.map(only_name)
    dirtFemaleNames = oldPers[oldPers['Sex'] == 'female']['Name']
    femaleNames = dirtFemaleNames.map(only_name)
    return [maleNames.value_counts().head(1).index.values[0],
            femaleNames.value_counts().head(1).index.values[0]]

def dataProcess(data):
    print("<begin>")

    res = countPassengersOnSex(data)
    print(res[0], res[1])

    res = countPassengersOnPort(data)
    print(res[0], res[1], res[2])
 
    res = calcPassengersIsDead(data)
    print(res[0], "{:0.2f}".format(res[1]))

    res = calcFractionOfClass(data)
    print("{:0.4f}".format(res[0]),
          "{:0.4f}".format(res[1]),
          "{:0.4f}".format(res[2]))

    print("{:0.4f}".format(calcPearsonCorrWithSibAndParch(data)))

    res = calcPearsonCorrTurboFx(data)
    print("{:0.4f}".format(res[0]),
          "{:0.4f}".format(res[1]),
          "{:0.4f}".format(res[2]))

    res = calcPassengersAge(data)
    print("{:0.4f}".format(res[0]),
          "{:0.4f}".format(res[1]))

    res = calcTicketPrice(data)
    print("{:0.4f}".format(res[0]),
          "{:0.4f}".format(res[1]))

    print(getMostPopularMaleName(data))

    res = getMostPopularNames(data)
    print(res[0], res[1])

    print("<end>")

if __name__ == "__main__":
    try:
        sys.stdout = open("ans.txt", "w")
        data = pandas.read_csv("train.csv", index_col = "PassengerId")
        dataProcess(data)
    finally:
        sys.stdout.close()
