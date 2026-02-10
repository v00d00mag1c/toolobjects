import {Renderable} from "/static/client/Objects/Renderable.js"

export class LogicalBlock extends Renderable {
    constructor(id) {
        super()
        this.id = id
    }

    render_function(node, settings = {}) {
        const _el = document.createElement('div')
        _el.className = 'logical-block'
        _el.dataset.id = this.id
        return node.appendChild(_el)
    }
}

export default LogicalBlock
