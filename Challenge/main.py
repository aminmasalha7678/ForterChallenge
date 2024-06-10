from thefuzz import fuzz
import csv


def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    count = 3
    billName = (billFirstName + " " + billLastName).lower()
    shipName = (shipFirstName + " " + shipLastName).lower()
    billNameOnCard = billNameOnCard.lower()
    names = [billName, shipName, billNameOnCard]
    for i in range(len(names) - 1):
        for j in range(i, len(names)):
            if i != j:
                if names[i] == names[j]:
                    count = count - 1
                elif doesContain(names[i], names[j]):
                    count = count - 1
                elif isTypo(names[i], names[j]):
                    count = count - 1
                elif isNickname(names[i], names[j]):
                    count = count - 1
            if j == 2:
                flippedName = flip(names[j])
                if names[i] == flippedName:
                    count = count - 1
                elif doesContain(names[i], flippedName):
                    count = count - 1
                elif isTypo(names[i], flippedName):
                    count = count - 1
                elif isNickname(names[i], flippedName):
                    count = count - 1
    if count == 0:
        return 1
    return count


#flips a name (used for billNameOnCard)
def flip(name):
    str = ""
    name = name.split()
    first = name[0]
    name[0] = name[len(name)-1]
    name[len(name)-1] = first
    for i in range(len(name)):
        str = str+name[i]+" "
    return str


#I'm assuming that nicknames can appear only on first names
def isNickname(name1, name2):
    name1 = name1.split()[0]
    name2 = name2.split()[0]
    with open('nicknames.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['name'].lower() == name1 or isTypo(row['name'].lower(), name1):
                if row['nickname'].lower() == name2 or isTypo(row['nickname'].lower(), name2):
                    return True
            elif row['nickname'].lower() == name1 or isTypo(row['nickname'].lower(), name1):
                if row['name'].lower() == name2 or isTypo(row['name'].lower(), name2):
                    return True
    return False


# checks if name1 is similar to name2
def isTypo(name1, name2):
    name1 = name1.split()
    name2 = name2.split()
    if len(name1) == len(name2):
        for i in range(len(name1)):
            if fuzz.ratio(name1[i], name2[i]) < 70:
                return False
    else:
        if fuzz.ratio(name1[0], name2[0]) < 70 or fuzz.ratio(name1[len(name1)-1], name2[len(name2)-1]) < 70:
            return False
    return True


# checks if name with middle names exist in names without middle names
def doesContain(str1, str2):
    str1 = str1.split()
    str2 = str2.split()
    if len(str1) == len(str2):
        return False
    else:
        if str1[0] + " " + str1[len(str1)-1] == str2[0] + " " + str2[len(str2)-1]:
            return True
        return False


if __name__ == '__main__':
    print(countUniqueNames("Debbie", "Egli", "Deborah", "Egli", "Deborah Egli"))  # 1
    print(countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"))  # 1
    print(countUniqueNames("Debora", "Egli", "Debie", "Egli", "Jad Egli"))  # 2 (contains everything nickname, typo in nickname and in regular name and different names)
    print(countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli"))  # 1
    print(countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah"))  # 1
    print(countUniqueNames("Michele", "Egli", "Deborah", "Egli", "Michele Egli"))  # 2
    print(countUniqueNames("Ahmad", "Egli", "Deborah", "Jaber", "Amin jaber masalha"))  # 3
    print(countUniqueNames("Catheen", "Egli", "Catleen", "Egli", "Kay Egli"))  # 1 (nickname with typo)
    print(countUniqueNames("Aaron Michael", "Smith", "Erin", "Smith", "Aaron Smith"))  # Expected: 1 (Aaron Michael, Erin are considered the same person)
    print(countUniqueNames("Aaron Michael", "Smith", "Ron", "Smith", "Aaron Michael Smith"))  # Expected: 1 (Aaron Michael, Ron are considered the same person)
    print(countUniqueNames("Aaron Michael", "Smith", "Ronnie", "Smith", "Aaron Michael Smith"))  # Expected: 1 (Aaron Michael, Ronnie are considered the same person)
    print(countUniqueNames("Aaro Michael", "Smith", "Erin", "Smith", "Aaron Michael Smith"))  # Expected: 1 (Aaro is a typo for Aaron, Erin is a nickname)
    print(countUniqueNames("Aaron Micheal", "Smith", "Ron", "Smith", "Aaron Michael Smith"))  # Expected: 1 (Micheal is a typo for Michael, Ron is a nickname)
    print(countUniqueNames("Aaron Michael", "Smit", "Ronnie", "Smit", "Aaron Michael Smit"))  # Expected: 1 (Smit is a typo for Smith, Ronnie is a nickname)
    print(countUniqueNames("Abel John", "Doe", "Ab", "Doe", "Abel John Doe"))  # Expected: 1 (Ab is a nickname for Abel)

