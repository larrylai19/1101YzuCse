mapping = {}
outputList = []

def createMap():
    print('mapping: ', end = '')
    for pair in input().split(','):
        l = pair.split(':')
        mapping[l[0]] = l[1]

def readAndConvert():
    global outputList
    with open('symbols.txt', 'r') as f:
        outputList = [s.replace(s[0], mapping[s[0]]).replace('\n', '') for s in f.readlines()]

def printRet():
    outputList.reverse()
    for s in outputList:
        print(s)

def main():
    createMap()
    readAndConvert()
    printRet()

if __name__ == '__main__':
    main()