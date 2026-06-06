from django.db import models


class ContactEnquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Enquiry'
        verbose_name_plural = 'Contact Enquiries'

    def __str__(self):
        return f"{self.name} — {self.subject}"
