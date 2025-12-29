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
                    <Input
                        type="number"
                        label="Qty"
                        v-model.number="cart[item.name]"
                        min="0"
                        placeholder="0"
                    />
                </div>
            </div>
          </div>
          <div class="mt-6 flex justify-end">
            <Button variant="solid" size="lg" @click="currentStep = 2" :disabled="!hasItemsInCart">
                Next: Service Channel
            </Button>
          </div>
        </div>

        <!-- Step 2: Service Channel -->
        <div v-else-if="currentStep === 2">
            <h2 class="text-2xl font-bold mb-6">What best describes you?</h2>
            <div v-if="channels.loading">Loading...</div>
            <div v-else class="space-y-4">
                <div 
                    v-for="channel in channels.data" 
                    :key="channel.name" 
                    class="border p-4 rounded-lg cursor-pointer flex items-start gap-3 hover:border-blue-500 transition-colors"
                    :class="{'border-blue-500 bg-blue-50': selectedChannel === channel.name}"
                    @click="selectedChannel = channel.name"
                >
                    <div class="mt-1 w-5 h-5 rounded-full border border-gray-400 flex items-center justify-center flex-shrink-0" :class="{'border-blue-600': selectedChannel === channel.name}">
                        <div v-if="selectedChannel === channel.name" class="w-3 h-3 rounded-full bg-blue-600"></div>
                    </div>
                    <div>
                        <div class="font-medium">{{ channel.channel_name }}</div>
                        <div class="text-gray-600 text-sm mt-1">{{ channel.channel_description }}</div>
                    </div>
                </div>
            </div>
            <div class="mt-6 flex justify-between">
                <Button variant="subtle" @click="currentStep = 1">Back</Button>
                <Button variant="solid" size="lg" @click="currentStep = 3" :disabled="!selectedChannel">
                    Next: Address
                </Button>
            </div>
        </div>

        <!-- Step 3: Address -->
        <div v-else-if="currentStep === 3">
            <h2 class="text-2xl font-bold mb-6">Select Address</h2>
            <div v-if="addresses.loading">Loading...</div>
            <div v-else class="space-y-4">
                <div 
                    v-for="addr in addresses.data" 
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
                <Button icon-left="plus" @click="openAddressDialog">
                    Add Another Address
                </Button>
            </div>
            <div class="mt-6 flex justify-between">
                <Button variant="subtle" @click="currentStep = 2">Back</Button>
                <Button variant="solid" size="lg" @click="handleAddressSelection" :disabled="!selectedAddress" :loading="resolvingTerritory">
                    Next: Contact
                </Button>
            </div>
        </div>

        <!-- Step 4: Contact -->
        <div v-else-if="currentStep === 4">
            <h2 class="text-2xl font-bold mb-6">Select Contact</h2>
            <div v-if="contacts.loading">Loading...</div>
            <div v-else class="space-y-4">
                 <div 
                    v-for="contact in contacts.data" 
                    :key="contact.name" 
                    class="border p-4 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                    :class="{'border-blue-500 bg-blue-50': selectedContact === contact.name}"
                    @click="selectedContact = contact.name"
                >
                    <div class="font-medium">{{ contact.first_name }} {{ contact.last_name }}</div>
                    <div class="text-gray-600 text-sm mt-1">
                        {{ contact.mobile_no }}
                    </div>
                </div>
                <Button icon-left="plus" @click="showContactDialog = true">
                    Add New Contact
                </Button>
            </div>
            <div class="mt-6 flex justify-between">
                <Button variant="subtle" @click="currentStep = 3">Back</Button>
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
                    <div class="text-sm font-semibold text-gray-500 uppercase mt-4">Address</div>
                    <div class="text-sm">{{ getAddressTitle(selectedAddress) }}</div>
                </div>

                <!-- Contact -->
                <div v-if="selectedContact">
                    <div class="text-sm font-semibold text-gray-500 uppercase mt-4">Contact</div>
                    <div class="text-sm">{{ getContactName(selectedContact) }}</div>
                </div>
            </div>

            <div class="mt-8 pt-4 border-t">
                <Button 
                    v-if="canSubmit" 
                    variant="solid" 
                    class="w-full" 
                    size="lg" 
                    @click="submitOrder" 
                    :loading="createOrder.loading"
                >
                    Submit Order
                </Button>
                <div v-else-if="currentStep === 4 && !selectedContact" class="text-sm text-gray-500 text-center">
                    Select a contact to submit
                </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Custom Modal for Address -->
    <div v-if="showAddressDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md mx-4 overflow-hidden">
            <div class="px-6 py-4 border-b flex justify-between items-center">
                <h3 class="text-lg font-bold">Add Address</h3>
                <button @click="showAddressDialog = false" class="text-gray-500 hover:text-gray-700">&times;</button>
            </div>
            <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
                <Input label="Store Name / Individual Name" v-model="addressForm.address_title" />
                <Input label="Address Line 1" v-model="addressForm.address_line1" />
                <Input label="Address Line 2 (Optional)" v-model="addressForm.address_line2" />
                <Input label="City" v-model="addressForm.city" />
                <Input label="Pincode" v-model="addressForm.pincode" />
                <Input label="State" v-model="addressForm.state" />
                <Input label="Country" v-model="addressForm.country" :disabled="true" />
                <Input label="County" v-model="addressForm.county" :disabled="true" />
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end gap-2">
                <Button variant="subtle" @click="showAddressDialog = false">Cancel</Button>
                <Button variant="solid" @click="createAddress.submit" :loading="createAddress.loading">Save</Button>
            </div>
        </div>
    </div>

    <!-- Custom Modal for Contact -->
    <div v-if="showContactDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md mx-4 overflow-hidden">
            <div class="px-6 py-4 border-b flex justify-between items-center">
                <h3 class="text-lg font-bold">Add Contact</h3>
                <button @click="showContactDialog = false" class="text-gray-500 hover:text-gray-700">&times;</button>
            </div>
            <div class="p-6 space-y-4">
                <Input label="First Name" v-model="contactForm.first_name" />
                <Input label="Last Name" v-model="contactForm.last_name" />
                <Input label="Mobile Number" v-model="contactForm.mobile_no" />
                <Input label="Email" v-model="contactForm.email_id" />
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end gap-2">
                <Button variant="subtle" @click="showContactDialog = false">Cancel</Button>
                <Button variant="solid" @click="createContact.submit" :loading="createContact.loading">Save</Button>
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
                <Button variant="solid" @click="resetOrder">Place Another Order</Button>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { Button, Input, createResource, createListResource, LoadingIndicator, frappeRequest } from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentStep = ref(1)
const cart = reactive({})
const selectedAddress = ref(null)
const selectedContact = ref(null)
const selectedChannel = ref(null)
const resolvedTerritory = ref(null)
const resolvingTerritory = ref(false)

const showAddressDialog = ref(false)
const showContactDialog = ref(false)
const showSuccessDialog = ref(false)

const addressForm = reactive({ address_title: '', address_line1: '', address_line2: '', city: '', pincode: '', state: '', country: 'India', county: '' })
const contactForm = reactive({ first_name: '', last_name: '', mobile_no: '', email_id: '' })

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
            fields: ['name', 'address_title', 'address_line1', 'city', 'pincode', 'county'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    }
})

const contacts = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Contact',
            fields: ['name', 'first_name', 'last_name', 'mobile_no'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    }
})

const createAddress = createResource({
    url: 'frappe.client.insert',
    makeParams(values) {
        return {
            doc: {
                doctype: 'Address',
                ...addressForm,
                links: [{ link_doctype: 'User', link_name: session.data }]
            }
        }
    },
    onSuccess(data) {
        showAddressDialog.value = false
        addresses.fetch()
        selectedAddress.value = data.name
    }
})

const createContact = createResource({
    url: 'frappe.client.insert',
    makeParams(values) {
        return {
            doc: {
                doctype: 'Contact',
                ...contactForm,
                links: [{ link_doctype: 'User', link_name: session.data }]
            }
        }
    },
    onSuccess(data) {
        showContactDialog.value = false
        contacts.fetch()
        selectedContact.value = data.name
    }
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
                order_date: new Date().toISOString(),
                user: session.data,
                delivery_address: selectedAddress.value,
                contact: selectedContact.value,
                resolved_territory: resolvedTerritory.value,
                service_category: selectedChannel.value,
                order_status: 'Initiated',
                items: lineItems
            }
        }
    },
    onSuccess(data) {
        showSuccessDialog.value = true
    },
    onError(err) {
        alert('Order creation failed: ' + (err.messages ? err.messages.join(', ') : err.message))
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
    return hasItemsInCart.value && selectedChannel.value && selectedAddress.value && selectedContact.value
})

// Methods
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

function getContactName(name) {
    const contact = contacts.data?.find(c => c.name === name)
    return contact ? `${contact.first_name} ${contact.last_name}` : name
}

function openAddressDialog() {
    // Pre-fill county from selected channel
    const channel = channels.data?.find(c => c.name === selectedChannel.value)
    addressForm.county = channel ? channel.channel_name : ''
    showAddressDialog.value = true
}

async function handleAddressSelection() {
    if (!selectedAddress.value) return
    
    resolvingTerritory.value = true
    try {
        const address = addresses.data.find(a => a.name === selectedAddress.value)
        if (address) {
            resolvedTerritory.value = await resolveTerritory(address)
        }
        currentStep.value = 4
    } catch (e) {
        console.error(e)
        alert('Error resolving territory')
    } finally {
        resolvingTerritory.value = false
    }
}

async function resolveTerritory(address) {
    // 1. Pincode
    if (address.pincode) {
        let res = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Service Territory',
                filters: [['territory_name', '=', address.pincode], ['allow_in_search', '=', 1]],
                limit_page_length: 1
            }
        })
        if (res.message && res.message.length > 0) return res.message[0].name
    }

    // 2. City
    if (address.city) {
        let res = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Service Territory',
                filters: [['territory_name', '=', address.city], ['allow_in_search', '=', 1]],
                limit_page_length: 1
            }
        })
        if (res.message && res.message.length > 0) return res.message[0].name
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
    if (res.message && res.message.length > 0) return res.message[0].name
    
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
    if (newStep === 3) {
        addresses.fetch()
    }
    if (newStep === 4) {
        contacts.fetch()
    }
})

</script>

