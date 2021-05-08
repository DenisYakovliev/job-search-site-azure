from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .models import *
from .forms import *
from .utils import *


def home_page(request):
    jobs = Job.objects.all().exclude(filled=True)[:6]
    popular_jobs = Job.objects.all().order_by('-views')[:3]
    return render(request, 'home.html', context={'newest_jobs': jobs, 'popular_jobs': popular_jobs})


def jobs_list(request):
    job_query = request.GET.get('job_query', '')
    location_query = request.GET.get('location', '')

    jobs = Job.objects.filter(Q(title__icontains=job_query) | Q(description__icontains=job_query),
                              Q(location__icontains=location_query) | Q(description__contains=location_query))

    jobs = jobs.exclude(filled=True)

    jobs_found = len(jobs)

    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'jobs_found': jobs_found,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }

    return render(request, 'market/jobs_list.html', context=context)


class JobDetail(View):
    template = 'market/job_detail.html'

    def get(self, request, job_id):
        model = Job
        obj = get_object_or_404(model, id=job_id)
        applicants = None

        if obj is not None:
            obj.views += 1
            obj.save()

            applicants = Applicant.objects.filter(job_id=obj.id)

        return render(request, self.template, context={model.__name__.lower(): obj, 'applicants': applicants})

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def post(self, request, job_id):
        model = ApplicantForm
        bound_form = model(request.POST, request.FILES)

        if bound_form.is_valid():
            new_object = bound_form.save(commit=False)
            new_object.user = request.user
            new_object.save()
        return self.get(request, job_id)


class JobCreate(ObjectCreateMixin, View):
    model = JobForm
    template = 'market/job_create.html'


class JobUpdate(ObjectUpdateMixin, View):
    model = Job
    template = 'market/job_update.html'
    model_form = JobForm


class JobDelete(ObjectDeleteMixin, View):
    model = Job
    template = 'market/job_delete.html'
    redirect_url = 'profile_jobs_panel_url'


class JobCancel(View):
    model = Applicant
    template = 'market/job_cancel.html'
    redirect_url = 'profile_jobs_panel_url'

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employee)
    def get(self, request, job_id):
        obj = get_object_or_404(self.model, job_id=job_id, user_id=request.user.id)
        print(obj.is_filled)
        if obj is not None:
            if obj.is_filled:
                return redirect('profile_jobs_panel_url')
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, job_id):
        obj = self.model.objects.get(user_id=request.user.id, job_id=job_id)
        obj.delete()
        return redirect(reverse(self.redirect_url))
