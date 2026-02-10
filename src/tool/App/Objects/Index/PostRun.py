from App.Objects.Object import Object
from App import app
from App.ACL.User import User
from App.ACL.Acts.GetHash import GetHash

class PostRun(Object):
    @classmethod
    def mount(cls):
        # Appending settings
        for item in app.ObjectsList.getItems().toList():
            if item.is_inited == False:
                continue

            item.appendSettings()

        # Creating root if not exists
        default_root_password = 'root'
        has_root = False
        for user in app.AuthLayer.getUsers():
            if user.name == 'root':
                has_root = True

        if has_root == False:
            app.AuthLayer.add_user(User(
                    name = 'root',
                    # 2manywraps
                    password_hash = GetHash().implementation({'string': default_root_password}).items[0].value
                )
            )
