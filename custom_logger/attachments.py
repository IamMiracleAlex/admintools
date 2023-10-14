import json, traceback

def make_attachment(request, exception):
    """
    Construct a slack style message attachment from
    request and exception
    """
    attachments = [
        {
            'title': repr(exception),
            'color': 'danger',
            "fallback": "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",

            "text": ''.join(traceback.format_tb(exception.__traceback__)),
	        "pretext": f"{type(exception).__name__} at {request.path}",

	        "color": "#D00000",
            'fields': [
                {
                    "title": "Method",
                    "value": request.META['REQUEST_METHOD'] ,
                    "short": True,
                },
                {
                    "title": "Path",
                    "value": request.path,
                    "short": True,
                },

                {
                    "title": 'GET Params',
                    "value": json.dumps(request.GET),
                    "short": False,
                },
                {
                    "title": "User",
                    "value": (request.user.email if request.user.is_authenticated else 'Anonymous'),
                    "short": True,
                },
                {
                    "title": "UA",
                    "value": request.META['HTTP_USER_AGENT'],
                    "short": False,
                },
            ],
        },

    ]

    return attachments
