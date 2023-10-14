
from distutils.version import StrictVersion

from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import boto3

from annotation.models import (
    Url, Task, Step, Country, Client, QueueUrlRelationship, ExtensionVersion
)
from annotation.serializers import (
    StepSerializer, StepSubmitSerializer, TaskResetSerializer, 
    UrlSerializer, AddUrlSerializer, AssignUrlSerializer, ClientSerializer, 
    CountrySerializer, UrlDeleteResetSerializer, UrlUpdateSerializer, ExtensionVersionSerializer
)

from .custom_filters import url_type_filter


class AnnotationHandler(APIView):
    """
    View handler for annotation.
    Get returns a new task while post submits data for each step
    """
    permission_classes = [IsAuthenticated, ]

    def get_next_task(self, mode: str):
        """
        Fetches a url from annotation queue and creates a new task from it
        Or retrieve an existing incomplete task
        """
        # Check and return an existing task
        user = self.request.user
        existing_task = user.tasks.filter(completed=False)
        step = None
        url = None
        annotator_queue = None
        if self.version:
            latest_version = ExtensionVersion.objects.last().version
            # returns `bool` for whether user CE is outdated or not
            if StrictVersion(self.version) < StrictVersion(latest_version):
                return Response({"detail": "You seem to be using an older version of the extension! Please upgrade to the latest version"}, 
                                    status=status.HTTP_426_UPGRADE_REQUIRED)

        if existing_task.exists():
            # A new get request should return an existing incomplete task
            task = existing_task.first()
            if task.steps.exists():
                # returning the last saved step to the CE so annotators can continue from 
                # from where they left off... SWEET!!!
                step = task.steps.last() 
            else:
                step = task.steps.create()
          
        elif user.queue:
            # fetch annotator queue urls
        
            annotator_queue = user.queue.content_object.urls.tbaq().exclude(
                            id__in=[task.url.id for task in user.tasks.all()])

            if annotator_queue.exists():
                url = annotator_queue.first()
        
        
            else:    
                # No annotator queue? Pick from tbaq urls
                tbaq = Url.objects.tbaq().exclude(
                    id__in=[task.url.id for task in user.tasks.all()])

                if tbaq.exists():
                    url = tbaq.first()
                    
        else:
            tbaq = Url.objects.tbaq().exclude(
                    id__in=[task.url.id for task in user.tasks.all()])

            if tbaq.exists():
                url = tbaq.first()

        if url:
            # CREATE A NEW TASK WITH THIS URL
            task = Task.objects.create(user=user, url=url, mode=mode)

            # UPDATE THE URL ANNOTATORS ASSIGNED COUNT IF IN ANNOTATOR MODE
            if mode == "annotator":
                url.annotators_assigned += 1
                url.save()

            # CREATE THE FIRST STEP FOR THIS TASK
            step = task.steps.create()

        if step:
            step = StepSerializer(step, context={'request': self.request})
            return Response(step.data)

        return Response({"detail": "No url to annotate at this time"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def get(self, request, **kwargs):
        """
        Gets a new task
        """
        mode = request.query_params.get(
            'mode', "annotator")  # retrieve mode or default to annotator
        self.version = request.query_params.get('version') 

        return self.get_next_task(mode)

    @swagger_auto_schema(request_body=StepSubmitSerializer, responses={200: StepSerializer})
    def post(self, request, **kwargs):
        """
        Submits annotation data for each step.
        A new step is returned after each submission or a new task if the last
        step was submitted
        """

        serializer = StepSubmitSerializer(data=request.data)
        mode = request.query_params.get('mode', "annotator")
        self.version = request.query_params.get('version') 

        if serializer.is_valid(raise_exception=True):
            request_body = serializer.validated_data
            url = request_body["url"]
            current_step = request_body["step"]
            bad_url =  request_body["step_data"].get("badUrlState")

            if bad_url:
                step = Step.objects.filter(
                    task__url__url=url, task__user=request.user).last()
                step.step_data = request_body["step_data"]
                step.save()
                step.task.state = "bad_url"
                step.task.reason_for_skipping_url =  bad_url
                step.task.completed = True
                step.task.save()

                return self.get_next_task(mode)

            else:
                try:
                    step = Step.objects.get(
                        task__url__url=url, step=current_step, task__user=request.user)
                    step.step_data = request_body["step_data"]
                    step.completed = True
                    step.save()

                except Step.DoesNotExist:
                    return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

            # IF THIS IS NOT THE LAST STEP, RETURN A NEW STEP:
            if step.next_step:
                try:
                    new_step = Step.objects.get(
                        task=step.task, step=step.next_step, task__user=request.user)
                except Step.DoesNotExist:
                    new_step = Step.objects.create(
                        task=step.task, step=step.next_step)

                new_step = StepSerializer(
                    new_step, context={'request': self.request})

                return Response(new_step.data)

            # OTHERWISE MARK TASK AS COMPLETE AND RETURN A NEW TASK/STEP
            else:
                task = step.task
                task.state = "completed"
                task.completed = True
                task.date_completed = timezone.now()
                task.save()

                # process task
                try:
                    serializer.process()
                except Exception as e:
                    return Response({'detail': f'Failed to process annotation data: {e}'}, status.HTTP_400_BAD_REQUEST)
                    
                return self.get_next_task(mode)


class ResetTask(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=TaskResetSerializer, responses={200: StepSerializer})
    def post(self, request, **kwargs):
        """
        Reset a task
        """
        serializer = TaskResetSerializer(request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                task = Task.objects.get(
                    user=request.user, url__url=serializer.validated_data["url"])
            except Task.DoesNotExist:
                return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

            # Delete all existing steps
            for step in task.steps.all():
                step.delete()

            # restart first step
            step = task.steps.create()
            step = StepSerializer(step, context={'request': self.request})
            return Response(step.data)



class TBAQCount(APIView):
    """
    Retrieve number of urls left in annotation queue
    """

    def get(self, request, **kwargs):

        return Response({"count": Url.objects.tbaq().count()})


class CEDownloadView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, **kwargs):
        s3 = boto3.client("s3")
        CE_BUCKET = settings.CE_S3_BUCKET or 'centricity-chrome-extension'

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': CE_BUCKET,
                'Key': 'centricity-chrome-extension.tgz'
            }
        )

        return HttpResponseRedirect(url)



class UrlsListView(generics.ListAPIView):
    '''List, search and filter all urls'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = UrlSerializer
    queryset = Url.objects.all().prefetch_related('country_set', 'client_set')

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q')
        status = self.request.query_params.get('status')
        url_type = self.request.query_params.get('urlType')
        priority = self.request.query_params.get('priority')
        client = self.request.query_params.get('client')
        country = self.request.query_params.get('country')
        start_date = self.request.query_params.get('startDate')
        end_date = self.request.query_params.get('endDate')

        if client:
            queryset = Client.objects.get(id=client).urls.all()
            if query:
                # regex query or normal query?
                if query.startswith('^'):
                    queryset = queryset.filter(url__iregex=query)
                else:    
                    queryset = queryset.filter(url__icontains=query)
            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if url_type:
                queryset = url_type_filter(queryset, url_type)
            if start_date and end_date:
                queryset = queryset.filter(created_at__range=[start_date, end_date])
            return queryset

        if country:
            queryset = Country.objects.get(id=country).urls.all()
            if query:
                # regex query or normal query?
                if query.startswith('^'):
                    queryset = queryset.filter(url__iregex=query)
                else:    
                    queryset = queryset.filter(url__icontains=query)
            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if url_type:
                queryset = url_type_filter(queryset, url_type)
            if start_date and end_date:
                queryset = queryset.filter(created_at__range=[start_date, end_date])
            return queryset

        if query:
            # regex query or normal query?
            if query.startswith('^'):
                queryset = queryset.filter(url__iregex=query)
            else:    
                queryset = queryset.filter(url__icontains=query)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if url_type:
            queryset = url_type_filter(queryset, url_type)
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])
        return queryset


class UrlsCreateView(APIView):
    '''Add a url, and assign to clients/countries'''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddUrlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Url was created successfully', status=status.HTTP_201_CREATED)


class ClientsListView(generics.ListAPIView):
    '''List all clients'''

    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    pagination_class = None


class CountriesListView(generics.ListAPIView):
    '''list all countries'''

    permission_classes = [IsAuthenticated]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    pagination_class = None


class ListAssignedUrlsView(generics.ListAPIView): 
    '''List all assigned urls''' 

    permission_classes = [IsAuthenticated]
    serializer_class = AssignUrlSerializer
    queryset = QueueUrlRelationship.objects.all()
    

class UrlRetrieveView(generics.RetrieveAPIView):
    '''Retrieve informations of a url'''

    permission_classes = [IsAuthenticated]
    serializer_class = UrlSerializer
    queryset = Url.objects.all()


class UrlUpdateView(generics.CreateAPIView):
    '''Edit/Assign urls in bulk/single'''

    permission_classes = [IsAuthenticated]
    serializer_class = UrlUpdateSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(UrlUpdateView, self).get_serializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Urls updated successfully')   


class UrlDeleteResetView(APIView):
    '''Delete and Reset urls in bulk/single'''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UrlDeleteResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            count = serializer.reset()
            return Response(f'{count} urls reset successfully', status=status.HTTP_205_RESET_CONTENT)

    def delete(self, request):
        serializer = UrlDeleteResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            count = serializer.destroy()   
            return Response(f'{count} urls deleted successfully', status=status.HTTP_204_NO_CONTENT)



class ExtensionVersionView(generics.CreateAPIView):
    '''Post latest version of the extension'''
    
    serializer_class = ExtensionVersionSerializer
