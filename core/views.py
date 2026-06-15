import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import ContactEnquiry


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)


def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html')


def services_view(request):
    return render(request, 'services.html')


def service_legal_view(request):
    return render(request, 'service_legal.html')


def service_corporate_view(request):
    return render(request, 'service_corporate.html')


def contact_view(request):
    form_data = {}
    if request.method == 'POST':
        # Honeypot: bots fill in the hidden "website" field; humans never see it
        if request.POST.get('website', '').strip():
            messages.success(request, 'Your message has been sent. We will be in touch shortly.')
            return redirect('contact')

        # Rate limit: one submission per 60 seconds per session
        now = time.time()
        last_submit = request.session.get('last_contact_submit', 0)
        if now - last_submit < 60:
            messages.error(request, 'Please wait a moment before submitting again.')
            form_data = {k: request.POST.get(k, '').strip() for k in ['name', 'email', 'subject', 'message']}
            return render(request, 'contact.html', {'form_data': form_data})

        name         = request.POST.get('name', '').strip()
        email        = request.POST.get('email', '').strip()
        subject      = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        errors = []

        if not all([name, email, subject, message_text]):
            errors.append('Please fill in all fields.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Please enter a valid email address.')

            if len(subject) > 50:
                errors.append('Subject must be 50 characters or fewer.')

            if len(message_text) > 250:
                errors.append('Message must be 250 characters or fewer.')

        form_data = {'name': name, 'email': email, 'subject': subject, 'message': message_text}

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            ContactEnquiry.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text,
            )
            request.session['last_contact_submit'] = now

            # Email notification
            plain = (
                f"New enquiry via OA Group website\n"
                f"{'─' * 40}\n"
                f"Name:    {name}\n"
                f"Email:   {email}\n"
                f"Subject: {subject}\n\n"
                f"{message_text}\n"
                f"{'─' * 40}\n"
                f"Reply directly to: {email}"
            )
            html = f"""
<div style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;max-width:560px;margin:0 auto;background:#0f0f0f;color:#D8D8D8;border:1px solid rgba(196,146,42,0.2);border-radius:4px;overflow:hidden;">
  <div style="background:#080808;padding:24px 32px;border-bottom:1px solid rgba(196,146,42,0.2);">
    <span style="font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#C4922A;">OA GROUP</span>
    <span style="font-size:11px;color:#555;margin-left:12px;">New Enquiry</span>
  </div>
  <div style="padding:32px;">
    <p style="margin:0 0 24px;font-size:20px;font-weight:400;color:#ffffff;">New message from <strong style="color:#C4922A;">{name}</strong></p>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr><td style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06);color:#777;width:80px;">From</td><td style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06);"><a href="mailto:{email}" style="color:#C4922A;text-decoration:none;">{email}</a></td></tr>
      <tr><td style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06);color:#777;">Subject</td><td style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06);color:#ffffff;">{subject}</td></tr>
    </table>
    <div style="margin-top:28px;padding:20px;background:#141414;border-left:2px solid #C4922A;border-radius:2px;">
      <p style="margin:0;font-size:15px;line-height:1.8;color:#D8D8D8;white-space:pre-wrap;">{message_text}</p>
    </div>
    <div style="margin-top:28px;">
      <a href="mailto:{email}?subject=Re: {subject}" style="display:inline-block;background:#C4922A;color:#000;padding:12px 28px;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;text-decoration:none;border-radius:2px;">Reply to {name} →</a>
    </div>
  </div>
  <div style="padding:16px 32px;background:#080808;border-top:1px solid rgba(196,146,42,0.1);font-size:11px;color:#444;">
    Sent from the OA Group contact form
  </div>
</div>"""
            send_mail(
                subject=f'OA Group — New Enquiry: {subject}',
                message=plain,
                from_email=f'OA Group <{settings.EMAIL_HOST_USER}>',
                recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                html_message=html,
                fail_silently=True,
            )

            messages.success(request, 'Your message has been sent. We will be in touch shortly.')
            return redirect('contact')

    return render(request, 'contact.html', {'form_data': form_data})
