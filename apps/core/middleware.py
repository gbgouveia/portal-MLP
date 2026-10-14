"""
Security and Content Security Policy (CSP) Middleware for MLP Portal.
"""

class SecurityHeadersMiddleware:
    """
    Applies security headers including Referrer-Policy and Content-Security-Policy (CSP)
    compatible with YouTube embeds, Firebase Web SDK, and Google Fonts.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Enforce strict-origin-when-cross-origin for YouTube embed referrer validity
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # CSP allowing YouTube embeds, Firebase, Google Fonts, and CDNs
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com https://www.gstatic.com https://apis.google.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' data: https: blob:; "
            "frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com https://*.firebaseapp.com; "
            "connect-src 'self' https://*.googleapis.com https://*.firebaseio.com https://identitytoolkit.googleapis.com https://securetoken.googleapis.com https://firestore.googleapis.com https://fcm.googleapis.com; "
            "media-src 'self' https: blob:;"
        )
        response['Content-Security-Policy'] = csp
        
        return response
