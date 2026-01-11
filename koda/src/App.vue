<template>
  <div class="flex flex-col min-h-screen">
    <header class="flex items-center justify-between px-6 py-4 border-b bg-white relative z-50">
      <div 
        class="flex items-center text-xl font-bold cursor-pointer group" 
        @click="router.push('/')"
      >
        <!-- SVG Logo (The 'K') -->
        <svg 
          viewBox="0 0 48 48" 
          class="w-6 h-6 mr-0.5 transition-transform duration-200 group-hover:scale-110" 
          xmlns="www.w3.org"
          fill="none" 
          stroke="currentColor" 
          stroke-width="3.5" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        >
          <!-- The outer box -->
          <path d="M40.5,5.5H7.5a2,2,0,0,0-2,2v33a2,2,0,0,0,2,2h33a2,2,0,0,0,2-2V7.5A2,2,0,0,0,40.5,5.5Z"/>
          <!-- The 'K' lines -->
          <line x1="17.31" y1="10.54" x2="17.31" y2="37.42"/>
          <line x1="20.78" y1="23.98" x2="30.69" y2="10.63"/>
          <line x1="20.78" y1="23.98" x2="30.69" y2="37.46"/>
          <line x1="20.78" y1="23.98" x2="17.31" y2="23.98"/>
        </svg>
        
        <!-- Remaining text -->
        <span class="tracking-tight">oda</span>
      </div>
      <div>
        <div v-if="session.data && session.data !== 'Guest'" class="flex items-center gap-2">
          <CustomDropdown :options="userMenuOptions">
            <button class="flex items-center gap-2 focus:outline-none">
              <Avatar :label="session.data" />
            </button>
          </CustomDropdown>
        </div>
        <div v-else>
          <a href="/koda/login" class="text-sm font-medium text-gray-700 hover:text-gray-900">Login</a>
        </div>
      </div>
    </header>
    <main class="flex flex-col justify-center items-center">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Avatar, createResource, frappeRequest } from 'frappe-ui'
import CustomDropdown from './components/CustomDropdown.vue'

const router = useRouter()
const session = reactive({
  data: 'Guest'
})

onMounted(async () => {
  try {
    let res = await frappeRequest({ url: 'frappe.auth.get_logged_user' })
    if (res) session.data = res.message || res
  } catch (e) {
    session.data = 'Guest'
  }
})

const logout = createResource({
  url: '/api/method/logout',
  onSuccess() {
    window.location.href = '/'
  },
  onError(error) {
    console.error('Logout failed:', error)
  },
})

const userMenuOptions = [
  {
    label: 'Signout',
    onClick: () => {
      logout.fetch()
    },
  },
]
</script>
