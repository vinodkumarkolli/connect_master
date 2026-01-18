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
      
      <!-- Hamburger Menu for Mobile -->
      <div class="md:hidden flex items-center">
        <button ref="hamburgerButtonRef" @click="toggleMobileMenu" class="text-gray-700 focus:outline-none">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path :class="{'hidden': isMobileMenuOpen, 'block': !isMobileMenuOpen}" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            <path :class="{'block': isMobileMenuOpen, 'hidden': !isMobileMenuOpen}" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <!-- Desktop Navigation -->
      <div class="hidden md:flex items-center gap-6">
        <CustomDropdown :options="productOptions">
          <button class="text-sm font-medium text-gray-700 hover:text-gray-900 flex items-center focus:outline-none">
            Products
            <svg class="ml-1 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </CustomDropdown>
        <router-link to="/about" custom v-slot="{ href, navigate }">
          <div>
            <a :href="href" @click="navigate" class="text-sm font-medium text-gray-700 hover:text-gray-900">About us</a>
          </div>
        </router-link>
        <router-link to="/contact" custom v-slot="{ href, navigate }">
          <div>
            <a :href="href" @click="navigate" class="text-sm font-medium text-gray-700 hover:text-gray-900">Contact us</a>
          </div>
        </router-link>
        <router-link to="/terms" custom v-slot="{ href, navigate }">
          <div>
            <a :href="href" @click="navigate" class="text-sm font-medium text-gray-700 hover:text-gray-900">Terms and Conditions</a>
          </div>
        </router-link>
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
      
      <!-- Mobile Menu Dropdown -->
      <div ref="mobileMenuRef" v-show="isMobileMenuOpen" class="md:hidden absolute top-full left-0 right-0 bg-white border-b shadow-lg z-50">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <div class="space-y-1">
            <button @click="isProductsOpen = !isProductsOpen" class="w-full flex justify-between items-center px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <span>Products</span>
              <svg :class="{'rotate-180': isProductsOpen}" class="w-5 h-5 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </button>
            <div v-show="isProductsOpen" class="pl-4 space-y-1">
               <router-link to="/sasb" custom v-slot="{ href, navigate }">
                  <a :href="href" @click="navigate" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">Sastry Balm</a>
               </router-link>
            </div>
          </div>
          <router-link to="/about" custom v-slot="{ href, navigate }">
            <a :href="href" @click="navigate" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">About us</a>
          </router-link>
          <router-link to="/contact" custom v-slot="{ href, navigate }">
            <a :href="href" @click="navigate" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">Contact us</a>
          </router-link>
          <router-link to="/terms" custom v-slot="{ href, navigate }">
            <a :href="href" @click="navigate" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">Terms and Conditions</a>
          </router-link>
          <div v-if="session.data && session.data !== 'Guest'" class="border-t border-gray-200 pt-2">
            <div class="flex items-center px-3 py-2">
              <Avatar :label="session.data" class="mr-2" />
              <span class="text-sm font-medium text-gray-700">{{ session.data }}</span>
            </div>
            <button @click="logout.fetch" class="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">Sign out</button>
          </div>
          <div v-else class="border-t border-gray-200 pt-2">
            <a href="/koda/login" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-md">Login</a>
          </div>
        </div>
      </div>
    </header>
    <main class="flex flex-col justify-center items-center pb-16">
      <router-view />
    </main>
    <footer class="fixed bottom-0 w-full py-2 text-center text-sm text-gray-600 border-t bg-white/80 backdrop-blur-md z-50">
      &copy; 2026 Sravi Enterprises. All rights reserved
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Avatar, createResource, frappeRequest } from 'frappe-ui'
import CustomDropdown from './components/CustomDropdown.vue'
import { useSession } from './composables/useSession'

const router = useRouter()
const isMobileMenuOpen = ref(false)
const isProductsOpen = ref(false)
const session = useSession()
const mobileMenuRef = ref(null)
const hamburgerButtonRef = ref(null)

router.afterEach(() => {
  isMobileMenuOpen.value = false
})

function handleClickOutside(event) {
  if (isMobileMenuOpen.value &&
      mobileMenuRef.value && !mobileMenuRef.value.contains(event.target) &&
      hamburgerButtonRef.value && !hamburgerButtonRef.value.contains(event.target)) {
    isMobileMenuOpen.value = false
  }
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  await session.fetch()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
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

const productOptions = [
  {
    label: 'Sastry Balm',
    onClick: () => {
      router.push('/sasb')
    },
  },
]

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>
