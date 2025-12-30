<template>
  <div class="flex flex-col min-h-screen">
    <header class="flex items-center justify-between px-6 py-4 border-b bg-white">
      <div class="text-xl font-bold cursor-pointer" @click="router.push('/')">Koda</div>
      <div>
        <div v-if="session.data && session.data !== 'Guest'" class="flex items-center gap-2">
          <CustomDropdown :options="userMenuOptions">
            <button class="flex items-center gap-2 focus:outline-none">
              <Avatar :label="session.data" />
            </button>
          </CustomDropdown>
        </div>
        <div v-else>
          <a href="/login" class="text-sm font-medium text-gray-700 hover:text-gray-900">Login</a>
        </div>
      </div>
    </header>
    <main class="flex-1">
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
