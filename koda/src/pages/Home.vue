<template>
  <div class="max-w-4xl mx-auto py-12 px-4">
    <div v-if="session.loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>

    <div v-else-if="!session.data || session.data === 'Guest'">
      <!-- Step 1: Welcome -->
      <div class="text-center space-y-6 py-12 md:py-20 bg-white p-4 md:p-6 rounded-lg shadow border border-gray-100">
        <h1 class="text-5xl font-bold text-gray-900">Koda</h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          We make buying of Sastry Balm easy by connecting you with local vendors/distributors/wholesalers
        </p>
        <div class="pt-8">
          <Button :appearance="'primary'" size="xl" @click="startOrdering">
            Start Ordering
          </Button>
        </div>
      </div>
      <!-- Process Flow Section -->
        <div class="mt-8 md:mt-16 mb-12 max-w-5xl mx-auto px-4 bg-white p-4 md:p-6 rounded-lg shadow border border-gray-100">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
                
                <!-- Connector Line (Hidden on mobile, visible on desktop) -->
                <div class="hidden md:block absolute top-1/4 left-0 w-full h-0.5 bg-gray-200 -z-10"></div>

                <!-- Step 1 -->
                <div class="flex flex-col items-center group">
                <div class="w-16 h-16 bg-blue-600 text-white rounded-2xl flex items-center justify-center shadow-lg mb-4 group-hover:scale-110 transition-transform duration-300">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-8 w-8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                    </svg>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">1. Place Order</h3>
                <p class="text-sm text-gray-500 text-center px-4 leading-relaxed">
                    Select your preferred Channel Partner and place your order directly on the Koda App.
                </p>
                </div>

                <!-- Step 2 -->
                <div class="flex flex-col items-center group">
                <div class="w-16 h-16 bg-indigo-600 text-white rounded-2xl flex items-center justify-center shadow-lg mb-4 group-hover:scale-110 transition-transform duration-300">
                    <svg xmlns="www.w3.org" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">2. Verification</h3>
                <p class="text-sm text-gray-500 text-center px-4 leading-relaxed">
                    Sravi Enterprises analyzes and allocates the best available Partner for your service.
                </p>
                </div>

                <!-- Step 3 -->
                <div class="flex flex-col items-center group">
                <div class="w-16 h-16 bg-emerald-600 text-white rounded-2xl flex items-center justify-center shadow-lg mb-4 group-hover:scale-110 transition-transform duration-300">
                    <svg xmlns="www.w3.org" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>
                <h3 class="text-lg font-bold text-gray-900 mb-2">3. Fulfillment</h3>
                <p class="text-sm text-gray-500 text-center px-4 leading-relaxed">
                    The Partner fulfills the order while you track live updates in real-time on our application.
                </p>
                </div>

            </div>
        </div>
    </div>

    <div v-else class="space-y-8">
      <!-- Dashboard for Logged In Users -->
      
      <!-- Top Pane: Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left Pane: Manage Actions -->
        <div class="bg-white p-4 md:p-6 rounded-lg shadow border border-gray-100 flex flex-col justify-center">
            <h2 class="text-lg font-semibold text-gray-800 mb-4">Manage</h2>
            <div class="flex flex-wrap gap-4">
                <Button @click="manageAddresses" class="w-full md:w-auto">Manage Addresses & Contacts</Button>
                <!-- <Button @click="manageContacts"> Contacts</Button> -->
            </div>
        </div>

        <!-- Right Pane: Create Order -->
        <div class="bg-white p-4 md:p-6 rounded-lg shadow border border-gray-100 flex flex-col items-center justify-center">
             <Button :appearance="'primary'" size="xl" @click="createOrder" class="w-full md:w-auto">
                Create Order
             </Button>
        </div>
      </div>

      <!-- Bottom Pane: Order History -->
      <div class="bg-white p-4 md:p-6 rounded-lg shadow border border-gray-100 min-h-[400px]">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">Order History</h2>
        </div>
        
        <div v-if="orders.loading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>
        <div v-else-if="orders.data && orders.data.length > 0" class="space-y-4">
            <div v-for="order in orders.data" :key="order.name" class="border p-4 rounded-lg flex flex-col sm:flex-row justify-between items-start sm:items-center hover:bg-gray-50 transition-colors gap-4">
                <div>
                    <div class="font-bold text-gray-900">{{ order.name }}</div>
                    <div class="text-sm text-gray-500">{{ formatDate(order.order_date) }}</div>
                    <!-- <div class="text-sm text-gray-600 mt-1">
                        <span class="font-medium">Items:</span> {{ orderQuantities[order.name] || 0 }}
                    </div> -->
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <span :class="getStatusClass(order.order_status)" class="px-3 py-1 rounded-full text-xs font-medium">
                        {{ order.order_status }}
                    </span>
                    <span class="px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                        {{ order.user }}
                    </span>
                    <Button size="sm" @click.stop="viewOrderSummary(order)">
                        Order Summary
                    </Button>
                    <Button size="sm" @click.stop="trackOrder(order)">
                        Track Order
                    </Button>
                </div>
            </div>
        </div>
        <div v-else class="text-center text-gray-500 py-20 border-2 border-dashed border-gray-200 rounded-lg">
            No orders found.
        </div>
      </div>
    </div>

    <!-- Summary Modal -->
    <div v-if="showSummaryDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-lg mx-4 overflow-hidden flex flex-col max-h-[80vh]">
            <div class="px-6 py-4 border-b">
                <h3 class="text-lg font-bold">Order Summary: {{ currentSummaryDoc?.name || 'Loading...' }}</h3>
            </div>
            <div class="p-6 overflow-y-auto">
                <div v-if="summaryLoading" class="py-4 text-center">Loading...</div>
                <div v-else-if="currentSummaryDoc" class="mt-4 space-y-4">
                    <!-- Items -->
                    <div>
                        <h4 class="font-bold text-sm uppercase text-gray-500 mb-2">Items</h4>
                        <div v-for="item in currentSummaryDoc.items" :key="item.name" class="flex justify-between items-center text-sm py-2 border-b last:border-0">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 bg-gray-100 rounded overflow-hidden flex-shrink-0">
                                    <img v-if="item.item_image" :src="item.item_image" class="w-full h-full object-cover" />
                                    <div v-else class="w-full h-full flex items-center justify-center text-gray-400 text-xs">No Img</div>
                                </div>
                                <div>
                                    <div class="font-medium">{{ item.item_name || item.item }}</div>
                                    <div class="text-gray-500 text-xs">Qty: {{ item.quantity }}</div>
                                </div>
                            </div>
                            <div class="font-medium">{{ formatCurrency(item.line_item_amount) }}</div>
                        </div>
                    </div>
                    
                    <!-- Details -->
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <h4 class="font-bold text-sm uppercase text-gray-500 mb-1">Status</h4>
                            <div class="text-sm">{{ currentSummaryDoc.order_status }}</div>
                        </div>
                        <div>
                            <h4 class="font-bold text-sm uppercase text-gray-500 mb-1">Date</h4>
                            <div class="text-sm">{{ formatDate(currentSummaryDoc.order_date) }}</div>
                        </div>
                    </div>

                    <!-- Address & Contact -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <h4 class="font-bold text-sm uppercase text-gray-500 mb-1">Delivery Address</h4>
                            <div v-if="currentSummaryAddress" class="text-sm text-gray-600">
                                <div>{{ currentSummaryAddress.address_title }}</div>
                                <div>{{ currentSummaryAddress.address_line1 }}</div>
                                <div>{{ currentSummaryAddress.city }}, {{ currentSummaryAddress.pincode }}</div>
                                <div v-if="currentSummaryAddress.state">{{ currentSummaryAddress.state }}</div>
                            </div>
                            <div v-else class="text-sm text-gray-600">{{ currentSummaryDoc.delivery_address }}</div>
                        </div>
                        <div>
                            <h4 class="font-bold text-sm uppercase text-gray-500 mb-1">Contact</h4>
                            <div v-if="currentSummaryContact" class="text-sm text-gray-600">
                                <div>{{ currentSummaryContact.first_name }} {{ currentSummaryContact.last_name }}</div>
                                <div>{{ currentSummaryContact.mobile_no }}</div>
                                <div v-if="currentSummaryContact.email_id">{{ currentSummaryContact.email_id }}</div>
                            </div>
                            <div v-else class="text-sm text-gray-600">{{ currentSummaryDoc.contact }}</div>
                        </div>
                    </div>

                    <!-- Territory -->
                    <div v-if="currentSummaryAddress && currentSummaryAddress.custom_resolved_territory">
                        <h4 class="font-bold text-sm uppercase text-gray-500 mb-1">Resolved Territory</h4>
                        <div class="text-sm text-gray-600">{{ currentSummaryAddress.custom_resolved_territory }}</div>
                    </div>
                </div>
            
            </div>
            <div class="px-6 py-4 border-t bg-gray-50 flex justify-end">
                <Button @click="showSummaryDialog = false">Close</Button>
            </div>
        </div>
    </div>

    <!-- Timeline Modal -->
    <div v-if="showTimelineDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-lg mx-4 overflow-hidden flex flex-col max-h-[80vh]">
            <div class="px-6 py-4 border-b">
                <h3 class="text-lg font-bold">Timeline: {{ currentTrackingOrder?.name || 'Loading...' }}</h3>
                <div v-if="currentTrackingTerritory" class="text-sm text-gray-500 mt-1">
                    Territory: {{ currentTrackingTerritory }}
                </div>
            </div>
            <div class="p-6 overflow-y-auto">
                <div v-if="timelineLoading" class="py-4 text-center">Loading...</div>
                <div v-else-if="timelineEvents.length === 0" class="py-4 text-gray-500 italic">No events found.</div>
                <div v-else class="mt-4 space-y-4">
                    <div v-for="(event, idx) in timelineEvents" :key="idx" class="border-l-2 border-blue-200 pl-4 pb-4 relative last:pb-0">
                        <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-blue-100 border-2 border-blue-500"></div>
                        <div class="text-xs text-gray-500">{{ formatDate(event.recorded_time) }}</div>
                        <div class="font-medium text-gray-900">{{ event.event_type }}</div>
                        <div class="text-sm text-gray-600 mt-1">
                            <span v-if="event.event_detail">{{ event.event_detail }}</span>
                            <span v-else-if="event.event_type === 'Status Update'">
                                Changed from {{ event.from_value }} to {{ event.to_value }}
                            </span>
                            <span v-else-if="event.event_type === 'Field Change'">
                                <span v-if="event.fieldname === 'channel_partner'">
                                    Changed <b>Channel Partner</b> from {{ event.from_value }} to {{ event.to_value }}
                                </span>
                                <span v-else-if="event.fieldname === 'resolved_territory'">
                                    Changed <b>Resolved Territory</b> from {{ event.from_value }} to {{ event.to_value }}
                                </span>
                                <span v-else-if="event.fieldname === 'service_category'">
                                    Changed <b>Service Category</b> from {{ event.from_value }} to {{ event.to_value }}
                                </span>
                                <span v-else>
                                    {{ event.fieldname }} changed
                                </span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="px-6 py-4 border-t bg-gray-50">
                <div v-if="showCommentInput" class="w-full">
                    <textarea v-model="commentText" class="w-full border rounded p-2 text-sm mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500" rows="3" placeholder="Type your comment here..."></textarea>
                    <div class="flex justify-end gap-2">
                        <Button @click="showCommentInput = false">Cancel</Button>
                        <Button :appearance="'primary'" @click="submitComment" :loading="submittingComment">Submit</Button>
                    </div>
                </div>
                <div v-else class="flex justify-end gap-2">
                    <Button @click="showCommentInput = true">Comment</Button>
                    <Button @click="showTimelineDialog = false">Close</Button>
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
        @success="onCommunicationSuccess"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { Button, frappeRequest, createResource, createListResource, Alert } from 'frappe-ui'
import { useRouter } from 'vue-router'
import Communication from '../components/Communication.vue'
import { useConsumerValidation } from '../composables/useConsumerValidation'
import { useSession } from '../composables/useSession'

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

const session = useSession()

const addresses = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Address',
            fields: ['name', 'address_title', 'address_line1', 'city', 'pincode', 'state', 'country', 'county', 'custom_is_default', 'custom_resolved_territory'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    },
    auto: false
})

const contacts = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        return {
            doctype: 'Contact',
            fields: ['name', 'first_name', 'last_name', 'mobile_no', 'email_id', 'address'],
            filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
        }
    },
    auto: false
})

const orders = createResource({
    url: 'frappe.client.get_list',
    makeParams(values) {
        const addressNames = addresses.data?.map(a => a.name) || []
        return {
            doctype: 'Connect Order',
            fields: ['name', 'order_date', 'order_status', 'user'],
            filters: {
                delivery_address: ['in', addressNames.length ? addressNames : ['']]
            },
            order_by: 'order_date desc'
        }
    },
    auto: false
})

const orderQuantities = reactive({})
const showTimelineDialog = ref(false)
const timelineEvents = ref([])
const timelineLoading = ref(false)
const currentTrackingOrder = ref(null)
const currentTrackingTerritory = ref('')

const showSummaryDialog = ref(false)
const summaryLoading = ref(false)
const currentSummaryDoc = ref(null)
const currentSummaryAddress = ref(null)
const currentSummaryContact = ref(null)

const showCommentInput = ref(false)
const commentText = ref('')
const submittingComment = ref(false)

async function submitComment() {
    if (!commentText.value.trim()) return
    
    submittingComment.value = true
    try {
        await frappeRequest({
            url: 'connect_master.connect_master.doctype.connect_order.connect_order.add_timeline_event',
            params: {
                order_name: currentTrackingOrder.value.name,
                event_type: 'Comment',
                payload: JSON.stringify({ comment: commentText.value })
            }
        })
        
        // Refresh timeline
        await trackOrder(currentTrackingOrder.value)
        
        // Reset UI
        commentText.value = ''
        showCommentInput.value = false
    } catch (e) {
        console.error('Failed to submit comment', e)
    } finally {
        submittingComment.value = false
    }
}

watch(() => orders.data, async (newOrders) => {
    if (newOrders && newOrders.length > 0) {
        // Reset
        Object.keys(orderQuantities).forEach(k => delete orderQuantities[k])

        // Fetch items for each order individually to avoid permission issues with child table
        await Promise.all(newOrders.map(async (order) => {
            try {
                const res = await frappeRequest({
                    url: 'frappe.client.get_value',
                    params: {
                        doctype: 'Connect Order',
                        filters: { name: order.name },
                        fieldname: 'items'
                    }
                })
                const val = res.message || res
                if (val && val.items && Array.isArray(val.items)) {
                    const total = val.items.reduce((sum, item) => sum + (item.quantity || 0), 0)
                    orderQuantities[order.name] = total
                }
            } catch (e) {
                console.error('Failed to fetch items for order', order.name, e)
            }
        }))
    }
})

async function trackOrder(order) {
    currentTrackingOrder.value = order
    currentTrackingTerritory.value = ''
    showTimelineDialog.value = true
    timelineLoading.value = true
    timelineEvents.value = []
    showCommentInput.value = false
    commentText.value = ''
    
    try {
        // Fetch full order doc to get timeline (avoids permission error on child table)
        const res = await frappeRequest({
            url: 'frappe.client.get',
            params: {
                doctype: 'Connect Order',
                name: order.name
            }
        })
        const doc = res.message || res

        if (doc.delivery_address) {
            try {
                const addrRes = await frappeRequest({
                    url: 'frappe.client.get_value',
                    params: {
                        doctype: 'Address',
                        filters: { name: doc.delivery_address },
                        fieldname: 'custom_resolved_territory'
                    }
                })
                const val = addrRes.message || addrRes
                if (val && val.custom_resolved_territory) {
                    currentTrackingTerritory.value = val.custom_resolved_territory
                }
            } catch (e) {
                console.error('Failed to fetch territory', e)
            }
        }

        if (doc && doc.timeline) {
            // Filter and sort timeline
            let events = doc.timeline.filter(e => !e.is_internal)
            // Sort by idx desc (Newest first)
            events.sort((a, b) => b.idx - a.idx)
            timelineEvents.value = events
        }
    } catch (e) {
        console.error(e)
    } finally {
        timelineLoading.value = false
    }
}

async function viewOrderSummary(order) {
    showSummaryDialog.value = true
    summaryLoading.value = true
    currentSummaryDoc.value = null
    currentSummaryAddress.value = null
    currentSummaryContact.value = null
    
    try {
        const res = await frappeRequest({
            url: 'frappe.client.get',
            params: {
                doctype: 'Connect Order',
                name: order.name
            }
        })
        const doc = res.message || res

        if (doc.items && doc.items.length > 0) {
            const itemNames = doc.items.map(i => i.item)
            try {
                const itemsRes = await frappeRequest({
                    url: 'frappe.client.get_list',
                    params: {
                        doctype: 'Connect Item',
                        filters: [['name', 'in', itemNames]],
                        fields: ['name', 'item_name', 'item_image']
                    }
                })
                const itemsDetails = itemsRes.message || itemsRes
                
                doc.items.forEach(lineItem => {
                    const detail = itemsDetails.find(d => d.name === lineItem.item)
                    if (detail) {
                        lineItem.item_name = detail.item_name
                        lineItem.item_image = detail.item_image
                    }
                })
            } catch (e) {
                console.error('Failed to fetch item details', e)
            }
        }

        currentSummaryDoc.value = doc

        if (doc.delivery_address) {
            const addrRes = await frappeRequest({
                url: 'frappe.client.get',
                params: { doctype: 'Address', name: doc.delivery_address }
            })
            currentSummaryAddress.value = addrRes.message || addrRes
        }

        if (doc.contact) {
            const contactRes = await frappeRequest({
                url: 'frappe.client.get',
                params: { doctype: 'Contact', name: doc.contact }
            })
            currentSummaryContact.value = contactRes.message || contactRes
        }
    } catch (e) {
        console.error(e)
    } finally {
        summaryLoading.value = false
    }
}

onMounted(async () => {
    const data = await session.fetch()
    if (data && data !== 'Guest') {
        await addresses.fetch()
        contacts.fetch()
        orders.fetch()
        checkAndPrompt()
    }

})

async function onCommunicationSuccess() {
    await addresses.fetch()
    await contacts.fetch()
    await checkAndPrompt()
}

function startOrdering() {
    window.location.href = '/koda/login'
}

function createOrder() {
    router.push('/order')
}

function manageAddresses() {
    router.push('/manage')
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value || 0)
}

function getStatusClass(status) {
    switch (status) {
        case 'Submitted': return 'bg-blue-100 text-blue-800'
        case 'Accepted': return 'bg-green-100 text-green-800'
        case 'Fulfilled': return 'bg-green-100 text-green-800'
        case 'Cancelled': return 'bg-red-100 text-red-800'
        case 'Rejected': return 'bg-red-100 text-red-800'
        default: return 'bg-gray-100 text-gray-800'
    }
}

//function manageContacts() {
//    router.push('/manage')
//}

</script>
