import { Ref } from 'vue'

let ws: WebSocket;

export class wSocket {
	send(data: string | Blob | ArrayBufferView | ArrayBufferLike)
	{
		ws.send(data);
	}

	constructor(toChange: Ref<number>)
	{
		ws = new WebSocket("ws://10.18.202.200/ws");
		ws.onmessage = (event: any) => {
			toChange.value++;
		}
	}
}
