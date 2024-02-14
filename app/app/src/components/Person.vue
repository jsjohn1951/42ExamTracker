<script setup lang="ts">
import { ref } from 'vue'
import { person } from '../common/iPerson'
import { apiUseFetch } from '../composable/api'
import { wTimer } from '../composable/websocket'
import StatusUpdate from './StatusUpdate.vue'

const props = defineProps<{
	api: apiUseFetch,
	item: person,
	started: boolean
}>()

let toChange = ref(0);
let timer: wTimer = new wTimer(toChange, (props.item.id ? props.item.id!.toString() : props.item.username!));

</script>

<template>
	<v-card class="pb-3" border flat>
	
		<v-list-item class="mb-2">
			<template v-slot:title>
				<!-- <v-row class="flex-between"> -->
				<div class="flex-between">
		  			<strong class="text-h6 mb-2">id: {{ item.id }}</strong>
		  			<strong class="text-h6 mb-2">{{ item.status }}</strong>
		  			<strong class="text-h6 mb-2">{{ item.gender }}</strong>
		  		</div>
			</template>

			<!-- Timer and number of breaks left -->
			<div class="d-flex align-center text-caption text-medium-emphasis me-1">
  				<v-icon icon="mdi-clock" start></v-icon>
  				<div class="text-truncate">00:00</div>
			</div>
			<div class="d-flex align-center text-caption text-medium-emphasis me-1">
				<v-icon icon="mdi-account-reactivate" start></v-icon>
				<div class="text-truncate">{{ item.num }}</div>
			</div>
		<!-- End Timer and number of breaks left -->
		</v-list-item>

		<div class="d-flex justify-space-between px-4">

			<!-- Set Status buttons -->
			<StatusUpdate :api="api" :timer="timer" :entry="item" :started="started"/>

		</div>
	</v-card>
</template>