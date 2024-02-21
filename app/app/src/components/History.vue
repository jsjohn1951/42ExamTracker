<script setup lang="ts">
import { ref } from 'vue'
import { apiUseFetch } from '../composable/api'

const props = defineProps<{
	apiUseFetch: apiUseFetch
}>()

const dialog = ref(false);
const exam = ref(false);
const loading = ref(false);
const api = props.apiUseFetch;

async function download()
{
	exam.value = true;
	loading.value = true;
	await api.getHistory();
	loading.value = false;
	dialog.value = false;
}
</script>

<template>
	<v-row justify="center">
		<v-dialog @click:outside="dialog = false" v-model="dialog" persistent width="500" height="300">
			<template v-slot:activator="{ props }">
			<v-btn v-bind="props" prepend-icon="mdi-tortoise">
					Download History
				</v-btn>
</template>
      <v-card class="flex-center flex-col">
        <v-card-title>
          <span class="text-h5">Download 'Logfile.txt'</span>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
		  	:loading="loading"
            color="blue-darken-1"
            variant="text"
			block
            @click="download()"
          >
            Execute
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>