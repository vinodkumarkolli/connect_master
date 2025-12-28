<template>
  <div class="max-w-4xl mx-auto py-12 px-4">
    <!-- Step 1: Welcome -->
    <div v-if="currentStep === 1" class="text-center space-y-6 py-20">
      <h1 class="text-5xl font-bold text-gray-900">Koda</h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        We make buying of Sastry Balm easy by connecting you with local vendors/distributors/wholesalers
      </p>
      <div class="pt-8">
        <Button variant="solid" size="xl" @click="currentStep = 2">
          Start Ordering
        </Button>
      </div>
    </div>

    <!-- Step 2: Items -->
    <div v-else-if="currentStep === 2">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold">Select Items</h2>
        <div class="text-gray-600">
            Total Items: {{ totalItems }}
        </div>
      </div>
      
      <div v-if="items.loading" class="flex justify-center py-12">
        <LoadingIndicator />
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div v-for="item in items.data" :key="item.name" class="border rounded-lg p-4 flex flex-col gap-3 bg-white shadow-sm hover:shadow-md transition-shadow">
            <div class="aspect-square bg-gray-100 rounded-md overflow-hidden relative">
                <img v-if="item.item_image" :src="item.item_image" class="w-full h-full object-cover" />
                <div v-else class="w-full h-full flex items-center justify-center text-gray-400 bg-gray-50">
                    <span class="text-sm">No Image</span>
                </div>
            </div>
            <div>
                <div class="font-bold text-lg truncate" :title="item.item_name">{{ item.item_name }}</div>
                <div class="text-gray-600 font-medium">{{ formatCurrency(item.item_mrp) }}</div>
            </div>
            <div class="mt-auto pt-2">
                <Input
                    type="number"
                    label="Quantity"
                    v-model.number="cart[item.name]"
                    min="0"
                    placeholder="0"
                />
            </div>
        </div>
      </div>
      <div class="mt-8 flex justify-between items-center border-t pt-6">
        <Button variant="subtle" @click="currentStep = 1">
            Back
        </Button>
        <Button variant="solid" size="lg" @click="currentStep = 3" :disabled="!hasItemsInCart">
            Next
        </Button>
      </div>
    </div>

    <!-- Step 3: Service Channel -->
    <div v-else-if="currentStep === 3">
        <h2 class="text-2xl font-bold mb-6">Select Service Channel</h2>
        <div v-if="channels.loading">Loading channels...</div>
        <div v-else class="space-y-4">
            <div 
                v-for="channel in channels.data" 
                :key="channel.name" 
                class="border p-4 rounded-lg cursor-pointer flex items-center gap-3 hover:border-blue-500 transition-colors"
                :class="{'border-blue-500 bg-blue-50': selectedChannel === channel.name}"
                @click="selectedChannel = channel.name"
            >
                <div class="w-5 h-5 rounded-full border border-gray-400 flex items-center justify-center" :class="{'border-blue-600': selectedChannel === channel.name}">
                    <div v-if="selectedChannel === channel.name" class="w-3 h-3 rounded-full bg-blue-600"></div>
                </div>
                <div>
                    <div class="font-medium">{{ channel.channel_name }}</div>
                    <div class="text-gray-600 text-sm">{{ channel.channel_description }}</div>
                </div>
            </div>
        </div>
        <div class="mt-8 flex justify-between items-center border-t pt-6">
            <Button variant="subtle" @click="currentStep = 2">Back</Button>
            <Button variant="solid" size="lg" @click="goToStep4" :disabled="!selectedChannel">Next</Button>
        </div>
    </div>

    <!-- Step 4: Auth -->
    <div v-else-if="currentStep === 4" class="max-w-md mx-auto">
        <h2 class="text-2xl font-bold mb-6 text-center">Login or Signup</h2>
        <div class="bg-white p-6 rounded-lg border shadow-sm space-y-4">
            <div v-if="authMode === 'login'">
                <Input label="Email" type="email" v-model="loginForm.email" />
                <Input label="Password" type="password" v-model="loginForm.password" class="mt-4" />
                <Button class="w-full mt-6" variant="solid" :loading="loginResource.loading" @click="loginResource.submit">
                    Login
                </Button>
                <div class="mt-4 text-center text-sm">
                    New here? <a href="#" @click.prevent="authMode = 'signup'" class="text-blue-600">Create an account</a>
                </div>
            </div>
            <div v-else>
                <Input label="Full Name" type="text" v-model="signupForm.fullName" />
                <Input label="Email" type="email" v-model="signupForm.email" class="mt-4" />
                <Button class="w-full mt-6" variant="solid" :loading="signupResource.loading" @click="signupResource.submit">
                    Signup
                </Button>
                <div class="mt-4 text-center text-sm">
                    Already have an account? <a href="#" @click.prevent="authMode = 'login'" class="text-blue-600">Login</a>
                </div>
            </div>
        </div>
         <div class="mt-8 flex justify-start">
            <Button variant="subtle" @click="currentStep = 3">
                Back
            </Button>
        </div>
    </div>

    <!-- Step 5: Address -->
    <div v-else-if="currentStep === 5">
        <h2 class="text-2xl font-bold mb-6">Select Delivery Address</h2>
        <!-- Address List -->
        <div v-if="addresses.loading">Loading addresses...</div>
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
            </div>
            <div v-if="!addresses.data || addresses.data.length === 0" class="text-gray-500 italic">
                No addresses found. Please add one.
            </div>
            <Button icon-left="plus" @click="showAddressDialog = true">
                Add New Address
            </Button>
        </div>
        <div class="mt-8 flex justify-between items-center border-t pt-6">
            <Button variant="subtle" @click="currentStep = 3">Back</Button>
            <Button variant="solid" size="lg" @click="handleAddressSelection" :disabled="!selectedAddress" :loading="resolvingTerritory">Next</Button>
        </div>
    </div>

    <!-- Step 6: Contact -->
    <div v-else-if="currentStep === 6">
        <h2 class="text-2xl font-bold mb-6">Select Contact</h2>
        <div v-if="contacts.loading">Loading contacts...</div>
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
             <div v-if="!contacts.data || contacts.data.length === 0" class="text-gray-500 italic">
                No contacts found. Please add one.
            </div>
            <Button icon-left="plus" @click="showContactDialog = true">
                Add New Contact
            </Button>
        </div>
        <div class="mt-8 flex justify-between items-center border-t pt-6">
            <Button variant="subtle" @click="currentStep = 5">Back</Button>
            <Button variant="solid" size="lg" @click="submitOrder" :loading="createOrder.loading">Submit Order</Button>
        </div>
    </div>

    <!-- Step 7: Success -->
    <div v-else-if="currentStep === 7" class="text-center py-20">
        <div class="text-green-500 text-6xl mb-6">✓</div>
        <h2 class="text-3xl font-bold mb-4">Order Placed Successfully!</h2>
        <p class="text-gray-600 mb-8">Thank you for your order.</p>
        <div class="flex justify-center gap-4">
            <Button variant="outline" @click="resetOrder">
                Place Another Order
            </Button>
            <!-- Placeholder for Orders link -->
            <Button variant="solid" @click="viewOrders">
                View Orders
            </Button>
        </div>
    </div>

    <!-- Dialogs -->
    <Dialog v-model="showAddressDialog" title="Add Address">
        <div class="p-4 space-y-4">
            <Input label="Address Title" v-model="addressForm.address_title" />
            <Input label="Address Line 1" v-model="addressForm.address_line1" />
            <Input label="City" v-model="addressForm.city" />
            <Input label="Pincode" v-model="addressForm.pincode" />
            <Input label="State" v-model="addressForm.state" />
            <Input label="Country" v-model="addressForm.country" />
        </div>
        <template #actions>
            <Button variant="solid" @click="createAddress.submit" :loading="createAddress.loading">Save</Button>
        </template>
    </Dialog>

    <Dialog v-model="showContactDialog" title="Add Contact">
        <div class="p-4 space-y-4">
            <Input label="First Name" v-model="contactForm.first_name" />
            <Input label="Last Name" v-model="contactForm.last_name" />
            <Input label="Mobile Number" v-model="contactForm.mobile_no" />
            <Input label="Email" v-model="contactForm.email_id" />
        </div>
        <template #actions>
            <Button variant="solid" @click="createContact.submit" :loading="createContact.loading">Save</Button>
        </template>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { Button, Input, Dialog, createResource, createListResource, LoadingIndicator, frappeRequest } from 'frappe-ui'

const currentStep = ref(1)
const cart = reactive({})
const selectedAddress = ref(null)
const selectedContact = ref(null)
const selectedChannel = ref(null)
const resolvedTerritory = ref(null)
const resolvingTerritory = ref(false)

const showAddressDialog = ref(false)
const showContactDialog = ref(false)
const authMode = ref('login')

const loginForm = reactive({ email: '', password: '' })
const signupForm = reactive({ fullName: '', email: '' })
const addressForm = reactive({ address_title: '', address_line1: '', city: '', pincode: '', state: '', country: 'India' })
const contactForm = reactive({ first_name: '', last_name: '', mobile_no: '', email_id: '' })

// Resources
const session = reactive({
    data: 'Guest',
    loading: true
})

onMounted(async () => {
    try {
        let res = await frappeRequest({ url: 'frappe.auth.get_logged_user' })
        if (res) {
            session.data = res.message || res
        }
    } catch (e) {
        // If permission error, we are Guest
        console.log('Session check failed, assuming Guest', e)
        session.data = 'Guest'
    } finally {
        session.loading = false
    }
})

const items = reactive({
    data: [],
    loading: true,
    error: null
})

const channels = reactive({
    data: [],
    loading: true,
    error: null
})

onMounted(async () => {
    // Fetch Items
    try {
        // Using native fetch for REST API to ensure correct behavior
        let params = new URLSearchParams({
            fields: JSON.stringify(['name', 'item_name', 'item_code', 'item_image', 'item_mrp']),
            limit_page_length: 100
        })
        let response = await fetch(`/api/resource/Connect Item?${params}`)
        if (!response.ok) {
            let errorText = await response.text()
            throw new Error(`HTTP ${response.status}: ${errorText}`)
        }
        let res = await response.json()
        
        if (res && res.data) {
            items.data = res.data
        } else {
            console.warn('Items fetch returned unexpected response:', res)
        }
    } catch (e) {
        items.error = e
        console.error(e)
        alert('Failed to load items: ' + (e.message || e.statusText || e))
    } finally {
        items.loading = false
    }

    // Fetch Channels
    try {
        let params = new URLSearchParams({
            fields: JSON.stringify(['name', 'channel_name', 'channel_description']),
            limit_page_length: 100
        })
        let response = await fetch(`/api/resource/Service Channel?${params}`)
        if (!response.ok) {
            let errorText = await response.text()
            throw new Error(`HTTP ${response.status}: ${errorText}`)
        }
        let res = await response.json()

        if (res && res.data) {
            channels.data = res.data
        } else {
            console.warn('Channels fetch returned unexpected response:', res)
        }
    } catch (e) {
        channels.error = e
        console.error(e)
        alert('Failed to load channels: ' + (e.message || e.statusText || e))
    } finally {
        channels.loading = false
    }
})

const addresses = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Address',
            fields: ['name', 'address_title', 'address_line1', 'city', 'pincode'],
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

const loginResource = createResource({
    url: 'login',
    makeParams(values) {
        return {
            usr: loginForm.email,
            pwd: loginForm.password
        }
    },
    onSuccess(data) {
        // Refresh session
        frappeRequest({ url: 'frappe.auth.get_logged_user' }).then(res => {
             session.data = res.message || res
             currentStep.value = 5
        })
    },
    onError(err) {
        alert('Login failed: ' + (err.messages ? err.messages.join(', ') : err.message))
    }
})

const signupResource = createResource({
    url: 'frappe.core.doctype.user.user.sign_up',
    makeParams(values) {
        return {
            email: signupForm.email,
            full_name: signupForm.fullName,
            redirect_to: ''
        }
    },
    onSuccess(data) {
        alert('Signup successful! Please check your email for verification or login if allowed.')
        authMode.value = 'login'
    },
    onError(err) {
        alert('Signup failed: ' + (err.messages ? err.messages.join(', ') : err.message))
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
        currentStep.value = 7
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

// Methods
function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)
}

function goToStep4() {
    if (session.data && session.data !== 'Guest') {
        currentStep.value = 5
    } else {
        currentStep.value = 4
    }
}

async function handleAddressSelection() {
    if (!selectedAddress.value) return
    
    resolvingTerritory.value = true
    try {
        const address = addresses.data.find(a => a.name === selectedAddress.value)
        if (address) {
            resolvedTerritory.value = await resolveTerritory(address)
            if (!resolvedTerritory.value) {
                console.warn('Could not resolve territory')
                // Proceed anyway? Or block? User said "assign the parent most".
                // If parent most also fails, we might have an issue.
            }
        }
        currentStep.value = 6
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
    // Assuming root has no parent.
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
    currentStep.value = 1
    Object.keys(cart).forEach(key => delete cart[key])
    selectedAddress.value = null
    selectedContact.value = null
    selectedChannel.value = null
    resolvedTerritory.value = null
}

function viewOrders() {
    alert('Navigate to Orders Page')
}

// Watchers
watch(currentStep, (newStep) => {
    if (newStep === 5) {
        addresses.fetch()
    }
    if (newStep === 6) {
        contacts.fetch()
    }
})

</script>
