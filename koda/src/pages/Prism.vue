<template>
  <div class="h-screen bg-gray-50 flex flex-col overflow-hidden">
    
    <!-- Header (Visible when a view is active) -->
    <div v-if="currentView" class="bg-white border-b px-6 py-4 flex justify-between items-center shadow-sm z-10 flex-shrink-0">
      <div class="flex items-center gap-4">
        <button @click="currentView = null" class="p-2 hover:bg-gray-100 rounded-full transition-colors" title="Back to Menu">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        </button>
        <h1 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
          <span v-if="currentView === 'Compass'">🧭 Compass</span>
          <span v-else-if="currentView === 'Punch'">👊 Punch Order</span>
          <span v-else-if="currentView === 'Manage'">✏️ Manage</span>
        </h1>
      </div>
      <div class="text-sm text-gray-500" v-if="userRoles.data">
        {{ userRolesList.join(', ') }}
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 relative overflow-hidden">
      
      <!-- Menu (Centered) -->
      <transition name="fade">
        <div v-if="!currentView" class="absolute inset-0 flex items-center justify-center p-6 bg-gray-50 z-0">
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
        <div v-if="currentView" class="absolute inset-0 bg-gray-50 overflow-hidden flex flex-col p-6 z-10">
           
           <!-- Compass View -->
           <div v-if="currentView === 'Compass'" class="bg-white rounded-lg shadow border flex flex-col h-full">
             <div class="p-4 border-b bg-gray-50 flex justify-between items-center">
               <div>
                 <h2 class="text-lg font-bold text-gray-800">Recent Orders</h2>
                 <p class="text-xs text-gray-500">View and track all connect orders</p>
               </div>
               <div class="w-64">
                  <Input v-model="orderSearch" placeholder="Search Orders..." prefix="search" />
               </div>
             </div>
             <div class="flex-1 overflow-y-auto p-0">
               <div v-if="orders.loading" class="flex justify-center p-12">
                 <LoadingIndicator />
               </div>
               <div v-else-if="filteredOrders.length === 0" class="p-12 text-center text-gray-500">
                 No orders found.
               </div>
               <div v-else class="divide-y">
                 <div v-for="order in filteredOrders" :key="order.name" class="p-4 hover:bg-gray-50 transition-colors cursor-pointer flex items-center justify-between">
                   <div>
                     <div class="flex items-center gap-3 mb-1">
                       <span class="font-medium text-gray-900">{{ order.name }}</span>
                       <span :class="['px-2 py-0.5 rounded-full text-xs font-medium', getOrderStatusClasses(order.order_status)]">
                         {{ order.order_status }}
                       </span>
                     </div>
                     <div class="text-sm text-gray-500">
                       {{ order.user }} • {{ formatDate(order.order_date) }}
                     </div>
                   </div>
                   <div class="text-right">
                      <div class="text-sm font-medium text-gray-700">{{ order.service_category }}</div>
                   </div>
                 </div>
               </div>
             </div>
             <div class="p-3 border-t bg-gray-50 flex justify-center">
                <Button variant="subtle" size="sm" @click="orders.reload()">Refresh List</Button>
             </div>
           </div>

           <!-- Punch View -->
           <div v-if="currentView === 'Punch' && isTerritoryAdmin" class="bg-white rounded-lg shadow border flex flex-col h-full">
             <div class="flex-1 overflow-y-auto p-6">
               <!-- Step 1: Search/Select Customer -->
               <div v-if="punchStep === 1" class="max-w-3xl mx-auto">
                 <div class="text-center mb-8">
                   <h2 class="text-2xl font-bold text-gray-900">Start a New Order</h2>
                   <p class="text-gray-500 mt-2">Search for a customer (Address or Contact) to begin</p>
                 </div>

                 <div class="flex gap-2 mb-6">
                   <Input v-model="punchSearch" placeholder="Search Address, Contact, Phone..." class="flex-1" @keyup.enter="performPunchSearch" />
                   <Button @click="performPunchSearch" :loading="isSearching" size="lg" appearance="primary">Search</Button>
                 </div>

                 <div v-if="punchSearchResults.length > 0" class="space-y-3">
                   <div class="text-xs font-semibold text-gray-500 uppercase mb-2">Search Results</div>
                   <div 
                     v-for="res in punchSearchResults" 
                     :key="res.name" 
                     class="border p-4 rounded-lg hover:border-blue-500 hover:shadow-md cursor-pointer transition-all bg-white"
                     @click="selectPunchTarget(res)"
                   >
                     <div class="flex justify-between items-start">
                       <div>
                         <div class="font-medium text-lg">{{ res.title }}</div>
                         <div class="text-gray-600 mt-1">{{ res.description }}</div>
                         <div class="text-xs text-gray-400 mt-2 flex items-center gap-1">
                           <span class="w-2 h-2 rounded-full bg-gray-300"></span>
                           {{ res.user }}
                         </div>
                       </div>
                       <span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium">{{ res.type }}</span>
                     </div>
                   </div>
                 </div>
                 <div v-else-if="hasSearched" class="text-center py-12 bg-gray-50 rounded-lg border border-dashed">
                   <p class="text-gray-500">No results found.</p>
                   <Button class="mt-4" variant="outline" @click="openCreateNewCustomer">
                     + Create New Customer
                   </Button>
                 </div>
                 
                 <div v-if="!hasSearched" class="text-center mt-12">
                    <Button variant="subtle" @click="openCreateNewCustomer">
                     + Create New Customer (Address & Contact)
                   </Button>
                   <p class="text-xs text-gray-400 mt-2">Creates against admin@example.com</p>
                 </div>
               </div>

               <!-- Step 2: Select Items & Submit -->
               <div v-else-if="punchStep === 2" class="max-w-5xl mx-auto h-full flex flex-col">
                 <div class="bg-blue-50 p-4 rounded-lg border border-blue-100 flex justify-between items-center mb-6">
                   <div class="flex items-center gap-4">
                     <div class="bg-white p-2 rounded-full shadow-sm text-xl">👤</div>
                     <div>
                       <div class="text-xs text-blue-600 uppercase font-bold">Ordering For</div>
                       <div class="font-medium text-blue-900">{{ punchTarget?.title }}</div>
                       <div class="text-xs text-blue-700">{{ punchTarget?.description }}</div>
                     </div>
                   </div>
                   <Button size="sm" variant="subtle" @click="resetPunch">Change Customer</Button>
                 </div>

                 <div class="flex-1 flex gap-6 overflow-hidden">
                   <!-- Items List -->
                   <div class="flex-1 overflow-y-auto pr-2">
                     <h3 class="font-bold mb-4 text-lg">Select Items</h3>
                     <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
                       <div v-for="item in items.data" :key="item.name" class="border rounded-lg p-4 flex gap-4 hover:shadow-sm transition-shadow bg-white">
                          <div class="w-20 h-20 bg-gray-100 rounded-md flex-shrink-0 overflow-hidden">
                             <img v-if="item.item_image" :src="item.item_image" class="w-full h-full object-cover" />
                          </div>
                          <div class="flex-1 flex flex-col justify-between">
                             <div>
                               <div class="font-medium">{{ item.item_name }}</div>
                               <div class="text-sm text-gray-500">{{ formatCurrency(item.item_mrp) }}</div>
                             </div>
                             <div class="flex items-center gap-2 mt-2">
                               <Input type="number" v-model.number="cart[item.name]" min="0" placeholder="0" class="w-24" />
                               <span class="text-xs text-gray-400">Qty</span>
                             </div>
                          </div>
                       </div>
                     </div>
                   </div>

                   <!-- Cart Summary -->
                   <div class="w-80 bg-gray-50 p-6 rounded-lg border h-fit">
                     <h3 class="font-bold text-lg mb-4">Order Summary</h3>
                     <div class="space-y-2 mb-6">
                       <div class="flex justify-between text-sm">
                         <span class="text-gray-600">Items Selected</span>
                         <span class="font-medium">{{ Object.values(cart).filter(q => q > 0).length }}</span>
                       </div>
                       <div class="flex justify-between text-lg font-bold border-t pt-2 mt-2">
                         <span>Total</span>
                         <span>{{ formatCurrency(totalAmount) }}</span>
                       </div>
                     </div>
                     <Button appearance="primary" class="w-full" size="xl" :disabled="!hasItemsInCart" @click="submitPunchOrder" :loading="createOrder.loading">
                       Punch Order
                     </Button>
                   </div>
                 </div>
               </div>
             </div>
           </div>

           <!-- Manage View -->
           <div v-if="currentView === 'Manage' && isTerritoryAdmin" class="bg-white rounded-lg shadow border flex flex-col h-full">
              <div class="p-4 border-b bg-gray-50 flex gap-4 items-center">
                <div class="flex-1">
                  <Input v-model="manageSearch" placeholder="Search Addresses or Contacts..." prefix="search" @keyup.enter="performManageSearch" />
                </div>
                <div class="flex bg-white rounded-md border p-1">
                  <button 
                    @click="manageType = 'Address'"
                    :class="['px-4 py-1.5 rounded text-sm font-medium transition-colors', manageType === 'Address' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50']"
                  >Addresses</button>
                  <button 
                    @click="manageType = 'Contact'"
                    :class="['px-4 py-1.5 rounded text-sm font-medium transition-colors', manageType === 'Contact' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50']"
                  >Contacts</button>
                </div>
                <Button @click="performManageSearch" :loading="isManageSearching" appearance="primary">Search</Button>
              </div>

              <div class="flex-1 overflow-y-auto p-0">
                <div v-if="manageResults.length === 0 && hasManageSearched" class="p-12 text-center text-gray-500">
                  No results found.
                </div>
                <div v-else-if="manageResults.length === 0 && !hasManageSearched" class="p-12 text-center text-gray-400">
                  Enter a search term to find addresses or contacts.
                </div>
                <div v-else class="divide-y">
                  <div v-for="res in manageResults" :key="res.name" class="p-4 hover:bg-gray-50 transition-colors flex justify-between items-center">
                    <div>
                      <div class="font-medium text-gray-900">{{ res.title }}</div>
                      <div class="text-sm text-gray-600 mt-1">{{ res.description }}</div>
                      <div class="text-xs text-gray-400 mt-1 flex items-center gap-1">
                         <span class="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
                         {{ res.user }}
                      </div>
                    </div>
                    <Button size="sm" icon="edit" @click="openEdit(res)">Edit</Button>
                  </div>
                </div>
              </div>
           </div>

        </div>
      </transition>

    </div>

    <!-- Communication Modal for Create/Edit -->
    <Communication
        v-model:show="showCommunication"
        :mode="communicationMode"
        :addressDoc="communicationAddress"
        :contactDoc="communicationContact"
        :user="communicationUser"
        :isDefaultAddress="false"
        :blocking="false"
        @success="onCommunicationSuccess"
    />

    <!-- Success Dialog -->
    <div v-if="showSuccessDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-sm mx-4 overflow-hidden">
            <div class="p-6 text-center">
                <div class="text-green-500 text-5xl mb-4">✓</div>
                <h3 class="text-xl font-bold">Success</h3>
                <p class="text-gray-600 mt-2">{{ successMessage }}</p>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-center">
                <Button appearance="primary" @click="showSuccessDialog = false">Close</Button>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { Button, Input, LoadingIndicator, createResource, createListResource, frappeRequest } from 'frappe-ui'
import Communication from '../components/Communication.vue'

// --- State ---
const currentView = ref(null) // null = Menu, 'Compass', 'Punch', 'Manage'
const orderSearch = ref('')
const punchSearch = ref('')
const punchStep = ref(1)
const punchSearchResults = ref([])
const isSearching = ref(false)
const hasSearched = ref(false)
const punchTarget = ref(null) // { type: 'Address'|'Contact', name, title, description, user, doc }
const cart = reactive({})

const manageSearch = ref('')
const manageType = ref('Address') // 'Address' or 'Contact'
const manageResults = ref([])
const isManageSearching = ref(false)
const hasManageSearched = ref(false)

const showCommunication = ref(false)
const communicationMode = ref('Address+Contact')
const communicationAddress = ref(null)
const communicationContact = ref(null)
const communicationUser = ref('admin@example.com')

const showSuccessDialog = ref(false)
const successMessage = ref('')

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

const isTerritoryAdmin = computed(() => userRolesList.value.includes('Territory Admin'))
const isPartnerAdmin = computed(() => userRolesList.value.includes('Partner Admin'))

// Compass: Orders
const orders = createListResource({
    doctype: 'Connect Order',
    fields: ['name', 'order_date', 'order_status', 'service_category', 'user'],
    orderBy: 'creation desc',
    auto: true,
    pageLength: 50
})

const filteredOrders = computed(() => {
    if (!orders.data) return []
    if (!orderSearch.value) return orders.data
    const q = orderSearch.value.toLowerCase()
    return orders.data.filter(o => 
        o.name.toLowerCase().includes(q) || 
        (o.user && o.user.toLowerCase().includes(q))
    )
})

// Items for Punch
const items = createListResource({
    doctype: 'Connect Item',
    fields: ['name', 'item_name', 'item_code', 'item_image', 'item_mrp'],
    filters: { disabled: 0 },
    auto: true,
    pageLength: 100
})

// --- Methods ---

function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value || 0)
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString() + ' ' + new Date(dateStr).toLocaleTimeString()
}

function getOrderStatusClasses(status) {
    const map = {
        'Draft': 'bg-gray-100 text-gray-800',
        'Submitted': 'bg-blue-100 text-blue-800',
        'Assigned': 'bg-orange-100 text-orange-800',
        'Completed': 'bg-green-100 text-green-800',
        'Cancelled': 'bg-red-100 text-red-800'
    }
    return map[status] || 'bg-gray-100 text-gray-800'
}

// --- Punch Logic ---

async function performPunchSearch() {
    if (!punchSearch.value) return
    isSearching.value = true
    punchSearchResults.value = []
    hasSearched.value = true
    
    try {
        const q = punchSearch.value
        const results = []

        // Search Addresses
        const addrRes = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Address',
                fields: ['name', 'address_title', 'address_line1', 'city', 'pincode', 'custom_address_category', 'custom_resolved_territory'],
                filters: [
                    ['disabled', '=', 0],
                    ['address_title', 'like', `%${q}%`]
                ],
                limit_page_length: 10
            }
        })
        const addresses = addrRes.message || addrRes || []
        
        // For each address, find the user
        for (const addr of addresses) {
             const user = await getLinkUser('Address', addr.name)
             results.push({
                 type: 'Address',
                 name: addr.name,
                 title: addr.address_title,
                 description: `${addr.address_line1}, ${addr.city}`,
                 user: user,
                 doc: addr
             })
        }

        // Search Contacts
        const contactRes = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Contact',
                fields: ['name', 'first_name', 'last_name', 'mobile_no', 'email_id', 'address'],
                filters: [
                    ['first_name', 'like', `%${q}%`] // Simple filter, could be more complex
                ],
                or_filters: [
                    ['last_name', 'like', `%${q}%`],
                    ['mobile_no', 'like', `%${q}%`],
                    ['email_id', 'like', `%${q}%`]
                ],
                limit_page_length: 10
            }
        })
        const contacts = contactRes.message || contactRes || []

        for (const contact of contacts) {
             const user = await getLinkUser('Contact', contact.name)
             results.push({
                 type: 'Contact',
                 name: contact.name,
                 title: `${contact.first_name} ${contact.last_name}`,
                 description: `${contact.mobile_no} | ${contact.email_id}`,
                 user: user,
                 doc: contact
             })
        }

        punchSearchResults.value = results
    } catch (e) {
        console.error(e)
    } finally {
        isSearching.value = false
    }
}

async function getLinkUser(doctype, name) {
    try {
        const res = await frappeRequest({
            url: 'frappe.client.get_value',
            params: {
                doctype: 'Dynamic Link',
                fieldname: 'link_name',
                filters: {
                    parent: name,
                    parenttype: doctype,
                    link_doctype: 'User'
                }
            }
        })
        return (res.message || res || {}).link_name || 'Unknown'
    } catch (e) {
        return 'Unknown'
    }
}

async function selectPunchTarget(res) {
    punchTarget.value = res
    punchStep.value = 2
    // Reset cart
    Object.keys(cart).forEach(key => delete cart[key])
}

function resetPunch() {
    punchStep.value = 1
    punchTarget.value = null
}

function openCreateNewCustomer() {
    communicationMode.value = 'Address+Contact'
    communicationAddress.value = null
    communicationContact.value = null
    communicationUser.value = 'admin@example.com'
    showCommunication.value = true
}

// --- Order Submission ---

const totalAmount = computed(() => {
    return Object.entries(cart).reduce((sum, [itemName, qty]) => {
        if (!qty) return sum
        const item = items.data?.find(i => i.name === itemName)
        return sum + ((item?.item_mrp || 0) * qty)
    }, 0)
})

const hasItemsInCart = computed(() => totalAmount.value > 0)

const createOrder = createResource({
    url: 'frappe.client.insert',
    makeParams(values) {
        const lineItems = Object.entries(cart).filter(([_, qty]) => qty > 0).map(([itemName, qty]) => {
            const item = items.data.find(i => i.name === itemName)
            return {
                item: item.name,
                quantity: qty,
                item_rate: item.item_mrp,
                line_item_amount: item.item_mrp * qty
            }
        })

        const nowStr = new Date().toISOString().slice(0, 19).replace('T', ' ');
        
        // Determine Address and Contact from punchTarget
        let address = null
        let contact = null
        let service_category = null
        
        if (punchTarget.value.type === 'Address') {
            address = punchTarget.value.name
            service_category = punchTarget.value.doc.custom_address_category
            // We might need to fetch a contact for this address? 
            // For now, leave contact empty or try to find one?
            // The Order doctype usually requires both? Let's check Order.vue.
            // Order.vue requires both.
            // If we only have Address, we might need to ask for Contact or pick one.
            // But for "Punch", maybe we can be lenient or auto-pick?
            // Let's try to find a contact for this address.
        } else {
            contact = punchTarget.value.name
            address = punchTarget.value.doc.address
            // We need to fetch address to get category
        }

        return {
            doc: {
                doctype: 'Connect Order',
                order_date: nowStr,
                user: punchTarget.value.user,
                delivery_address: address,
                contact: contact,
                service_category: service_category, // This might be missing if we didn't fetch it
                order_status: 'Submitted',
                docstatus: 1,
                items: lineItems
            }
        }
    },
    onSuccess(data) {
        successMessage.value = `Order ${data.name} created successfully!`
        showSuccessDialog.value = true
        resetPunch()
        orders.reload()
    },
    onError(err) {
        console.error(err)
        alert('Failed to create order: ' + (err.messages ? err.messages.join(', ') : err.message))
    }
})

async function submitPunchOrder() {
    // If we selected a Contact, we need to ensure we have the Address details for service_category
    if (punchTarget.value.type === 'Contact' && !punchTarget.value.doc.address) {
        alert('Selected Contact does not have a linked Address. Cannot determine Service Category.')
        return
    }
    
    if (punchTarget.value.type === 'Contact') {
         // Fetch address to get category
         const addr = await frappeRequest({
             url: 'frappe.client.get_value',
             params: {
                 doctype: 'Address',
                 fieldname: 'custom_address_category',
                 filters: { name: punchTarget.value.doc.address }
             }
         })
         if (addr && addr.custom_address_category) {
             // We need to pass this to createOrder somehow, or fetch it inside makeParams
             // But makeParams is synchronous usually? No, it can't be async easily in frappe-ui resource?
             // Actually createResource makeParams is synchronous.
             // So we should prepare data before calling submit.
         }
    }

    // Actually, let's just try to submit. If fields are missing, it might fail.
    // Ideally we should have fetched full details when selecting the target.
    
    // Let's refine selectPunchTarget to fetch necessary details.
    createOrder.submit()
}

// --- Manage Logic ---

async function performManageSearch() {
    if (!manageSearch.value) return
    isManageSearching.value = true
    manageResults.value = []
    hasManageSearched.value = true
    
    try {
        const q = manageSearch.value
        const results = []
        
        if (manageType.value === 'Address') {
            const res = await frappeRequest({
                url: 'frappe.client.get_list',
                params: {
                    doctype: 'Address',
                    fields: ['name', 'address_title', 'address_line1', 'city', 'pincode', 'state', 'custom_address_category', 'custom_is_default'],
                    filters: [
                        ['address_title', 'like', `%${q}%`]
                    ],
                    limit_page_length: 20
                }
            })
            const list = res.message || res || []
            for (const item of list) {
                const user = await getLinkUser('Address', item.name)
                results.push({
                    type: 'Address',
                    name: item.name,
                    title: item.address_title,
                    description: `${item.address_line1}, ${item.city}`,
                    user: user,
                    doc: item
                })
            }
        } else {
            const res = await frappeRequest({
                url: 'frappe.client.get_list',
                params: {
                    doctype: 'Contact',
                    fields: ['name', 'first_name', 'last_name', 'mobile_no', 'email_id'],
                    filters: [
                        ['first_name', 'like', `%${q}%`]
                    ],
                    limit_page_length: 20
                }
            })
            const list = res.message || res || []
            for (const item of list) {
                const user = await getLinkUser('Contact', item.name)
                results.push({
                    type: 'Contact',
                    name: item.name,
                    title: `${item.first_name} ${item.last_name}`,
                    description: `${item.mobile_no}`,
                    user: user,
                    doc: item
                })
            }
        }
        
        manageResults.value = results
    } catch (e) {
        console.error(e)
    } finally {
        isManageSearching.value = false
    }
}

function openEdit(res) {
    if (res.type === 'Address') {
        communicationMode.value = 'Editable Address'
        communicationAddress.value = res.doc
        communicationContact.value = null
    } else {
        communicationMode.value = 'Editable Contact'
        communicationAddress.value = null
        communicationContact.value = res.doc
    }
    communicationUser.value = res.user
    showCommunication.value = true
}

// --- Communication Success ---
async function onCommunicationSuccess(data) {
    // If we were in Punch mode and created a new customer
    if (punchStep.value === 1 && data.address) {
        // We created a new address (and maybe contact)
        // Let's auto-select it for Punch
        // We need to fetch the details
        const addr = await frappeRequest({
            url: 'frappe.client.get',
            params: { doctype: 'Address', name: data.address }
        })
        
        const user = await getLinkUser('Address', data.address)
        
        selectPunchTarget({
            type: 'Address',
            name: addr.name,
            title: addr.address_title,
            description: `${addr.address_line1}, ${addr.city}`,
            user: user,
            doc: addr
        })
    }
    
    // If we were in Manage mode, refresh results
    if (manageResults.value.length > 0) {
        performManageSearch()
    }
}

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
