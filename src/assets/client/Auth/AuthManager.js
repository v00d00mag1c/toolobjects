export class AuthManager {
    async auth(username, password) {
        const _usrs = await window.app.rpc.call({
            'i': 'App.ACL.Tokens.Get',
            'username': username,
            'password': password,
        })

        return _usrs.items[0].value
    }

    reg(token) {
        localStorage.setItem('users', `[\"${token}\"]`)
    }

    remove() {
        localStorage.setItem('users', null)
    }

    get_token() {
        const _users = JSON.parse(localStorage.getItem('users'))

        if (_users && _users.length > 0) {
            return _users[0]
        }
    }
}
