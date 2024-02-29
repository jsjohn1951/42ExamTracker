import { person, api } from '../common/iPerson';
import { Ref } from 'vue'
import { wSocket } from './websocket';
import { NumBreaks } from '@/common/iNumBreaks';
import { token } from '@/common/iToken';
// import { Blob } from 'buffer';
import { useCookies } from "vue3-cookies";

export class cookieClass {
	cookie = useCookies();

	setAuth (data: string)
	{
		this.cookie.cookies.set('Auth', data);
	}

	getAuth ()
	{
		const data = this.cookie.cookies.get('Auth');
		return (data);
	}

	deleteAuth ()
	{
		this.cookie.cookies.remove('Auth');
	}
}

export class apiAuth {
	cookie = new cookieClass();

	async validate(token: token)
	{
		const request = {
			method: "POST",
    		headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(
				{
					access_token: token.access_token,
					token_type: token.token_type
				}
			)
		};

		const res = await fetch ('/api/validate',request).then(async res => {
			const data = await res.json();

			if (!res.ok)
			{
				console.log('error received');
				return Promise.reject(((data && data.message) || res.status));
			}
			return (data);
		}
		).catch(error => {
			console.error('There was an error!', error);
    	});
		return (res);
	}

	async auth()
	{
		let data = this.cookie.getAuth();
		if (data)
		{
			let res = await this.validate((data as unknown) as token);
			if (res)
				return true ;
			this.cookie.deleteAuth();
			return false ;
			// res.then(() => {
			// 	return true ;
			// }).catch(() => {
			// 	return false ;
			// })
		}
		return (false);
	}
}
export class apiUseFetch {
	ws: Ref<wSocket>;
	cookie = useCookies();

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

	async timeStarted ()
	{
		let data: any

		await fetch ('/api/time/startTime',
		{
			method: 'GET',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		return (data as string);
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

	async getHistory()
	{
		let data: any;

		await fetch (`/api/history`,
		{
			method: 'GET',
		}).then(async(res) => {
			await res.blob().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		console.log('data: ', data);
		const url = window.URL.createObjectURL(data);
		let a = document.createElement('a');
		a.href = url;
		a.download = "Logfile.txt";
		document.body.appendChild(a);
		a.click();
		a.remove();
		return (data as string);
	}

	async getBreaks()
	{
		let data: any;

		await fetch (`/api/breaks`,
		{
			method: 'GET',
		}).then(async(res) => {
			await res.json().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		return (data as NumBreaks);
	}

	async getIdHistory(id: string)
	{
		let data: any;

		await fetch (`/api/history/${id}`,
		{
			method: 'GET',
		}).then(async(res) => {
			await res.blob().then((d) => {
				data = d;
		})
		}).catch((err) => {
			console.log('error: ', err);
		})
		console.log('data: ', data);
		const url = window.URL.createObjectURL(data);
		let a = document.createElement('a');
		a.href = url;
		a.download = `Logfile_${id}.txt`;
		document.body.appendChild(a);
		a.click();
		a.remove();
		return (data as string);
	}

	async postTimeZone(tmInfo: string)
	{
		const request = {
			method: "POST",
    		headers: { "Content-Type": "application/json" },
			body: JSON.stringify(
				{
					tm: tmInfo
				}
			)
		};

		const res = await fetch ('/api/timezone',request).then(async res => {
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

	async authenticate(user: string, pw: string)
	{
		const info = {
			'grant_type': '',
			'username': user,
			'password': pw,
			'scope': '',
			'client_id': '',
			'client_secret': ''
		}

		let bod = new URLSearchParams();
		bod.set('grant_type', '');
		bod.set('username', user);
		bod.set('password', pw);

		console.log('body: ', bod.toString());
		const request = {
			method: "POST",
    		headers: {
				"Content-Type": "application/x-www-form-urlencoded"
			},
			body: bod.toString()
		};

		const res = await fetch ('/api/login',request).then(async res => {
			const data = await res.json();

			if (!res.ok)
			{
				console.log('error received');
				return Promise.reject(((data && data.message) || res.status));
			}
			return (data);
		}
		).catch(error => {
			console.error('There was an error!', error);
    	});
		return (res);
	}
}