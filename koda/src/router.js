import { createRouter, createWebHistory } from 'vue-router'
import { frappeRequest } from 'frappe-ui'
import { useSession } from '@/composables/useSession'

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
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
  },
  {
    path: '/dash',
    name: 'Prism',
    component: () => import('@/pages/Prism.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/pages/About.vue'),
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/pages/Contact.vue'),
  },
  {
    path: '/terms',
    name: 'TermsAndConditions',
    component: () => import('@/pages/TermsAndConditions.vue'),
  },
  {
    path: '/sasb',
    name: 'Sasb',
    component: () => import('@/pages/Sasb.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/koda'),
  routes,
})

let cachedRoles = null

router.beforeEach(async (to, from, next) => {
  const session = useSession()
  try {
    let cachedUser = session.data
    if (!cachedUser) {
        cachedUser = await session.fetch()
    }

    if (to.name === 'Restricted') {
        next()
        return
    }

    if (cachedUser === 'Guest') {
        if (to.name === 'Home' || to.name === 'Login' || to.name === 'About' || to.name === 'Contact' || to.name === 'TermsAndConditions' || to.name === 'Sasb') {
            next()
        } else {
            next({ name: 'Home' })
        }
        return
    }

    if (!cachedRoles) {
        // console.log('Fetching roles for user:', cachedUser)
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

    if (to.name === 'Prism') {
        if (cachedRoles.includes('Territory Admin') || cachedRoles.includes('Partner Admin')) {
            next()
        } else {
            next({ name: 'Restricted' })
        }
        return
    }

    if (cachedRoles.includes('Territory Admin') || cachedRoles.includes('Partner Admin')) {
        if (to.name === 'Home') {
            next({ name: 'Prism' })
            return
        }
        next()
        return
    }

    if (cachedRoles.includes('Customer')) {
        next()
    } else {
        next({ name: 'Restricted' })
    }
  } catch (e) {
    next()
  }
})

export default router
