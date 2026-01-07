<template>
  <div class="bg-white rounded-lg shadow border flex flex-col h-full">
    <div class="p-4 border-b bg-gray-50 flex justify-between items-center">
      <div>
        <h2 class="text-lg font-bold text-gray-800">Recent Orders</h2>
        <p class="text-xs text-gray-500">View and track all connect orders</p>
      </div>
      <div class="w-64">
        <Input v-model="orderSearch" placeholder="Search Orders..." />
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
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, Input, LoadingIndicator, createListResource } from 'frappe-ui'

const orderSearch = ref('')

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
</script>
