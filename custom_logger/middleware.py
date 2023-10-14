import time, json, sys, os
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

import requests, rollbar

from .models import RequestLog
from .attachments import make_attachment

import logging
db_logger = logging.getLogger('db')
rollbar.init(os.environ.get('ROLLBAR_ACCESS_TOKEN'), settings.ENVIRONMENT)

        
SENSITIVE_KEYS = ('password', 'token', 'access', 'refresh')

class LogAllMiddleware(MiddlewareMixin):

    def process_request(self,request):

        #attach request time to the request object
        request.cl_request_time = time.time()

        #We cannot read request body more than once. So we make a duplicate of it
        request.dup_body = request.body

        try:
            rlog = RequestLog.objects.create(
                user = request.user if request.user.is_authenticated else None,
                request_url = request.build_absolute_uri(),
                request_querystring = request.META['QUERY_STRING'],
                request_headers = self.mask_sensitive_data(request.headers),
                request_body = self.mask_sensitive_data(request.dup_body),
                request_method = request.META['REQUEST_METHOD'],
                duration = 0.00 #Just a placeholder
            )
            request.__uid = rlog.id

        except Exception as e:
            db_logger.exception(msg=e)
        

        return None

    def mask_sensitive_data(self, value):
        """
        Hide sensitive keys specified in sensitive_keys from the dictionary.
        Loops recursively over nested dictionaries.
        """
        try:
            dictionary = json.loads(str(value, 'utf-8'))
        except:
            return str(value)

        if isinstance(dictionary, dict):
            dict_copy = dictionary.copy()  #Used as iterator to avoid the 'DictionaryHasChanged' error
            for field in dict_copy.keys():
                if field in SENSITIVE_KEYS:
                    dictionary[field] = '*' * len(dictionary[field])
                if isinstance(dictionary[field], dict):
                    self.mask_sensitive_data(dictionary[field])
        return dictionary


    def process_response(self, request, response):
        #Log api requests only, not admin pages
        if not "admin" in request.path:

            #An error in saving log shouldn't terminate the request
            try:
                log = RequestLog.objects.get(id=request.__uid)
                log.duration = time.time() - request.cl_request_time
                log.response_body = self.mask_sensitive_data(response.content)
                log.response_status = response.status_code

                log.save()

            except Exception as e:
                db_logger.exception(msg=e)

        return response

    def process_exception(self, request, exception):
        #Log the exception details
        db_logger.exception(exception)
        rollbar.report_exc_info(sys.exc_info(), request)


        # if not settings.DEBUG:
            
        #     #Notify on slack
        #     #TODO: Make request async
        #     main_text = "Centricity Annotation API has reported an error!"

        #     data = {
        #         'payload': json.dumps({'text': main_text, 'attachments': make_attachment(request, exception)}),
        #     }
        #     webhook_url = "https://hooks.slack.com/services/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"
        #     r = requests.post(webhook_url, data=data)

        return None
