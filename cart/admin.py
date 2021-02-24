from django.contrib import admin
from django.shortcuts import render
from .models import Payment
from django.urls import path
from django.template.response import TemplateResponse
from .models import Form

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        add_urls = [
            path('client_info/', self.admin_site.admin_view(self.add_view), name="client_info"),
        ]
        return add_urls + urls

    def add_view(self, request):
        context = {
            'order_list': Form.objects.all().order_by('-created_at'),
        }
        return render(request, "admin/cart/payment/client_info.html", context)
