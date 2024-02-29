// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { apiAuth } from '@/composable/api'
let authenticate = new apiAuth();

const routes = [
  {
    path: '/',
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Data.vue')
      },
	  {
        path: '/login',
        name: 'login',
        component: () => import('@/views/Login.vue')
      }
    ],
  },
  {
	path: '/:pathMatch(.*)*',
	name: 'NotFound',
	component: () => import('@/views/404.vue')
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from) => {
	const auth = await authenticate.auth();
	if (!auth && to.name == 'Home')
		return {name: 'login'};
	if (auth && to.name == 'login')
		return {name: 'Home'};
})

export default router