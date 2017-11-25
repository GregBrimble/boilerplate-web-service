from functools import wraps

class Protection:

    whitelisted = None
    domain = None

    # Exemption from `authentication()`
    def login_exempt(self, f):
        if getattr(f, 'login_required', False):
            f.login_exempt = False
        else:
            f.login_exempt = True
        return f

    # Requiring login in absence of `authentication()`
    def login_required(self, f):
        if getattr(f, 'login_exempt', False):
            f.login_exempt = False

        f.login_required = True
        return f
