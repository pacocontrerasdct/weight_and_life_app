from datetime import datetime as datetime

# Format Weights from DataBase to present them on the Html
def formatW(weights):

  for weight in weights:
    weight.weight = format(weight.weight, '.3f')
    weight.weight_date = datetime.date(weight.weight_date)
    
  return weights


