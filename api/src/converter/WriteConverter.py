from python_framework import Converter, ConverterMethod

from dto import WriteDto, MessageWriteDto

@Converter()
class WriteConverter:

    @ConverterMethod(requestClass=[[MessageWriteDto.MessageWriteResponseDto]])
    def toResponseDto(self, messageResponseDtoList) :
        return WriteDto.WriteResponseDto(
            messageWriteList = messageResponseDtoList
        )
