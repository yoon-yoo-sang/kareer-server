from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.services import AuthenticationService


# Create your views here.
class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        try:
            tokens = AuthenticationService().signup(**request.data)
            return Response(tokens, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        try:
            tokens = AuthenticationService().authenticate(**request.data)
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
