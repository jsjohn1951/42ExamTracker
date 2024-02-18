export enum status {
	seated = 'SEATED',
	away = 'AWAY',
	emergency = 'EMERGENCY'
}

export enum gen {
	male = "Male",
	female = "Female"
}

export interface person {
	id?: string,
	username?: string,
	status: status,
	gender: gen,
	num: number,
	time: string | undefined
}

export interface api {
	id?: number,
	user?: string,
	status: status,
	gender: gen,
	num: number,
	time: string | undefined
}