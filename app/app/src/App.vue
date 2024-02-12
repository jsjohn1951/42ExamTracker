<script setup lang="ts">
import Data from '@/components/Data.vue'
</script>

<template>
	<v-theme-provider theme="dark">
	<v-app>
			<v-main>
					<div class="app-container">
						<Data/>
					</div>
			</v-main>
		</v-app>
	</v-theme-provider>
</template>

<style>
.app-container {
	height: fit-content;
	min-height: 100vh;
	width: 100vw;
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
