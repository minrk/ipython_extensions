def repr_request(r, p, cycle):
    p.text('{} {}\n'.format(r.status_code, r.url))
    p.text('headers: ')
    for name in sorted(r.headers):
        p.text('  {}: {}\n'.format(name, r.headers[name]))
    p.text('\nbody ({}):\n'.format(r.headers.get('content-type', 'unknown')))
    try:
        p.pretty(r.json())
    except ValueError:
        try:
            if len(r.text) > 1024:
                p.text(r.text[:1024])
                p.text('...[%i bytes]' % len(r.content))
            else:
                p.text(r.text)
        except Exception:
            if len(r.content) > 1024:
                p.pretty(r.content[:1024])
                p.text('...[%i bytes]' % len(r.content))
            else:
                p.pretty(r.content)

def load_ipython_extension(ip):
    ip.display_formatter.formatters['text/plain'].for_type('requests.models.Response', repr_request)
