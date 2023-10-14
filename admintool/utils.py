
from datetime import datetime, timedelta


def metric_query_generator(lambda_name: str, metric_name: str):
    lambda_id = lambda_name.replace("-", "_")
    lambda_id = lambda_id + "_" + metric_name

    return {
        "Id": lambda_id,
        "MetricStat": {
            "Metric": {
                "Namespace": "AWS/Lambda",
                "MetricName": metric_name,
                "Dimensions": [
                    {
                        "Name": "FunctionName",
                        "Value": lambda_name
                    },
                    {
                        "Name": "Resource",
                        "Value": lambda_name
                    }
                ],
            },
            "Period": 60,
            "Stat": "Sum"
        }
    }


def leftpad(n, spaces=2):
    if spaces < 1:
        raise IndexError
    str_n = str(n)
    c = math.log(n, 10)
    m = spaces - 1
    while c < m:
        str_n = '0' + str_n
        c += 1
    return str_n


def date_n_days_ago(N: int):
    return datetime.now() - timedelta(days=N)


def return_date(days_ago: int = 1):
    d = date_n_days_ago(days_ago)
    year = d.year
    month = leftpad(d.month)
    day = leftpad(d.day)
    print(year, month, day)
    dayString = f"{year}{month}{day}"
    return dayString, year, month, day


def get_full_name(email):
    """
    At the time of writing this, we don't have full names of our users.
    This function tries to infer that from their email
    """
    full_name = email.split("@")[0]
    if "." in full_name:
        first_name, last_name = full_name.split(".")
        return {"first_name":first_name, "last_name":last_name}
    
    return {"first_name":full_name, "last_name":""}