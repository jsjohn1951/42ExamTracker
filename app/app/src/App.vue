<script setup lang="ts">
import Data from '@/components/Data.vue'
</script>

<template>
	<v-theme-provider theme="dark">
	<v-app style="width: 100vw;">
			<v-main style="width: 100vw;">
					<div class="app-container flex-center" style="padding: 50px;">
						<Suspense>
							<Data/>
						</Suspense>
					</div>
			</v-main>
		</v-app>
	</v-theme-provider>
</template>

<style>
html, body, #app {
	width: 100%;
	overflow-x: hidden;
	margin: 0;
	padding: 0;
	scrollbar-width: none;
	-ms-overflow-style: none;
}

html::-webkit-scrollbar {
    display: none;
}

.app-container {
	height: fit-content;
	min-height: 100vh;
	width: 100vw;
}

#app {
  margin: 0;
  padding: 0;
}

.flex-center {
	display: flex;
	justify-content: center;
	align-items: center;
}

.flex-col {
	display: flex;
	flex-direction: column;
}

.flex-between {
	display: flex;
	justify-content: space-between;
}

.flex-start {
	display: flex;
	justify-content: start;
	align-items: center;
}

.flex-end {
	display: flex;
	justify-content: end;
	align-items: center;
}
</style>
