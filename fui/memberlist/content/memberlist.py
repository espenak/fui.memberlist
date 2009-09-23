"""Definition of the MemberList content type and associated schemata and
other logic.

This file contains a number of comments explaining the various lines of
code. Other files in this sub-package contain analogous code, but will 
not be commented as heavily.

Please see README.txt for more information on how the content types in
this package are used.
"""

import re

from zope.interface import implements
from zope.component import adapter, getMultiAdapter, getUtility
from zope.app.container.interfaces import INameChooser
from Acquisition import aq_inner, aq_parent
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectInitializedEvent
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content import base

from fui.memberlist.interfaces import IMemberList
from fui.memberlist.config import PROJECTNAME
from fui.memberlist import MemberListMessageFactory as _


from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import directlyProvides

def allMembers(context):
	terms = []

	pm = context.portal_membership
	acl_users = getToolByName(context, 'acl_users')
	for member_id in pm.listMemberIds():
		user = acl_users.getUserById(member_id)
		if user is not None:
			member_name = user.getProperty('fullname') or member_id
			terms.append(SimpleVocabulary.createTerm(
				member_id, str(member_id), member_name))
	return SimpleVocabulary(terms)
directlyProvides(allMembers, IVocabularyFactory)



# This is the Archetypes schema, defining fields and widgets. We extend
# the one from ATContentType's ATFolder with our additional fields.
schema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
	atapi.LinesField("currentmembers",
		required = False,
		searchable = False,
		storage = atapi.AnnotationStorage(),
		vocabulary_factory = "fui.memberlist.allMembers",
		widget = atapi.InAndOutWidget(
			size = 20,
			label = u"Current FUI members")
		),

	atapi.LinesField("exclude",
		required = False,
		searchable = False,
		storage = atapi.AnnotationStorage(),
		vocabulary_factory = "fui.memberlist.allMembers",
		widget = atapi.InAndOutWidget(
			size = 20,
			label = u"Exclude",
			description = "Users which are excluded from old members listing.")
		),

	atapi.LinesField("nonusers",
		required = False,
		searchable = False,
		storage = atapi.AnnotationStorage(),
		widget = atapi.LinesWidget(
			label = u"Without plone user",
			description = "Old members without a Plone user. "\
				"One name followed by an optional : and a " \
				"short description on each line. " \
				"Example: 'Ola Normann:v06-h08'.")
		),
	))

# We want to ensure that the properties we use as field properties (see
# below), use AnnotationStorage. Without this, our property will conflict
# with the attribute with the same name that is being managed by the default
# attributestorage
schema['title'].storage = atapi.AnnotationStorage()


class MemberList(base.ATCTContent):
	""" """
	implements(IMemberList)
	
	# The portal type name must be set here, matching the one in types.xml
	# in the GenericSetup profile
	portal_type = "MemberList"
	
	# We then associate the schema with our content type
	schema = schema 


# This line tells Archetypes about the content type
atapi.registerType(MemberList, PROJECTNAME)
