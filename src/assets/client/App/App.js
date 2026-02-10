import { RPC } from "/static/client/App/RPC.js"
import { Page } from "/static/client/Page/Page.js"
import { AuthManager } from "/static/client/Auth/AuthManager.js"
import { Auth } from "/static/client/Pages/Auth.js"
import { Object } from "/static/client/Pages/Object.js"

class Router {
    async route(hash) {
        switch (hash) {
            case '':
                return await new Auth().render({}, document.querySelector(`#app .logical-block[data-id='content']`))
            default:
                return await new Object().render({}, document.querySelector(`#app .logical-block[data-id='content']`))
        }
    }
}

export class App {
    rpc = null
    page = null

    async run() {
        this.rpc = new RPC()
        this.page = new Page()
        this.auth = new AuthManager()
        this.rpc.run()
        this.router = new Router()

        if (new URL(location.href).searchParams.get('draw') == '1') {
            await this.page.create()
            await this.router.route(location.hash)

            window.addEventListener('hashchange', async (e) => {
                console.log(e)
                await this.router.route(location.hash.replace('#', ''))
            })
        } else {
            document.querySelector('body').insertAdjacentHTML('beforeend', `
                <div id="main_msg">
                    <style>
                        #main_msg p {
                            padding: 0px;
                            margin: 0px;
                        }
                    </style>
                    <p>Use <b>/api</b> to call,</p>
                    <p>Or <b>/rpc</b>, or <b>window.app.rpc.call({"i": ...}) in DevTools.</b></p>
                    <p>Or use <a href="?draw=1">raw js version</a></b></p>
                </div>
            `)
        }
    }
}

export default App
