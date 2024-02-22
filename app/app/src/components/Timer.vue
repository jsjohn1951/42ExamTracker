<script setup lang="ts">
import { onUnmounted, ref } from 'vue'
import { apiUseFetch } from '../composable/api'

const props = defineProps<{
	api: apiUseFetch
}>()

// Timer
const timer = ref('00:00:00');
let interval: NodeJS.Timeout
let sec: number = 0
let min: number = 0
let hour: number = 0

const timeStarted = await props.api.timeStarted();
const timeBegan = new Date(timeStarted).valueOf();
interval = setInterval(()=>{
	const current = new Date().valueOf()
	const timeElapsed = ref(current - timeBegan)
	timeElapsed.value /= 10;
	timeElapsed.value /= 100;
	sec = Math.floor((timeElapsed.value % 60));
	min = Math.floor(Math.floor(timeElapsed.value / 60) % 60);
	hour = Math.floor(Math.floor(timeElapsed.value / 3600) % 60);
	timer.value = `${('00'+hour).slice(-2)}:${('00'+min).slice(-2)}:${('00'+sec).slice(-2)}`;
	}, 1000);

onUnmounted(()=> {
	clearInterval(interval)
})
</script>

<template>
	<div style="height: fit-content;">

		<v-expand-transition>
			<v-progress-circular
				indeterminate
				color="green"
				:rotate="360"
				:size="200"
				:width="10"
			>
				<div class="flex-col">
					<div class="text-truncate text-h4" style="color: white;">
						<strong>{{ timer }}</strong>
					</div>
					<div class="text-subtitle-1" style="color: white;">Exam in Progress</div>
				</div>
			</v-progress-circular>
		</v-expand-transition>

	</div>
</template>