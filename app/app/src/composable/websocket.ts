import { Ref } from 'vue'

let ws: WebSocket;
let toChange: Ref<number>;

export class wSocket {
	send(data: string | Blob | ArrayBufferView | ArrayBufferLike)
	{
		ws.send(data);
	}

	constructor(toChange: Ref<number>)
	{
		ws = new WebSocket("ws://127.0.0.1/ws");
		toChange = toChange;
		ws.onmessage = (event: any) => {
			toChange.value++;
			console.log('message received!');
		}
	}
}
