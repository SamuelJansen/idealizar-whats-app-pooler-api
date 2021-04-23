from python_framework import Converter, ConverterMethod

from dto import AuthenticationDto

@Converter()
class AuthenticationConverter:

    @ConverterMethod(requestClass=[AuthenticationDto.AuthenticationResponseDto])
    def toResponse(self, status) :
        return AuthenticationDto.AuthenticationResponseDto(status=status)
