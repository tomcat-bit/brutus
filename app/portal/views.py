import io
import csv
from django.shortcuts import render, redirect
from django.conf import settings
from http import HTTPStatus
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from portal.models import Record
from portal.form import CSVForm

def home(request):
    records = Record.objects.get_queryset().order_by('seq')
    page = request.GET.get('page', 1)
    num_records = Record.objects.all().count()

    paginator = Paginator(records, 10)
    try:
        recs = paginator.page(page)
    except PageNotAnInteger:
        recs = paginator.page(1)
    except EmptyPage:
        recs = paginator.page(paginator.num_pages)

    return render(request, 'portal/home.html', {'records': recs, 'num_records': num_records})

# Upload a CSV file and insert Record models into the database
def upload(request):
    if request.method == 'POST':
        if len(request.FILES) == 0:
            return render(request, 'portal/upload.html', {'error': 'No file was selected'}, status=HTTPStatus.NO_CONTENT)

        file = request.FILES['file']
        try:
            data_set = file.read().decode('UTF-8')
        except UnicodeDecodeError as e:
            return render(request, 'portal/upload.html', {'error': "Could not decode file"}, status=HTTPStatus.BAD_REQUEST)

        io_string = io.StringIO(data_set)
        next(io_string)

        # Blocking inserts. Might do bulk transaction instead
        for column in csv.reader(io_string, delimiter=','):
            try:
                _, created = Record.objects.update_or_create(
                    seq=column[0],
                    first_name=column[1],
                    last_name=column[2],
                    age=column[3],
                    street=column[4],
                    city=column[5],
                    state=column[6],
                    latitude=column[7],
                    longitude=column[8],
                    ccnumber=column[9]
                )
            except IndexError as e:
                return render(request, 'portal/upload.html', {'error': e}, status=HTTPStatus.BAD_REQUEST)

        return render(
            request, 'portal/upload.html', 
            {'message': 'Succsessfully uploaded records to database'},
            status=HTTPStatus.CREATED)

    return render(request, 'portal/upload.html', status=HTTPStatus.OK)

# Find a record, given a sequence number (key)
def search_result(request):
    key = request.POST.get('seq', None)
    if key:
        try:
            result = Record.objects.filter(seq=key)
            if result:
                return render(request, 'portal/search_result.html', {"result": result.get()}, status=HTTPStatus.OK)
        except ValueError:
                return render(request, 'portal/search_result.html', {"error": "Key is not an integer"}, status=HTTPStatus.OK)

    error = "Could not find record with the given key"
    return render(
        request, 
        'portal/search_result.html', 
        {"error": error}, 
        status=HTTPStatus.NOT_FOUND)
