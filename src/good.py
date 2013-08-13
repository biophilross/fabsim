###############################################################################
# DEFINE GOOD CLASS
###############################################################################

class Good:
  #idInput (float)
  #priceInput (float)
  #quantityInput(int)
  def __init__(self, idInput, priceInput):
    self.goodID = idInput
    self.price = priceInput

  def getID(self):
    return self.goodID

  def getPrice(self):
    return self.price