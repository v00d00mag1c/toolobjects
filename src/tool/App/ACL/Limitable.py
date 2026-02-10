from App import app
from App.ACL.Permissions.ObjectPermission import ObjectPermission

class Limitable():
    @classmethod
    def canBeUsedBy(self, user):
        if user == None:
            return app.AuthLayer.compare_permissions(ObjectPermission(
                object_name = self.getClassNameJoined(),
                user = None,
                action = 'call',
                allow = True
            ))

        # ???
        if user.name == 'root':
            return True

        return user.can('call', self)
