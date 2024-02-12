import { person, api } from '../common/iPerson';
import { Ref } from 'vue'
import { wSocket } from './websocket';
import { NumBreaks } from '@/common/iNumBreaks';

export class apiUseFetch {
	ws: Ref<wSocket>

	async users ()
	{
		let data: any

		await fetch ('/api/v1/users',
		{
			method: 'GET',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		return (data as api[]);
	}

	async started ()
	{
		let data: any

		await fetch ('/api/v1/start',
		{
			method: 'GET',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		return (data as string == "STARTED" ? true : false);
	}

	async postBreaks (breaks: NumBreaks)
	{
		const request = {
			method: "POST",
    		headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				perFacility: parseInt(breaks.perFacility),
				perPerson: parseInt(breaks.perPerson)
			})
		};

		const res = await fetch ('/api/v1/breaks',request).then(async res => {
			const data = await res.json();

			if (!res.ok)
			{
				console.log('error received');
				return Promise.reject(((data && data.message) || res.status));
			}
			this.ws.value.send(request.body)
		}
		).catch(error => {
    	  console.error('There was an error!', error);
    	});
	}

	async postUser (nPerson: person)
	{
		const request = {
			method: "POST",
    		headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				id: parseInt(nPerson.id ? nPerson.id : '0'),
				user: nPerson.username,
				gender: nPerson.gender,
				status: nPerson.status
			})
		};

		const res = await fetch ('/api/v1/users',request).then(async res => {
			const data = await res.json();

			if (!res.ok)
			{
				console.log('error received');
				return Promise.reject(((data && data.message) || res.status));
			}
			this.ws.value.send(request.body)
		}
		).catch(error => {
    	  console.error('There was an error!', error);
    	});
	}

	async putStart(start: boolean)
	{
		const request = {
			method: "POST",
    		headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				examStart: (start ? "STARTED" : "NOT RUNNING")
			})
		};

		const res = await fetch ('/api/v1/start',request).then(async res => {
			const data = await res.json();

			if (!res.ok)
			{
				console.log('error received');
				return Promise.reject(((data && data.message) || res.status));
			}
			this.ws.value.send(request.body)
		}
		).catch(error => {
    	  console.error('There was an error!', error);
    	});
	}

	constructor(ws: Ref<wSocket>)
	{
		this.ws = ws;
	}
}