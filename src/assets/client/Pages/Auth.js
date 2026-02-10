import { Component } from "/static/client/Components/Component.js"

export class Auth extends Component {
    name = 'auth'

    async render(i, node) {
        node.innerHTML = `
            <span>Auth</span>
            <div>
                <input type='text' placeholder='username' id='username'>
                <input type='text' placeholder='password' id='password'>
            </div>
            <div>
                <input type='button' value='auth' id='do_auth'>
            </div>
            <div></div>
        `

        node.querySelector('#do_auth').addEventListener('click', async (e) => {
            const _token = await window.app.auth.auth(node.querySelector('#username').value, node.querySelector('#password').value)
            window.app.auth.reg(_token)
        })
    }
}

export default Auth
