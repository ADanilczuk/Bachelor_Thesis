
def saveInTxt(fileName, dataName, data, space):
    with open(fileName+ '.txt', 'a') as file:
        file.write("%s\n" % dataName)
        for a in range(len(data)-1):
            file.write("%s" % data[a])
            file.write("%s" % space)
        file.write("%s;\n" % data[len(data)-1])