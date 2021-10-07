# import random
# import string

# from dreamaway.authentication.tools import generate_pin, get_url_appkey
# from dreamaway.authorization.tools import get_role_default
# from dreamaway.base.emails import send_mail
# from dreamaway.users.models import User


# class UserService:

#     user = None

#     def __init__(self, user=None):
#         self.user = user if user is not None else None

#     @staticmethod
#     def register(email, password, request, mail=True):
#         short_username = email.split('@')
#         num_random = random.randrange(0, 99999, 4)
#         random_username = str(short_username[0]) + str(num_random)
#         user = User.objects.create(username=random_username, email=email)
#         user.set_password(password)
#         user.roles.add(get_role_default())
#         user.save()
#         if mail:
#             pin = generate_pin(user=user, base=string.ascii_letters + string.digits, action='activate', digits=16)
#             send_mail(
#                 title='Registro | DreamAway',
#                 template='users/register.html',
#                 data={
#                     'content': pin,
#                     'destination': email,
#                     'url_from': f'{get_url_appkey(request.headers)}/confirmation/{email}/{pin}'
#                 },
#                 to_email=email
#             )

#         return user

#     def get_roles(self):
#         print(self.user)
