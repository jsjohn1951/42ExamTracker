<script setup lang="ts">
import { ref, watch } from 'vue'
import { person, status, gen, api } from '../common/iPerson'
import Add from './Add.vue'
import InitExam from './InitExam.vue'
import Person from './Person.vue'
import Remove from './Remove.vue'
import Away from './Away.vue'
import Clear from './Clear.vue'
import EndExam from './EndExam.vue'
import History from './History.vue'
import Manual from './Manual.vue'
import Timer from './Timer.vue'
import { wSocket } from '../composable/websocket'
import { apiUseFetch } from '../composable/api'

const search = ref('');
const dPersons = ref([] as person[]);
const searchRes = ref([] as person[]);
const dis = ref(0);
const toChange = ref(0);
const ws = new wSocket(toChange);
const useFetch = new apiUseFetch(ref(ws));

// Timer
// const timer = ref('00:00:00');
// let interval: NodeJS.Timeout
// let sec: number = 0
// let min: number = 0
// let hour: number = 0

let i = 0;

const started = ref(false);

await useFetch.postTimeZone(Intl.DateTimeFormat().resolvedOptions().timeZone);

async function setUp ()
{
	let nRes = await useFetch.users();
	let item: api;

	for (item of nRes)
	{
		let found = dPersons.value.find((obj) => {
			return (item.id?.toString() == obj.id)
		})
		if (!found)
			dPersons.value.push({
				id: item.id ? item.id!.toString() : item.user!,
				username: item.user ? item.user! : '',
				status: item.status ? item.status! : status.seated,
				gender: item.gender ? item.gender! : gen.male,
				num: item.num ? item.num! : 0,
				time: item.time ? item.time : undefined
			})
	}
	started.value = await useFetch.started();
}

async function sync()
{
	let item: person;
	searchRes.value = [] as person[];

	for (item of dPersons.value)
	{
		searchRes.value.push(item);
	}
}

// async function setTimer()
// {
// 	if (!started.value)
// 		return ;
// 	const timeStarted = await useFetch.timeStarted();
// 	console.log(timeStarted.valueOf());
// 	const timeBegan = new Date(timeStarted).valueOf();
// 	interval = setInterval(()=>{
// 		const current = new Date().valueOf()
// 		const timeElapsed = ref(current - timeBegan)
// 		timeElapsed.value /= 10;
// 		timeElapsed.value /= 100;
// 		sec = Math.floor((timeElapsed.value % 60));
// 		min = Math.floor(Math.floor(timeElapsed.value / 60) % 60);
// 		hour = Math.floor(Math.floor(timeElapsed.value / 3600) % 60);
// 		timer.value = `${('00'+hour).slice(-2)}:${('00'+min).slice(-2)}:${('00'+sec).slice(-2)}`;
// }, 1000);
// }

await setUp();
await sync();
// await setTimer();

watch(search, async (newVal, oldVal) => {
	if (search.value != '')
	{
		searchRes.value = dPersons.value.filter((person) => person.id == search.value);
		if (searchRes.value.length == 0)
			searchRes.value = dPersons.value.filter((person) => person.username?.includes(search.value));
	}
	else
		await sync();
	dis.value++;
})

watch(toChange, async (newVal, oldVal) => {
	dPersons.value = [] as person[];
	searchRes.value = [] as person[];
	await setUp();
	await sync();
	search.value = '';
	dis.value++;
})

function updateDisplay()
{
	dis.value++;
}
</script>

<template>
	<div class="flex-center flex-col" style="width: 100vw; height: fit-content; padding: 18px; gap: 24px;">
		<Timer v-if="started" :api="useFetch"/>
		<!-- <div style="height: fit-content;">

		<v-expand-transition>
		<v-progress-circular
			v-if="started"
			indeterminate
      color="green"
	  :rotate="360"
      :size="200"
      :width="10"
    >
	<div class="flex-center flex-col" style="gap: 15px;">
			<div class="text-truncate">{{ timer }}</div>
			<div>Exam in Progress</div>
	</div>
		</v-progress-circular>
	</v-expand-transition>

		</div> -->
		<v-row class="flex-between" style="gap: 30px;">
			<v-col class="flex-start">
				<InitExam :started="started" :apiUseFetch="useFetch" @start="started = true"/>
			</v-col>
			<v-col class="flex-center">
				<Clear :started="started" :apiUseFetch="useFetch"/>
			</v-col>
			<v-col class="flex-center">
				<Manual :started="started" :apiUseFetch="useFetch"/>
			</v-col>
			<v-col class="flex-center">
				<History :apiUseFetch="useFetch"/>
			</v-col>
			<v-col class="flex-center">
				<EndExam :started="started" :apiUseFetch="useFetch"/>
			</v-col>
		</v-row>
		<div>
		<v-card class="flex-center flex-col">
					<v-card-title class="text-subtitle-2"><v-breadcrumbs :items="['42Exam', 'InsertOrRemove']"></v-breadcrumbs></v-card-title>
					<v-row>
						<v-col>
							<Add @reload="toChange++" :apiUseFetch="useFetch"/>
						</v-col>
						<v-col>
							<Remove @reload="toChange++" :apiUseFetch="useFetch"/>
						</v-col>
					</v-row>
				</v-card>
		<v-card class="flex-center flex-col" style="padding: 0px 15px 0px 15px; max-width: 900px;">
			<v-card-title class="text-subtitle-2"><v-breadcrumbs :items="['42Exam', 'Control Panel']"></v-breadcrumbs></v-card-title>
		<v-card>

			<v-data-iterator :items="searchRes" :items-per-page="6">
				<template v-slot:header>
					<v-toolbar class="px-2">
						<v-text-field
							v-model="search"
							clearable
							density="comfortable"
							hide-details
							placeholder="Search"
							prepend-inner-icon="mdi-magnify"
							style="max-width: 300px;"
							variant="solo"
						/>
					</v-toolbar>
				</template>
				<template v-slot:default="{ items }">
					<v-container class="pa-2" :key="dis">
						<v-row>
							<v-col v-for="item in items">
								<Person :away="false" :api="useFetch" :item="item.raw" :started="started"/>
							</v-col>
						</v-row>
					</v-container>
				</template>

				<!-- Footer -->
				<template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
					<div class="d-flex align-center justify-center pa-4">
						<v-btn :disabled="page === 1" icon="mdi-arrow-left" density="comfortable" variant="tonal" rounded @click="prevPage(); updateDisplay()"></v-btn>
						<div class="mx-2 text-caption">
							Page {{ page }} of {{ pageCount }}
						</div>
						<v-btn :disabled="page >= pageCount" icon="mdi-arrow-right" density="comfortable" variant="tonal" rounded @click="nextPage(); updateDisplay()"></v-btn>
					</div>
				</template>
			</v-data-iterator>
		</v-card>
	</v-card>
	<v-row>
		<v-col>
			<Suspense>
				<Away away :useFetch="useFetch" :key="toChange"/>
			</Suspense>
		</v-col>
	</v-row>
	</div>
	</div>
	</template>