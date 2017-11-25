from functools import wraps

class Protection:

    whitelisted = None
    domain = None

    # Exemption from `authentication()`
    def login_exempt(self, f):
        @wraps(f)
        def with_exemption(*args, **kwargs):
            if getattr(f, 'login_required', False):
                logging.error("Both @login_exempt and @login_required on %s. Defaulting to @login_required..." % str(f))
                f.login_exempt = False
            else:
                f.login_exempt = True
            return f
        return with_exemption

    # Requiring login in absence of `authentication()`
    def login_required(self, f):
        @wraps(f)
        def with_requirement(*args, **kwargs):
            if getattr(f, 'login_exempt', False):
                logging.error("Both @login_exempt and @login_required on %s. Defaulting to @login_required..." % str(f))
                f.login_exempt = False

            f.login_required = True
            return f
        return with_requirement
