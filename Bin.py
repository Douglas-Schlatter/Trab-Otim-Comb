class Bin:
  def __init__(self, id, lowerLimit, upperLimit):
    self.id = id
    self.lowerLimit = lowerLimit
    self.upperLimit = upperLimit
    self.numberOfBalls = 0
    self.currentValue = 0
  
def UpdateValue(self):
  self.currentValue = self.numberOfBalls*(self.numberOfBalls+1)/2
  

def SetBalls(self, targetNumBalls):
  self.numberOfBalls = targetNumBalls
  UpdateValue(self)

def IsValidToPut(self):
  if(self.numberOfBalls+1<=self.upperLimit):
    return True
  else:
    return False
def IsValidToTake():
  if(self.numberOfBalls-1>=self.lowerLimit):
    return True
  else:
    return False


  