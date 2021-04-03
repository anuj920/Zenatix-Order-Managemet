from datetime import datetime

def generateOrderId():
    return "OR"+str(datetime.now().year)+datetime.now().strftime("%d%m%H%M%S")