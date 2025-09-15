#
# Author: Rohtash Lakra
#

def checkPermission(user, permission_name) -> bool:
    """Checks if the user has a specific permission"""
    for role in user.roles:
        for permission in role.permissions:
            if permission.name == permission_name:
                return True
    return False
