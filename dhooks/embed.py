import datetime
from typing import Union


class Embed:
    """
    Class that represents a discord embed.

    Parameters
    -----------
    \*\*title: str, optional
        Defaults to :class:`None`.
        The title of the embed.

    \*\*description: str, optional
        Defaults to :class:`None`.
        The description of the embed.

    \*\*url: str, optional
        URL of the embed. It requires :attr:`title` to be set.

    \*\*timestamp: str, optional
        ``ISO 8601`` timestamp of the embed. If set to a "now",
        the current time is set as the timestamp.
        
    \*\*color: int (or hex), optional
        Color of the embed.
        
    \*\*image_url: str, optional
        URL of the image.
        
    \*\*thumbnail_url: str, optional
        URL of the thumbnail.
        
    """  # noqa: W605

    __slots__ = (
        'color', 'title', 'url', 'author',
        'description', 'fields', 'image',
        'thumbnail', 'footer', 'timestamp',
    )

    def __init__(self, **kwargs):
        """
        Initialises an Embed object.
        """
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.description = kwargs.get('description')

        self.timestamp = kwargs.get('timestamp')
        if self.timestamp == "now":  # sets the timestamp to the current time
            self.timestamp = str(datetime.datetime.utcnow())

        self.author = None
        self.thumbnail = None
        self.image = None
        self.footer = None
        self.fields = []

        image_url = kwargs.get("image_url")
        if image_url is not None:
            self.set_image(image_url)

        thumbnail_url = kwargs.get("thumbnail_url")
        if thumbnail_url is not None:
            self.set_thumbnail(thumbnail_url)

    def del_field(self, index: int) -> None:
        """
        Deletes a field by index.

        Parameters
        ----------
        index: int
            Index of the field to delete.

        """
        self.fields.pop(index)

    def set_title(self, title: str, url: str = None) -> None:
        """
        Sets the title of the embed.

        Parameters
        ----------
        title: str
            Title of the embed.

        url: str or None, optional
            URL hyperlink of the title.

        """
        self.title = title
        self.url = url

    def set_timestamp(self, time: Union[str, datetime.datetime] = None,
                      now: bool = False) -> None:
        """
        Sets the timestamp of the embed.

        Parameters
        ----------
        time: str or :class:`datetime.datetime`
            The ``ISO 8601`` timestamp from the embed.

        now: bool
            Defaults to :class:`False`.
            If set to :class:`True` the current time is used for the timestamp.

        """
        if now:
            self.timestamp = str(datetime.datetime.utcnow())
        else:
            self.timestamp = str(time)

    def add_field(self, name: str, value: str, inline: bool = True) -> None:
        """
        Adds an embed field.

        Parameters
        ----------
        name: str
            Name attribute of the embed field.

        value: str
            Value attribute of the embed field.

        inline: bool
            Defaults to :class:`True`.
            Whether or not the embed should be inline.

        """
        field = {
            'name': name,
            'value': value,
            'inline': inline
        }
        self.fields.append(field)

    def set_author(self, name: str, icon_url: str = None, url: str = None) -> \
            None:
        """
        Sets the author of the embed.

        Parameters
        ----------
        name: str
            The author's name.

        icon_url: str, optional
            URL for the author's icon.

        url: str, optional
            URL hyperlink for the author.

        """
        self.author = {
            'name': name,
            'icon_url': icon_url,
            'url': url
        }

    def set_thumbnail(self, url: str) -> None:
        """
        Sets the thumbnail of the embed.

        Parameters
        ----------
        url: str
            URL of the thumbnail.

        """
        self.thumbnail = {'url': url}

    def set_image(self, url: str) -> None:
        """
        Sets the image of the embed.

        Parameters
        ----------
        url: str
            URL of the image.

        """
        self.image = {'url': url}

    def set_footer(self, text: str, icon_url: str = None) -> None:
        """
        Sets the footer of the embed.

        Parameters
        ----------
        text: str
            The footer text.

        icon_url: str, optional
            URL for the icon in the footer.

        """
        self.footer = {
            'text': text,
            'icon_url': icon_url
        }

    def to_dict(self) -> dict:
        """
        Turns the :class:`Embed` object into a dictionary.
        """
        return {
            key: getattr(self, key)
            for key in self.__slots__
            if getattr(self, key) is not None
        }
