import { Ref } from 'vue'

let ws: WebSocket;

export class wTimer {
	wsTimer: WebSocket;
	send(data: string | Blob | ArrayBufferView | ArrayBufferLike)
	{
		this.wsTimer.send(data);
	}

	constructor(toChange: Ref<number>, id: string)
	{
		this.wsTimer = new WebSocket(`ws://10.13.1.11/ws/time/${id}`);
		this.wsTimer.onmessage = (event: any) => {
			console.log('timer data: ', event.data);
			toChange.value++;
		}
	}
}

export class wSocket {
	send(data: string | Blob | ArrayBufferView | ArrayBufferLike)
	{
		ws.send(data);
	}

	constructor(toChange: Ref<number>)
	{
		ws = new WebSocket("ws://10.13.1.11/ws");
		ws.onmessage = (event: any) => {
			toChange.value++;
		}
	}
}
