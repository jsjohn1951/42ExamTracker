<script setup lang="ts">
import { ref } from 'vue'

const dialog = ref(false);

async function download()
{
	dialog.value = false;
}
</script>

<template>
	<v-row justify="center">
		<v-dialog @click:outside="dialog = false" v-model="dialog" persistent width="500" height="300">
			<template v-slot:activator="{ props }">
			<v-btn v-bind="props" prepend-icon="mdi-book-open-page-variant">
					Manual
				</v-btn>
</template>
      <v-card class="flex-center flex-col">
        <v-card-title>
          <span class="text-h5">User Manual</span>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
			block
            @click="dialog = false"
          >
            Finish Reading
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>