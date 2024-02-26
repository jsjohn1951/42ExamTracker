import { Ref } from 'vue'

let ws: WebSocket;

export class wSocket {
	send(data: string | Blob | ArrayBufferView | ArrayBufferLike)
	{
		ws.send(data);
	}

	constructor(toChange: Ref<number>)
	{
		if (import.meta.env.VITE_MODE === "DEV")
			ws = new WebSocket(`ws://${import.meta.env.VITE_URL}/ws`);
		else
			ws = new WebSocket(`wss://${import.meta.env.VITE_URL}/ws`);
		ws.onmessage = (event: any) => {
			toChange.value++;
		}
	}
}
