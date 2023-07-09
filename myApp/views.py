from django.shortcuts import render,get_object_or_404,redirect
from django.http import response,HttpResponse,Http404
from django.template import loader
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import files,Folder
from .encryption_util import *
from datetime import *
# @login_required(login_url='login')
def home(request):
    print(request.user.id)
    encrypted_userid = encrypt(request.user.id)
    return render(request,'index.html',{'time':datetime.now().time(),'date':date.today(),'id':encrypted_userid })



def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['password2']
        if password==confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'this Email is already in use')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request,"passwords didn't match")
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('myfiles',pk=encrypt(request.user.id))
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')

    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

# def post(request,pk):
#     user=request.user.username
#     return render(request,'post.html',{"pk":pk})
# def counter(request):
#     # text=request.POST['text']
#     # text=len(text.split())
#     # # print(text)
#     text=['user','user1','user2',]
#     return render(request, 'counter.html',{'text':text})''
# @login_required(login_url='login')

def uploading(request,pk):
        if request.method=="POST":
            aa=request.POST,request.FILES
            # print(str(aa))
            # print(aa.is_valid())
            if aa:
                client_file=request.FILES.getlist('file') 
                print(client_file)
                for fil in client_file:
                            # data=fil.save(commit=False)
                            # login_user=User.objects.get(username=request.user.username)
                            # data.user=login_user
                            # data.save()
                            folder = get_object_or_404(Folder, id=pk)
                            new_file=files(user=request.user,file=fil, folder=folder)
                            new_file.save()

                return redirect('folder_contents',folder_id=pk)
        return render(request, 'uploading.html')

@login_required(login_url='login')
def new(request):
    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        parent_folder_id = request.POST.get('parent_folder_id')
        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id)
        folder = Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
        return redirect('folder_contents', folder_id=folder.id)
    # return render(request, 'create_folder.html')
    return render(request,'new.html')

@login_required(login_url='login')
def create_folder(request,folder_id):
        if request.method == 'POST':
            folder_name = request.POST['folder_name']
            parent_folder = get_object_or_404(Folder, id=folder_id)
            folder = Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
            return redirect('folder_contents', folder_id=folder.id)
        return render(request, 'create_folder.html',{'folder_id': folder_id})

@login_required(login_url='login')
def folders(request,pk):
    pk=decrypt(pk)
    print(pk)
    user = get_object_or_404(User, id=pk)
    folders = Folder.objects.filter(user=user,parent_folder=None)

    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        parent_folder_id = request.POST.get('parent_folder_id')
        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id)
        folder = Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
        # return redirect('myfiles', folder_id=folder.id)


    return render(request, 'myfiles.html', {'folders':folders, 'files_by':user})


def folder_contents(request, folder_id):
    encrypted_userid = encrypt(request.user.id)
    folder = get_object_or_404(Folder, id=folder_id) 
    print(folder.parent_folder)
    subfolders = Folder.objects.filter(parent_folder=folder) 
    print(subfolders)
    filess = files.objects.filter(folder=folder) 
    print(files)
    print(filess)
    if request.method == 'POST':
        folder_name = request.POST['folder_name']
        parent_folder_id = request.POST.get('parent_folder_id')
        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id)
        folder = Folder.objects.create(user=request.user, name=folder_name, parent_folder=parent_folder)
        return redirect('folder_contents',folder_id=parent_folder_id)

    return render(request, 'folder_contents.html', {'folder': folder, 'subfolders': subfolders, 'files': filess, 'id':encrypted_userid})


def uploads(request,pk):
    user = get_object_or_404(User, id=pk) #
    username=user.username
    main_folder = Folder.objects.filter(user=user,parent_folder=None)
    # folder = Folder.objects.filter()
    print(main_folder)
    # print(subfolders)
    main_folders=[]
    subfolders=[]
    files_list=[]
    for folder in main_folder:
        main_folders.append(folder)
        subfolders.append(Folder.objects.filter(parent_folder=folder))
        files_list.append(files.objects.filter(folder=folder))
    print(subfolders,files_list)
    # if subfolders is None:
    #     print(subfolders)
    # else:
    #      print('no')
    # print(filess)
    context={
    'file': files.objects.filter(user=pk),
    'file_by':pk,
    'file_of':username,
    'total':len(files.objects.filter(user=pk)),
    'main_folders':main_folders,
    'subfolders':subfolders,
    'files_list':files_list

    }
    return render(request, 'uploads.html', context)

def delete_file(request,pk):
    fil=get_object_or_404(files, id=pk)
    context={
        'file_name': fil
    }
    # print(fil)
    if  request.user != fil.user:
        return HttpResponse("can't proceed unauthorized access")
    else:
        fil.delete()
    
    return render(request,'delete.html', context)

def delete_folder(request,pk):
    folder=get_object_or_404(Folder, id=pk)
    if  request.user != folder.user:
        return HttpResponse("can't proceed unauthorized access")
    else:
        folder.delete()
    return render(request, 'delete_folder.html', {'folder':folder})
