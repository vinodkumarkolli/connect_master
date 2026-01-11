<template>
  <div class="bg-white rounded-lg shadow border flex flex-col h-full">
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

         <div v-if="isSearching" class="flex justify-center py-12">
            <LoadingIndicator />
         </div>
         <div v-else-if="punchSearchResults.length > 0 || restrictedSearchResults.length > 0" class="space-y-6">
           <!-- Allowed Results -->
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
                   <div class="flex flex-col items-end gap-2">
                       <span v-if="res.doc.custom_resolved_territory" class="px-2 py-1 bg-blue-50 text-blue-600 rounded text-xs font-medium border border-blue-100">
                           {{ res.doc.custom_resolved_territory }}
                       </span>
                       <Button size="sm" variant="subtle" @click="openAddressSummary(res)">Summary</Button>
                   </div>
                 </div>
               </div>
           </div>

           <!-- Restricted Results -->
           <div v-if="restrictedSearchResults.length > 0" class="space-y-3">
               <div class="text-xs font-semibold text-red-500 uppercase mb-2">Other Territories (Restricted)</div>
               <div
                 v-for="res in restrictedSearchResults"
                 :key="res.name"
                 class="border p-4 rounded-lg bg-gray-50 opacity-75 cursor-not-allowed"
               >
                 <div class="flex justify-between items-start">
                   <div>
                     <div class="font-medium text-lg text-gray-700">{{ res.title }}</div>
                     <div class="text-gray-600 mt-1">{{ res.description }}</div>
                     
                     <!-- Admin Details -->
                     <div v-if="res.admin_details && res.admin_details.length > 0" class="mt-3 pt-3 border-t border-gray-200">
                        <div class="text-xs font-semibold text-gray-500 mb-1">Territory Admin Contact:</div>
                        <div v-for="admin in res.admin_details" :key="admin.email" class="text-sm text-gray-700">
                            {{ admin.full_name }} ({{ admin.mobile_no || admin.email }})
                        </div>
                     </div>
                     <div v-else class="mt-3 pt-3 border-t border-gray-200 text-xs text-gray-400 italic">
                        No admin contact details available.
                     </div>
                   </div>
                   <div class="flex flex-col items-end gap-2">
                       <span class="px-2 py-1 bg-gray-200 text-gray-500 rounded text-xs font-medium">Restricted</span>
                       <span v-if="res.doc.custom_resolved_territory" class="px-2 py-1 bg-gray-100 text-gray-500 rounded text-xs font-medium border border-gray-200">
                           {{ res.doc.custom_resolved_territory }}
                       </span>
                       <Button size="sm" variant="subtle" @click="openAddressSummary(res)">Summary</Button>
                   </div>
                 </div>
               </div>
           </div>
         </div>
         <div v-else-if="hasSearched" class="text-center py-12 bg-gray-50 rounded-lg border border-dashed">
           <p class="text-gray-500">No results found.</p>
         </div>
       </div>

       <!-- Step 2: Select Contact -->
       <div v-else-if="punchStep === 2" class="max-w-3xl mx-auto">
          <div class="mb-6 flex items-center justify-between">
             <h2 class="text-2xl font-bold text-gray-900">Select Contact</h2>
             <Button variant="subtle" @click="punchStep = 1">Back</Button>
          </div>
          
          <div v-if="availableContacts.length > 0" class="space-y-3">
             <div
               v-for="contact in availableContacts"
               :key="contact.name"
               class="border p-4 rounded-lg hover:border-blue-500 hover:shadow-md cursor-pointer transition-all bg-white"
               @click="selectContact(contact)"
             >
               <div class="font-medium text-lg">{{ contact.first_name }} {{ contact.last_name }}</div>
               <div class="text-gray-600 mt-1">{{ contact.mobile_no }}</div>
               <div class="text-gray-500 text-sm">{{ contact.email_id }}</div>
             </div>
          </div>
          <div v-else class="text-center py-12">
             <p class="text-gray-500">No contacts found for this address.</p>
          </div>
       </div>

       <!-- Step 3: Select Items & Submit -->
       <div v-else-if="punchStep === 3" class="max-w-5xl mx-auto h-full flex flex-col">
         <div class="bg-blue-50 p-4 rounded-lg border border-blue-100 flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4 md:gap-0">
           <div class="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-8 w-full md:w-auto">
             <!-- Address Info -->
             <div class="flex items-center gap-3">
                <div class="bg-white p-2 rounded-full shadow-sm text-xl">📍</div>
                <div>
                   <div class="text-xs text-blue-600 uppercase font-bold">Address</div>
                   <div class="font-medium text-blue-900">{{ punchTarget?.title }}</div>
                   <div class="text-xs text-blue-700">{{ punchTarget?.description }}</div>
                </div>
             </div>
             
             <!-- Contact Info -->
             <div class="flex items-center gap-3" v-if="selectedContactDoc">
                <div class="bg-white p-2 rounded-full shadow-sm text-xl">👤</div>
                <div>
                   <div class="text-xs text-blue-600 uppercase font-bold">Contact</div>
                   <div class="font-medium text-blue-900">{{ selectedContactDoc.first_name }} {{ selectedContactDoc.last_name }}</div>
                   <div class="text-xs text-blue-700">{{ selectedContactDoc.mobile_no }}</div>
                </div>
             </div>
           </div>
           
           <div class="flex gap-2 w-full md:w-auto justify-end">
               <Button size="sm" variant="subtle" @click="punchStep = 2">Change Contact</Button>
               <Button size="sm" variant="subtle" @click="resetPunch">Start Over</Button>
           </div>
         </div>

         <div class="flex-1 flex flex-col md:flex-row gap-6 overflow-hidden">
           <!-- Items List -->
           <div class="flex-1 overflow-y-auto pr-2 w-full">
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
           <div class="w-full md:w-80 bg-gray-50 p-6 rounded-lg border flex flex-col max-h-full md:h-auto flex-shrink-0">
             <h3 class="font-bold text-lg mb-4 border-b pb-2 flex-shrink-0">Order Summary</h3>
             
             <div class="space-y-4 mb-6 overflow-y-auto flex-1">
                <!-- Items -->
                <div>
                    <div class="text-sm font-semibold text-gray-500 uppercase">Items</div>
                    <div v-if="!hasItemsInCart" class="text-gray-400 italic text-sm">No items selected</div>
                    <div v-else class="space-y-2 mt-2">
                        <div v-for="(qty, itemName) in cart" :key="itemName" v-show="qty > 0" class="flex justify-between text-sm">
                            <div class="flex-1 pr-2 overflow-hidden">
                                <div class="truncate" :title="getItemName(itemName)">{{ getItemName(itemName) }}</div>
                                <div class="text-xs text-gray-500">@ {{ formatCurrency(getItemMRP(itemName)) }}</div>
                            </div>
                            <div class="text-right flex-shrink-0">
                                <div class="font-medium">x {{ qty }}</div>
                                <div class="text-xs text-gray-500">{{ formatCurrency(getItemAmount(itemName, qty)) }}</div>
                            </div>
                        </div>
                        <div class="border-t pt-2 mt-2 flex justify-between font-bold">
                            <span>Total</span>
                            <span>{{ formatCurrency(totalAmount) }}</span>
                        </div>
                        <div class="text-xs text-gray-500">(This price is indicative and total is calculated from MRP. Final price may vary based on partner and other factors)</div>
                    </div>
                </div>

                <!-- Channel -->
                <div v-if="punchTarget?.doc?.custom_address_category">
                    <div class="text-sm font-semibold text-gray-500 uppercase mt-4">Channel</div>
                    <div class="text-sm">{{ getChannelName(punchTarget.doc.custom_address_category) }}</div>
                </div>
             </div>

             <div class="flex-shrink-0 pt-4 border-t">
                <Button appearance="primary" class="w-full" size="xl" :disabled="!hasItemsInCart" @click="submitPunchOrder" :loading="createOrder.loading">
                  Punch Order
                </Button>
             </div>
           </div>
         </div>
       </div>
     </div>

    <!-- Communication Modal for Create -->
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

    <!-- Address Summary Modal -->
    <div v-if="showAddressSummaryDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md mx-4 overflow-hidden flex flex-col max-h-[80vh]">
            <div class="px-6 py-4 border-b flex justify-between items-center">
                <h3 class="text-lg font-bold">Address Summary</h3>
                <button @click="showAddressSummaryDialog = false" class="text-gray-500 hover:text-gray-700">&times;</button>
            </div>
            <div class="p-6 overflow-y-auto" v-if="summaryAddress">
                <div class="mb-4">
                    <div class="text-xs font-semibold text-gray-500 uppercase">Address</div>
                    <div class="font-medium text-lg">{{ summaryAddress.title }}</div>
                    <div class="text-gray-600">{{ summaryAddress.description }}</div>
                    <div class="text-sm text-gray-500 mt-1" v-if="summaryAddress.doc.custom_resolved_territory">
                        Territory: {{ summaryAddress.doc.custom_resolved_territory }}
                    </div>
                </div>
                
                <div>
                    <div class="text-xs font-semibold text-gray-500 uppercase mb-2">Linked Contacts</div>
                    <div v-if="summaryContacts.length > 0" class="space-y-2">
                        <div v-for="contact in summaryContacts" :key="contact.name" class="bg-gray-50 p-3 rounded border">
                            <div class="font-medium">{{ contact.full_name }}</div>
                            <div class="text-sm text-gray-600">{{ contact.mobile_no }}</div>
                            <div class="text-xs text-gray-500" v-if="contact.email_id">{{ contact.email_id }}</div>
                        </div>
                    </div>
                    <div v-else class="text-gray-500 italic text-sm">No linked contacts found.</div>
                </div>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end">
                <Button @click="showAddressSummaryDialog = false">Close</Button>
            </div>
        </div>
    </div>

    <!-- Channel Partner Selection Modal -->
    <div v-if="showChannelPartnerDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md mx-4 overflow-hidden flex flex-col max-h-[80vh]">
            <div class="px-6 py-4 border-b flex justify-between items-center">
                <h3 class="text-lg font-bold">Select Channel Partner</h3>
                <button @click="showChannelPartnerDialog = false" class="text-gray-500 hover:text-gray-700">&times;</button>
            </div>
            <div class="p-6 overflow-y-auto">
                <div v-if="channelPartners.loading" class="flex justify-center">
                    <LoadingIndicator />
                </div>
                <div v-else class="space-y-2">
                    <template v-if="channelPartners.data && channelPartners.data.length > 0">
                        <div
                            v-for="partner in channelPartners.data"
                            :key="partner.name"
                            class="border p-4 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                            :class="{'ring-2 ring-blue-500 bg-blue-50': selectedChannelPartner === partner.name}"
                            @click="selectedChannelPartner = partner.name"
                        >
                            <div class="font-medium">{{ partner.partner_name }}</div>
                            <div class="text-gray-600 text-sm mt-1" v-if="partner.description">{{ partner.description }}</div>
                            <div class="text-gray-500 text-xs mt-2" v-if="partner.address_html" v-html="partner.address_html"></div>
                            <div class="text-gray-500 text-xs mt-1" v-if="partner.contact_html" v-html="partner.contact_html"></div>
                        </div>
                    </template>
                    <div v-else class="text-center text-gray-500 mb-4">
                        No Channel Partners found for this area.
                    </div>

                    <div
                        class="border p-4 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                        :class="{'ring-2 ring-blue-500 bg-blue-50': selectedChannelPartner === 'custom'}"
                        @click="selectedChannelPartner = 'custom'"
                    >
                        <div class="font-medium">Couldn't find the Partner I am looking</div>
                        <div class="text-gray-600 text-sm mt-1">Be assured. We will find a Channel Partner as soon as possible</div>
                        
                        <div v-if="selectedChannelPartner === 'custom'" class="mt-3" @click.stop>
                            <textarea
                                v-model="customPartnerDescription"
                                rows="2"
                                class="w-full border rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500 outline-none"
                                placeholder="Please describe the partner you are looking for..."
                            ></textarea>
                        </div>
                    </div>
                </div>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end gap-2">
                <Button variant="subtle" @click="showChannelPartnerDialog = false">Cancel</Button>
                <Button appearance="primary" :disabled="!selectedChannelPartner" @click="confirmOrder" :loading="createOrder.loading">
                    Confirm & Submit
                </Button>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Button, Input, createResource, createListResource, frappeRequest, LoadingIndicator } from 'frappe-ui'
import Communication from './Communication.vue'

const session = createResource({
    url: 'frappe.auth.get_logged_user',
    auto: true
})

const punchSearch = ref('')
const punchStep = ref(1)
const punchSearchResults = ref([])
const restrictedSearchResults = ref([])
const isSearching = ref(false)
const hasSearched = ref(false)
const punchTarget = ref(null)
const selectedContact = ref(null)
const selectedContactDoc = ref(null)
const availableContacts = ref([])
const cart = reactive({})

const showChannelPartnerDialog = ref(false)
const channelPartners = reactive({ data: [], loading: false })
const selectedChannelPartner = ref(null)
const customPartnerDescription = ref('')

const showAddressSummaryDialog = ref(false)
const summaryAddress = ref(null)
const summaryContacts = ref([])

async function openAddressSummary(res) {
    summaryAddress.value = res
    summaryContacts.value = []
    showAddressSummaryDialog.value = true
    
    try {
        const contactsRes = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Contact',
                fields: ['name', 'first_name', 'last_name', 'mobile_no', 'email_id'],
                filters: [['address', '=', res.name], ['unsubscribed', '=', 0]]
            }
        })
        const list = contactsRes.message || contactsRes || []
        summaryContacts.value = list.map(c => ({
            name: c.name,
            full_name: `${c.first_name} ${c.last_name}`,
            mobile_no: c.mobile_no,
            email_id: c.email_id
        }))
    } catch (e) {
        console.error(e)
    }
}

const showCommunication = ref(false)
const communicationMode = ref('Address+Contact')
const communicationAddress = ref(null)
const communicationContact = ref(null)
const communicationUser = ref('customer@example.com')

const showSuccessDialog = ref(false)
const successMessage = ref('')

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

function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value || 0)
}

function getItemName(name) {
    const item = items.data?.find(i => i.name === name)
    return item ? item.item_name : name
}

function getItemMRP(name) {
    const item = items.data?.find(i => i.name === name)
    return item ? item.item_mrp : 0
}

function getItemAmount(itemName, qty) {
    const item = items.data?.find(i => i.name === itemName)
    return (item?.item_mrp || 0) * qty
}

function getChannelName(name) {
    const channel = channels.data?.find(c => c.name === name)
    return channel ? channel.channel_name : name
}

async function getLinkUser(doctype, name) {
    try {
        const res = await frappeRequest({
            url: 'connect_master.api.get_document_user',
            params: {
                doctype: doctype,
                name: name
            }
        })
        return res.message || res || 'Unknown'
    } catch (e) {
        return 'Unknown'
    }
}

async function performPunchSearch() {
    if (!punchSearch.value) return
    isSearching.value = true
    punchSearchResults.value = []
    restrictedSearchResults.value = []
    hasSearched.value = false
    
    try {
        const q = punchSearch.value
        
        const res = await frappeRequest({
            url: 'connect_master.api.search_addresses_for_punch',
            params: { query: q }
        })
        const data = res.message || res
        punchSearchResults.value = data.allowed || []
        restrictedSearchResults.value = data.restricted || []
        
        hasSearched.value = true
    } catch (e) {
        console.error(e)
    } finally {
        isSearching.value = false
    }
}

async function selectPunchTarget(res) {
    punchTarget.value = res
    punchStep.value = 2
    Object.keys(cart).forEach(key => delete cart[key])
    selectedContact.value = null
    selectedContactDoc.value = null
    availableContacts.value = []
    await fetchContactsForAddress(res.name)
}

function selectContact(contact) {
    selectedContact.value = contact.name
    selectedContactDoc.value = contact
    punchStep.value = 3
}

async function fetchContactsForAddress(addressName) {
    try {
        const res = await frappeRequest({
            url: 'frappe.client.get_list',
            params: {
                doctype: 'Contact',
                fields: ['name', 'first_name', 'last_name', 'mobile_no', 'email_id'],
                filters: [['address', '=', addressName], ['unsubscribed', '=', 0]]
            }
        })
        availableContacts.value = res.message || res || []
        if (availableContacts.value.length === 1) {
            selectContact(availableContacts.value[0])
        }
    } catch (e) {
        console.error(e)
    }
}

function resetPunch() {
    punchStep.value = 1
    punchTarget.value = null
    selectedContact.value = null
    selectedContactDoc.value = null
    availableContacts.value = []
    selectedChannelPartner.value = null
    customPartnerDescription.value = ''
}

async function fetchChannelPartners() {
    channelPartners.loading = true
    channelPartners.data = []
    selectedChannelPartner.value = null
    customPartnerDescription.value = ''
    
    const territory = punchTarget.value.doc.custom_resolved_territory
    const channel = punchTarget.value.doc.custom_address_category
    
    if (!territory) {
        // If no territory, proceed with submission without partner selection
        createOrder.submit()
        return
    }

    try {
        const res = await frappeRequest({
            url: 'connect_master.connect_master.doctype.connect_order.connect_order.get_channel_partners',
            params: {
                territory: territory,
                channel: channel
            }
        })
        channelPartners.data = res.message || res
        showChannelPartnerDialog.value = true
    } catch (e) {
        console.error(e)
        alert('Failed to fetch Channel Partners')
    } finally {
        channelPartners.loading = false
    }
}

function confirmOrder() {
    createOrder.submit()
}


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
        
        let address = punchTarget.value.name
        let service_category = punchTarget.value.doc.custom_address_category
        let contact = selectedContact.value
        
        const doc = {
            doctype: 'Connect Order',
            order_date: nowStr,
            user: session.data,
            delivery_address: address,
            contact: contact,
            service_category: service_category,
            order_status: (selectedChannelPartner.value && selectedChannelPartner.value !== 'custom') ? 'Assigned' : 'Submitted',
            channel_partner: (selectedChannelPartner.value && selectedChannelPartner.value !== 'custom') ? selectedChannelPartner.value : undefined,
            order_notes: selectedChannelPartner.value === 'custom' ? customPartnerDescription.value : undefined,
            docstatus: 1,
            items: lineItems
        }

        if (selectedChannelPartner.value && selectedChannelPartner.value !== 'custom') {
            doc.timeline = [
                {
                    event_type: "Status Update",
                    recorded_time: nowStr,
                    is_internal: 0,
                    fieldname: "order_status",
                    from_value: "Submitted",
                    to_value: "Assigned",
                    created_by: session.data
                },
                {
                    event_type: "Field Change",
                    recorded_time: nowStr,
                    is_internal: 0,
                    fieldname: "channel_partner",
                    from_value: '',
                    to_value: selectedChannelPartner.value,
                    created_by: session.data
                }
            ]
        }
        if(selectedChannelPartner.value === 'custom'){
            doc.timeline = [
                {
                    event_type: "Status Update",
                    recorded_time: nowStr,
                    is_internal: 0,
                    fieldname: "order_status",
                    from_value: "Initiated",
                    to_value: "Submitted",
                    created_by: session.data
                }
            ]
        }

        return { doc }
    },
    onSuccess(data) {
        showChannelPartnerDialog.value = false
        successMessage.value = `Order ${data.name} created successfully!`
        showSuccessDialog.value = true
        resetPunch()
    },
    onError(err) {
        console.error(err)
        alert('Failed to create order: ' + (err.messages ? err.messages.join(', ') : err.message))
    }
})

async function submitPunchOrder() {
    if (!selectedContact.value) {
        alert('Please select a contact')
        return
    }
    fetchChannelPartners()
}

async function onCommunicationSuccess(data) {
    if (data.address) {
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
}
</script>
