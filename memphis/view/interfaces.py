""" memphis.view interfaces """
from zope import interface


class LayoutNotFound(LookupError):
    """ Layout not found exception """


class IView(interface.Interface):
    """ view """

    __name__ = interface.Attribute('Name')
    __parent__ = interface.Attribute('Parent')

    context = interface.Attribute('Context')
    request = interface.Attribute('Request')
    template = interface.Attribute('Template')
    layout = interface.Attribute('Layout name')

    content_type = interface.Attribute('Content type')
    response_headers = interface.Attribute('Response headers')
    response_status = interface.Attribute('Response status')

    def update():
        """Update the pagelet data."""

    def render():
        """Render the pagelet content w/o o-wrap."""

    def __call__():
        """Update and render pagelet"""


class IPagelet(interface.Interface):
    """ pagelet """

    context = interface.Attribute('Context')

    request = interface.Attribute('Request')

    template = interface.Attribute('Template')

    def update():
        """Update the pagelet data."""

    def render():
        """Render the pagelet content w/o o-wrap."""

    def __call__():
        """Update and render pagelet"""


class IPageletType(interface.Interface):
    """ pagelet interface type """


class ILayout(interface.Interface):
    """ layout """

    template = interface.Attribute('Layout template')

    view = interface.Attribute('Parent view')
    context = interface.Attribute('Parent view context')

    mainview = interface.Attribute('Initial view')
    maincontext = interface.Attribute('Initial view context')

    template = interface.Attribute('Layout template')

    def update():
        """Update the layout data """

    def render():
        """Render the layout """

    def __call__(layout=None, view=None, *args, **kw):
        """ build layout tree and render """


class IRenderer(interface.Interface):
    """ renderer """

    content_type = interface.Attribute('Renderer content_type')

    def __call__(result):
        """ render result """


# navigation root
class INavigationRoot(interface.Interface):
    """ site root """


# status message
class IMessage(interface.Interface):
    """ message """

    def render(message):
        """ render message """


class IStatusMessage(interface.Interface):
    """ message service """

    def add(text, type='info'):
        """ add message text as message to service """

    def clear():
        """ return all mesasges and clear """

    def messages():
        """ return all messages """
