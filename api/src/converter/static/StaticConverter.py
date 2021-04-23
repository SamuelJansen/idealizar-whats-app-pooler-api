from python_helper import ObjectHelper

def getValueOrDefaultValue(value, defaultValue) :
    return value if ObjectHelper.isNotNone(value) else defaultValue
