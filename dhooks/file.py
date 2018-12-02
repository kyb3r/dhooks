class File:
    """
    Data class that represents a file that can be sent to discord.

    Parameters
    ----------
    fp : str or :class:`io.BytesIO`
        A file path or a binary stream that is the file. If a file path
        is provided, this class will open and close the file for you.

    name : str, optional
        The name of the file that discord will use, if not provided,
        defaults to the file name or the binary stream's name.
    """

    def __init__(self, fp, name=''):
        if isinstance(fp, str):
            self.fp = open(fp, 'rb')
            self._manual_opened = True
            self.name = name if name else fp
        else:
            self.fp = fp
            self._manual_opened = False
            self.name = name if name else getattr(fp, 'name', 'filename')
        self._close = self.fp.close
        self.fp.close = lambda: None  # prevent aiohttp from closing the file

    def seek(self, offset=0, *args, **kwargs):
        self.fp.seek(offset, *args, **kwargs)

    def close(self):
        self.fp.close = self._close
        if self._manual_opened:
            self.fp.close()
