from django.db.models import Sum
from django.shortcuts import get_object_or_404

from house_app.models import Apartment, Account, Transfers, Invoice
from services_app.models import Tariff
from user_app.models import UserProfile


def user(request):
    user = None
    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, id=request.user.id)
        apart = Apartment.objects.filter(owner=user)
    else:
        apart = None

    return {
        'new_users': UserProfile.objects.filter(status='new'),
        'user': user,
        'message_list': user.owner_messages.all() if user else None,
        'apartments_list': apart if apart else None,
        'apartment_first': apart.first() if apart else None,
        'invoices_list': Invoice.objects.filter(apartment__owner=user).distinct('apartment_id'),
        'balance':
            Account.objects.filter(status='active', balance__gt=0).aggregate(total_balance=Sum('balance'))[
                'total_balance'],
        'debt':
            Account.objects.filter(status='active', balance__lt=0).aggregate(total_debt=Sum('balance'))[
                'total_debt'],
        'cashbox':
            Transfers.objects.filter(completed=True).aggregate(total_cash=Sum('amount'))[
                'total_cash'],
    }
