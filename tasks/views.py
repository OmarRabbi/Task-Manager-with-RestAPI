from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from .models import Task, TaskImage
# Create your views here.

class TaskCreateView(View):
    template_name = 'task_create.html'
    success_url = '/'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        # Create the task object
        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status
        )

        # Handle image uploads
        if 'photos' in request.FILES:
            photos = request.FILES.getlist('photos')
            for photo in photos:
                TaskImage.objects.create(task=task, image=photo)

        return redirect(self.success_url)


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Fetch all tasks and prefetch related images to reduce database queries
        queryset = Task.objects.prefetch_related('images').all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

def login_page(request):
    # if request.method == "POST":
    #     data = request.POST
    #     username = data.get('username')
    #     password = data.get('password')
    #     if not User.objects.filter(username = username).exists():
    #         messages.info(request, 'Invalid username')
    #         return redirect('/login/')
    #     user = authenticate(username=username,password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('/')
    #     else:
    #         messages.info(request, 'Invalid password')
    #         return redirect('/login/')
    return render(request, 'login.html', context={'page' : 'login'})
def logout_page(request):
    logout(request)
    return redirect('/login/')
def register_page(request):
    # if request.method == "POST":
    #     data = request.POST
    #     first_name = data.get('first_name')
    #     email = data.get('email')
    #     username = data.get('username')
    #     password = data.get('password')
    #     user = User.objects.filter(username = username)
    #     if user.exists():
    #         messages.info(request, 'Username already taken')
    #         return redirect('/register/')
    #     user = User.objects.create(
    #         first_name = first_name,
    #         email = email,
    #         username = username,
    #     )
    #     user.set_password(password)
    #     user.save()
    #     messages.info(request, 'Account created Successfully')
    return render(request, 'register.html', context={'page' : 'login'})