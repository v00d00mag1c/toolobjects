export class Renderable {
    dom_element = null

    render(node, settings = {}) {
        this.dom_element = this.render_function(node, settings)
    }
}

export default Renderable
