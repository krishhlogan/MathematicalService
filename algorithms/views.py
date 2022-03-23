from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.


@api_view(["GET"])
def fibonacci(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK,data={"status":True,"message":"success"})


@api_view(["GET"])
def ackermann(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK,data={"status":True,"message":"success"})


@api_view(["GET"])
def factorial(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK,data={"status":True,"message":"success"})