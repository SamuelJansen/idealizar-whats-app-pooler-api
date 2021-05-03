from python_helper import ObjectHelper
from python_framework import StaticConverter
from domain import MessageConstants

def getLastOwner(lastOwner) :
    return StaticConverter.getValueOrDefault(lastOwner, MessageConstants.UNKNOWN_OWNER)
