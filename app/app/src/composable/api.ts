import { person, api } from '../common/iPerson';
import { Ref } from 'vue'
import { wSocket } from './websocket';
import { NumBreaks } from '@/common/iNumBreaks';

export class apiUseFetch {
	ws: Ref<wSocket>;

	constructor(ws: Ref<wSocket>)
	{
		this.ws = ws;
	}

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

	async time ()
	{
		let data: any

		await fetch ('/api/current/time',
		{
			method: 'GET',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		return (data as number);
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

	async putUser (nPerson: person, num: Ref<number>)
	{
		const request = {
			method: "PUT",
    		headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				id: parseInt(nPerson.id ? nPerson.id : '0'),
				user: nPerson.username,
				gender: nPerson.gender,
				status: nPerson.status,
				num: nPerson.num
			})
		};

		const res = await fetch ('/api/v1/users',request).then(async res => {
			const data = await res.json();

			if (!res.ok)
			{
				console.log('error received');
				return Promise.reject(((data && data.message) || res.status));
			}
			this.ws.value.send(`PUTUSER ${request.body}`)
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

	async deleteUserId(id: string)
	{
		let data: any;

		await fetch (`/api/v1/users/id/${id}`,
		{
			method: 'DELETE',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
			this.ws.value.send(`deleting user:${id}`)
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
	}

	async deleteUserUsr(id: string)
	{
		let data: any;

		await fetch (`/api/v1/users/user/${id}`,
		{
			method: 'DELETE',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
			this.ws.value.send(`deleting user:${id}`)
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
	}

	async clearAll()
	{
		let data: any;

		await fetch (`/api/v1/users/clear`,
		{
			method: 'DELETE',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
			this.ws.value.send(`deleting all`)
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
	}

	async getUsersAway()
	{
		let data: any;

		await fetch (`/api/v1/users/away`,
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
}