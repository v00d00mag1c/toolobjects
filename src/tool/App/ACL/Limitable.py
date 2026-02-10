from App.ACL.Permissions.Permission import Permission

class Limitable():
    @classmethod
    def canBeUsedBy(cls, user):
        if user == None:
            return Permission.check(Permission(
                object_name = cls.getClassNameJoined(),
                #user = None,
                action = 'call',
                #allow = True
            ))

        # ???
        if user.name == 'root':
            if user.is_from_token() == True:
                return user.is_expired() == False

            return True

        return user.can('call', cls)
