###############################################################################
# DEFINE GOOD CLASS
###############################################################################

class Good:
  #idInput (float)
  #priceInput (float)
  #quantityInput(int)
  def __init__(self, idInput, priceInput, quantityInput):
    self.goodID = idInput
    self.price = priceInput
    self.quantity = quantityInput

  def getID(self):
    return self.goodID

  def getPrice(self):
    return self.price

  def getQuantity(self):
    return self.quantity

  #quantityRequested (int)
  def decrementQuantityBy(self, quantityRequested):
    self.quantity = self.quantity - quantityRequested

  #quantityRequested (int)
  def incrementQuantityBy(self, quantityRequested):
    self.quantity = self.quantity + quantityRequested

