import ssl

from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class EmailBackend(SMTPEmailBackend):
    """SMTP backend that doesn't verify the mail server's TLS certificate.

    The cPanel mail server serves a cert for webmail.<domain> with an
    incomplete chain when connecting via mail.<domain>, which fails the
    default certificate verification even though the connection itself
    is encrypted.
    """

    @property
    def ssl_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
