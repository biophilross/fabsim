###############################################################################
# DEFINE PRODUCER CLASS
###############################################################################

class Producer:
  #inventory (Array of Goods)
  #rate (int)
  #id (string)
  def __init__(self, idInput, inventoryInput):
    self.inventory = inventoryInput
    self.producerID = idInput
    self.profits = 0

  def getID(self):
    return self.producerID

  def getInventory(self):
    return self.inventory

  def getProfits(self):
    return self.profits

  def getAverageGoodPrice(self):
    prices = [good.getPrice() for good in self.getInventory()]
    return sum(prices) / len(self.getInventory())

  def getAverageGoodID(self):
    ids = [good.getID() for good in self.getInventory()]
    return sum(ids) / len(self.getInventory())

  #currentGoods (Array of Goods)
  #goodDemanded (float)
  def getClosestTo(self, currentGoods, goodDemanded):
    return min(currentGoods, key = lambda good: abs(goodDemanded - good.getID()))

  #good (Good object)
  def sell(self, good):
    if good in self.inventory:
      self.profits = self.profits + good.getPrice()

  def __str__(self):
    for good in self.inventory:
      print "GoodID: " + str(good.getID()) + " Price: " + str(good.getPrice()) + "\n"