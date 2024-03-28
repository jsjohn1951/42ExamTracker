<script setup lang="ts">
import { ref, Ref } from 'vue';
import { person, status, gen } from '../common/iPerson';
import { apiUseFetch } from '../composable/api'

const props = defineProps<{
	apiUseFetch: apiUseFetch
}>();

const emit = defineEmits({
	reload: ({ res : boolean}) => {
		return true;
	}
});

const pId = ref('');
const pUsername = ref('');
const pGender = ref(gen.male);
const expand = ref(false)
const api = props.apiUseFetch;
const err = ref(false);

async function submit()
{
	if (!pId.value.length && !pUsername.value.length)
	{
		err.value = true;
		return;
	}
	let nPerson: person = {
		id: pId.value,
		username: pUsername.value,
		status: status.seated,
		gender: pGender.value,
		num: 0,
		time: ''
	}
	await api.postUser(nPerson);

	pId.value = '';
	pUsername.value = '';
	err.value = false;
}

</script>

<template>
<v-sheet @mouseover="expand = true" @mouseleave="expand = false, err = false" width="300" class="mx-auto flex-center flex-col">
    <v-form @submit.prevent style="width: 100%;">

		<!-- <v-expand-transition>

			<v-text-field
			v-if="expand"
			v-model="pId"
			label="Id"
			/>

		</v-expand-transition> -->

		<v-expand-transition>

			<v-text-field
			v-if="expand"
			v-model="pUsername"
			label="Intra Login / Card ID"
			/>
		</v-expand-transition>

		<v-expand-transition>
			<p v-if="expand && err" class="text-overline font-weight-thin text-center" style="color: red;">Both Id and Username cannot be empty*</p>
		</v-expand-transition>
		<v-expand-transition>

			<div v-if="expand" class="flex-start" style="width: 100%; height: fit-content; padding-left: 18px;">
				<v-switch
				v-if="expand"
				@click="pGender != gen.female ? pGender = gen.female : pGender = gen.male"
				:label="pGender">
				</v-switch>
			</div>

		</v-expand-transition>


      <v-btn @click="submit()" type="submit" block class="mt-2">Add Person</v-btn>
    </v-form>
  </v-sheet>
</template>