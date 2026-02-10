from App.ACL.Permissions.Permission import Permission

class Limitable():
    @classmethod
    def canBeUsedBy(self, user):
        if user == None:
            return Permission.check(Permission(
                object_name = self.getClassNameJoined(),
                user = None,
                action = 'call',
                allow = True
            ))

        # ???
        if user.name == 'root':
            return True

        return user.can('call', self)
