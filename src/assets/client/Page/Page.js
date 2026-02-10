import { LogicalBlock } from "/static/client/Page/LogicalBlock.js"
import { default_page_styles } from "/static/client/Page/Styles.js"

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
                <div class="logical-block" data-id="tabs"></div>
                <div class="logical-content-blocks">
                    <div class="logical-block" data-id="sidebar"></div>
                    <div class="logical-block" data-id="content"></div>
                </div>
                <div class="logical-block" data-id="footer"></div>
            </div>
        `
        this._block_names.forEach(name => {
            this.blocks.push(new LogicalBlock(name, document.querySelector(`#app .logical-block[data-id='${name}']`)))
        })
    }
}

export default Page
