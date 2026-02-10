const exist_types = ['ping', 'object', 'log']

export class RPCEvent {
    type = null
    event_index = 0
    payload = {}

    static fromData(data) {
        const _item = new RPCEvent()
        _item.type = data.type
        _item.event_index = Number(data.event_index)
        _item.payload = data.payload

        return _item
    }

    send(ws) {
        ws.send(this.stringify())
    }

    stringify() {
        return JSON.stringify({"type": this.type, "event_index": this.event_index, "payload": this.payload})
    }
}

export default RPCEvent
