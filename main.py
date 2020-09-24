import os
import threading
import card
import calculator
import datetime
import multiprocessing

timeList = []


def readfile(path, cards):
    """
        Reads file and parses lines.

        This reads a file line for line and parses each line to a card object.
        The card object gets appended to the given list.

        :param path: Path to file
        :param cards: list of cards
        :type path: str
        :type cards: list
    """

    assert path is not None

    file = open(path, 'r')

    for line in file.readlines():
        cards.append(parsestringtocard(line))
    file.close()

    assert cards is not None


def writefile(path, cards):
    """
        Write list of cards to file.

        This writes a list of card objects to the given path.

        :param path: Path to file
        :param cards: list of cards
        :type path: str
        :type cards: list
    """

    assert path is not None and cards is not None

    with open(path, 'w') as file:
        for c in cards:
            file.write(str(c) + '\n')

    assert os.path.isfile(path)
    file.close()

def parsestringtocard(line):
    """
        Split string into card object attributes.

        This splits a string into a card object. When the split array length is 1,
        the returned card object has only a name attribute.
        When the split array length is larger than 1, the returned card object got all attributes.

        :param line: String from file input
        :type line: str
        :return: Card object from parsed string
        :rtype: card
    """

    assert line is not None

    split = line.split('|')
    if len(split) == 1:
        c = card.Card(split[0].rstrip('\n'))
    else:
        c = card.Card(split[0], split[1], split[2], split[3], split[4].rstrip('\n'))
    assert c is not None
    return c


def correctName(scrambledCard, lists):
    """
        Search for correct name for given card.

        Compares the name of the given card with all reference cards.
        Creates a calculator object for each comparison.
        Returns new name if calculated Levensthein distance is less than 0.26, otherwise old name.

        :param scrambledCard: Single scrambled card
        :param lists: list of all required lists (scrambled cards, reference cards, repaired cards)
        :type scrambledCard: card
        :type lists: list
        :return: (new) name for the given card
        :rtype: str
    """

    assert lists is not None

    for y in range(0, len(lists[1])):

        calc = calculator.Calculator(scrambledCard.name, lists[1][y].name)

        if calc.replaceName():
            print("Correct Card name found! Changed: " + scrambledCard.name + " => " + lists[1][y].name)
            name = lists[1][y].name
            repairedCard = scrambledCard
            repairedCard.name = name
            lists[2].append(repairedCard)

            assert name is not None
            return name

    print("Correct Card name for '" + scrambledCard.name + "' cannot be found!")

    assert scrambledCard.name is not None
    assert scrambledCard.name == scrambledCard.name
    return scrambledCard.name


def correctNamesInSection(indexFrom, indexUntil, lists):
    """
        Search for correct name for scramble cards between given list indexes.

        This starts the searching task for all scramble card list items between the indexes indexFrom and indexUntil.

        :param indexFrom: Start index
        :param indexUntil: End index
        :param lists: list of all required lists (scrambled cards, reference cards, repaired cards)
        :type indexFrom: int
        :type indexUntil: int
        :type lists: list
    """

    assert 0 <= indexFrom <= indexUntil
    assert lists is not None

    for x in range(indexFrom, indexUntil):

        name = correctName(lists[0][x], lists)

        repairedCard = lists[0][x]
        repairedCard.name = name
        lists[0][x] = repairedCard

        print("(" + str(x) + "/" + str(indexUntil) + ")")
        print()

    assert lists is not None


def startMultiCorrectionProcess(multiProcess, processCount, lists):
    """
        Starts threading/multiprocessing correction task.

        This starts a given amount of threads/processes, that will search for a correct card name.
        Set multiProcess to "0" for threading, set multiProcess to "1" for multiprocessing

        :param multiProcess: whether to use threading or multiprocessing
        :param processCount: The number of threads/processes that will be used
        :param lists: list of all required lists (scrambled cards, reference cards, repaired cards)
        :type multiProcess: int
        :type processCount: int
        :type lists: list
    """

    assert 0 < processCount
    assert lists is not None

    start = datetime.datetime.now()

    pOverview = []

    for x in range(0, processCount):
        indexFrom = int(len(lists[0]) / processCount * x)
        indexUntil = int(len(lists[0]) / processCount * (x + 1))

        if multiProcess:
            pOverview.append(multiprocessing.Process(target=correctNamesInSection,
                                                     args=(indexFrom, indexUntil, lists,),
                                                     daemon=True))
        else:
            pOverview.append(threading.Thread(target=correctNamesInSection,
                                              args=(indexFrom, indexUntil, lists,),
                                              daemon=True))
        pOverview[x].start()

    for x in range(0, len(pOverview)):
        pOverview[x].join()

    end = datetime.datetime.now()
    diff = end - start
    timeList.append(diff)
    mode = "Processing" if multiProcess else "Threading"
    if multiProcess:
        print("Multi " + mode + " Correction Process tool:", diff.total_seconds(), " seconds\n")
    else:
        print("Multi " + mode + " Correction Process tool:", diff.total_seconds(), " seconds\n")

    assert lists is not None


def startSoloCorrectionProcess(lists):
    """
        Starts the correction task.

        This starts a single task, that will start searching for a correct card name.

        :param lists: list of all required lists (scrambled cards, reference cards, repaired cards)
        :type lists: list
    """

    assert lists is not None

    start = datetime.datetime.now()

    correctNamesInSection(0, len(lists[0]), lists)

    end = datetime.datetime.now()
    diff = end - start
    timeList.append(diff)
    print("Solo Correction Process tool:", diff.total_seconds(), " seconds\n")

    assert lists is not None


def main():
    scrambledCards = multiprocessing.Manager().list()
    referenceCards = []
    repairedCards = multiprocessing.Manager().list()
    lists = [scrambledCards, referenceCards, repairedCards]

    # read the files with scrambled and reference name in two processes
    threadscramblefile = threading.Thread(target=readfile, args=("files/scrambled.txt", lists[0],),
                                          daemon=True)
    threadreferencefile = threading.Thread(target=readfile, args=("files/reference.txt", lists[1],),
                                           daemon=True)
    start = datetime.datetime.now()

    threadscramblefile.start()
    threadreferencefile.start()

    threadscramblefile.join()
    threadreferencefile.join()

    end = datetime.datetime.now()
    diff = end - start
    print("File reading process took: ", diff.total_seconds(), " seconds\n")

    # start correction process
    # startMultiCorrectionProcess(1, 10, lists)
    startMultiCorrectionProcess(0, 10, lists)
    # startSoloCorrectionProcess(lists)

    writefile("files/outAll.txt", scrambledCards)
    writefile("files/outRepaired.txt", repairedCards)

    for t in timeList:
        print(t.total_seconds())


if __name__ == '__main__':
    main()
