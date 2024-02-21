import { Ref } from 'vue'

let ws: WebSocket;

export class wSocket {
	send(data: string | Blob | ArrayBufferView | ArrayBufferLike)
	{
		ws.send(data);
	}

	constructor(toChange: Ref<number>)
	{
		ws = new WebSocket("ws://10.13.4.4/ws");
		ws.onmessage = (event: any) => {
			toChange.value++;
		}
	}
}
