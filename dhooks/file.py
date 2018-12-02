from typing import BinaryIO, Union


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

    def __init__(self, fp: Union[BinaryIO, str], name: str = ''):
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

    def seek(self, offset: int = 0, *args, **kwargs):
        """
        A shortcut to ``self.fp.seek``.

        """

        return self.fp.seek(offset, *args, **kwargs)

    def close(self, force=False) -> None:
        """
        Closes the file if the file was opened by :class:`File`,
        if not, this does nothing.

        Parameters
        ----------
        force: bool
            If set to :class:`True`, force close every file.

        """
        self.fp.close = self._close
        if self._manual_opened or force:
            self.fp.close()
