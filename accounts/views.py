from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.http import JsonResponse, FileResponse
from django.views.generic import View, UpdateView
from django.contrib.auth.views import LogoutView, LoginView, FormView
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from .models import User
from .forms import *
from market.utils import *
from market.models import *
from market.forms import *

import io
from reportlab.pdfgen import canvas


class EmployeeRegisterView(View):
    def get(self, request):
        form = EmployeeRegisterForm()
        return render(request, 'accounts/employee/register.html', context={'form': form})

    def post(self, request):
        bound_form = EmployeeRegisterForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()

            email = bound_form.cleaned_data['email']
            password = bound_form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home_page_url')
        return render(request, 'accounts/employee/register.html', context={'form': bound_form})


class EmployerRegisterView(View):
    def get(self, request):
        form = EmployerRegisterForm()
        return render(request, 'accounts/employer/register.html', context={'form': form})

    def post(self, request):
        bound_form = EmployerRegisterForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()

            email = bound_form.cleaned_data['email']
            password = bound_form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home_page_url')
        return render(request, 'accounts/employer/register.html', context={'form': bound_form})


class UserLoginView(FormView):
    form_class = UserLoginForm
    success_url = 'home_page_url'
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Вход'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home_page_url')


class ProfileDetailView(View):
    model = User
    template = 'accounts/user_detail.html'

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def get(self, request):
        obj = get_object_or_404(self.model, id=request.user.id)
        return render(request, self.template, context={'user': obj})


class ProfileUpdateView(UpdateView):
    model = User
    # form_class = EmployeeUpdateForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('profile_detail_url')

    def get_form_class(self):
        if self.request.user.role == 'employee':
            self.form_class = EmployeeUpdateForm
            return self.form_class
        else:
            self.form_class = EmployerUpdateForm
            return self.form_class

    @method_decorator(login_required(login_url=reverse_lazy('home_page_url')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class ProfileJobsPanelView(View):
    template = 'accounts/user_jobs_panel.html'

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def get(self, request):
        if request.user.role == 'employee':
            self.objects = Applicant.objects.filter(user_id=self.request.user.id).order_by('-created_at')
            self.template = 'accounts/employee/jobs_panel.html'
        else:
            self.objects = Job.objects.filter(user_id=self.request.user.id)

        paginator = Paginator(self.objects, 10)
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
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
        }

        return render(request, self.template, context=context)


class ProfileApplicantsDetailView(View):
    model = Applicant
    template = 'accounts/employer/applicants_detail.html'

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employer)
    def get(self, request):
        objs = self.model.objects.filter(job__user_id=self.request.user.id)
        objs_found = len(objs)

        paginator = Paginator(objs, 5)
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
            'is_paginated': is_paginated,
            'objs_found': objs_found,
            'prev_url': prev_url,
            'next_url': next_url,
        }

        return render(request, template_name=self.template, context=context)

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def post(self, request):
        applicant = Applicant.objects.get(id=request.POST['applicant'])
        applicant.is_filled = True
        applicant.last_date = timezone.now()
        applicant.save()
        not_filled_applicants = Applicant.objects.filter(job_id=applicant.job.id).exclude(user_id=applicant.user.id)
        not_filled_applicants.delete()

        job = Job.objects.get(id=applicant.job.id)
        job.filled = True
        job.last_date = timezone.now()
        job.price = job.price + int((job.last_date - job.created_at).days) * 2
        job.save()
        return redirect('profile_jobs_panel_url')


class AdminDashboardView(View):
    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def get(self, request):
        if request.user.role != 'admin':
            raise PermissionDenied
        else:
            jobs = Job.objects.all()

            jobs_found = len(jobs)

            paginator = Paginator(jobs, 10)
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

            return render(request, 'accounts/admin/dashboard.html', context=context)


class AdminDataDownloadView(View):
    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def get(self, request):
        if request.user.role != 'admin':
            raise PermissionDenied
        else:
            data = dict()
            data['model'] = 'Job'
            data['fields'] = [f.name for f in Job._meta.get_fields()]
            data['model_data'] = list(Job.objects.all().values())

            response = JsonResponse(data)
            response['Content-Disposition'] = 'attachment; filename=job-table-data.json'
            return response


class ProfileDataDownloadView(View):
    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employer)
    def get(self, request):
        data = dict()
        data['model'] = 'Job'
        data['fields'] = [f.name for f in Job._meta.get_fields()]
        data['model_data'] = list(Job.objects.filter(user_id=request.user.id).values())

        response = JsonResponse(data)
        response['Content-Disposition'] = 'attachment; filename=user-jobs-data.json'
        return response


class JobInviteDownloadView(View):
    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employee)
    def get(self, request, id):
        applicant = get_object_or_404(Applicant, id=id)

        if request.user.id != applicant.user.id:
            raise PermissionDenied
        else:
            buffer = io.BytesIO()

            p = canvas.Canvas(buffer)
            p.setTitle('Job Invite')
            p.drawString(50, 750, "Dear candidate!")

            text = "Our company has approved your application for a job:"
            p.drawString(50, 650, text)
            text = "\"{}\"".format(applicant.job.title)
            p.drawString(50, 630, text)
            text = "We invite you to join the team of company employees for this position."
            p.drawString(50, 610, text)

            p.drawString(50, 500, "Salary: {}$".format(applicant.job.salary))
            p.drawString(50, 480, "Company address: {}".format(applicant.job.location))
            p.drawString(50, 460, "Company email: {}".format(applicant.user.email))
            p.drawString(50, 100, "Application Acceptance Date:")
            p.drawString(50, 80, "{}".format(applicant.created_at.date()))

            p.showPage()
            p.save()

            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='job-invite.pdf')
