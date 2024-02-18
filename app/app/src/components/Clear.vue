<script setup lang="ts">
import { ref } from 'vue'
import { NumBreaks } from '@/common/iNumBreaks';
import { apiUseFetch } from '../composable/api'

const props = defineProps<{
	started: boolean,
	apiUseFetch: apiUseFetch
}>()

const dialog = ref(false);
const exam = ref(false);
const clear = ref(false);
const loading = ref(false);
const api = props.apiUseFetch;

async function clearAll()
{
	exam.value = true;
	if (clear.value)
	{
		loading.value = true;
		await api.clearAll();
		loading.value = false;
	}
	dialog.value = false;
}

function isClear()
{
	if (clear.value)
		return 'Yes';
	else
		return 'No';
}
</script>

<template>
	<v-row justify="center">
		<v-dialog v-model="dialog" persistent width="500" height="300">
			<template v-slot:activator="{ props }">
			<v-btn :disabled="started" v-bind="props" prepend-icon="mdi-nuke">
					Clear People
				</v-btn>
</template>
      <v-card class="flex-center flex-col">
        <v-card-title>
          <span class="text-h5">Clear All People From Server</span>
        </v-card-title>
		<v-card-subtitle v-if="clear" style="color: red;">
			This action is permanent!
		</v-card-subtitle>
        <v-card-text>
          <v-container class="flex-center flex-col" style="width: 100%;">
            <v-row style="width: 100%;">
			  <v-col
			  cols="12"
                sm="6"
				class="flex-center"
				style="width: fit-content; min-width: 200px;"
              >
			  <v-switch
				@click="clear ? clear = false : clear = true"
				:label="isClear()">
				</v-switch>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
		  	:loading="loading"
            color="blue-darken-1"
            variant="text"
			block
            @click="clearAll()"
          >
            Execute
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>