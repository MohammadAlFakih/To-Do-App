from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Task

def home(request):
    return render(request,'tasks/home.html')


def background(request):
    return render(request,'tasks/background.html')

class UserTaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks/user_tasks.html'
    context_object_name = 'tasks'
    paginate_by = 2
    def get_queryset(self):
        user_name = self.request.user.username
        logged_user = get_object_or_404(User,username=self.kwargs.get('username'))
        if user_name != logged_user.username:
            messages.success(self.request,"You cannot access these informations",extra_tags='warning')
            return
        return Task.objects.filter(user=logged_user).order_by('due_date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uncompleted_tasks'] = Task.objects.filter(user=self.request.user,status=0).count()
        return context
        
    
class UserTaskUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    fields = ['title','status','priority','due_date','description']
    #Make the text area unersizable
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['description'].widget.attrs['class'] = 'unresizable'
        return context
    def test_func(self):
        if self.request.user.username != self.kwargs['username']:
            return False
        return True
    def form_invalid(self,form):
        url = reverse('task_detail',kwargs={'username':self.kwargs['username'],'pk':self.kwargs['pk']})
        return redirect(url)
    def form_valid(self,form):
        messages.success(self.request,'Update Completed',extra_tags='completed')
        return super().form_valid(form)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['description'].required = False
        return form
    
class UserTaskDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Task
    def get_success_url(self):
        username = self.request.user.username
        success_url = f'/{username}'
        messages.success(self.request,"Deletion Completed",extra_tags='completed')
        return success_url
    def test_func(self):
        if self.request.user.username != self.kwargs['username']:
            return False
        return True
    
class UserTaskCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    fields = ['title','status','priority','due_date','description']
    
    #Make the text area unersizable
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['description'].widget.attrs['class'] = 'unresizable'
        return context
    
    def test_func(self):
        if self.request.user.username != self.kwargs['username']:
            return False
        return True
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        messages.success(self.request,'Creation Completed',extra_tags='completed')
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['status'].required = False
        form.fields['description'].required = False
        return form