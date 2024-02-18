<script setup lang="ts">
import { person, status, gen, api } from '../common/iPerson'
import { Ref, ref } from 'vue'
import Person from './Person.vue'
import { apiUseFetch } from '../composable/api'

const props = defineProps<{
	useFetch: apiUseFetch
}>()

let entryMale: Ref<person[]> = ref([]);
let entryFemale: Ref<person[]> = ref([]);
let item;
const apiFetch = props.useFetch;
const started = ref(true);
const all = ref(await apiFetch.getUsersAway());

for (item of all.value)
{
	const entity = {
		id: item.id ? item.id!.toString() : item.user!,
		username: item.user ? item.user! : '',
		status: item.status ? item.status! : status.seated,
		gender: item.gender ? item.gender! : gen.male,
		num: item.num ? item.num! : 0,
		time: item.time ? item.time! : undefined
	}
	if (item.gender == gen.male)
		entryMale.value.push(entity);
	else
		entryFemale.value.push(entity);
}
</script>

<template>
	<v-card class="flex-center flex-col" style="padding: 0px 15px 0px 15px; max-width: 900px;">
		<v-row>
			<v-card-title class="text-subtitle-2"><v-breadcrumbs :items="['42Exam', 'Away']"></v-breadcrumbs></v-card-title>
		</v-row>
		<v-row>
			<v-col>
				<v-card class="flex-center flex-col" style="min-width: 260px; padding: 12px; gap: 12px;">
					<v-card-title class="text-subtitle-2">Male</v-card-title>
					<div v-for="item in entryMale">
						<Person :away="true" :api="useFetch" :item="item" :started="started"/>
					</div>
				</v-card>
			</v-col>
			<v-col>
				<v-card class="flex-center flex-col" style="min-width: 260px; padding: 12px; gap: 12px;">
					<v-card-title class="text-subtitle-2">Female</v-card-title>
					<div v-for="item in entryFemale">
						<Person :away="true" :api="useFetch" :item="item" :started="started"/>
					</div>
				</v-card>
			</v-col>
		</v-row>
	</v-card>
</template>