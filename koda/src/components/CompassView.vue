<template>
  <div class="bg-white rounded-lg shadow border flex flex-col h-full relative overflow-hidden">
    <!-- Header -->
    <div class="p-4 border-b bg-gray-50 flex flex-col gap-4 flex-shrink-0">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-bold text-gray-800">Connect Orders</h2>
          <p class="text-xs text-gray-500">Manage and track orders</p>
        </div>
        <div class="flex items-center gap-2">
            <!-- View Selector -->
            <div class="flex bg-gray-200 rounded p-1">
                <button @click="currentView = 'List'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', currentView === 'List' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">List</button>
                <button @click="currentView = 'Kanban'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', currentView === 'Kanban' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">Kanban</button>
                <button @click="currentView = 'Summary'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', currentView === 'Summary' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">Summary</button>
            </div>
            <Button @click="showFilters = !showFilters" :variant="hasActiveFilters ? 'solid' : 'subtle'" size="sm">
                Filters {{ hasActiveFilters ? '(Active)' : '' }}
            </Button>
        </div>
      </div>
      
      <div class="flex justify-between items-center gap-4">
          <!-- Tabs -->
          <div class="flex gap-6 border-b border-transparent">
              <button
                v-for="tab in tabs"
                :key="tab"
                @click="activeTab = tab; orders.reload()"
                :class="['pb-2 text-sm font-medium border-b-2 transition-colors', activeTab === tab ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
              >
                {{ tab }}
              </button>
          </div>
          
          <!-- Search -->
          <div class="w-64">
            <Input v-model="searchQuery" placeholder="Search Orders..." @keyup.enter="orders.reload()" />
          </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto p-0 relative bg-gray-50">
      <div v-if="orders.loading" class="flex justify-center p-12">
        <LoadingIndicator />
      </div>
      <div v-else-if="orders.error" class="p-12 text-center text-red-500">
        {{ orders.error.message || 'Error loading orders' }}
        <div class="mt-2">
            <Button size="sm" @click="orders.reload()">Retry</Button>
        </div>
      </div>
      <div v-else-if="!orders.data || orders.data.length === 0" class="p-12 text-center text-gray-500">
        No orders found.
      </div>
      <div v-else class="h-full">
          <!-- List View -->
          <div v-if="currentView === 'List'" class="bg-white min-h-full">
             <div class="divide-y">
                 <div v-for="order in orders.data" :key="order.name" class="p-4 hover:bg-gray-50 transition-colors cursor-pointer flex items-center justify-between group">
                    <div class="flex items-start gap-4">
                        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-lg">
                            📦
                        </div>
                        <div>
                            <div class="flex items-center gap-2 mb-1">
                                <span class="font-medium text-gray-900">{{ order.name }}</span>
                                <span :class="['px-2 py-0.5 rounded-full text-xs font-medium', getOrderStatusClasses(order.order_status)]">
                                    {{ order.order_status }}
                                </span>
                            </div>
                            <div class="text-sm text-gray-600">
                                {{ order.address_title }} • {{ order.custom_resolved_territory }}
                            </div>
                            <div class="text-xs text-gray-500 mt-1">
                                {{ order.user }} • {{ formatDate(order.order_date) }}
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="text-right">
                            <div class="text-sm font-medium text-gray-700">{{ getChannelName(order.service_category) }}</div>
                            <div class="text-xs text-gray-500 mt-1" v-if="order.channel_partner">{{ getPartnerName(order.channel_partner) }}</div>
                        </div>
                        <button @click.stop="toggleMenu(order.name, $event)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                        </button>
                    </div>
                 </div>
             </div>
          </div>
          
          <!-- Kanban View -->
          <div v-else-if="currentView === 'Kanban'" class="flex h-full overflow-x-auto p-4 gap-4 items-start">
              <div v-for="status in kanbanStatuses" :key="status" class="w-72 flex-shrink-0 flex flex-col bg-gray-100 rounded-lg max-h-full">
                  <div class="p-3 font-bold text-gray-700 text-sm uppercase flex justify-between items-center">
                      {{ status }}
                      <span class="bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full text-xs">{{ getOrdersByStatus(status).length }}</span>
                  </div>
                  <div class="p-2 space-y-2 overflow-y-auto flex-1">
                      <div v-for="order in getOrdersByStatus(status)" :key="order.name" class="bg-white p-3 rounded shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
                          <div class="flex justify-between items-start mb-2">
                              <span class="font-medium text-sm text-gray-900">{{ order.name }}</span>
                              <span class="text-xs text-gray-400">{{ formatDateShort(order.order_date) }}</span>
                          </div>
                          <div class="text-xs text-gray-600 mb-2 line-clamp-2">{{ order.address_title }}</div>
                          <div class="text-xs text-gray-400 mb-2 truncate" v-if="order.channel_partner">
                              {{ getPartnerName(order.channel_partner) }}
                          </div>
                          <div class="flex justify-between items-center mt-2 pt-2 border-t border-gray-100">
                              <span class="text-xs font-medium text-blue-600">{{ getChannelName(order.service_category) }}</span>
                              <div class="flex items-center gap-2">
                                  <div class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-xs" :title="order.user">
                                      {{ order.user ? order.user[0].toUpperCase() : '?' }}
                                  </div>
                                  <button @click.stop="toggleMenu(order.name, $event)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                                  </button>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
          
          <!-- Summary View -->
          <div v-else-if="currentView === 'Summary'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-4">
              <div v-for="order in orders.data" :key="order.name" class="bg-white p-4 rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer flex flex-col">
                  <div class="flex justify-between items-start mb-3">
                      <div>
                          <div class="font-bold text-gray-900">{{ order.name }}</div>
                          <div class="text-xs text-gray-500">{{ formatDate(order.order_date) }}</div>
                      </div>
                      <span :class="['px-2 py-1 rounded text-xs font-medium', getOrderStatusClasses(order.order_status)]">
                          {{ order.order_status }}
                      </span>
                  </div>
                  
                  <div class="flex-1 space-y-2 mb-4">
                      <div class="flex items-start gap-2 text-sm">
                          <span class="text-gray-400 w-4">📍</span>
                          <span class="text-gray-700 line-clamp-2">{{ order.address_title }}</span>
                      </div>
                      <div class="flex items-center gap-2 text-sm">
                          <span class="text-gray-400 w-4">🏷️</span>
                          <span class="text-gray-700">{{ getChannelName(order.service_category) }}</span>
                      </div>
                      <div class="flex items-center gap-2 text-sm" v-if="order.channel_partner">
                          <span class="text-gray-400 w-4">🤝</span>
                          <span class="text-gray-700 truncate">{{ getPartnerName(order.channel_partner) }}</span>
                      </div>
                  </div>
                  
                  <div class="pt-3 border-t flex justify-between items-center">
                      <div class="text-xs text-gray-500">
                          {{ order.custom_resolved_territory }}
                      </div>
                      <div class="flex items-center gap-2">
                          <div class="text-xs font-medium text-blue-600">
                              {{ order.user }}
                          </div>
                          <button @click.stop="toggleMenu(order.name, $event)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                          </button>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    </div>
    
    <!-- Action Menu Overlay -->
    <div v-if="activeMenuOrderId" class="fixed inset-0 z-40" @click="closeMenu"></div>
    
    <!-- Action Menu Dropdown -->
    <div v-if="activeMenuOrderId"
         class="fixed z-50 bg-white rounded-lg shadow-xl border w-40 py-1 overflow-hidden"
         :style="{ top: menuPosition.top + 'px', left: menuPosition.left + 'px' }">
        <button v-for="action in menuActions"
                :key="action"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                @click="closeMenu">
            {{ action }}
        </button>
    </div>

    <!-- Overlay for filters -->
    <div v-if="showFilters" class="absolute inset-0 bg-black bg-opacity-20 z-10" @click="showFilters = false"></div>

    <!-- Filter Sidebar -->
    <div v-if="showFilters" class="absolute inset-y-0 right-0 w-80 bg-white shadow-2xl border-l z-20 flex flex-col transform transition-transform duration-300 ease-in-out">
        <div class="p-4 border-b flex justify-between items-center bg-gray-50">
            <h3 class="font-bold text-gray-800">Filters</h3>
            <button @click="showFilters = false" class="text-gray-500 hover:text-gray-700 text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-5 space-y-6">
            <!-- Filter Fields -->
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Service Category</label>
                <select v-model="filters.custom_address_category" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white">
                    <option value="">All Categories</option>
                    <option v-for="opt in serviceChannels.data" :key="opt.name" :value="opt.name">{{ opt.channel_name }}</option>
                </select>
            </div>
            
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Territory</label>
                <div class="relative">
                    <Autocomplete
                        v-model="filters.custom_resolved_territory"
                        :options="territoryOptions"
                        placeholder="Select Territory"
                    />
                </div>
                <div v-if="filters.custom_resolved_territory" class="mt-3 flex items-center gap-2 bg-blue-50 p-2 rounded border border-blue-100">
                    <input type="checkbox" v-model="filters.include_child_territories" id="inc_child" class="rounded text-blue-600 focus:ring-blue-500" />
                    <label for="inc_child" class="text-sm text-blue-800 cursor-pointer select-none">Include Child Territories</label>
                </div>
            </div>
            
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Channel Partner</label>
                <div class="relative">
                    <Autocomplete
                        v-model="filters.channel_partner"
                        :options="partnerOptions"
                        placeholder="Select Partners"
                        :multiple="true"
                    />
                </div>
            </div>
            
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Order Status</label>
                <select v-model="filters.order_status" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white">
                    <option value="">All Statuses</option>
                    <option v-for="status in availableStatuses" :key="status" :value="status">{{ status }}</option>
                </select>
            </div>
        </div>
        <div class="p-4 border-t bg-gray-50 flex gap-3">
            <Button class="flex-1" variant="subtle" @click="clearFilters">Clear All</Button>
            <Button class="flex-1" appearance="primary" @click="applyFilters">Apply Filters</Button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { Button, Input, LoadingIndicator, createResource, createListResource, Autocomplete } from 'frappe-ui'

const tabs = ['Active', 'Unresolved', 'History']
const activeTab = ref('Active')
const currentView = ref('List')
const showFilters = ref(false)
const searchQuery = ref('')


const isTerritoryAdmin = computed(() => {
    return userInfo.data?.roles?.includes('Territory Admin')
})

const activeMenuOrderId = ref(null)
const menuPosition = reactive({ top: 0, left: 0 })

const menuActions = computed(() => {
    if (isTerritoryAdmin.value) {
        if (activeTab.value === 'Active') return ['Action 21', 'Action 22', 'Action 23']
        if (activeTab.value === 'Unresolved') return ['Action 24', 'Action 25']
        if (activeTab.value === 'History') return ['Action 26', 'Action 27', 'Action 28']
    }
    if (activeTab.value === 'Active') return ['Action 1', 'Action 2', 'Action 3']
    if (activeTab.value === 'Unresolved') return ['Action 4', 'Action 5']
    if (activeTab.value === 'History') return ['Action 6', 'Action 7', 'Action 8']
    return []
})

function toggleMenu(orderId, event) {
    if (activeMenuOrderId.value === orderId) {
        activeMenuOrderId.value = null
        return
    }
    const rect = event.currentTarget.getBoundingClientRect()
    menuPosition.top = rect.bottom + 5
    menuPosition.left = rect.right - 160
    activeMenuOrderId.value = orderId
}

function closeMenu() {
    activeMenuOrderId.value = null
}

const filters = reactive({
    custom_address_category: '',
    custom_resolved_territory: '',
    include_child_territories: false,
    channel_partner: [],
    order_status: ''
})

const allStatuses = ['Submitted', 'Assigned', 'Accepted', 'Rejected', 'Held', 'Cancelled', 'Fulfilled']
const partnerAdminStatuses = ['Assigned', 'Accepted', 'Rejected', 'Cancelled', 'Fulfilled']

const userInfo = createResource({
    url: 'connect_master.api.get_user_info',
    auto: true
})

const isPartnerAdmin = computed(() => {
    return userInfo.data?.roles?.includes('Partner Admin')
})

const availableStatuses = computed(() => {
    if (isPartnerAdmin.value) {
        return partnerAdminStatuses
    }
    return allStatuses
})

// Set partner filter when user info loads
watch(() => userInfo.data, (info) => {
    if (info && info.partners && info.partners.length > 0 && isPartnerAdmin.value) {
        // Pre-select all assigned partners? Or let user choose?
        // User said "show a multi-select dropdown".
        // If I pre-select all, it filters by all.
        // If I select none, it filters by none (which means all for System Manager, but for Partner Admin it should mean "all assigned").
        // But get_compass_orders handles permission logic separately.
        // So if filter is empty, Partner Admin still only sees assigned partners' orders.
        // So I don't need to pre-select.
        // But the user might want to filter by specific one.
        filters.channel_partner = []
    }
})

const orders = createResource({
    url: 'connect_master.api.get_compass_orders',
    auto: true,
    makeParams() {
        return {
            tab: activeTab.value,
            filters: JSON.stringify(filters),
            search: searchQuery.value
        }
    }
})

// Watchers to reload data
// watch(activeTab, () => {
//     orders.reload()
// })

function applyFilters() {
    orders.reload()
    showFilters.value = false
}

function clearFilters() {
    filters.custom_address_category = ''
    filters.custom_resolved_territory = ''
    filters.include_child_territories = false
    filters.channel_partner = []
    filters.order_status = ''
    applyFilters()
}

const hasActiveFilters = computed(() => {
    return filters.custom_address_category || 
           filters.custom_resolved_territory || 
           (filters.channel_partner && filters.channel_partner.length > 0) || 
           filters.order_status
})

// Helper Resources
const serviceChannels = createResource({
    url: 'connect_master.api.get_allowed_service_categories',
    auto: true
})

const territories = createResource({
    url: 'connect_master.api.get_allowed_territories',
    auto: true
})

const territoryOptions = computed(() => {
    if (!territories.data) return []
    return territories.data.map(t => ({
        label: t.territory_name,
        value: t.name
    }))
})

const partners = createResource({
    url: 'connect_master.api.get_allowed_partners',
    auto: true
})

const partnerOptions = computed(() => {
    if (!partners.data) return []
    return partners.data.map(p => ({
        label: p.partner_name,
        value: p.name
    }))
})

// Helpers
function getChannelName(name) {
    const c = serviceChannels.data?.find(x => x.name === name)
    return c ? c.channel_name : name
}

function getPartnerName(name) {
    const p = partners.data?.find(x => x.name === name)
    return p ? p.partner_name : name
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString() + ' ' + new Date(dateStr).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
}

function formatDateShort(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString()
}

function getOrderStatusClasses(status) {
    const map = {
        'Draft': 'bg-gray-100 text-gray-800',
        'Submitted': 'bg-blue-100 text-blue-800',
        'Assigned': 'bg-orange-100 text-orange-800',
        'Accepted': 'bg-purple-100 text-purple-800',
        'Completed': 'bg-green-100 text-green-800',
        'Fulfilled': 'bg-green-100 text-green-800',
        'Cancelled': 'bg-red-100 text-red-800',
        'Rejected': 'bg-red-100 text-red-800',
        'Held': 'bg-yellow-100 text-yellow-800'
    }
    return map[status] || 'bg-gray-100 text-gray-800'
}

// Kanban Helpers
const kanbanStatuses = computed(() => {
    if (activeTab.value === 'History') return ['Fulfilled', 'Cancelled', 'Rejected']
    return ['Submitted', 'Assigned', 'Accepted', 'Held']
})

function getOrdersByStatus(status) {
    if (!orders.data) return []
    return orders.data.filter(o => o.order_status === status)
}
</script>
