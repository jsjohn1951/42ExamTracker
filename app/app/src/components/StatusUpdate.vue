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
	try{
		const away = await api.getUsersAway();
		const breaks = await api.getBreaks();
		let gen = away.filter((element, index, array)=>{
			return (element.gender == entry.value.gender)
		})

		if (stat == status.away && gen.length >= parseInt(breaks.perFacility))
		{
			alert('Too many people in facility')
			return ;
		}
		entry.value.status = stat;
		entry.value.id = '0';
		await api.putUser(entry.value, num);
	} catch (err)
	{
		console.log(err);
		return ;
	}
}

async function download()
{
	if (entry.value.id && entry.value.id != '')
		await api.getIdHistory(entry.value.id);
}
</script>

<template>
		<v-row>
			<v-col>
				<v-btn
				@click="download()"
				:disabled="!started"
				border
				flat
				size="small"
				class="text-none"
				text="Download History" />
			</v-col>

			<v-col>
				<v-btn
				@click="update(status.away)"
				:disabled="!started || entry.status == status.away || !entry.num"
				border
				flat
				size="small"
				class="text-none"
				text="Away" />
			</v-col>

			<v-col>
				<v-btn
				@click="update(status.emergency)"
				:disabled="!started || entry.status == status.emergency"
				border
				flat
				size="small"
				class="text-none"
				text="Emergency" />
			</v-col>

			<v-col>
				<v-btn
				@click="update(status.seated)"
				:disabled="!started || entry.status == status.seated"
				border
				flat
				size="small"
				class="text-none"
				text="Back" />
			</v-col>
		</v-row>
	</template>