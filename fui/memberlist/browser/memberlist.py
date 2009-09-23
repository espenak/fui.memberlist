from os import listdir, sep
from os.path import isdir, join, exists, dirname
import codecs

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from Products.statusmessages.interfaces import IStatusMessage


DEFAULT_PORTRAIT_URL = "defaultUser.gif"


def cmpMemberDict(a, b):
	return cmp(a["fullname"], b["fullname"])


class MemberList(BrowserView):
	__call__ = ViewPageTemplateFile('memberlist.pt')

	def __init__(self, *args, **kwargs):
		BrowserView.__init__(self, *args, **kwargs)
		self.ctx = aq_inner(self.context)
		self.exclude = set(self.ctx.getExclude())
		self.current = set(self.ctx.getCurrentmembers())

	def currentMembers(self):
		pm = self.ctx.portal_membership
		out = []
		for memberId in self.current:
			member = pm.getMemberById(memberId)
			if member:
				out.append(self._memberInfo(memberId, member))
		out.sort(cmpMemberDict)
		return out

	def oldMembers(self):
		pm = self.ctx.portal_membership
		out = []
		for memberId in pm.listMemberIds():
			if not memberId in self.exclude and not memberId in self.current:
				member = pm.getMemberById(memberId)
				out.append(self._memberInfo(memberId, member))

		for u in self.ctx.getNonusers():
			x = u.split(":", 1)
			name = x[0]
			if len(x) == 2:
				description = x[1]
			else:
				description = None

			out.append(dict(
				username = None,
				email = None,
				homeFolder = None,
				fullname = name,
				portrait_url = DEFAULT_PORTRAIT_URL,
				description = description,
				homepage = None))

		out.sort(cmpMemberDict)
		return out

	def _memberInfo(self, memberId, member):
		portal = getToolByName(self.ctx, "portal_url").getPortalObject()
		portrait = portal.portal_memberdata.portraits.get(memberId)
		if portrait:
			portrait_url = portrait.absolute_url()
		else:
			portrait_url = DEFAULT_PORTRAIT_URL

		homeFolder = portal.Members.get(memberId)
		if homeFolder and len(homeFolder.contentItems()) > 0:
			homeFolder = homeFolder.absolute_url()
		else:
			homeFolder = None

		if self.ctx.portal_membership.isAnonymousUser():
			email = member.getProperty("email").replace("@", " (at) ")
		else:
			email = member.getProperty("email")

		return dict(
				username = memberId,
				email = email,
				fullname = member.getProperty("fullname"),
				portrait_url = portrait_url,
				homeFolder = homeFolder,
				description = member.getProperty("description"),
				homepage = member.getProperty("home_page")
			)
