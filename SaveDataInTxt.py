
def saveInTxt(fileName, dataName, data, space, methodName=''):
    with open(fileName+ '.txt', 'a') as file:
        if dataName!= '': file.write("%s\n" % dataName)
        if (methodName!= ''):
            file.write("%s" % methodName)
            file.write("%s" % space)
        for a in range(len(data)-1):
            file.write("%s" % data[a])
            file.write("%s" % space)
        file.write("%s \\ \n" % data[len(data)-1])