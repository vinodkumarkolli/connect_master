<template>
  <div class="max-w-7xl mx-auto py-8 px-4">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Left Pane: Form -->
      <div class="lg:col-span-2">
        
        <!-- Step 1: Items -->
        <div v-if="currentStep === 1">
          <h2 class="text-2xl font-bold mb-6">Select Items</h2>
          <div v-if="items.loading" class="flex justify-center py-12">
            <LoadingIndicator />
          </div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div v-for="item in items.data" :key="item.name" class="border rounded-lg p-4 flex gap-4 bg-white shadow-sm">
                <div class="w-24 h-24 bg-gray-100 rounded-md overflow-hidden flex-shrink-0">
                    <img v-if="item.item_image" :src="item.item_image" class="w-full h-full object-cover" />
                    <div v-else class="w-full h-full flex items-center justify-center text-gray-400 text-xs">No Image</div>
                </div>
                <div class="flex-1 flex flex-col justify-between">
                    <div>
                        <div class="font-bold truncate" :title="item.item_name">{{ item.item_name }}</div>
                        <div class="text-gray-600 text-sm">{{ formatCurrency(item.item_mrp) }}</div>
                    </div>
                    <div class="mt-2">
                        <Input
                            type="number"
                            label="Qty"
                            v-model.number="cart[item.name]"
                            min="0"
                            placeholder="0"
                            class="w-24"
                        />
                    </div>
                </div>
            </div>
          </div>
          <div class="mt-6 flex justify-end">
          <Button appearance="primary" size="lg" @click="currentStep = 2" :disabled="!hasItemsInCart">
              Next: Address
          </Button>
        </div>
      </div>

      <!-- Step 2: Address -->
      <div v-else-if="currentStep === 2">
          <h2 class="text-2xl font-bold mb-6">Select Address</h2>
          <div v-if="addresses.loading">Loading...</div>
          <div v-else class="space-y-4">
              
              <div v-if="isCustomer" class="flex flex-col md:flex-row gap-6">
                  <div class="md:w-1/3 flex flex-col gap-2">
                      <Button appearance="success" class="w-full md:w-auto" @click="showAddressDialog = true">
                          Change Delivery Address
                      </Button>
                      <Button appearance="danger" class="w-full md:w-auto" @click="navigateToManage">
                          Manage Addresses
                      </Button>
                  </div>

                  <div class="md:w-2/3">
                      <div v-if="selectedAddress" class="border p-4 rounded-lg bg-white shadow-sm">
                          <div class="flex justify-between items-start">
                              <div>
                                  <div class="font-bold text-gray-900">{{ getAddressTitle(selectedAddress) }}</div>
                                  <div class="text-gray-600 text-sm mt-2 leading-relaxed">
                                      {{ getAddressDetails(selectedAddress) }}
                                  </div>
                              </div>
                              <div v-if="isAddressDefault(selectedAddress)" class="px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full">
                                  Default
                              </div>
                          </div>
                      </div>
                      <div v-else class="text-gray-500 italic p-4 border border-dashed rounded-lg text-center">
                          No address selected. Please select a delivery address.
                      </div>
                  </div>
              </div>

              <div v-else class="space-y-4">
                  <Input v-model="addressSearch" placeholder="Search Address..." />
                  <div
                      v-for="addr in filteredAddresses"
                      :key="addr.name"
                      class="border p-4 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                      :class="{'border-blue-500 bg-blue-50': selectedAddress === addr.name}"
                      @click="selectedAddress = addr.name"
                  >
                      <div class="font-medium">{{ addr.address_title }}</div>
                      <div class="text-gray-600 text-sm mt-1">
                          {{ addr.address_line1 }}, {{ addr.city }}, {{ addr.pincode }}
                      </div>
                      <div class="text-gray-500 text-xs mt-1" v-if="addr.county">County: {{ addr.county }}</div>
                  </div>
              </div>
          </div>
          <div class="mt-6 flex justify-between">
                <Button variant="subtle" @click="currentStep = 1">Back</Button>
                <Button appearance="primary" size="lg" @click="handleAddressSelection" :disabled="!selectedAddress" :loading="resolvingTerritory">
                    Next: Contact
                </Button>
            </div>
        </div>

        <!-- Step 3: Contact -->
        <div v-else-if="currentStep === 3">
            <h2 class="text-2xl font-bold mb-6">Select Contact</h2>
            <div v-if="contacts.loading">Loading...</div>
            <div v-else class="space-y-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div
                        v-for="contact in filteredContacts"
                        :key="contact.name"
                        class="border p-4 rounded-lg cursor-pointer hover:border-blue-500 transition-colors flex justify-between items-start bg-white shadow-sm"
                        :class="{'border-blue-500 bg-blue-50': selectedContact === contact.name, 'opacity-75': contact.unsubscribed}"
                        @click="selectContact(contact, $event)"
                    >
                        <div>
                            <div class="flex items-center gap-2 mb-1">
                                <div class="font-medium">{{ contact.first_name }} {{ contact.last_name }}</div>
                                <span v-if="!contact.unsubscribed" class="px-2 py-0.5 text-xs bg-green-100 text-green-800 rounded-full">Active</span>
                                <span v-else class="px-2 py-0.5 text-xs bg-red-100 text-red-800 rounded-full">Disabled</span>
                            </div>
                            <div class="text-gray-600 text-sm">
                                {{ contact.mobile_no }}
                            </div>
                            <div class="text-gray-500 text-xs mt-1" v-if="contact.email_id">
                                {{ contact.email_id }}
                            </div>
                        </div>
                        <div class="dropdown-wrapper">
                            <CustomDropdown :options="getContactOptions(contact)">
                                <button class="text-gray-400 hover:text-gray-600 p-1 focus:outline-none">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                                </button>
                            </CustomDropdown>
                        </div>
                    </div>
                    
                    <!-- Add New Contact Card -->
                    <div
                        class="border border-dashed border-gray-300 p-4 rounded-lg cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-gray-500 min-h-[100px]"
                        @click="openAddContact"
                    >
                        <div class="bg-gray-100 p-2 rounded-full mb-2">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                        </div>
                        <span class="font-medium">Add New Contact</span>
                    </div>
                </div>
            </div>
            <div class="mt-6 flex justify-between">
                <Button variant="subtle" @click="currentStep = 2">Back</Button>
            </div>
        </div>

      </div>

      <!-- Right Pane: Summary -->
      <div class="lg:col-span-1">
        <div class="bg-gray-50 p-6 rounded-lg sticky top-4 border">
            <h2 class="text-xl font-bold mb-4 border-b pb-2">Order Summary</h2>
            
            <div class="space-y-4">
                <!-- Items -->
                <div>
                    <div class="text-sm font-semibold text-gray-500 uppercase">Items</div>
                    <div v-if="!hasItemsInCart" class="text-gray-400 italic text-sm">No items selected</div>
                    <div v-else class="space-y-2 mt-2">
                        <div v-for="(qty, itemName) in cart" :key="itemName" v-show="qty > 0" class="flex justify-between text-sm">
                            <span class="truncate flex-1 pr-2">{{ getItemName(itemName) }}</span>
                            <span class="font-medium">x {{ qty }}</span>
                        </div>
                    </div>
                </div>

                <!-- Channel -->
                <div v-if="selectedChannel">
                    <div class="text-sm font-semibold text-gray-500 uppercase mt-4">Channel</div>
                    <div class="text-sm">{{ getChannelName(selectedChannel) }}</div>
                </div>

                <!-- Address -->
                <div v-if="selectedAddress">
                    <div class="text-sm font-semibold text-gray-500 uppercase mt-4">Delivery Address</div>
                    <div class="text-sm font-medium">{{ getAddressTitle(selectedAddress) }}</div>
                    <div class="text-sm text-gray-600 mt-1">{{ getAddressDetails(selectedAddress) }}</div>
                </div>

                <!-- Contact -->
                <div v-if="selectedContact">
                    <div class="text-sm font-semibold text-gray-500 uppercase mt-4">Contact</div>
                    <div class="text-sm font-medium">{{ getContactName(selectedContact) }}</div>
                    <div class="text-sm text-gray-600 mt-1">{{ getContact(selectedContact)?.mobile_no }}</div>
                    <div class="text-sm text-gray-600" v-if="getContact(selectedContact)?.email_id">{{ getContact(selectedContact)?.email_id }}</div>
                </div>
            </div>

            <div class="mt-8 pt-4 border-t">
                <Button
                    v-if="canSubmit"
                    appearance="primary"
                    class="w-full"
                    size="lg"
                    @click="submitOrder"
                    :loading="createOrder.loading"
                >
                    Submit Order
                </Button>
                <div v-else-if="currentStep === 3 && !selectedContact" class="text-sm text-gray-500 text-center">
                    Select a contact to submit
                </div>
            </div>
        </div>
      </div>
    </div>


    <!-- Custom Modal for Success -->
    <div v-if="showSuccessDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-sm mx-4 overflow-hidden">
            <div class="p-6 text-center">
                <div class="text-green-500 text-5xl mb-4">✓</div>
                <h3 class="text-xl font-bold">Order Placed Successfully!</h3>
                <p class="text-gray-600 mt-2">Thank you for your order.</p>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-center">
                <Button appearance="primary" @click="$router.push('/')">Navigate to Home</Button>
            </div>
        </div>
    </div>

    <!-- Custom Modal for Error -->
    <div v-if="showErrorDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-sm mx-4 overflow-hidden">
            <div class="p-6">
                <Alert type="warning" title="Error">
                    {{ errorMessage }}
                </Alert>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end">
                <Button @click="showErrorDialog = false">Close</Button>
            </div>
        </div>
    </div>

    <!-- Address Selection Modal -->
    <div v-if="showAddressDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-4xl mx-4 overflow-hidden max-h-[80vh] flex flex-col">
            <div class="px-6 py-4 border-b flex justify-between items-center">
                <h3 class="text-lg font-bold">Select Delivery Address</h3>
                <button @click="showAddressDialog = false" class="text-gray-500 hover:text-gray-700">&times;</button>
            </div>
            <div class="p-6 overflow-y-auto">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div
                        v-for="addr in addresses.data"
                        :key="addr.name"
                        class="border p-4 rounded-lg cursor-pointer hover:border-blue-500 transition-colors relative bg-white"
                        :class="{'ring-2 ring-blue-500': selectedAddress === addr.name, 'bg-blue-50 border-blue-200': addr.custom_is_default}"
                        @click="selectAddressFromModal(addr.name)"
                    >
                        <div class="font-medium">{{ addr.address_title }}</div>
                        <div class="text-gray-600 text-sm mt-1">
                            {{ addr.address_line1 }}, {{ addr.city }}, {{ addr.pincode }}
                        </div>
                        <div v-if="addr.custom_is_default" class="absolute top-2 right-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full">Default</div>
                    </div>
                    <div v-if="!addresses.data || addresses.data.length === 0" class="col-span-full text-gray-500 italic p-4 text-center">
                        No active addresses found.
                    </div>
                </div>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end gap-2">
                <Button variant="subtle" @click="showAddressDialog = false">Cancel</Button>
            </div>
        </div>
    </div>


    <Communication
        v-model:show="showCommunication"
        :mode="communicationMode"
        :addressDoc="communicationAddress"
        :contactDoc="communicationContact"
        :user="session.data"
        :isDefaultAddress="isDefaultAddress"
        :blocking="isBlocking"
        @success="onCommunicationSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { Button, Input, createResource, createListResource, LoadingIndicator, frappeRequest, Alert } from 'frappe-ui'
import { useRouter } from 'vue-router'
import CustomDropdown from '../components/CustomDropdown.vue'
import Communication from '../components/Communication.vue'
import { useConsumerValidation } from '../composables/useConsumerValidation'

const router = useRouter()
const {
    checkAndPrompt,
    showCommunication,
    communicationMode,
    communicationAddress,
    communicationContact,
    isBlocking,
    isDefaultAddress,
    userRoles
} = useConsumerValidation()
const currentStep = ref(1)
const cart = reactive({})
const selectedAddress = ref(null)
const selectedContact = ref(null)
const selectedChannel = ref(null)
const resolvedTerritory = ref(null)
const resolvingTerritory = ref(false)
const addressSearch = ref('')

const showAddressDialog = ref(false)
const showSuccessDialog = ref(false)
const showErrorDialog = ref(false)
const errorMessage = ref('')

function showError(msg) {
    errorMessage.value = msg
    showErrorDialog.value = true
}

// Resources
const session = createResource({
    url: 'frappe.auth.get_logged_user',
    auto: true,
    onError() {
        // If not logged in, redirect
        window.location.href = '/login?redirect-to=/koda/order'
    }
})

const items = createListResource({
    doctype: 'Connect Item',
    fields: ['name', 'item_name', 'item_code', 'item_image', 'item_mrp'],
    filters: { disabled: 0 },
    auto: true,
    pageLength: 100
})

const channels = createListResource({
    doctype: 'Service Channel',
    fields: ['name', 'channel_name', 'channel_description'],
    filters: { disabled: 0 },
    auto: true,
    pageLength: 100
})

const addresses = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Address',
            fields: ['name', 'address_title', 'address_line1', 'city', 'pincode', 'county', 'custom_address_category', 'custom_is_default'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User'], ['disabled', '=', 0]]
        }
    }
})

const contacts = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Contact',
            fields: ['name', 'first_name', 'last_name', 'mobile_no', 'address', 'unsubscribed'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    }
})

const filteredContacts = computed(() => {
    if (!contacts.data) return []
    let list = contacts.data
    if (selectedAddress.value) {
        list = list.filter(c => c.address === selectedAddress.value)
    }
    return list
})

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

        return {
            doc: {
                doctype: 'Connect Order',
                order_date: (() => {
                    const now = new Date();
                    const pad = (n) => (n < 10 ? '0' + n : n);
                    return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
                })(),
                user: session.data,
                delivery_address: selectedAddress.value,
                contact: selectedContact.value,
                resolved_territory: resolvedTerritory.value,
                service_category: selectedChannel.value,
                order_status: 'Submitted',
                docstatus: 1,
                items: lineItems
            }
        }
    },
    onSuccess(data) {
        showSuccessDialog.value = true
    },
    onError(err) {
        showError('Order creation failed: ' + (err.messages ? err.messages.join(', ') : err.message))
    }
})

// Computed
const totalItems = computed(() => {
    return Object.values(cart).reduce((sum, qty) => sum + (qty || 0), 0)
})

const hasItemsInCart = computed(() => {
    return totalItems.value > 0
})

const canSubmit = computed(() => {
    return hasItemsInCart.value && selectedChannel.value && selectedAddress.value && selectedContact.value && resolvedTerritory.value
})

const filteredAddresses = computed(() => {
    if (!addresses.data) return []
    if (!addressSearch.value) return addresses.data
    const q = addressSearch.value.toLowerCase()
    return addresses.data.filter(a =>
        (a.address_title && a.address_title.toLowerCase().includes(q)) ||
        (a.address_line1 && a.address_line1.toLowerCase().includes(q)) ||
        (a.city && a.city.toLowerCase().includes(q)) ||
        (a.pincode && a.pincode.toLowerCase().includes(q))
    )
})

const isCustomer = computed(() => {
    if (!userRoles.data) return false
    const roles = Array.isArray(userRoles.data) ? userRoles.data : (userRoles.data.message || [])
    return roles.includes('Customer') || roles.includes('Consumer')
})

// Methods
function selectAddressFromModal(name) {
    selectedAddress.value = name
    showAddressDialog.value = false
}

function navigateToManage() {
    if (confirm("it will be navigating outside and all changes will be lost")) {
        router.push({ name: 'Manage' })
    }
}

function selectContact(contact, event) {
    if (contact.unsubscribed) return
    if (event && event.target && event.target.closest('.dropdown-wrapper')) return
    selectedContact.value = contact.name
}

function isAddressDefault(name) {
    const addr = addresses.data?.find(a => a.name === name)
    return addr ? !!addr.custom_is_default : false
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)
}

function getItemName(name) {
    const item = items.data?.find(i => i.name === name)
    return item ? item.item_name : name
}

function getChannelName(name) {
    const channel = channels.data?.find(c => c.name === name)
    return channel ? channel.channel_name : name
}

function getAddressTitle(name) {
    const addr = addresses.data?.find(a => a.name === name)
    return addr ? addr.address_title : name
}

function getAddressDetails(name) {
    const addr = addresses.data?.find(a => a.name === name)
    if (!addr) return ''
    return `${addr.address_line1}, ${addr.city}, ${addr.pincode}`
}


function getContact(name) {
    return contacts.data?.find(c => c.name === name)
}

function getContactName(name) {
    const contact = contacts.data?.find(c => c.name === name)
    return contact ? `${contact.first_name} ${contact.last_name}` : name
}

function getContactOptions(contact) {
    const options = []
    
    if (!contact.unsubscribed) {
        options.push({
            label: 'Edit Contact',
            onClick: () => openEditContact(contact)
        })
    }

    options.push({
        label: contact.unsubscribed ? 'Enable Contact' : 'Disable Contact',
        onClick: () => toggleContactSubscription(contact)
    })
    
    return options
}

function openAddContact() {
    const addrDoc = addresses.data.find(a => a.name === selectedAddress.value)
    communicationMode.value = 'Contact'
    communicationAddress.value = addrDoc
    communicationContact.value = null
    isBlocking.value = false
    showCommunication.value = true
}

function openEditContact(contact) {
    communicationMode.value = 'Editable Contact'
    communicationAddress.value = null
    communicationContact.value = contact
    isBlocking.value = false
    showCommunication.value = true
}

async function toggleContactSubscription(contact) {
    const action = contact.unsubscribed ? 'enable' : 'disable'
    if (confirm(`Are you sure you want to ${action} this contact?`)) {
        await frappeRequest({
            url: 'frappe.client.set_value',
            params: {
                doctype: 'Contact',
                name: contact.name,
                fieldname: 'unsubscribed',
                value: contact.unsubscribed ? 0 : 1
            }
        })
        contacts.fetch()
    }
}

async function handleAddressSelection() {
    if (!selectedAddress.value) return
    
    resolvingTerritory.value = true
    try {
        const address = addresses.data.find(a => a.name === selectedAddress.value)
        if (address) {
            selectedChannel.value = address.custom_address_category
            resolvedTerritory.value = await resolveTerritory(address)
        }

        if (!resolvedTerritory.value) {
            showError('Service is not available in this area. Please select a different address.')
            return
        }

        currentStep.value = 3
    } catch (e) {
        console.error(e)
        showError('Error resolving territory')
    } finally {
        resolvingTerritory.value = false
    }
}

async function resolveTerritory(address) {
    // 1. Pincode
    if (address.pincode) {
        const pincode = address.pincode.toString().trim()
        // Try exact match on name first
        try {
             let res = await frappeRequest({
                url: 'frappe.client.get_value',
                params: {
                    doctype: 'Service Territory',
                    fieldname: 'name',
                    filters: { name: pincode }
                }
            })
            const val = res.message || res
            if (val && val.name) return val.name
        } catch (e) {
            // ignore
        }

        // Fallback to territory_name search
        let res = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Service Territory',
                filters: [['territory_name', '=', pincode]],
                limit_page_length: 1
            }
        })
        const list = res.message || res
        if (Array.isArray(list) && list.length > 0) return list[0].name
    }

    // 2. City
    if (address.city) {
        const city = address.city.toString().trim()
        let res = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Service Territory',
                filters: [['territory_name', '=', city], ['allow_in_search', '=', 1]],
                limit_page_length: 1
            }
        })
        const list = res.message || res
        if (Array.isArray(list) && list.length > 0) return list[0].name
    }

    // 3. Parent most (Root)
    let res = await frappeRequest({
        url: 'frappe.client.get_list',
        params: {
            doctype: 'Service Territory',
            filters: [['parent_service_territory', '=', '']],
            limit_page_length: 1
        }
    })
    const list = res.message || res
    if (Array.isArray(list) && list.length > 0) return list[0].name
    
    return null
}

function submitOrder() {
    createOrder.submit()
}

function resetOrder() {
    showSuccessDialog.value = false
    currentStep.value = 1
    Object.keys(cart).forEach(key => delete cart[key])
    selectedAddress.value = null
    selectedContact.value = null
    selectedChannel.value = null
    resolvedTerritory.value = null
}

// Watchers
watch(currentStep, (newStep) => {
    if (newStep === 2) {
        addresses.fetch()
    }
    if (newStep === 3) {
        contacts.fetch()
    }
})

watch(() => addresses.data, (val) => {
    if (val && !selectedAddress.value) {
        const defaultAddr = val.find(a => a.custom_is_default)
        if (defaultAddr) selectedAddress.value = defaultAddr.name
    }
}, { immediate: true })

onMounted(async () => {
    await checkAndPrompt()
})

async function onCommunicationSuccess(data) {
    if (currentStep.value === 2) addresses.fetch()
    if (currentStep.value === 3) {
        await contacts.fetch()
        if (data && data.contact) {
            selectedContact.value = data.contact
        }
    }
    await checkAndPrompt()
}
</script>

