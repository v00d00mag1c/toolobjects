import { LogicalBlock } from "/static/client/Page/LogicalBlock.js"
import { default_page_styles } from "/static/client/Page/Styles.js"
import { ObjectsList } from "/static/client/Components/ObjectsList.js"

export class Page {
    blocks = []
    _block_names = ['tabs', 'sidebar', 'content', 'footer']

    _get_block_by_name(name) {
        let item = null
        this.blocks.forEach(_item => {
            if (_item.id == name) {
                item = _item
            }
        })

        return item
    }

    async create() {
        document.body.innerHTML = `
            <style>
                ${await default_page_styles()}
            </style>
            <div id="app">
                <div class="logical-block" data-id="tabs">
                    <a href="#">Auth</a>
                </div>
                <div class="logical-content-blocks">
                    <div class="logical-block" data-id="sidebar"></div>
                    <div class="logical-block" data-id="content"></div>
                </div>
                <div class="logical-block" data-id="footer"></div>
            </div>
        `
        await this.load_head()

        try {
            await new ObjectsList().render(document.querySelector(`#app .logical-block[data-id='sidebar']`))
        } catch(e) {}

        this._block_names.forEach(name => {
            this.blocks.push(new LogicalBlock(name, document.querySelector(`#app .logical-block[data-id='${name}']`)))
        })
    }

    async load_head() {
        try {
            const _obj = await window.app.rpc.call({"i": "App.Config.Get", "key": "app.name"})

            document.title = _obj['data']['app.name']
        } catch(e){}
    }
}

export default Page
