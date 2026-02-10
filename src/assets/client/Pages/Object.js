
export class Object {
    name = 'object'

    async render(i, node) {
        const name = location.hash.replace('#', '')
        const _obj = await window.app.rpc.call({
            'i': 'App.Objects.Index.Get',
            'name': name,
            'load_module': true
        })
        const object = _obj.items[0]

        node.innerHTML =  `
            <span id='name'>Object</span>
            <div id='args'></div>
            <div>
                <input type="button" id="_run" value="run">
            </div>
        `

        object.module.arguments.forEach(argument => {
            node.querySelector('#args').insertAdjacentHTML('beforeend', `
                <div id="argument" data-id="${argument.name}">
                    <span>${argument.name}</span>
                    <div>
                        <input type="text">
                    </div>
                </div>
            `)
        })

        node.querySelector('#_run').addEventListener('click', async (e) => {
            const _args = {
                'i': name
            }
            node.querySelectorAll('#args #argument').forEach(item => {
                const _val = item.querySelector('input').value
                if (_val != '') {
                    _args[item.dataset.id] = _val
                }
            })

            await window.app.rpc.call(_args)
        })
        console.log(object)
    }
}
