<script setup lang="ts">
import { apiUseFetch } from '../composable/api'
import { person, status, api } from '../common/iPerson'
import { wTimer } from '../composable/websocket'
import { ref } from 'vue'

const props = defineProps < {
	api: apiUseFetch,
	timer: wTimer,
	entry: person,
	started: boolean
} > ();

const entry = ref(props.entry);
const api = props.api;
const timer = props.timer;
const num = ref(0);

async function update(stat: status)
{
	entry.value.status = stat;
	await api.putUser(entry.value, num);
	if (entry.value.status == status.away)
		timer.send('ACK ' + JSON.stringify(entry.value));
}
</script>

<template>
	<v-btn
		@click="update(status.away)"
		:disabled="!started || entry.status == status.away || !entry.num"
		border
		flat
		size="small"
		class="text-none"
		text="Away" />
	
	<v-btn
		@click="update(status.emergency)"
		:disabled="!started || entry.status == status.emergency"
		border
		flat
		size="small"
		class="text-none"
		text="Emergency" />
	
	<v-btn
		@click="update(status.seated)"
		:disabled="!started || entry.status == status.seated"
		border
		flat
		size="small"
		class="text-none"
		text="Seated" />
</template>