from zope.interface import Interface
from zope import schema

from zope.app.container.constraints import contains

from fui.memberlist import MemberListMessageFactory as _


class IMemberList(Interface):
	""" A memberlist. """
