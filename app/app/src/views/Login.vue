<script setup lang="ts">
import { ref } from 'vue'
import { apiUseFetch, cookieClass } from '../composable/api'
import { wSocket } from '../composable/websocket'
import { useRouter } from 'vue-router';

const router = useRouter();
const toChange = ref(0);
const username = ref('');
const password = ref('');
const usernameRules = ref([ value => {
	if (username.value == '')
		return 'Please enter valid username!'
	return true
}]);
const passwordRules = ref([ value => {
	if (password.value == '')
		return 'Please enter valid password!'
	return true
}]);
const ws = new wSocket(toChange);
const api = new apiUseFetch(ref(ws));
const cookie = new cookieClass();
const noAuth = ref(false);

async function submit()
{
	noAuth.value = false;
	const token = await api.authenticate(username.value, password.value);
	if (token)
	{
		cookie.setAuth(token);
		router.go(0);
		return ;
	}
	noAuth.value = true;
}
</script>

<template>
	<div class="flex-center flex-col" style="width: 100vw; height: fit-content; padding: 18px; gap: 24px;">
		<v-card>
			<v-card-title>Please Login to Proceed</v-card-title>
			<v-sheet width="300" class="mx-auto">
				<v-form @submit.prevent validate-on="submit">
					<v-text-field v-model="username" :rules="usernameRules" label="Username"></v-text-field>
					<v-text-field v-model="password" :rules="passwordRules" label="Password"></v-text-field>
					<p v-if="noAuth" style="color: red; width: 100%;" class="font-weight-thin flex-center text-overline">Incorrect Username or Password</p>
					<v-btn type="submit" @click="submit" block class="mt-2">Submit</v-btn>
				</v-form>
			</v-sheet>
		</v-card>
	</div>
</template>
