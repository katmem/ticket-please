from django.shortcuts import redirect

def anonymous_required(redirect_url):
    """
    Decorator that limits access to views only to non-logged-in users.
    Usage:
    @anonymous_required(redirect_url='company_info')
    def homepage(request):
        return render(request, 'homepage.html')
    """

    def _wrapped(view_func):
        def check_anonymous(request, *args, **kwargs):
            view = view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view
        return check_anonymous
    return _wrapped
