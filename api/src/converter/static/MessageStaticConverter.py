from python_helper import ObjectHelper
from domain import MessageConstants

def getLastOwnerOrDefault(lastOwner) :
    lastOwner if ObjectHelper.isNotNone(lastOwner) else MessageConstants.UNKNOWN_OWNER
