import json
import boto3
from datetime import datetime, timedelta, date, time

from django.db.models import Count
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from admintool.utils import date_n_days_ago, metric_query_generator, get_full_name
from annotation.models import Url, Task
from users.models import User
from admintool.serializers import DataStatusSerializer
from admintool.models import DataStatus


cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")


class StatusView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, **kwargs):
        seven_days_ago = date_n_days_ago(7)
        today = date_n_days_ago(0)
        metric_names = [
            "Errors"
        ]
        lambda_names = [
            "bees-wax-data-processor-dev-daily_event_table",
            "bees-wax-data-processor-dev-daily_page_view_table",
            "bees-wax-data-processor-dev-daily_traffic_table",
            "bees-wax-data-processor-dev-domain_url_pageviews_view",
            "bees-wax-data-processor-dev-daily_priority_queue_urls",
            "bees-wax-data-processor-dev-daily_priority_queue_domains",
            "bees-wax-data-processor-dev-daily_athena_cleanup",
            "completed-tasks-dev-completed_tasks",
            "new-intent-table-dev-create_intent_table",
            "new-annotation-apis-dev-schedules_update_labelled_urls"
        ]

        metric_queries = []
        for lambda_f in lambda_names:
            for metric in metric_names:
                metric_queries.append(metric_query_generator(lambda_f, metric))

        response = cloudwatch.get_metric_data(
            MetricDataQueries=metric_queries,
            StartTime=seven_days_ago,
            EndTime=today,
        )

        for metric in response["MetricDataResults"]:
            # convert the original Timestamp and Values - to format consumable by FE
            metric["data"] = [{'timestamp': timestamp, "values": values} for timestamp, values in zip(metric["Timestamps"][:10], metric["Values"][:10] )]
            del metric["Timestamps"]
            del metric["Values"]

        # message = Message(body=response)
        return Response(response)


class UrlStatsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, **kwargs):

        now = timezone.now()
        year, week, _ = now.isocalendar()

        tasks = Task.objects.filter(mode="annotator", state="completed")

        urls_qs = Url.objects.all()

        stats = [
            {"name": "all_urls", "figures": urls_qs.count()},
            {"name": "known_urls", "figures": urls_qs.filter(known=True).count()},
            {"name": "annotated_urls", "figures": tasks.count()},
            {"name": "greenlisted_urls", "figures": urls_qs.filter(status="green").count()},
            {"name": "redlisted_urls", "figures": urls_qs.filter(status="red").count()},
            {"name": "tbaq", "figures": Url.objects.tbaq().count()},
            {"name": "raw_urls", "figures": urls_qs.filter(status="amber").count()}
        ]

        tasks_this_month = tasks.filter(date_completed__month=now.month, date_completed__year=year)

        top_annotators = tasks_this_month.filter().annotate(num_tasks=Count('user')).order_by('-num_tasks')[:7]
        top_annotators = [task.user for task in top_annotators]

        top_annotators = [{"user":user.email, "count":tasks_this_month.filter(user=user).count()} for user in top_annotators]



        categories = []
        annotated_figures = []
        tasks = Task.objects.filter(mode="annotator", state="completed")

        counter = 0

        while counter < 7:
            counter += 1
            weeks_ago = now - timedelta(days=counter*7)
            last_day_of_the_week = weeks_ago + timedelta(days=5 - weeks_ago.weekday())
            weekstamp = last_day_of_the_week.strftime("%b %d")
            weeks_ago = weeks_ago.isocalendar()[1]

            annotated_figures.append(tasks.filter(date_completed__week=weeks_ago).count())
            categories.append(weekstamp)

        annotation_stats = {"categories":categories, "annotated_figures":annotated_figures}

        today = datetime.combine(date.today(), time())

        #doing a compute for the last month's id here
        last_month_id = now.month -1 if now.month > 1 else 12

        stats_breakdown = [
            {"metric":"today", "count":tasks.filter(date_completed__gte=today).count()},
            {"metric":"this_week", "count":tasks.filter(date_completed__week=week, date_completed__year=year).count()},
            {"metric":"this_month", "count":tasks.filter(date_completed__month=now.month, date_completed__year=year).count()},
            {"metric":"last_month", "count":tasks.filter(date_completed__month=last_month_id, date_completed__year=year).count()},
            {"metric":"all_time", "count":tasks.count()}
        ]


        users = [get_full_name(user.email) for user in User.objects.filter(user_type="annotator")]

        return Response(
            {"stats": stats,
            "users": users,
            "annotation_stats": annotation_stats,
            "top_annotators": top_annotators,
            "stats_breakdown": stats_breakdown}
            )


class DataStatusView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DataStatusSerializer
    queryset = DataStatus.objects.all()


@api_view(http_method_names=["get"])
@permission_classes([IsAuthenticated,])
def verify_email_for_ses(request):
    ses = boto3.client('ses', region_name="us-east-1")
    response = ses.verify_email_identity(EmailAddress = request.user.email)

    return Response(response)