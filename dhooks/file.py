class File:
    '''Data class that represents a file that can be sent to discord

    Parameters
    ----------
    fp : :class:`str` or :class:`BinaryIO`
        A filepath or a binary stream that is the file. If a filepath
        is provided, this class will open and close the file for you.
    name : :class:`str`, optional
        The name of the file that discord will use, if not provided,
        defaults to the filepath or the binary stream's name
    '''

    content_type = 'application/octet-stream'

    def __init__(self, fp, name=None):
        self.fp = fp
        self.name = name or (fp if isinstance(fp, str) else getattr(fp, 'name', 'file'))

    def open(self):
        if isinstance(self.fp, str): # its a filepath
             self.fp = open(self.fp, 'rb')
        return self.fp
    
    def close(self):
        if not isinstance(self.fp, str):
            self.fp.close()