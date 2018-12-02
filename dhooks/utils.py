from base64 import b64encode
import types
import functools


def copy_func(f):
    # noinspection PyArgumentList
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g


def alias(*aliases):
    def decorator(func):
        new_func = copy_func(func)
        new_func.__doc__ = 'Alias for :meth:`{0.__name__}`.'.format(func)
        func._aliases = {a: new_func for a in aliases}
        return func
    return decorator


def aliased(cls):
    original_methods = cls.__dict__.copy()
    for method in original_methods.values():
        if hasattr(method, '_aliases'):
            for name, func in method._aliases.items():
                if name in original_methods.keys():
                    raise ValueError("{} already existed in {}, "
                                     "cannot create alias."
                                     .format(name, cls.__name__))
                setattr(cls, name, func)
    return cls


def mime_type(data):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data.startswith(b'\xFF\xD8') and \
            data.rstrip(b'\0').endswith(b'\xFF\xD9'):
        return 'image/jpeg'
    elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or \
            data.startswith(b'\x47\x49\x46\x38\x39\x61'):
        return 'image/gif'
    else:
        raise ValueError('Unsupported image type given.')


def bytes_to_base64_data(data):
    fmt = 'data:{mime};base64,{data}'
    mime = mime_type(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)
