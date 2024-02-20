<script setup lang="ts">
import { ref } from 'vue'
import { VCardText } from 'vuetify/lib/components/index.mjs';

const dialog = ref(false);

async function download()
{
	dialog.value = false;
}
</script>

<template>
	<v-row justify="center">
		<v-dialog @click:outside="dialog = false" v-model="dialog" width="900">
			<template v-slot:activator="{ props }">
			<v-btn v-bind="props" prepend-icon="mdi-book-open-page-variant">
					Manual
				</v-btn>
</template>
      <v-card class="flex-center flex-col">
        <v-card-title style="padding: 10px;">
          <span class="text-h5">User Manual</span>
        </v-card-title>
		<v-card-text class="text-body-2 font-weight-light">
			<div style="max-height: 500px;">
			<div>
				The following is some useful info to help Proctors and Staff to get started:
			</div>
			<br>
			<div>
				<ol>
					<img style="width: 100%; max-width: 400px;" src="/example2.png"/>
					<li>Use the 'add' / 'remove' buttons within the "42Exam / InsertOrRemove" section to add a student / pisciner to the session.
						<br>
						<ul>
							<li>On hover-over these buttons will drop down a form prompting the proctor to enter
								either an id !number! (found on pisciner / student access cards), or an intra Login if no id exists.
							</li>
							<li>
								The 'add' button will prompt the proctor to select either Male / Female in order to properly track
								the number of persons per facility.
							</li>
						</ul>
					</li>

					<img src="/example1.png" style="width: 100%; max-width: 300px;"/>
					<li>Once added the proctor will notice a new pisciner / student entry within the "42Exam / Control Panel" section. Several Options
						are present to allow the proctor to view that pisciner / student's history, and to set the status of that pisciner / student.
						<ul>
							<li>
								<strong>Download History</strong> - allows a staff member / proctor to download a .txt history file (including the status change and timestamp) related to that entry.
							</li>
							<li>
								<strong>Away</strong> - will change the status of the student / pisciner to away (indicating that they have left the lab and entered a facility, e.g. 'washroom'),
								and starts a timer that will be displayed within the "42Exam / Away" section.
							</li>
							<li>
								<strong>Emerency</strong> - button marks the student / pisciner as having an emergency and ensures that emergencies are logged as well as
								when a student / pisciner enters or leaves the lab.
							</li>
							<li>
								<strong>Back</strong> - button marks the student / pisciner as having returned to the lab.
							</li>
						</ul>
					</li>

					<img src="/example3.png" style="width: 100%; max-width: 300px;"/>
					<li>
						Using the search-bar within the "42Exam / Control Panel" section allows the proctor / staff to search for a specific pisciner / student either by
						their access card id or by their Intra Login.
					</li>

				</ol>
				<v-card-actions>
				  <v-spacer/>
				  <v-btn
					color="blue-darken-1"
					variant="text"
					block
					@click="dialog = false"
				  >
					Finish Reading
				  </v-btn>
				</v-card-actions>
			</div>
		</div>
		</v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<style scoped>
ul > li {
    margin-left: 15px;
}

ol > li {
    padding-bottom: 20px;
}
</style>