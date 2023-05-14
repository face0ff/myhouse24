from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView, FormView
from django.contrib import messages

from house_app.models import Apartment, Account
from house_app.views import check_user_is_staff
from user_app.forms import *
from user_app.models import Role, UserProfile


# Create your views here.

class Roles(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'roles.html'
    success_url = reverse_lazy('roles')
    qs = Role.objects.all()
    print(qs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_formset'] = RoleFormSet(queryset=self.qs, prefix='role')
        return context

    def post(self, *args, **kwargs):
        self.object = None
        formset = RoleFormSet(self.request.POST or None, queryset=self.qs, prefix='role')
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        formset.save(commit=False)
        for form in formset:
            item = form.save(commit=False)
            item.save()
        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, formset, **kwargs):
        print(formset.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(formset=formset))

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'users'), login_url='login_admin'), name='dispatch')
class UsersList(ListView):
    model = UserProfile
    template_name = 'users_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = UserProfile.objects.exclude(role_id__isnull=True)
        if self.request.GET.get('user'):
            object_list = object_list.filter(Q(last_name__icontains=self.request.GET.get('user')) |
                                       Q(first_name__icontains=self.request.GET.get('user')))
        if self.request.GET.get('role'):
            object_list = object_list.filter(role__roles=self.request.GET.get('role'))
        if self.request.GET.get('telephone'):
            object_list = object_list.filter(telephone__icontains=self.request.GET.get('telephone'))
        if self.request.GET.get('email'):
            object_list = object_list.filter(email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('status'):
            object_list = object_list.filter(status=self.request.GET.get('status'))
        paginator = Paginator(object_list, 3)  # 3 posts in each page
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            object_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            object_list = paginator.page(paginator.num_pages)

        # print(object_list.object_list)
        context['object_list'] = object_list
        context['page'] = page
        return context



class UserCreate(CreateView):
    model = UserProfile
    template_name = 'user_create.html'
    form_class = UserForm
    success_url = reverse_lazy('users_list')


class UserDetail(DetailView):
    model = UserProfile
    template_name = 'user_detail.html'


class UserUpdate(UpdateView):
    model = UserProfile
    template_name = 'user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_list')

    def form_valid(self, form):
        try:
            body_text = f"Ваш новый пароль - {form.cleaned_data['password1']}"
            send_mail('Админ молодец', body_text, None, [form.cleaned_data['email']], fail_silently=False)
            return super().form_valid(form)
        except:
            return super().form_valid(form)

def user_delete(request, pk):
    user = get_object_or_404(UserProfile, id=pk)
    user.delete()
    return redirect('users_list')

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'owner'), login_url='login_admin'), name='dispatch')
class OwnersList(ListView):
    model = UserProfile
    template_name = 'owners_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = UserProfile.objects.filter(role_id__isnull=True)

        if self.request.GET.get('filter-name') == '1':
            object_list = object_list.order_by('last_name')
        if self.request.GET.get('filter-name') == '0':
            object_list = object_list.order_by('-last_name')
        if self.request.GET.get('filter-date') == '1':
            object_list = object_list.order_by('date_joined')
        if self.request.GET.get('filter-date') == '0':
            object_list = object_list.order_by('-date_joined')
        if self.request.GET.get('id'):
            object_list = object_list.filter(user_id__icontains=self.request.GET.get('id'))
        if self.request.GET.get('name'):
            object_list = object_list.filter(Q(last_name__icontains=self.request.GET.get('name')) |
                                       Q(first_name__icontains=self.request.GET.get('name')) |
                                       Q(patronymic__icontains=self.request.GET.get('name')))
        if self.request.GET.get('email'):
            object_list = object_list.filter(email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('telephone'):
            object_list = object_list.filter(telephone__icontains=self.request.GET.get('telephone'))
        if self.request.GET.get('date'):
            object_list = object_list.filter(date_joined=self.request.GET.get('date'))
        if self.request.GET.get('status'):
            object_list = object_list.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('house'):
            object_list = object_list.filter(apartment__house=self.request.GET.get('house'))
        if self.request.GET.get('apartment'):
            apartments = Apartment.objects.select_related('owner').filter(
                number__icontains=self.request.GET.get('apartment')
            )
            owners_idx = [x.owner.id for x in apartments if x.owner]
            object_list = object_list.filter(pk__in=owners_idx)
        if self.request.GET.get('debt'):
            if self.request.GET.get('debt') == 'yes':
                personal_accounts = Account.objects.select_related('apartment',
                                                                           'apartment__owner').filter(balance__lt=0)
                owners_idx = [x.apartment.owner.id for x in personal_accounts if x.apartment and x.apartment.owner]
                object_list = object_list.filter(pk__in=owners_idx)
            else:
                personal_accounts = Account.objects.select_related('apartment',
                                                                           'apartment__owner').filter(balance__gte=0)
                owners_idx = [x.apartment.owner.id for x in personal_accounts if x.apartment and x.apartment.owner]
                object_list = object_list.filter(pk__in=owners_idx)


        paginator = Paginator(object_list, 5)  # 3 posts in each page
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            object_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            object_list = paginator.page(paginator.num_pages)
        context['object_list'] = object_list
        context['houses'] = House.objects.all()
        context['personal_accounts'] = Account.objects.select_related('apartment', 'apartment__owner').all()
        context['page'] = page
        return context


class OwnerDetail(DetailView):
    model = UserProfile
    template_name = 'owner_detail.html'

class OwnerCreate(CreateView):
    model = UserProfile
    template_name = 'owner_create.html'
    form_class = OwnerForm
    success_url = reverse_lazy('owners_list')

class OwnerUpdate(UpdateView):
    model = UserProfile
    template_name = 'owner_update.html'
    form_class = OwnerUpdateForm
    success_url = reverse_lazy('owners_list')

    def form_valid(self, form):
        try:
            body_text = f"Ваш новый пароль - {form.cleaned_data['password1']}"
            send_mail('Админ молодец', body_text, None, [form.cleaned_data['email']], fail_silently=False)
            return super().form_valid(form)
        except:
            return super().form_valid(form)


def owner_delete(request, pk):
    user = get_object_or_404(UserProfile, id=pk)
    user.status = 'disable'
    user.save()
    return redirect('owners_list')


class OwnerInvite(FormView):
    template_name = 'owner_invite.html'
    form_class = InviteForm
    success_message = 'Приглашение владельцу успешно отправлено!'
    success_url = reverse_lazy('owners_list')

    def form_valid(self, form):
        body_text = render_to_string('text.txt')
        send_mail('Приглашение в Demo CRM 24', body_text, None, [form.cleaned_data['email']], fail_silently=False)

        return super().form_valid(form)



def login_admin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        print(username , password)
        if username == 'admin@mail.com' and password == '12345678Qw':
            try:
                User = get_user_model()
                user = User.objects.get(email=username)
                login(request, user)
                return redirect('/admin')
            except:
                messages.info(request, 'Похоже админ все')

        try:
            user = UserProfile.objects.get(email=username)
            if user.role and user.check_password(password):
                login(request, user)
                return redirect('/admin')
            else:
                messages.info(request, 'Неверный пароль')
        except:
            messages.info(request, 'Неверный логин или пароль')


    context = {}
    return render(request, 'login_admin.html', context)

def login_owner(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        print(username, password)
        try:
            user = UserProfile.objects.get(Q(email=username) | Q(user_id=username))
            print(user)
            if not user.role and user.check_password(password):
                login(request, user)
                apartment = Apartment.objects.filter(owner=user.id).values('id').first()
                apart_id=apartment['id']
                url = f'/cabinet/apartment_detail/{apart_id}'
                return redirect(url)
            else:
                messages.info(request, 'Неверный пароль')
        except:
            messages.info(request, 'Неверный логин или пароль')
    context = {}
    return render(request, 'login_owner.html', context)

def logout_page(request):
    logout(request)
    return redirect('login_owner')