import RandomRNAStringGenerator
import time


#The BWT table struct holds all of our important information
class BWTTable:
    n = None
    alphabet = None
    sa = None
    bwt = None
    rsa = None
    cTable = None
    oIndex = None
    oTable = None

    def __init__(self, n):
        if n == None:
            raise Exception("Input string is required!")
        if type(n) != type("This is a string"):
            raise Exception("Input has to be a string!")

        self.n = n
        self.findAlphabet()

        self.generateSuffixArray()

        self.genCTable()
        self.genOTable()



    #Naive solutions ---------------------------------------------------------------------------------------------------
    def generateSuffixArray(self):
        suffixes = []
        for i in range(len(self.n)):
            suffixes.append(self.n[i: len(self.n)] + self.n[0: i])

        suffixArray = []
        for s in sorted(suffixes):
            suffixArray.append(suffixes.index(s))
        self.sa = suffixArray


    def generateBWT(suffixes, suffixArray):
        bwt = ""
        for i in range(len(suffixArray)):
            bwt += suffixes[suffixArray[i]][-1]
        return bwt


    def exactSearch(n, k):
        matches = []
        for i in range(len(n)):
            if n[i : i + len(k)] == k:
                matches.append(i)

        return matches


    def approximateSearch(n, k, threshHold=0):
        matches = []
        for i in range(len(n) - len(k)):
            hammingDistance = 0
            for j in range(i, i + len(k)):
                if n[j] != k[j - i]:
                    hammingDistance += 1
                    if hammingDistance > threshHold:
                        break
                if j == i + len(k) - 1:
                    matches.append(i)

        return matches


    def findAlphabet(self):
        alphabet = []
        for i in self.n:
            if i not in alphabet: alphabet.append(i)
        alphabet.sort()
        self.alphabet = alphabet


    def BWTLookup(self, i):
        nIndex = self.sa[i]
        if nIndex == 0:
            return self.n[-1]
        else:
            return self.n[nIndex - 1]


    #Burrows Wheeler transformation search -----------------------------------------------------------------------------
    def genCTable (self):
        cTable = []
        for i in self.alphabet:
            cTable.append(0)
            for j in self.n:
                if i > j: cTable[self.alphabet.index(i)] += 1

        self.cTable = cTable


    def genOTable(self):
        oIndices = self.alphabet.copy()
        oTable = []

        for i in range(len(oIndices)):
            oTable.append([0])

        for i in range(len(self.n)):
            for j in range(len(oIndices)):
                if self.BWTLookup(i) == self.alphabet[j]:
                    oTable[j].append(oTable[j][i] + 1)
                else:
                    oTable[j].append(oTable[j][i])

        self.oIndices = oIndices
        self.oTable = oTable


    def initBwtSearchIter(self, k):
        L = 0
        R = len(self.n)

        #If our key is longer than our string there will be no match
        if len(k) > len(self.n):
            R = 0
            L = 1

        i = len(k) - 1

        while i >= 0 and L < R:
            a = self.oIndices[0:].index(k[i])
            L = self.cTable[a] + self.oTable[a][L]
            R = self.cTable[a] + self.oTable[a][R]
            i -= 1

        i = L
        LRI = (L, R, i)
        self.getMatchIndices(LRI)


    def getMatchIndices(self, LRI):
        matches = []
        L = LRI[0]
        R = LRI[1]

        for i in range(R - L):
            matches.append(self.sa[L + i])
        matches.sort()

        print(matches)


    def genDTable(n, alp, k, rsa, cTable, roIndex, roTable):
        dTable = []
        minEdits = 0
        L = 0
        R = len(n)

        for i in range(len(k)):
            a = roIndex[0:].index(k[i])
            L = cTable[a] + roTable[a][L]
            R = cTable[a] + roTable[a][R]

            if L >= R:
                minEdits += 1
                L = 0
                R = len(n)
            dTable.append(minEdits)

        return dTable


    def initBWTApproxSearch(n, alp, k, cTable, oIndex, oTable, maxEdits):
        L = 0
        R = len(n)
        i = len(k) - 1
        matchA = k[i]

        for i in range(1, len(alp) - 1):
            newL = cTable[a] + oTable[a][L]
            newR = cTable[a] + oTable[a][R]

            if a == matchA:
                editCost = 0
            else:
                editCost = 1

            if not maxEdits - editCost < 0:
                break
            if not newL >= newR:
                break

            edits = "M"
            recursiveApproxMatch(newL, newR, i - 1, 1, maxEdits - editCost, edits + 1)

            edits = "I"
            recursiveApproxMatch(L, R, i - 1, 0, maxEdits - 1, edits + 1)

            L = len(k)
            R = 0
            nextInterval = 0

        return L, R, nextInterval


    def recursiveApproxMatch(L, R, i, dTable, editsLeft, maxEdits , edits):
        if i >= 0:
            lowerLim = dTable[i]
        else:
            lowerLim = 0

        if editsLeft < lowerLim:
            return

        iva = [[], []]
        if i < 0:
            iva[0].append(L)
            iva[1].append(R)

        revEdits = reversed(edits)
        editsToCigar(cigar, revEdits) #todo very unsure about this

        return


    #Linear suffix array construction by almost pure induced sorting ---------------------------------------------------
    def SAIS(self):

        def classifyLAndSTypes():
            LSTypes = "S"
            inString = self.n[::-1]
            for i in range(1, len(self.n)):
                if inString[i - 1] == inString[i]:
                    LSTypes += LSTypes[i - 1]
                else:
                    if inString[i - 1] < inString[i]:
                        LSTypes += "L"
                    else:
                        LSTypes += "S"
            LSTypes = LSTypes[::-1]

            return LSTypes

        def findLMSIndices(LSTypes):
            LMSIndices = []
            if LSTypes[0] == "S": LMSIndices.append(0)
            for i in range(len(LSTypes)):
                if LSTypes[i] == "S" and LSTypes[i - 1] != "S":
                    LMSIndices.append(i)
            return LMSIndices

        def findBucketBeginnings():
            beginnings = [].append(0)
            for i in range(1, len(self.alphabet)):
                beginnings[i] = beginnings[i - 1] + buckets[i - 1]
            return beginnings

        def findBucketEnds():
            ends = [].append(buckets[0])
            for i in range(1, len(alp)):
                ends[i] = ends[i - 1] + buckets[i - 1]
            return ends

        def placeLMS(x, n, LMSIndices, ends):
            SA = []
            findBucketEnds()
            for i in range(len(n)):
                if i in LMSIndices:
                    SA[ends[x[i]]] = i


        self.sa = None #TODO


    def genBuckets(n, alphabet, sa, LMSIndices, LMSsubstrings):
        buckets = []
        for i in alphabet:
            buckets.append([i])
        print(buckets)

        for i in sa:
            for j in range(len(buckets)):
                if i[0] == buckets[j][0]:
                    buckets[j].append(i)
                    break

        for i in buckets:
            i.sort()

        return buckets



    #Pretty printing -------------------------------------------------------------------------------------------------------
    def prettyPrint(self):
        print("\nString we are working on:", self.n)
        print("In the alphabet:", self.alphabet)
        print()


        print("Suffix array:", self.sa)
        print()


        print("C table:")
        for i in range(len(self.cTable)): print(self.alphabet[i], ":", self.cTable[i])
        print()


        print("Otable:")
        printBwt = "      "
        for i in range(len(self.n)):
            printBwt += self.BWTLookup(i) + "  "
        print(printBwt)
        for i in range(len(self.oTable)):
            print(self.oIndices[i], self.oTable[i])
        print()

        print("Searching")
        self.initBwtSearchIter("iss")


#Tests -----------------------------------------------------------------------------------------------------------------
def testMississippi():
    n = "mmiissiissiippii$"
    bwtTable = BWTTable(n)
    k = "iss"
    bwtTable.prettyPrint()

def testGoogol():
    n = "googol$"
    k = ""

def testABBCABA():
    n = "ABBCABA$"
    k = "AB"

def timeTest(n, k):
    start = time.time_ns()
    s = generateSuffixes(n)
    print("Suffixes done", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    sa = generateSuffixArray(s)
    print("Sorting done", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    bwt = generateBWT(s, sa)
    print("Generated bwt", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    alp = findAlphabet(n)
    print("Generated alphabet", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    LS = LSTypes(n)
    print("Found LS types", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    LMS = findLMSSuffixes(n, LS)
    print("Found LMS", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    LMSS = findLMSSubstring(n, LMS)
    print("Found LMS substrings", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    exactSearch(n, k)
    print("Searching naive:", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    cTable = genCTable(n, alp)
    print("C table generation", (time.time_ns() - start) / 1000, "micro seconds")
    oTableTime = time.time_ns()
    oInd, oTable = genOTable(bwt, alp)
    print("O table generation", (time.time_ns() - oTableTime) / 1000, "micro seconds")
    searchTime = time.time_ns()
    lri = initBwtSearchIter(n, k, cTable, oInd, oTable)
    print("Searching", (time.time_ns() - searchTime) / 1000, "micro seconds")
    print("Total search time", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    matches = getMatchIndices(sa, lri)
    print("matching", (time.time_ns() - start) / 1000, "micro seconds")

def timeTestSeveralK(n, k):
    start = time.time_ns()
    s = generateSuffixes(n)
    print("Suffixes done", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    sa = generateSuffixArray(s)
    print("Sorting done", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    bwt = generateBWT(s, sa)
    print("Generated bwt", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    alp = findAlphabet(n)
    print("Generated alphabet", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    LS = LSTypes(n)
    print("Found LS types", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    LMS = findLMSSuffixes(n, LS)
    print("Found LMS", (time.time_ns() - start) / 1000, "micro seconds")
    start = time.time_ns()
    LMSS = findLMSSubstring(n, LMS)
    print("Found LMS substrings", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    for i in k:
        exactSearch(n, k)
    print("Searching naive:", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    cTable = genCTable(n, alp)
    print("C table generation", (time.time_ns() - start) / 1000, "micro seconds")
    oTableTime = time.time_ns()
    oInd, oTable = genOTable(bwt, alp)
    print("O table generation", (time.time_ns() - oTableTime) / 1000, "micro seconds")
    searchTime = time.time_ns()
    for i in k:
        lri = initBwtSearchIter(n, i, cTable, oInd, oTable)
    print("Searching", (time.time_ns() - searchTime) / 1000, "micro seconds")
    print("Total search time", (time.time_ns() - start) / 1000, "micro seconds")
    print()

    start = time.time_ns()
    matches = getMatchIndices(sa, lri)
    print("matching", (time.time_ns() - start) / 1000, "micro seconds")

#testGoogol()
testMississippi()
#testRandomNucleotideString(100, 10)
#testRandomNucleotideStringMoreK(10000, 5, 100)
#testABBCABA()