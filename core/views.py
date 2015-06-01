from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

import datetime
import os

from SchPark.settings import BASE_DIR
from forms import JobForm
from models import Job


class DashboardView(View):
    template_name = 'core/dashboard.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        #Render templates
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


class NewJobView(View):
    template_name = 'core/new_job.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        form = JobForm()

        #Render templates
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            now = datetime.datetime.now()
            name = request.POST['name']
            description = request.POST['description']
            interval = request.POST['interval']
            interval_options = request.POST['interval_options']
            arguments = request.POST['arguments']
            active = False
            try:
                request.POST['active']
                active = True
            except:
                pass

            file = request.FILES['file']
            file_content = file.read()
            file_name = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + name.replace(' ', '-') + '.py'
            f = open(BASE_DIR + '/job_files/' + file_name, 'w')
            f.write(file_content)
            f.close()

            #Save job
            new_job = Job(name=name, description=description, interval=interval, interval_options=interval_options, arguments=arguments, active=active, file_name=file_name)
            new_job.save()

            res = 'Job created'

        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


class JobsView(View):
    template_name = 'core/jobs.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()

        #Render templates
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


class JobView(View):
    template_name = 'core/job.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)

        #Render templates
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


@login_required
def disable_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.active = False
    job.save()
    return HttpResponseRedirect('/job/' + job_id)


@login_required
def enable_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.active = True
    job.save()
    return HttpResponseRedirect('/job/' + job_id)


@login_required
def delete_job(request, job_id):
    job = Job.objects.get(id=job_id)
    filename = job.file_name
    os.remove(BASE_DIR + '/job_files/' + filename)
    job.delete()
    return HttpResponseRedirect('/jobs/')


class SparkConsoleView(View):
    template_name = 'core/spark-console.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        #Render templates
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))
