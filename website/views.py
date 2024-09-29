from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as conf_settings
from .models import Store, Medicine
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')
        
def service(request):
    return render(request, 'website/service.html')

def pricing(request):
    return render(request, 'website/pricing.html')

def blog(request):
    return render(request, 'website/blog.html')

def blog_details(request):
    return render(request, 'website/blog_details.html')

def catalogue(request):
    return render(request, 'website/catalogue.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['message_name']
        email = request.POST['message_email']
        message = request.POST['message']
        
        #send email to default address
        send_mail(
            'Follow up required for - ' + name,
            message,
            email,
            [conf_settings.CONTACT_US_FORM_EMAIL_TO],
            fail_silently=False,
        )

        messages.success(request, f'Hi {name}, Thanks for contacting us. We will follow up with you within next few business days.')
        return redirect('contact')
    else:
        return render(request, 'website/contact.html')

def store(request):
    stores = Store.objects.all()
    return render(request, 'website/store.html', {'stores': stores})

def genstores(request):
    stores = Store.objects.all()
    return render(request, 'website/genstores.html', {'stores': stores})

def get_districts(request):
    state = request.GET.get('state')
    districts = Store.objects.filter(store_state=state).values_list('store_district', flat=True).distinct()
    return JsonResponse({'districts': list(districts)})

def get_stores(request):
    state = request.GET.get('state')
    district = request.GET.get('district')
    if state and district:
        stores = Store.objects.filter(
            store_state=state, 
            store_district=district
        ).values(
            'store_code', 
            'store_state', 
            'store_district', 
            'store_address', 
            'store_pincode', 
            'store_contact'
        )
        return JsonResponse({'stores': list(stores)})
    
    return JsonResponse({'stores': []})

@csrf_protect
def search_medicines(request):
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        # Perform your database query to get medicines matching the search query
        medicines = Medicine.objects.filter(name__icontains=search_query)

        # Prepare the response
        results = []
        for med in medicines:
            results.append({
                'name': med.name,
                'price': med.price,
                'description': med.description,
                'image': med.image.url if med.image else '/path/to/default/image.jpg'  # Fallback if no image
            })

        return JsonResponse({'medicines': results})

