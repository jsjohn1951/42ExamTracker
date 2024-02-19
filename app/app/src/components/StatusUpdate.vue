<script setup lang="ts">
import { apiUseFetch } from '../composable/api'
import { person, status, api } from '../common/iPerson'
import { ref } from 'vue'

const props = defineProps < {
	api: apiUseFetch,
	entry: person,
	started: boolean,
	away?: boolean
} > ();

const entry = ref(props.entry);
const api = props.api;
const num = ref(0);

async function update(stat: status)
{
	const away = await api.getUsersAway();
	const breaks = await api.getBreaks();
	console.log('breaks: ', breaks.perFacility)
	let gen = away.filter((element, index, array)=>{
		return (element.gender == entry.value.gender)
	})

	if (stat == status.away && gen.length >= parseInt(breaks.perFacility))
		return ;
	entry.value.status = stat;
	await api.putUser(entry.value, num);
}
</script>

<template>
	<!-- <div style="width: 100%;">
		<v-row > -->
			<!-- <v-col class="flex-start"> -->
				<v-btn
				@click="update(status.away)"
				:disabled="!started || entry.status == status.away || !entry.num"
				border
				flat
				size="small"
				class="text-none"
				text="Away" />
			<!-- </v-col> -->
			
			<!-- <v-col class="flex-center"> -->
				<v-btn
				@click="update(status.emergency)"
				:disabled="!started || entry.status == status.emergency"
				border
				flat
				size="small"
				class="text-none"
				text="Emergency" />
			<!-- </v-col> -->
			
			<!-- <v-col class="flex-end"> -->
				<v-btn
				@click="update(status.seated)"
				:disabled="!started || entry.status == status.seated"
				border
				flat
				size="small"
				class="text-none"
				text="Seated" />
			<!-- </v-col> -->
		<!-- </v-row>
	</div> -->
	</template>