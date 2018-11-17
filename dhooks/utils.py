from base64 import b64encode

try:
    import ujson as json
except ImportError:
    import json


def alias(*aliases):
    def decorator(func):
        func._aliases = set(aliases)
        return func
    return decorator

def aliased(cls):
    original_methods = cls.__dict__.copy()
    for name, method in original_methods.items():
        if hasattr(method, '_aliases'):
            for alias in method._aliases - set(original_methods):
                setattr(cls, alias, method)
    return cls

def mime_type(data):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data.startswith(b'\xFF\xD8') and data.rstrip(b'\0').endswith(b'\xFF\xD9'):
        return 'image/jpeg'
    elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
        return 'image/gif'
    else:
        raise ValueError('Unsupported image type given')

def bytes_to_base64_data(data):
    fmt = 'data:{mime};base64,{data}'
    mime = mime_type(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)

def try_json(text):
    if not text:
        return None # request successful but no response.
    return json.loads(text)