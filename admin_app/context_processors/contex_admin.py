from django.shortcuts import get_object_or_404

from user_app.models import UserProfile


def user(request):
    user = None
    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, id=request.user.id)

    return {
        'new_users': UserProfile.objects.filter(status='new'),
        'user': user,
        }