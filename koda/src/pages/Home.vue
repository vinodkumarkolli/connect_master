<template>
  <div class="max-w-4xl mx-auto py-12 px-4">
    <div v-if="session.loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>

    <div v-else-if="!session.data || session.data === 'Guest'">
      <!-- Step 1: Welcome -->
      <div class="text-center space-y-6 py-20">
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
    </div>

    <div v-else class="space-y-8">
      <!-- Dashboard for Logged In Users -->
      
      <!-- Top Pane: Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left Pane: Manage Actions -->
        <div class="bg-white p-6 rounded-lg shadow border border-gray-100 flex flex-col justify-center">
            <h2 class="text-lg font-semibold text-gray-800 mb-4">Manage</h2>
            <div class="flex flex-wrap gap-4">
                <Button @click="manageAddresses">Manage Addresses & Contacts</Button>
                <!-- <Button @click="manageContacts"> Contacts</Button> -->
            </div>
        </div>

        <!-- Right Pane: Create Order -->
        <div class="bg-white p-6 rounded-lg shadow border border-gray-100 flex flex-col items-center justify-center">
             <Button :appearance="'primary'" size="xl" @click="createOrder" class="w-full md:w-auto">
                Create Order
             </Button>
        </div>
      </div>

      <!-- Bottom Pane: Order History -->
      <div class="bg-white p-6 rounded-lg shadow border border-gray-100 min-h-[400px]">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">Order History</h2>
            <!-- Filters Placeholder -->
            <div class="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded">Filters</div>
        </div>
        
        <!-- Order List Placeholder -->
        <div class="text-center text-gray-500 py-20 border-2 border-dashed border-gray-200 rounded-lg">
            No orders found.
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
import { ref, reactive, onMounted } from 'vue'
import { Button, frappeRequest, createResource } from 'frappe-ui'
import { useRouter } from 'vue-router'
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
            fields: ['name', 'address_title', 'address_line1', 'city', 'pincode', 'state', 'country', 'county', 'custom_is_default'],
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

onMounted(async () => {
    try {
        let res = await frappeRequest({ url: 'frappe.auth.get_logged_user' })
        if (res) {
            session.data = res.message || res
            await addresses.fetch()
            await contacts.fetch()
            
            await checkAndPrompt()
        }
    } catch (e) {
        session.data = null
    } finally {
        session.loading = false
    }
})

async function onCommunicationSuccess() {
    await addresses.fetch()
    await contacts.fetch()
    await checkAndPrompt()
}

function startOrdering() {
    window.location.href = '/login?redirect-to=/koda/order'
}

function createOrder() {
    router.push('/order')
}

function manageAddresses() {
    router.push('/manage')
}

//function manageContacts() {
//    router.push('/manage')
//}
</script>
