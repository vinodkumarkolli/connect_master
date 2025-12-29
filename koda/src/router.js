import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: '/order',
    name: 'Order',
    component: () => import('@/pages/Order.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/koda'),
  routes,
})

export default router
