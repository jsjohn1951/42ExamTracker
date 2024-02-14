<script setup lang="ts">
import { ref, watch } from 'vue'
import { person, status, gen, api } from '../common/iPerson'
import Add from './Add.vue'
import InitExam from './InitExam.vue'
import Person from './Person.vue'
import { wSocket } from '../composable/websocket'
import { apiUseFetch } from '../composable/api'

const search = ref('');
const dPersons = ref([] as person[]);
const toChange = ref(0);
const ws = new wSocket(toChange);
const useFetch = new apiUseFetch(ref(ws));
const res = ref(useFetch.users());

let i = 0;

const started = ref(false);

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
				num: item.num ? item.num! : 0
			})
	}
	started.value = await useFetch.started();
}

setUp();

watch(toChange, async (newVal, oldVal) => {
	dPersons.value = [] as person[];
	res.value = useFetch.users();
	setUp();
})


async function endExam ()
{
	started.value = false;
	await useFetch.putStart(false);
}
</script>

<template>
	<div class="flex-center flex-col" style="width: 100vw; height: fit-content; padding: 18px; gap: 24px;">
		<div style="height: fit-content;">

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
			<img src="https://42.fr/wp-content/uploads/2021/05/42-Final-sigle-seul.svg">
			<div>Exam in Progress</div>
	</div>
		</v-progress-circular>
	</v-expand-transition>



		</div>
		<v-row class="flex-between" style="width: 100%; max-width: 1200px;">
			<v-col class="flex-start">
				<InitExam :started="started" :apiUseFetch="useFetch" @start="started = true"/>
			</v-col>
			<v-col>
				<Add @reload="toChange++" :apiUseFetch="useFetch"/>
			</v-col>
			<v-col @click="endExam()" class="flex-center">
				<v-btn :disabled="!started" prepend-icon="mdi-meteor">
					End Exam
				</v-btn>
			</v-col>
		</v-row>
		<v-card style="max-width: 900px;">
			<v-data-iterator :items="dPersons" :items-per-page="9" :search="search">
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
				></v-text-field>
			  </v-toolbar>
</template>
  
<template v-slot:default="{ items }">
	<v-container class="pa-2">
		<v-row>
			<v-col v-for="item in items">
				<Person :api="useFetch" :item="item.raw" :started="started"/>
				<!-- <v-card class="pb-3" border flat>

					<v-list-item class="mb-2">
						<template v-slot:title>
						
						<div class="flex-between">
						  <strong class="text-h6 mb-2">id: {{ item.raw.id }}</strong>
						  <strong class="text-h6 mb-2">{{ item.raw.status }}</strong>
						  <strong class="text-h6 mb-2">{{ item.raw.gender }}</strong>
						  </div>
						</template>

					
					<div class="d-flex align-center text-caption text-medium-emphasis me-1">
					  <v-icon icon="mdi-clock" start></v-icon>
					  <div class="text-truncate">00:00</div>
					</div>
					<div class="d-flex align-center text-caption text-medium-emphasis me-1">
					  <v-icon icon="mdi-account-reactivate" start></v-icon>
					  <div class="text-truncate">{{ item.raw.num }}</div>
					</div>
					
				  </v-list-item>
  
				  <div class="d-flex justify-space-between px-4">

					
					<StatusUpdate :api="useFetch" :entry="item.raw" :started="started"/>

				  </div>
				</v-card> -->
			  </v-col>
			</v-row>
		  </v-container>
		</template>
  
		<!-- Footer -->
<template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
	<div class="d-flex align-center justify-center pa-4">
		<v-btn :disabled="page === 1" icon="mdi-arrow-left" density="comfortable" variant="tonal" rounded @click="prevPage"></v-btn>
	
		<div class="mx-2 text-caption">
			Page {{ page }} of {{ pageCount }}
		</div>
	
		<v-btn :disabled="page >= pageCount" icon="mdi-arrow-right" density="comfortable" variant="tonal" rounded @click="nextPage"></v-btn>
	</div>
</template>
	  </v-data-iterator>
	</v-card>
	</div>
  </template>