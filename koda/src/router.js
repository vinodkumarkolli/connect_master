import { createRouter, createWebHistory } from 'vue-router'
import { frappeRequest } from 'frappe-ui'

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
  {
    path: '/manage',
    name: 'Manage',
    component: () => import('@/pages/Manage.vue'),
  },
  {
    path: '/restricted',
    name: 'Restricted',
    component: () => import('@/pages/Restricted.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/koda'),
  routes,
})

let cachedUser = null
let cachedRoles = null

router.beforeEach(async (to, from, next) => {
  try {
    if (!cachedUser) {
        let res = await frappeRequest({ url: 'frappe.auth.get_logged_user' })
        cachedUser = res.message || res
        console.log('Fetched User:', cachedUser)
    }

    if (to.name === 'Restricted') {
        next()
        return
    }

    if (cachedUser === 'Guest') {
        if (to.name === 'Home') {
            next()
        } else {
            next({ name: 'Home' })
        }
        return
    }

    if (!cachedRoles) {
        console.log('Fetching roles for user:', cachedUser)
        let res = await frappeRequest({
            url: 'connect_master.utils.get_user_roles'
        })
        // console.log('get_user_roles response:', res)
        
        if (Array.isArray(res)) {
            cachedRoles = res
        } else if (res && Array.isArray(res.message)) {
            cachedRoles = res.message
        } else {
            cachedRoles = []
        }
        // console.log('Fetched Roles:', cachedRoles)
    } else {
        // console.log('Using Cached Roles:', cachedRoles)
    }

    if (cachedRoles.includes('Customer')) {
        console.log('Access Granted')
        next()
    } else {
        console.log('Access Denied. Redirecting to Restricted.')
        next({ name: 'Restricted' })
    }
  } catch (e) {
    console.error('Auth check failed', e)
    next()
  }
})

export default router
