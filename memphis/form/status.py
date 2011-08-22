""" formError status message type """
from zope import interface
from pyramid.interfaces import IRequest

from memphis import view, config
from memphis.view.message import Message
from memphis.form.interfaces import IErrorViewSnippet


class FormErrorStatusMessage(Message):
    config.adapts(IRequest, name='formError')

    template = view.template('memphis.form:templates/message.pt')

    def render(self, message):
        self.message = message[0]
        if IErrorViewSnippet.providedBy(self.message):
            self.message = self.message.render()

        self.errors = [
            err for err in message[1:]
            if IErrorViewSnippet.providedBy(err) and err.widget is None]

        return self.template(
            message = self.message,
            errors = self.errors,
            request = self.request)
