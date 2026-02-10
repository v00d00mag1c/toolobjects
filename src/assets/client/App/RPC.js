import {RPCEvent} from "/static/client/App/RPCEvent.js"

export class RPC {
    events = {
        index: 0
    }
    connection = null
    callback_dictionary = {}

    run() {
        this.connection = new WebSocket(`ws://${location.host}/rpc`)

        this.connection.onopen = () => {
            const event = new RPCEvent()
            event.type = 'ping'
            event.event_index = 0
            event.payload = {}

            event.send(this.connection)
        }

        this.connection.onmessage = (event) => {
            const rpc_event = RPCEvent.fromData(JSON.parse(event.data))
            const callback = this.callback_dictionary[rpc_event.event_index]

            switch(rpc_event.type) {
                case "log":
                    console.log(`Logger message: `, rpc_event.payload)

                    break
                case "object":
                    if (callback) {
                        callback.resolve(rpc_event.payload)
                        this.callback_dictionary[rpc_event.event_index] = null
                    }
            }
        }
    }

    async call(args, attempt = 0) {
        if (attempt > 5) {
            throw Error()
        }

        if (!this.connection.readyState) {
            await new Promise(resolve => setTimeout(resolve, 100))

            return await this.call(args, attempt + 1)
        }

        if (this.connection.readyState > 1) {
            console.log('websocket closed, reconnecting')
            this.run()
        }

        return new Promise((resolve, reject) => {
            const event = new RPCEvent()
            event.type = 'object'
            event.event_index = this.get_index()
            event.payload = args

            this.callback_dictionary[event.event_index] = {resolve, reject}

            try {
                event.send(this.connection)
            } catch(err) {
                console.error(err)
                reject(err)
            }
        })
    }

    get_index() {
        this.update()

        return this.events.index
    }

    update() {
        this.events.index += 1
    }
}

export default RPC
