import logging
from datetime import datetime

import redis
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .managers.AlgorithmManager import handle_fibonacci, validate_input, handle_factorial, handle_ackermann

# Get an instance of a logger
logger = logging.getLogger('django')


@api_view(["GET"])
def health_check(request):
    logger.info(f"Healthcheck success")
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
        logger.error(msg=f"TypeError. Request data: {request.data}.", exc_info=te)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"TypeError. {str(te)}", "status": False})
    except ValueError as ve:
        logger.error(msg=f"ValueError. Request data: {request.data}.", exc_info=ve)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"ValueError. {str(ve)}", "status": False})
    except redis.exceptions.ConnectionError as ce:
        logger.critical(msg=f"Connection error. Request data: {request.data}.", exc_info=ce)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {str(ce)}"})
    except Exception as e:
        logger.error(msg=f"Exception, while calculating fibonacci. Request data: {request.data}.", exc_info=e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {e}"})


@api_view(["GET", "POST"])
def ackermann(request):
    try:
        m = request.data.get("m")
        n = request.data.get("n")
        validate_input(m, 0)
        validate_input(n, 0)
        m, n = int(m), int(n)
        ackermann_result = handle_ackermann(m, n)
        return Response(status=status.HTTP_200_OK,
                        data={"status": True, "result": ackermann_result, "message": "Success"})

    except TypeError as te:
        logger.error(msg=f"TypeError. Request data: {request.data}.", exc_info=te)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"TypeError. {str(te)}", "status": False})
    except ValueError as ve:
        logger.error(msg=f"ValueError. Request data: {request.data}.", exc_info=ve)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"ValueError. {str(ve)}", "status": False})
    except redis.exceptions.ConnectionError as ce:
        logger.critical(msg=f"Connection error. Request data: {request.data}.", exc_info=ce)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {str(ce)}"})
    except Exception as e:
        logger.error(msg=f"Exception, while calculating fibonacci. Request data: {request.data}.", exc_info=e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {e}"})


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
        logger.error(msg=f"TypeError. Request data: {request.data}.", exc_info=te)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"TypeError. {str(te)}", "status": False})
    except ValueError as ve:
        logger.error(msg=f"ValueError. Request data: {request.data}.", exc_info=ve)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"message": f"ValueError. {str(ve)}", "status": False})
    except ConnectionError as ce:
        logger.critical(msg=f"Connection error. Request data: {request.data}.", exc_info=ce)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {str(ce)}"})
    except Exception as e:
        logger.error(msg=f"Exception, while calculating fibonacci. Request data: {request.data}.", exc_info=e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"status": False, "message": f"Exception occurred. {e}"})

