<script setup lang="ts">
import { ref } from 'vue'
import { NumBreaks } from '@/common/iNumBreaks';
import { apiUseFetch } from '../composable/api'

const props = defineProps<{
	started: boolean,
	apiUseFetch: apiUseFetch
}>()

const emit = defineEmits({
	start: ({ res : boolean}) => {
		return true;
	}
});

const dialog = ref(false);
const exam = ref(false);
const perPerson = ref('');
const perFacility = ref('');
const loading = ref(false);
const api = props.apiUseFetch;

async function startExam()
{
	exam.value = true;
	if (!perPerson.value.length || !perFacility.value.length)
		alert('Please choose an approriate value for both fields');
	else
	{
		loading.value = true;
		await api.postBreaks({
			perFacility: perFacility.value,
			perPerson: perPerson.value 
		});
		await api.putStart(true);
		loading.value = false;
		dialog.value = false;
		emit('start', true);
	}

}
</script>

<template>
	<v-row justify="center">
		<v-dialog v-model="dialog" persistent width="1024">
			<template v-slot:activator="{ props }">
			<v-btn :disabled="started" v-bind="props" prepend-icon="mdi-google-downasaur">
					Start Exam
				</v-btn>
</template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Facility Permissions</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
			  <v-col
			  cols="12"
                sm="6"
              >
                <v-select
                  :items="['1', '2', '3', '4', '5', '6']"
                  label="Number Of Entries to Facility Permitted per Person*"
                  required
				  v-model="perPerson"
                ></v-select>
              </v-col>
              <v-col
			  cols="12"
                sm="6"
              >
                <v-select
                  :items="['1', '2', '3', '4', '5', '6']"
                  label="Total Persons Permitted Within Facility at Once*"
                  required
				  v-model="perFacility"
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
		  	:loading="loading"
            color="blue-darken-1"
            variant="text"
			block
            @click="startExam()"
          >
            Start Exam
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>