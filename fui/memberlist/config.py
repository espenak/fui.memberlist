"""Common configuration constants
"""

PROJECTNAME = "fui.memberlist"
PROMOTIONS_PORTLET_COLUMN = u"plone.rightcolumn"

# This maps portal types to their corresponding add permissions.
# These are referenced in the root product __init__.py, during
# Archetypes/CMF type initialisation. The permissions here are
# also defined in content/configure.zcml, so that they can be
# looked up as a Zope 3-style IPermission utility.

# We prefix the permission names with our product name to group
# them sensibly. This is good practice, because it makes it
# easier to find permissions in the Security tab in the ZMI.

ADD_PERMISSIONS = {
	"MemberList" : "fui.memberlist: Add MemberList",
}
