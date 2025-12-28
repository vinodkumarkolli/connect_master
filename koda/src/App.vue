<template>
  <div class="flex flex-col min-h-screen">
    <header class="flex items-center justify-between px-6 py-4 border-b bg-white">
      <div class="text-xl font-bold">Koda</div>
      <div>
        <div v-if="session.data && session.data !== 'Guest'" class="flex items-center gap-2">
          <Dropdown :options="userMenuOptions">
            <template #default>
              <button class="flex items-center gap-2 focus:outline-none">
                <Avatar :label="session.data" />
              </button>
            </template>
          </Dropdown>
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
import { Avatar, Dropdown, createResource, frappeRequest } from 'frappe-ui'

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
  url: 'logout',
  onSuccess() {
    window.location.reload()
  },
})

const userMenuOptions = [
  {
    label: 'Orders',
    onClick: () => {
      // Navigate to orders
      console.log('Navigate to orders')
    },
  },
  {
    label: 'Manage',
    onClick: () => {
      // Navigate to manage
      console.log('Navigate to manage')
    },
  },
  {
    label: 'Signout',
    onClick: () => {
      logout.fetch()
    },
  },
]
</script>
