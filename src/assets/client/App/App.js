import { RPC } from "/static/client/App/RPC.js"
import { Page } from "/static/client/Page/Page.js"

export class App {
    rpc = null
    page = null

    async run() {
        this.rpc = new RPC()
        this.page = new Page()
        this.rpc.run()

        await this.page.create()
    }
}

export default App
