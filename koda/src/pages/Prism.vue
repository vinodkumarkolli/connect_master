<template>
  <div class="w-full bg-gray-50 flex flex-col">
    
    <!-- Header (Visible when a view is active) -->
    <div v-if="currentView" class="bg-white border-b px-4 py-3 sm:px-6 sm:py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center shadow-sm z-10 flex-shrink-0 gap-2 sm:gap-0">
      <div class="flex items-center gap-3 w-full sm:w-auto">
        <button @click="currentView = null" class="p-2 hover:bg-gray-100 rounded-full transition-colors flex-shrink-0" title="Back to Menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        </button>
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900 flex items-center gap-2 truncate">
          <span v-if="currentView === 'Compass'">🧭 Compass</span>
          <span v-else-if="currentView === 'Punch'">👊 Punch Order</span>
          <span v-else-if="currentView === 'Manage'">✏️ Manage</span>
        </h1>
      </div>
      <div class="text-xs sm:text-sm text-gray-500 pl-11 sm:pl-0" v-if="userRoles.data">
        {{ displayRoles.join(', ') }}
      </div>
    </div>

    <!-- Main Content -->
    <div class="w-full relative">
      
      <!-- Menu (Centered) -->
      <transition name="fade">
        <div v-if="!currentView" class="flex items-center justify-center p-6 bg-gray-50 z-0 w-full">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl w-full">
            
            <!-- Punch Card -->
            <div
              v-if="isTerritoryAdmin"
              @click="currentView = 'Punch'"
              class="bg-white p-10 rounded-3xl shadow-lg hover:shadow-2xl border border-gray-100 cursor-pointer transition-all transform hover:-translate-y-2 flex flex-col items-center text-center group h-80 justify-center"
            >
              <div class="w-28 h-28 bg-red-50 rounded-full flex items-center justify-center mb-8 group-hover:bg-red-100 transition-colors group-hover:scale-110 duration-300">
                <span class="text-6xl">👊</span>
              </div>
              <h2 class="text-3xl font-bold text-gray-900 mb-3">Punch</h2>
              <p class="text-gray-500 text-lg">Create orders on behalf of customers</p>
            </div>

            <!-- Compass Card -->
            <div
            v-if="isTerritoryAdmin"
              @click="currentView = 'Compass'"
              class="bg-white p-10 rounded-3xl shadow-lg hover:shadow-2xl border border-gray-100 cursor-pointer transition-all transform hover:-translate-y-2 flex flex-col items-center text-center group h-80 justify-center"
            >
              <div class="w-28 h-28 bg-blue-50 rounded-full flex items-center justify-center mb-8 group-hover:bg-blue-100 transition-colors group-hover:scale-110 duration-300">
                <span class="text-6xl">🧭</span>
              </div>
              <h2 class="text-3xl font-bold text-gray-900 mb-3">Compass</h2>
              <p class="text-gray-500 text-lg">View and track all connect orders</p>
            </div>

            <!-- Manage Card -->
            <div 
              v-if="isTerritoryAdmin"
              @click="currentView = 'Manage'"
              class="bg-white p-10 rounded-3xl shadow-lg hover:shadow-2xl border border-gray-100 cursor-pointer transition-all transform hover:-translate-y-2 flex flex-col items-center text-center group h-80 justify-center"
            >
              <div class="w-28 h-28 bg-green-50 rounded-full flex items-center justify-center mb-8 group-hover:bg-green-100 transition-colors group-hover:scale-110 duration-300">
                <span class="text-6xl">✏️</span>
              </div>
              <h2 class="text-3xl font-bold text-gray-900 mb-3">Manage</h2>
              <p class="text-gray-500 text-lg">Search & Edit Addresses/Contacts</p>
            </div>

          </div>
        </div>
      </transition>

      <!-- Modules (Full Screen) -->
      <transition name="slide-up">
        <div v-if="currentView" class="bg-gray-50 flex flex-col p-6 z-10 w-full">
           
           <!-- Compass View -->
           <CompassView v-if="currentView === 'Compass'" />

           <!-- Punch View -->
           <PunchView v-if="currentView === 'Punch' && isTerritoryAdmin" />

           <!-- Manage View -->
           <ManageView v-if="currentView === 'Manage' && isTerritoryAdmin" />

        </div>
      </transition>

    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'
import CompassView from '../components/CompassView.vue'
import PunchView from '../components/PunchView.vue'
import ManageView from '../components/ManageView.vue'

// --- State ---
const currentView = ref(null) // null = Menu, 'Compass', 'Punch', 'Manage'

// --- Resources ---

const session = createResource({
    url: 'frappe.auth.get_logged_user',
    auto: true
})

const userRoles = createResource({
    url: 'connect_master.utils.get_user_roles',
    auto: true
})

const userRolesList = computed(() => {
    if (!userRoles.data) return []
    return Array.isArray(userRoles.data) ? userRoles.data : (userRoles.data.message || [])
})

const displayRoles = computed(() => {
    const allowed = ['Customer', 'Territory Admin', 'Partner Admin', 'System Manager']
    return userRolesList.value.filter(r => allowed.includes(r))
})

const isTerritoryAdmin = computed(() => userRolesList.value.includes('Territory Admin'))
const isPartnerAdmin = computed(() => userRolesList.value.includes('Partner Admin'))

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-up-enter-from {
  transform: translateY(20px);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
