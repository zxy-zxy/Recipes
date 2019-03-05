from django.contrib.auth import get_user_model

UserModel = get_user_model()


def create_user(email, password):
    user = UserModel.objects.create_user(
        email=email,
        password=password
    )
    return user
