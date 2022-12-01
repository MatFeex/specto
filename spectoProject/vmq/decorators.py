from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func (request, *args, **kwargs):
            user = request.user
            if user.username :
                if user.is_active: 
                    if user.groups.exists():#test if user exists in groups
                        group=user.groups.all()[0].name
                        if  group and (group in allowed_roles):
                            return view_func (request, *args, **kwargs)
                        else: return render(request,'vmq/error.html',{'message':f"Restricted permissions for '{user.username}' : Your request has been denied"})
                    else: return render(request,'vmq/error.html',{'message':f"Undefined permissions for '{user.username}' : access denied by default"})
                else: return render(request,'vmq/error.html',{'message':f'{user.username} is not active'})
            else: return render(request,'vmq/error.html',{'message':'Non-logged-in user : access denied'})
            #         else: messages.error(request, 'Your request has been denied: restricted permissions')
            #     else:messages.error(request, f'{user.username} is not active')
            # else: messages.error(request, f'{user.username} is not registered')
        return wrapper_func
    return decorator




# def allowed_users(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func (request, *args, **kwargs):
#             message=''
#             username='bibas'
#             user = User.objects.get(username=username)
#             if user:
#                 if user.is_active:  
#                     if user.groups.exists():#test if user exists in groups
#                         group=user.groups.all()[0].name
#                         if  group and (group in allowed_roles):
#                             return view_func (request, *args, **kwargs)
#                     else:
#                             message='not allowed to acces !'
#                             return render(request,'shortage/error.html',{'username':username,'message':message})
#                 else:
#                     message='is not active'
#                     return render(request,'shortage/error.html',{'username':username,'message':message})
#             else:  
#                 message='not found'
#                 return render(request,'shortage/error.html',{'username':username,'message':message})
#         return wrapper_func
#     return decorator
