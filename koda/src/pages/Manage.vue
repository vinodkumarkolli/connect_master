<template>
  <div class="max-w-4xl mx-auto py-12 px-4">
    <div class="flex justify-between items-center mb-8">
      <div class="flex items-center gap-4">
        <Button icon-left="arrow-left" variant="subtle" @click="router.push('/')">Home</Button>
        <h1 class="text-3xl font-bold text-gray-900">Manage Addresses & Contacts</h1>
      </div>
      <Button :appearance="'primary'" @click="openAddAddress">Add Address</Button>
    </div>

    <div v-if="addresses.loading" class="flex justify-center py-12">
      <LoadingIndicator />
    </div>

    <div v-else class="space-y-6">
      <div v-for="addr in sortedAddresses" :key="addr.name" class="bg-white rounded-lg shadow border border-gray-200" :class="{'opacity-75': addr.disabled}">
        <!-- Address Header -->
        <div class="px-6 py-4 border-b bg-gray-50 flex justify-between items-start rounded-t-lg">
          <div>
            <div class="flex items-center gap-2">
                <h3 class="text-lg font-bold text-gray-800">{{ addr.address_title }}</h3>
                <span v-if="addr.custom_is_default" class="px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full">Default</span>
                <span v-if="addr.disabled" class="px-2 py-0.5 text-xs bg-red-100 text-red-800 rounded-full">Disabled</span>
            </div>
            <div class="text-gray-600 text-sm mt-1">
              {{ addr.address_line1 }}, {{ addr.address_line2 ? addr.address_line2 + ', ' : '' }}
              {{ addr.city }}, {{ addr.state }} - {{ addr.pincode }}
            </div>
          </div>
          <CustomDropdown :options="getAddressOptions(addr)">
             <button class="text-gray-400 hover:text-gray-600 p-1 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
             </button>
          </CustomDropdown>
        </div>

        <!-- Contacts Section -->
        <div class="px-6 py-4">
            <div class="flex justify-between items-center mb-4">
                <h4 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">Contacts</h4>
                <Button size="sm" icon-left="plus" @click="openAddContact(addr)">Add Contact</Button>
            </div>
            
            <div v-if="getContactsForAddress(addr.name).length === 0" class="text-sm text-gray-400 italic">
                No contacts linked to this address.
            </div>
            
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="contact in getContactsForAddress(addr.name)" :key="contact.name" class="border rounded p-3 flex justify-between items-start hover:bg-gray-50">
                    <div>
                        <div class="flex items-center gap-2">
                            <div class="text-sm font-normal text-gray-700">{{ contact.first_name }} {{ contact.last_name }}</div>
                            <span v-if="!contact.unsubscribed" class="px-2 py-0.5 text-xs bg-green-100 text-green-800 rounded-full">Active</span>
                            <span v-else class="px-2 py-0.5 text-xs bg-red-100 text-red-800 rounded-full">Disabled</span>
                        </div>
                        <div class="font-bold text-gray-900">{{ contact.mobile_no || contact.phone }}</div>
                        <div class="text-sm text-gray-500">{{ contact.email_id }}</div>
                    </div>
                    <CustomDropdown v-if="!addr.disabled" :options="getContactOptions(contact)">
                        <button class="text-gray-400 hover:text-gray-600 p-1 focus:outline-none">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                        </button>
                    </CustomDropdown>
                    <button v-else class="text-gray-300 p-1 cursor-not-allowed">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                    </button>
                </div>
            </div>
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
        @success="refreshData"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Button, LoadingIndicator, createResource, frappeRequest } from 'frappe-ui'
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
    isDefaultAddress
} = useConsumerValidation()

const session = reactive({
    data: null,
    loading: true
})

const addresses = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Address',
            fields: ['name', 'address_title', 'address_line1', 'address_line2', 'city', 'pincode', 'state', 'country', 'county', 'custom_is_default', 'disabled'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    },
    auto: false
})

const sortedAddresses = computed(() => {
    if (!addresses.data) return []
    return [...addresses.data].sort((a, b) => {
        if (a.custom_is_default && !b.custom_is_default) return -1
        if (!a.custom_is_default && b.custom_is_default) return 1
        return (a.disabled || 0) - (b.disabled || 0)
    })
})

const contacts = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Contact',
            fields: ['name', 'first_name', 'last_name', 'mobile_no', 'phone', 'email_id', 'address', 'unsubscribed'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    },
    auto: false
})

onMounted(async () => {
    try {
        let res = await frappeRequest({ url: 'frappe.auth.get_logged_user' })
        if (res) {
            session.data = res.message || res
            refreshData()

            await checkAndPrompt()
        }
    } catch (e) {
        session.data = null
    } finally {
        session.loading = false
    }
})

function refreshData() {
    addresses.fetch()
    contacts.fetch()
}

function getContactsForAddress(addressName) {
    return (contacts.data || []).filter(c => c.address === addressName)
}

function openAddAddress() {
    communicationMode.value = 'Address+Contact'
    communicationAddress.value = null
    communicationContact.value = null
    isDefaultAddress.value = (!addresses.data || addresses.data.length === 0)
    isBlocking.value = false
    showCommunication.value = true
}

function openAddContact(address) {
    communicationMode.value = 'Contact'
    communicationAddress.value = address
    communicationContact.value = null
    isBlocking.value = false
    showCommunication.value = true
}

function getAddressOptions(addr) {
    if (addr.disabled) {
        return [{
            label: 'Enable Address',
            onClick: () => enableAddress(addr)
        }]
    }

    return [
        {
            label: 'Edit Address',
            onClick: () => {
                communicationMode.value = 'Editable Address'
                communicationAddress.value = addr
                communicationContact.value = null
                isBlocking.value = false
                showCommunication.value = true
            }
        },
        {
            label: 'Mark as Default',
            disabled: !!addr.custom_is_default,
            onClick: () => makeAddressDefault(addr)
        },
        {
            label: 'Disable Address',
            onClick: () => disableAddress(addr)
        }
    ]
}

function getContactOptions(contact) {
    return [
        {
            label: 'Edit Contact',
            onClick: () => {
                communicationMode.value = 'Editable Contact'
                communicationAddress.value = null // Not needed for contact edit
                communicationContact.value = contact
                isBlocking.value = false
                showCommunication.value = true
            }
        },
        {
            label: contact.unsubscribed ? 'Enable Contact' : 'Disable Contact',
            onClick: () => toggleContactSubscription(contact)
        }
    ]
}

const disableDoc = createResource({
    url: 'frappe.client.set_value',
    onSuccess() {
        refreshData()
    }
})

async function disableAddress(addr) {
    if (confirm('Are you sure you want to disable this address?')) {
        try {
            // 1. Set custom_is_default = 0
            if (addr.custom_is_default) {
                await frappeRequest({
                    url: 'frappe.client.set_value',
                    params: {
                        doctype: 'Address',
                        name: addr.name,
                        fieldname: 'custom_is_default',
                        value: 0
                    }
                })
            }

            // 2. Unsubscribe all contacts
            const addressContacts = getContactsForAddress(addr.name)
            const contactUpdates = addressContacts
                .filter(c => !c.unsubscribed)
                .map(c => frappeRequest({
                    url: 'frappe.client.set_value',
                    params: {
                        doctype: 'Contact',
                        name: c.name,
                        fieldname: 'unsubscribed',
                        value: 1
                    }
                }))
            
            await Promise.all(contactUpdates)

            // 3. Disable address
            await frappeRequest({
                url: 'frappe.client.set_value',
                params: {
                    doctype: 'Address',
                    name: addr.name,
                    fieldname: 'disabled',
                    value: 1
                }
            })

            refreshData()
        } catch (e) {
            console.error(e)
        }
    }
}

function enableAddress(addr) {
    if (confirm('Are you sure you want to enable this address?')) {
        disableDoc.submit({
            doctype: 'Address',
            name: addr.name,
            fieldname: 'disabled',
            value: 0
        })
    }
}

function toggleContactSubscription(contact) {
    const action = contact.unsubscribed ? 'enable' : 'disable'
    if (confirm(`Are you sure you want to ${action} this contact?`)) {
        disableDoc.submit({
            doctype: 'Contact',
            name: contact.name,
            fieldname: 'unsubscribed',
            value: contact.unsubscribed ? 0 : 1
        })
    }
}

async function makeAddressDefault(addr) {
    const currentDefault = addresses.data.find(a => a.custom_is_default)
    if (currentDefault) {
        await frappeRequest({
            url: 'frappe.client.set_value',
            params: {
                doctype: 'Address',
                name: currentDefault.name,
                fieldname: 'custom_is_default',
                value: 0
            }
        })
    }

    await frappeRequest({
        url: 'frappe.client.set_value',
        params: {
            doctype: 'Address',
            name: addr.name,
            fieldname: 'custom_is_default',
            value: 1
        }
    })
    
    refreshData()
}
</script>
