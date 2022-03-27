import logging
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .managers.AlgorithmManager import handle_fibonacci, validate_input, handle_factorial

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


@api_view(["GET"])
def health_check(request):
    return Response(status=status.HTTP_200_OK, data={"message": f"PING! {datetime.now()}", "status": True})


@api_view(["GET", "POST"])
def fibonacci(request):
    try:
        number = request.data.get("number")
        validate_input(number, 1)
        number = int(number)
        fibonacci_number = handle_fibonacci(number)
        return Response(status=status.HTTP_200_OK,
                        data={"status": True, "result": fibonacci_number, "message": "Success"})

    except TypeError as te:
        print(str(te))
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"TypeError. {str(te)}", "status": False})
    except ValueError as ve:
        print(str(ve))
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"ValueError. {str(ve)}", "status": False})
    except Exception as e:
        print(str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {e}"})


@api_view(["GET", "POST"])
def ackermann(request):
    try:
        print(request.data)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def factorial(request):
    try:
        number = request.data.get("number")
        validate_input(number, 0)
        number = int(number)
        factorial_result = handle_factorial(number)
        return Response(status=status.HTTP_200_OK,
                        data={"status": True, "result": factorial_result, "message": "Success"})

    except TypeError as te:
        print(str(te))
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"TypeError. {str(te)}", "status": False})
    except ValueError as ve:
        print(str(ve))
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"ValueError. {str(ve)}", "status": False})
    except Exception as e:
        print(str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {e}"})
