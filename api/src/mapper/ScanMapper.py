from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

from dto import ScanDto

@Mapper()
class ScanMapper:

    @MapperMethod(requestClass=[ScanDto.ScanRequestDto], responseClass=[ScanDto.ScanResponseDto])
    def fromRawMessageListToResponseDtoList(self, requestDto, responseDto, rawMessageList=None) :
        if ObjectHelper.isNotNone(rawMessageList) :
            responseDto.messageList = []
            self.mapper.message.fromRawMessageListToResponseDtoList(responseDto.messageList, rawMessageList=rawMessageList)
        return responseDto
