from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView

from house_app.views import check_user_is_staff
from site_app.forms import MainForm, SeoForm, BlockFormSet, ContactsForm, InfoForm, GalleryForm, AditGalleryForm, \
    FilesFormSet, ServiceForm
from site_app.models import Main, Block, Contacts, Seo, Info, Gallery, AditGallery, Files, Service

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class IndexSite(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main'] = Main.objects.all()
        context['blockk'] = Block.objects.all()
        context['contacts'] = Contacts.objects.all()
        return context
@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class InfoSite(TemplateView):
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Info.objects.all().first()
        context['file'] = Files.objects.all()
        context['gallery'] = Gallery.objects.all()
        context['aditGallery'] = AditGallery.objects.all()
        return context

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class ServiceSite(TemplateView):
    template_name = 'service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blockk'] = Block.objects.filter(service_id=2)
        return context

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class ContactsSite(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contacts.objects.all().first()
        return context


@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class MainAdmin(CreateView):
    model = Main
    template_name = 'main_page_admin.html'
    form_class = MainForm
    inst = Main.objects.all().first()
    obj_seo = get_object_or_404(Seo, pk=inst.seo.pk)
    qs = Block.objects.filter(service_id=1)

    def get_success_url(self):
        return reverse('main_page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['block_formset'] = BlockFormSet(queryset=self.qs, prefix='block')
        context['seo_form'] = SeoForm(instance=self.obj_seo)
        context['main_form'] = MainForm(instance=self.inst)
        return context

    def post(self, *args, **kwargs):
        self.object = None
        block_formset = BlockFormSet(self.request.POST, self.request.FILES, queryset=self.qs, prefix='block')
        main_form = MainForm(self.request.POST, self.request.FILES, instance=self.inst)
        seo_form = SeoForm(self.request.POST, instance=self.obj_seo)

        if all([main_form.is_valid(), seo_form.is_valid(), block_formset.is_valid()]):
            return self.form_valid(main_form, seo_form, block_formset)
        else:
            return self.form_invalid(main_form, seo_form, block_formset)

    def form_valid(self, main_form, seo_form, block_formset):
        mainform = main_form.save(commit=False)
        seo = seo_form.save(commit=False)
        seo.save()
        mainform.seo = seo
        blocks = block_formset.save(commit=False)
        for block in blocks:
            block.main = main_form.instance
            block.save()
        mainform.save()

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, main_form, seo_form, block_formset, **kwargs):
        print(main_form.errors)
        print(seo_form.errors)
        print(block_formset.errors)

        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(main_form=main_form, seo_form=seo_form, block_formset=block_formset))

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class ContactsAdmin(CreateView):
    model = Contacts
    template_name = 'contacts_admin.html'
    form_class = ContactsForm
    inst = Contacts.objects.all().first()
    obj_seo = get_object_or_404(Seo, pk=inst.seo.pk)


    def get_success_url(self):
        return reverse('contacts_page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_form'] = SeoForm(instance=self.obj_seo)
        context['contacts_form'] = ContactsForm(instance=self.inst)

        return context

    def post(self, *args, **kwargs):
        self.object = None
        contacts_form = ContactsForm(self.request.POST, self.request.FILES, instance=self.inst)
        seo_form = SeoForm(self.request.POST, instance=self.obj_seo)

        if all([contacts_form.is_valid(), seo_form.is_valid()]):
            return self.form_valid(contacts_form, seo_form)
        else:
            return self.form_invalid(contacts_form, seo_form)

    def form_valid(self, contacts_form, seo_form):
        contacts = contacts_form.save(commit=False)
        seo = seo_form.save(commit=False)
        seo.save()
        contacts.seo = seo
        contacts.save()

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, contacts_form, seo_form, **kwargs):
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(main_form=contacts_form, seo_form=seo_form))

@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class InfoAdmin(CreateView):

    model = Info
    template_name = 'info_admin.html'
    form_class = InfoForm
    inst = Info.objects.all().first()
    obj_seo = get_object_or_404(Seo, pk=inst.seo.pk)
    qs = Files.objects.all()

    def get_success_url(self):
        return reverse('info_page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo_form'] = SeoForm(instance=self.obj_seo)
        context['info_form'] = InfoForm(instance=self.inst)
        context['gallery_form'] = GalleryForm(self.request.POST, self.request.FILES, prefix='gal')
        context['images'] = Gallery.objects.all()
        context['adit_gallery_form'] = AditGalleryForm(self.request.POST, self.request.FILES, prefix='adit')
        context['adit_images'] = AditGallery.objects.all()
        context['files_formset'] = FilesFormSet(queryset=self.qs, prefix='files')
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        print(self.request.FILES)
        self.object = None
        info_form = InfoForm(self.request.POST, self.request.FILES, instance=self.inst)
        seo_form = SeoForm(self.request.POST, instance=self.obj_seo)
        gallery_form = GalleryForm(self.request.POST, self.request.FILES, prefix='gal')
        adit_gallery_form = AditGalleryForm(self.request.POST, self.request.FILES, prefix='adit')
        files_formset = FilesFormSet(self.request.POST, self.request.FILES, prefix='files')


        if all([info_form.is_valid(), seo_form.is_valid(), gallery_form.is_valid(), adit_gallery_form.is_valid(), files_formset.is_valid()]):
            return self.form_valid(info_form, seo_form, gallery_form, adit_gallery_form, files_formset)
        else:
            return self.form_invalid(info_form, seo_form, gallery_form, adit_gallery_form, files_formset)

    def form_valid(self, info_form, seo_form, gallery_form, adit_gallery_form, files_formset):
        print(gallery_form)
        info = info_form.save(commit=False)
        seo = seo_form.save(commit=False)
        seo.save()
        info.seo = seo
        gallery = gallery_form.save(commit=False)
        if gallery.image:
            gallery.save()
        adit_gallery = adit_gallery_form.save(commit=False)
        if adit_gallery.adit_image:
            adit_gallery.save()
        if files_formset.files:
            for file in files_formset:
                item = file.save(commit=False)
                item.save()
        info.save()

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, info_form, seo_form, gallery_form, adit_gallery_form, files_formset, **kwargs):
        print(info_form.errors)
        print(gallery_form.errors)
        print(adit_gallery_form.errors)
        print(files_formset.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(main_form=info_form, seo_form=seo_form, gallery_form=gallery_form,
                                  adit_gallery_form=adit_gallery_form, files_formset=files_formset))


def del_img(request, type, id):
    print("000000000000000000000000000000000000000000000000")
    print(type, id)
    if type == 'service':
        if id == 0:
            return redirect('service_page')
        item = Block.objects.filter(pk=id)
        item.delete()
        return redirect('service_page')
    if type == 'file':
        item = Files.objects.filter(pk=id)
        item.delete()
    if type == 'gal':
        item = Gallery.objects.filter(pk=id)
        item.delete()
    if type == 'adit':
        item = AditGallery.objects.filter(pk=id)
        item.delete()
    return redirect('info_page')
@method_decorator(user_passes_test(lambda u: check_user_is_staff(u, 'site_management'), login_url='login_admin'), name='dispatch')
class ServiceAdmin(CreateView):
    model = Service
    template_name = 'service_admin.html'
    form_class = ServiceForm
    inst = get_object_or_404(Service, id=2)
    obj_seo = get_object_or_404(Seo, pk=inst.seo.pk)
    qs = Block.objects.filter(service_id=2)

    def get_success_url(self):
        return reverse('service_page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['block_formset'] = BlockFormSet(queryset=self.qs, prefix='block')
        context['seo_form'] = SeoForm(instance=self.obj_seo)

        return context

    def post(self, *args, **kwargs):
        self.object = None
        print(self.request.POST)
        block_formset = BlockFormSet(self.request.POST, self.request.FILES, prefix='block')
        seo_form = SeoForm(self.request.POST, instance=self.obj_seo)

        if all([seo_form.is_valid(), block_formset.is_valid()]):
            return self.form_valid(seo_form, block_formset)
        else:
            return self.form_invalid(seo_form, block_formset)

    def form_valid(self, seo_form, block_formset):

        seo = seo_form.save(commit=False)
        seo.save()
        blocks = block_formset.save(commit=False)
        for block in blocks:
            block.service = self.inst
            block.save()

        messages.success(self.request, "Valid form")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, seo_form, block_formset, **kwargs):
        print(block_formset.errors)
        messages.error(self.request, "Invalid form")
        return self.render_to_response(
            self.get_context_data(seo_form=seo_form, block_formset=block_formset))
