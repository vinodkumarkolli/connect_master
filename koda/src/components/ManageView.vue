<template>
  <div class="bg-white rounded-lg shadow border flex flex-col h-full">
      <div class="p-4 border-b bg-gray-50 flex gap-4 items-center">
        <div class="flex-1">
            <Input v-model="manageSearch" placeholder="Search Addresses or Contacts..." @keyup.enter="performManageSearch" />
        </div>
        <Button @click="performManageSearch" :loading="isManageSearching" appearance="primary">Search</Button>
        <Button @click="openAddAddress" icon="plus">Add Address</Button>
      </div>

      <div class="flex-1 overflow-y-auto p-4">
        <div v-if="isManageSearching" class="flex justify-center py-12">
            <LoadingIndicator />
        </div>
        <div v-else-if="manageResults.length === 0 && restrictedResults.length === 0 && hasManageSearched" class="p-12 text-center text-gray-500">
          No results found.
        </div>
        <div v-else-if="manageResults.length === 0 && restrictedResults.length === 0 && !hasManageSearched" class="p-12 text-center text-gray-400">
          Enter a search term to find addresses or contacts.
        </div>
        <div v-else class="space-y-6">
            <!-- Allowed Results -->
            <div v-if="manageResults.length > 0" class="space-y-4">
                <div class="text-xs font-semibold text-gray-500 uppercase">Allowed Results</div>
                <div v-for="res in manageResults" :key="res.name" class="border rounded-lg bg-white shadow-sm" :class="{'opacity-75': res.doc.disabled}">
                    <div class="px-4 py-3 border-b bg-gray-50 flex justify-between items-start rounded-t-lg">
                        <div>
                            <div class="flex items-center gap-2">
                                <div class="font-medium text-lg text-gray-900">{{ res.title }}</div>
                                <span v-if="res.doc.disabled" class="px-2 py-0.5 text-xs bg-red-100 text-red-800 rounded-full">Disabled</span>
                            </div>
                            <div class="text-gray-600">{{ res.description }}</div>
                            <div class="text-xs text-gray-400 mt-1 flex items-center gap-1">
                                <span class="w-1.5 h-1.5 rounded-full bg-gray-300"></span>
                                {{ res.user }}
                            </div>
                        </div>
                        <CustomDropdown :options="getAddressOptions(res)">
                             <button class="text-gray-400 hover:text-gray-600 p-1 focus:outline-none">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                             </button>
                        </CustomDropdown>
                    </div>

                    <!-- Contacts List -->
                    <div class="p-4">
                        <div class="flex justify-between items-center mb-3">
                            <div class="text-xs font-semibold text-gray-500 uppercase">Contacts</div>
                            <Button size="sm" icon="plus" @click="openAddContact(res)">Add Contact</Button>
                        </div>
                        
                        <div v-if="res.contacts && res.contacts.length > 0" class="grid gap-2">
                            <div v-for="contact in res.contacts" :key="contact.name" class="flex justify-between items-center p-3 bg-gray-50 rounded border hover:bg-gray-100 transition-colors">
                                <div>
                                    <div class="flex items-center gap-2">
                                        <div class="font-medium text-sm">{{ contact.full_name }}</div>
                                        <span v-if="!contact.unsubscribed" class="px-2 py-0.5 text-xs bg-green-100 text-green-800 rounded-full">Active</span>
                                        <span v-else class="px-2 py-0.5 text-xs bg-red-100 text-red-800 rounded-full">Disabled</span>
                                    </div>
                                    <div class="text-xs text-gray-500">{{ contact.mobile_no }}</div>
                                    <div class="text-xs text-gray-400" v-if="contact.email_id">{{ contact.email_id }}</div>
                                </div>
                                <CustomDropdown :options="getContactOptions(contact, res)">
                                    <button class="text-gray-400 hover:text-gray-600 p-1 focus:outline-none">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="19" cy="12" r="1"></circle><circle cx="5" cy="12" r="1"></circle></svg>
                                    </button>
                                </CustomDropdown>
                            </div>
                        </div>
                        <div v-else class="text-sm text-gray-400 italic">
                            No contacts linked to this address.
                        </div>
                    </div>
                </div>
            </div>

            <!-- Restricted Results -->
            <div v-if="restrictedResults.length > 0" class="space-y-4">
                <div class="text-xs font-semibold text-red-500 uppercase">Restricted Results</div>
                <div v-for="res in restrictedResults" :key="res.name" class="border rounded-lg bg-gray-50 opacity-75">
                    <div class="px-4 py-3 border-b flex justify-between items-start">
                        <div>
                            <div class="font-medium text-lg text-gray-700">{{ res.title }}</div>
                            <div class="text-gray-600">{{ res.description }}</div>
                            <div class="mt-2">
                                <span class="px-2 py-1 bg-gray-200 text-gray-500 rounded text-xs font-medium">Restricted</span>
                                <span v-if="res.doc.custom_resolved_territory" class="ml-2 px-2 py-1 bg-gray-100 text-gray-500 rounded text-xs font-medium border border-gray-200">
                                    {{ res.doc.custom_resolved_territory }}
                                </span>
                            </div>
                        </div>
                    </div>
                     <!-- Contacts List for Restricted -->
                    <div class="p-4">
                        <div class="text-xs font-semibold text-gray-500 uppercase mb-2">Contacts</div>
                        <div v-if="res.contacts && res.contacts.length > 0" class="grid gap-2">
                            <div v-for="contact in res.contacts" :key="contact.name" class="flex justify-between items-center p-2 bg-white rounded border">
                                <div>
                                    <div class="font-medium text-sm">{{ contact.full_name }}</div>
                                    <div class="text-xs text-gray-500">{{ contact.mobile_no }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>

      <!-- Communication Modal for Edit/Add -->
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
   </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, Input, frappeRequest, LoadingIndicator } from 'frappe-ui'
import Communication from './Communication.vue'
import CustomDropdown from './CustomDropdown.vue'

const manageSearch = ref('')
const manageResults = ref([])
const restrictedResults = ref([])
const isManageSearching = ref(false)
const hasManageSearched = ref(false)

const showCommunication = ref(false)
const communicationMode = ref('Address+Contact')
const communicationAddress = ref(null)
const communicationContact = ref(null)
const communicationUser = ref('customer@example.com')
const isDefaultAddress = ref(false)

async function performManageSearch() {
    if (!manageSearch.value) return
    isManageSearching.value = true
    manageResults.value = []
    restrictedResults.value = []
    hasManageSearched.value = false
    
    try {
        const q = manageSearch.value
        const res = await frappeRequest({
            url: 'connect_master.api.search_addresses_for_punch',
            params: { query: q }
        })
        const data = res.message || res
        manageResults.value = data.allowed || []
        restrictedResults.value = data.restricted || []
        hasManageSearched.value = true
    } catch (e) {
        console.error(e)
    } finally {
        isManageSearching.value = false
    }
}

function openAddAddress() {
    communicationMode.value = 'Address+Contact'
    communicationAddress.value = null
    communicationContact.value = null
    communicationUser.value = 'customer@example.com'
    isDefaultAddress.value = false
    showCommunication.value = true
}

function openEditAddress(res) {
    communicationMode.value = 'Editable Address'
    communicationAddress.value = res.doc
    communicationContact.value = null
    communicationUser.value = res.user
    isDefaultAddress.value = false
    showCommunication.value = true
}

function openAddContact(res) {
    communicationMode.value = 'Contact'
    communicationAddress.value = res.doc
    communicationContact.value = null
    communicationUser.value = res.user
    showCommunication.value = true
}

function openEditContact(contact, res) {
    communicationMode.value = 'Editable Contact'
    communicationAddress.value = null
    communicationContact.value = contact
    communicationUser.value = res.user
    showCommunication.value = true
}

function onCommunicationSuccess(data) {
    if (hasManageSearched.value) {
        performManageSearch()
    }
}

function getAddressOptions(res) {
    const addr = res.doc
    if (addr.disabled) {
        return [{
            label: 'Enable Address',
            onClick: () => enableAddress(res)
        }]
    }

    return [
        {
            label: 'Edit Address',
            onClick: () => openEditAddress(res)
        },
        {
            label: 'Disable Address',
            onClick: () => disableAddress(res)
        }
    ]
}

function getContactOptions(contact, res) {
    return [
        {
            label: 'Edit Contact',
            onClick: () => openEditContact(contact, res)
        },
        {
            label: contact.unsubscribed ? 'Enable Contact' : 'Disable Contact',
            onClick: () => toggleContactSubscription(contact)
        }
    ]
}

async function disableAddress(res) {
    const addr = res.doc
    if (confirm('Are you sure you want to disable this address?')) {
        try {
            // 1. Unsubscribe all contacts
            const contactUpdates = (res.contacts || [])
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

            // 2. Disable address
            await frappeRequest({
                url: 'frappe.client.set_value',
                params: {
                    doctype: 'Address',
                    name: addr.name,
                    fieldname: 'disabled',
                    value: 1
                }
            })

            performManageSearch()
        } catch (e) {
            console.error(e)
        }
    }
}

async function enableAddress(res) {
    const addr = res.doc
    if (confirm('Are you sure you want to enable this address?')) {
        try {
            await frappeRequest({
                url: 'frappe.client.set_value',
                params: {
                    doctype: 'Address',
                    name: addr.name,
                    fieldname: 'disabled',
                    value: 0
                }
            })
            performManageSearch()
        } catch (e) {
            console.error(e)
        }
    }
}

async function toggleContactSubscription(contact) {
    const action = contact.unsubscribed ? 'enable' : 'disable'
    if (confirm(`Are you sure you want to ${action} this contact?`)) {
        try {
            await frappeRequest({
                url: 'frappe.client.set_value',
                params: {
                    doctype: 'Contact',
                    name: contact.name,
                    fieldname: 'unsubscribed',
                    value: contact.unsubscribed ? 0 : 1
                }
            })
            performManageSearch()
        } catch (e) {
            console.error(e)
        }
    }
}
</script>
