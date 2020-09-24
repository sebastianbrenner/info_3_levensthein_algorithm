class Card:
    def __init__(self, name="", mana="", cmc="", category="", count=0):
        self.__name = name
        self.__mana = mana
        self.__cmc = cmc
        self.__category = category  # category = type
        self.__count = count

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, n):
        self.__name = n

    @property
    def manacost(self):
        return self.__mana

    @manacost.setter
    def manacost(self, mana):

        self.__mana = mana

    @property
    def cmc(self):
        return self.__cmc

    @cmc.setter
    def cmc(self, cmc):
        self.__cmc = cmc

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category):
        self.__category = category

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        self.__count = count

    def __str__(self):
        # custom string method
        return self.__name + "|" + self.__mana + "|" + self.__cmc + "|" + self.__category + "|" + str(self.__count)
