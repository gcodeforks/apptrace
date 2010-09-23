apptrace_URL_PATTERNS  = ['^/$']
apptrace_TRACE_MODULES = ['guestbook.py', 'handlers.py']

def webapp_add_wsgi_middleware(app):
    from apptrace.middleware import apptrace_middleware
    return apptrace_middleware(app)
