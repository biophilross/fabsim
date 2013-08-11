import goods

###############################################################################
# DEFINE PRODUCER CLASS
###############################################################################

class Producer:
  #inventory (Array of Goods)
  #rate (int)
  #id (string)
  def __init__(self, inventory, rate, idInput):
    self.inventory = inventory
    self.rate = rate
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

  def getClosestTo(self, goodDemanded):
    currentGoods = [good for good in self.getInventory() if good.getQuantity() != 0]
    if currentGoods: #currentGoods is not empty
      return min(currentGoods, key = lambda good: abs(goodDemanded - good.getID()))
    else: #there is no best good because inventory is empty
      return Good(0, 0, 0)

  #good (Good object)
  def sell(self, good):
    if good in self.inventory and good.getQuantity() > 0:
      # good.decrementQuantityBy(1)
      self.profits = self.profits + good.getPrice()

  def updateInventory(self):
    for good in self.inventory:
      good.incrementQuantityBy(self.rate)

  def __str__(self):
    for good in self.inventory:
      print "GoodID: " + str(good.getID()) + "   Price: " + str(good.getPrice()) + "  Quantity: " + str(good.getQuantity()) + "\n"

