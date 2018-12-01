import datetime


class Embed:
    """Class that represents a discord embed.

    The following parameters can be passed in during creation.

    Parameters
    -----------
    \*\*title: str, optional
        Defaults to :class:`None`.
        The title of the embed.

    \*\*description: str, optional
        Defaults to :class:`None`.
        The description of the embed.

    \*\*url: str, optional
        Defaults to :class:`None`.
        The URL of the embed.

    \*\*timestamp: str, optional
        Defaults to :class:`None`.
        The ``ISO 8601`` timestamp of the embed. If set to an empty string,
        the current time is set as the timestamp.
        
    \*\*color: int, optional
        Defaults to :class:`None`.
        The color of the embed.
    """  # noqa: W605

    __slots__ = (
        'color', 'title', 'url', 'author',
        'description', 'fields', 'image',
        'thumbnail', 'footer', 'timestamp',
    )

    def __init__(self, **kwargs):
        """Initialises an Embed object"""
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.description = kwargs.get('description')
        self.fields = kwargs.get('fields', [])

        self.timestamp = kwargs.get('timestamp', None)
        if self.timestamp == "":  # sets the timestamp to the current time
            self.timestamp = str(datetime.datetime.utcnow())

        self.author = None
        self.thumbnail = None
        self.image = None
        self.footer = None

    def del_field(self, index: int):
        """Deletes a field by index"""
        self.fields.pop(index)

    def set_title(self, title: str, url: str):
        """Sets the title of the embed"""
        self.title = title
        self.url = url

    def set_timestamp(self, time: str = None, now: bool = False):
        """Sets the timestamp of the embed.

        Parameters
        ----------
        time: :class:`str`
            The ISO 8601 timestamp.
        now: :class:`bool`
            If set to true the current time is used for the timestamp.
        """
        if now:
            self.timestamp = str(datetime.datetime.utcnow())
        else:
            self.timestamp = str(time)

    def add_field(self, name: str, value: str, inline: bool = True):
        """Adds a field."""
        field = {
            'name': name,
            'value': value,
            'inline': inline
        }
        self.fields.append(field)

    def set_author(self, name: str, icon_url: str = None, url: str = None):
        """Sets the author of the embed."""
        self.author = {
            'name': name,
            'icon_url': icon_url,
            'url': url
        }

    def set_thumbnail(self, url: str):
        """Sets the thumbnail of the embed."""
        self.thumbnail = {'url': url}

    def set_image(self, url):
        """Sets the image of the embed."""
        self.image = {'url': url}

    def set_footer(self, text: str, icon_url: str = None):
        """Sets the footer of the embed."""
        self.footer = {
            'text': text,
            'icon_url': icon_url
        }

    def to_dict(self) -> dict:
        """Turns the object into a dictionary."""
        return {
            key: getattr(self, key)
            for key in self.__slots__
            if hasattr(self, key) and getattr(self, key)
        }
