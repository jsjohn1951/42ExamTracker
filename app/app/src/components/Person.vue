<script setup lang="ts">
import { ref } from 'vue'
import { person } from '../common/iPerson'
import { apiUseFetch } from '../composable/api'
import StatusUpdate from './StatusUpdate.vue'
import { onMounted } from 'vue'
import { onUnmounted } from 'vue'

const props = defineProps<{
	api: apiUseFetch,
	item: person,
	started: boolean,
	away: boolean
}>()


let interval: NodeJS.Timeout

let sec: number = 0
let min: number = 0
let hour: number = 0
const res = ref('00:00:00');

if (props.away)
{
	let timeBegan = new Date().valueOf();
	if (props.item.time)
		timeBegan = new Date(props.item.time).valueOf();
	interval = setInterval(()=>{

		const current = new Date().valueOf()
		const timeElapsed = ref(current - timeBegan)
		timeElapsed.value /= 10;
		timeElapsed.value /= 100;
		sec = Math.floor((timeElapsed.value % 60));
		min = Math.floor(Math.floor(timeElapsed.value / 60) % 60);
		hour = Math.floor(Math.floor(timeElapsed.value / 3600) % 60);
		res.value = `${('00'+hour).slice(-2)}:${('00'+min).slice(-2)}:${('00'+sec).slice(-2)}`;
	}, 1000);
}

onUnmounted(()=> {
	if (props.away)
		clearInterval(interval)
})
</script>

<template>
	<v-card class="pb-3" border flat style="min-width: 250px;">

		<v-list-item class="mb-2">
			<template v-slot:title>
				<!-- <v-row class="flex-between"> -->
				<div class="flex-between">
		  			<strong class="text-h6 mb-2">id: {{ item.id }}</strong>
		  			<!-- <strong class="text-h6 mb-2">{{ item.status }}</strong> -->
		  			<strong class="text-h6 mb-2">{{ item.gender }}</strong>
		  		</div>
			</template>
			<template v-slot:subtitle>
				<div style="width: 100%;" class="flex-center">
					<strong class="text-h6 mb-2">{{ item.status }}</strong>
				</div>
			</template>

			<!-- Timer and number of breaks left -->
			<div v-if="away" class="d-flex align-center text-caption text-medium-emphasis me-1">
  				<v-icon icon="mdi-clock" start></v-icon>
  				<div v-if="hour == 0 && min < 15" class="text-truncate">{{ res }}</div>
				<div v-else class="text-truncate" style="color: red;">{{ res }}</div>
			</div>
			<div class="d-flex align-center text-caption text-medium-emphasis me-1">
				<v-icon icon="mdi-account-reactivate" start></v-icon>
				<div class="text-truncate">{{ item.num }}</div>
			</div>
		<!-- End Timer and number of breaks left -->
		</v-list-item>


		<div class="flex-center flex-column" style="padding: 18px;">

			<!-- Set Status buttons -->
			<StatusUpdate :away="true" :api="api" :entry="item" :started="started"/>

		</div>
	</v-card>
</template>