import requests 
import logging 
import inspect
from functools import wraps

log = logging.getLogger("API")

class APIClient:
    def __init__(self):
        """
            Add proxy configurations and other configurations in the inherited classes.
        """
        self.session = requests.Session()

    def _log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.debug("Function called.", func.__name__)
            arguments = inspect.signature(func).bind(*args, **kwargs)
            arguments.apply_defaults()
            for (k,v) in dict(arguments.arguments).items():
                log.debug(f'{k.capitalize()}:{v}')
            result = func(*args, **kwargs)
            if(result.is_success):
                log.info(f'Response: Success {result.success["message"]}')
            else:
                log.error(f'Response: Failure {result.error}')
            return result
        return wrapper


    @_log 
    def post(self, endpoint, payload, headers= {}):
        headers["Content-Type"] = "application/json"
        resp = self.session.post(endpoint, json=payload, headers=headers)
        return Result(resp)

    @_log
    def delete(self, endpoint, params={}, headers={}):
        resp = self.session.delete(endpoint, params=params, headers=headers)
        return Result(resp)
    
    @_log
    def get(self, endpoint, params={}, headers={}):
        resp = self.session.get(endpoint, params=params, headers=headers)
        return Result(resp)



class Result:
    def __init__(self, response):
        self.is_success = (response.status_code == 200)
        if self.is_success:
            self.success = response.json()
        else:
            self.error = Error(response)

    def get_value_or_404(self, key):
        if self.is_success:
            if key in self.success.keys():
                return self.success[key]
            else:
                raise ValueError("Key not found")
        else:
            raise self.error

class Error(RuntimeError):
    def __init__(self, errorResponse):
        self.error_code = errorResponse.status_code
        try:
            self.error_message = errorResponse.json()["message"]
        except:
            self.error_message = "Error message not found."

