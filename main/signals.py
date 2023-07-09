from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from main.models import Author


@receiver(pre_social_login)
def handle_pre_social_login(sender, request, sociallogin, **kwargs):
    print(sociallogin.user.username)
    email = sociallogin.user.email
    sociallogin.user.username = email.split("@")[0].replace(".", "-")
    # sociallogin.user.save()

# @receiver(social_account_added)
# def social_account_added_receiver(request, sociallogin, **kwargs):
    

# from django.contrib.auth import get_user_model
# from django.dispatch import receiver
# from allauth.socialaccount.signals import pre_social_login
# from main.models import Author

# User = get_user_model()

# @receiver(pre_social_login)
# def handle_social_login(sender, request, sociallogin, **kwargs):
#     user_data = sociallogin.account.extra_data

#     print(user_data)

    # # Retrieve the username from the email address
    # email = user_data.get('email')
    # first_name = user_data.get('name')
    # # last_name = user_data.get('family_name')
    # username = email.split('@')[0]

    # # Retrieve or create the User object
    # # try:
    # # user = User.objects.get(username=username)
    # # except User.DoesNotExist:
    # #     # Create a new User object if it doesn't exist
    # user = User.objects.create_user(username=username, email=email, first_name=first_name)
    # print(user)

    # # Create or update the associated Author object
    # author, created = Author.objects.get_or_create(user=user)
    # if created:
    #     # Perform any additional setup for the newly created Author object
    #     # author.dob = user_data.get('dob')
    #     # author.profile_pic = user_data.get('profile_pic')
    #     # ... set other fields as needed
    #     author.save()

    # # You now have access to the User and Author objects for further processing
    # # Example: Print the User and Author usernames
    # print(f"User: {user.username}")
    # print(f"Author: {author.user.username}")