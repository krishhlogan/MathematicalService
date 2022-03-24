from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .managers.AlgorithmManager import handle_fibonacci, handle_ackermann, handle_factorial


# Create your views here.


@api_view(["GET"])
def fibonacci(request):
    try:
        number = request.data.get("number")
        if number is None:
            raise ValueError("Number Argument missing")
        fibonacci_number = handle_fibonacci(number)
        return Response(status=status.HTTP_200_OK,
                        data={"status": True, "result": fibonacci_number, "message": "Success"})

    except ValueError as ve:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"Exception occured. {ve}", "status": False})
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {e}"})


@api_view(["GET"])
def ackermann(request):
    try:
        print(request.data)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def factorial(request):
    try:
        print(request.data)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
