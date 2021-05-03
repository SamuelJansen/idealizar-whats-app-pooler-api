from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

from dto import MessageDto

@Mapper()
class MessageMapper:

    @MapperMethod(requestClass=[[MessageDto.MessageResponseDto]])
    def fromRawMessageListToResponseDtoList(self, responseDtoList, rawMessageList=None) :
        if ObjectHelper.isNotNone(rawMessageList) :
            for rawMessage in rawMessageList :
                responseDtoList.append(self.fromRawMessageToResponseDto(rawMessage=rawMessage))

    @MapperMethod()
    def fromRawMessageToResponseDto(self, rawMessage=None) :
        if ObjectHelper.isNotNone(rawMessage) :
            errorList = []
            return MessageDto.MessageResponseDto(
                key = self.service.scan.getMessageKey(errorList, message=rawMessage),
                html = self.service.scan.getMessageHtml(errorList, message=rawMessage),
                errorList = errorList
            )
