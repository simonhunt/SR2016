def mapToLimits(value, upperLimit = 100, lowerLimit = - 100):
        output = value
        if (value > upperLimit):
            output = upperLimit
            
        elif (value < lowerLimit):
            output = lowerLimit
        return output