from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactEnquiry


def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html')


def services_view(request):
    return render(request, 'services.html')


def contact_view(request):
    form_data = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if not all([name, email, subject, message_text]):
            messages.error(request, 'Please fill in all fields.')
            form_data = {'name': name, 'email': email, 'subject': subject, 'message': message_text}
        else:
            ContactEnquiry.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text,
            )
            messages.success(request, 'Your message has been sent. We will be in touch shortly.')
            return redirect('contact')

    return render(request, 'contact.html', {'form_data': form_data})
