import { Component } from "/static/client/Components/Component.js"

export class ObjectsList extends Component {
    async render(node) {
        node.innerHTML = `<div id="objects_list"></div>`

        try {
            const _items = await window.app.rpc.call({"i": "App.Objects.Index.GetList", "key": "app.name"})
            _items.items.forEach(item => {
                const _parts = item.parts
                _parts.push(item.title)
                const name = _parts.join('.')
                node.querySelector('#objects_list').insertAdjacentHTML('beforeend', `
                    <div><a href="#${name}">${name}</a></div>
                `)
            })
        } catch(e) {
        }
    }
}
