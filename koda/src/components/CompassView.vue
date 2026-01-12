<template>
  <div class="bg-white rounded-lg shadow border flex flex-col h-full relative overflow-hidden">
    <!-- Header -->
    <div class="p-4 border-b bg-gray-50 flex flex-col gap-4 flex-shrink-0">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 md:gap-0">
        <div>
          <h2 class="text-lg font-bold text-gray-800">Connect Orders</h2>
          <p class="text-xs text-gray-500">Manage and track orders</p>
        </div>
        <div class="flex items-center gap-2 flex-wrap w-full md:w-auto">
            <!-- View Selector -->
            <div class="flex bg-gray-200 rounded p-1">
                <button @click="currentView = 'List'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', currentView === 'List' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">List</button>
                <button @click="currentView = 'Kanban'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', currentView === 'Kanban' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">Kanban</button>
                <button @click="currentView = 'Summary'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', currentView === 'Summary' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">Summary</button>
            </div>
            <Button @click="showFilters = !showFilters" :variant="hasActiveFilters ? 'solid' : 'outline'" size="sm">
                <template #prefix>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                </template>
                Filters {{ hasActiveFilters ? '(Active)' : '' }}
            </Button>
            <Button v-if="isSystemManager" @click="rebuildTree" :loading="treeRebuildResource.loading" variant="subtle" size="sm">
                Rebuild Tree
            </Button>
        </div>
      </div>
      
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <!-- Tabs -->
          <div class="flex gap-6 border-b border-transparent w-full md:w-auto overflow-x-auto">
              <button
                v-for="tab in tabs"
                :key="tab"
                @click="activeTab = tab; orders.reload()"
                :class="['pb-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2', activeTab === tab ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700']"
              >
                {{ tab }}
                <span v-if="orderCounts.data && orderCounts.data[tab] > 0" :class="['px-1.5 py-0.5 rounded-full text-xs', activeTab === tab ? 'bg-blue-100 text-blue-600' : 'bg-gray-200 text-gray-600']">
                    {{ orderCounts.data[tab] }}
                </span>
              </button>
          </div>
          
          <!-- Search -->
          <div class="w-full md:w-64">
            <Input v-model="searchQuery" placeholder="Search Orders..." @keyup.enter="orders.reload(); orderCounts.reload()" />
          </div>
      </div>
    </div>

    <!-- Main Content -->
    <div :class="['flex-1 p-0 relative bg-gray-50', currentView === 'Kanban' ? 'overflow-hidden' : 'overflow-y-auto']">
      <div v-if="orders.loading" class="flex justify-center p-12">
        <LoadingIndicator />
      </div>
      <div v-else-if="orders.error" class="p-12 text-center text-red-500">
        {{ orders.error.message || 'Error loading orders' }}
        <div class="mt-2">
            <Button size="sm" @click="orders.reload()">Retry</Button>
        </div>
      </div>
      <div v-else-if="!orders.data || orders.data.length === 0" class="p-12 text-center text-gray-500">
        <span v-if="activeTab === 'History'">There are no orders in your Inbox</span>
        <span v-else>No orders found.</span>
      </div>
      <div v-else class="h-full">
          <!-- List View -->
          <div v-if="currentView === 'List'" class="bg-white min-h-full">
             <div class="divide-y">
                 <div v-for="order in orders.data" :key="order.name" class="p-4 hover:bg-gray-50 transition-colors cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between group gap-4 sm:gap-0">
                    <div class="flex items-start gap-4 w-full sm:w-auto">
                        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-lg">
                            📦
                        </div>
                        <div>
                            <div class="flex items-center gap-2 mb-1">
                                <span class="font-medium text-gray-900">{{ order.name }}</span>
                                <span :class="['px-2 py-0.5 rounded-full text-xs font-medium', getOrderStatusClasses(order.order_status)]">
                                    {{ order.order_status }}
                                </span>
                            </div>
                            <div class="text-sm text-gray-600">
                                {{ order.address_title }} • {{ order.custom_resolved_territory }}
                            </div>
                            <div class="text-xs text-gray-500 mt-1">
                                {{ order.user }} • {{ getDaysAgo(order.order_date) }}
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-4 w-full sm:w-auto justify-between sm:justify-end">
                        <div class="text-left sm:text-right">
                            <div class="text-sm font-medium text-gray-700">{{ getChannelName(order.service_category) }}</div>
                            <div class="text-xs text-gray-500 mt-1" v-if="order.channel_partner">{{ getPartnerName(order.channel_partner) }}</div>
                        </div>
                        <button @click.stop="toggleMenu(order.name)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                        </button>
                    </div>
                 </div>
             </div>
          </div>
          
          <!-- Kanban View -->
          <div v-else-if="currentView === 'Kanban'" class="flex h-full overflow-x-auto p-4 gap-4 items-start relative">
              <div v-if="activeKanbanMenu" class="fixed inset-0 z-0" @click="activeKanbanMenu = null"></div>
              <div v-for="status in kanbanStatuses" :key="status" class="w-72 flex-shrink-0 flex flex-col bg-gray-100 rounded-lg max-h-full z-10">
                  <div class="p-3 font-bold text-gray-700 text-sm uppercase flex justify-between items-center">
                      <div class="flex items-center gap-2">
                          {{ status }}
                          <span class="bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full text-xs">{{ getOrdersByStatus(status).length }}</span>
                      </div>
                      <div class="relative">
                          <button @click.stop="toggleKanbanMenu(status)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-200">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                          </button>
                          <div v-if="activeKanbanMenu === status" class="absolute right-0 top-full mt-1 w-40 bg-white rounded-md shadow-lg border z-20 py-1">
                              <button @click="downloadKanbanCsv(status); activeKanbanMenu = null" class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                                  Download CSV
                              </button>
                          </div>
                      </div>
                  </div>
                  <div class="p-2 space-y-2 overflow-y-auto flex-1">
                      <div v-for="order in getOrdersByStatus(status)" :key="order.name" class="bg-white p-3 rounded shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
                          <div class="flex justify-between items-start mb-2">
                              <span class="font-medium text-sm text-gray-900">{{ order.name }}</span>
                              <span class="text-xs text-gray-400">{{ formatDateShort(order.order_date) }}</span>
                          </div>
                          <div class="text-xs text-gray-600 mb-2 line-clamp-2">{{ order.address_title }}</div>
                          <div class="text-xs text-gray-400 mb-2 truncate" v-if="order.channel_partner">
                              {{ getPartnerName(order.channel_partner) }}
                          </div>
                          <div class="flex justify-between items-center mt-2 pt-2 border-t border-gray-100">
                              <span class="text-xs font-medium text-blue-600">{{ getChannelName(order.service_category) }}</span>
                              <div class="flex items-center gap-2">
                                  <div class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-xs" :title="order.user">
                                      {{ order.user ? order.user[0].toUpperCase() : '?' }}
                                  </div>
                                  <button @click.stop="toggleMenu(order.name)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                                  </button>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
          
          <!-- Summary View -->
          <div v-else-if="currentView === 'Summary'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-4">
              <div v-for="order in orders.data" :key="order.name" class="bg-white p-4 rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer flex flex-col">
                  <div class="flex justify-between items-start mb-3">
                      <div>
                          <div class="font-bold text-gray-900">{{ order.name }}</div>
                          <div class="text-xs text-gray-500">{{ formatDate(order.order_date) }}</div>
                      </div>
                      <span :class="['px-2 py-1 rounded text-xs font-medium', getOrderStatusClasses(order.order_status)]">
                          {{ order.order_status }}
                      </span>
                  </div>
                  
                  <div class="flex-1 space-y-2 mb-4">
                      <div class="flex items-start gap-2 text-sm">
                          <span class="text-gray-400 w-4">📍</span>
                          <span class="text-gray-700 line-clamp-2">{{ order.address_title }}</span>
                      </div>
                      <div class="flex items-center gap-2 text-sm">
                          <span class="text-gray-400 w-4">🏷️</span>
                          <span class="text-gray-700">{{ getChannelName(order.service_category) }}</span>
                      </div>
                      <div class="flex items-center gap-2 text-sm" v-if="order.channel_partner">
                          <span class="text-gray-400 w-4">🤝</span>
                          <span class="text-gray-700 truncate">{{ getPartnerName(order.channel_partner) }}</span>
                      </div>
                  </div>
                  
                  <div class="pt-3 border-t flex justify-between items-center">
                      <div class="text-xs text-gray-500">
                          {{ order.custom_resolved_territory }}
                      </div>
                      <div class="flex items-center gap-2">
                          <div class="text-xs font-medium text-blue-600">
                              {{ order.user }}
                          </div>
                          <button @click.stop="toggleMenu(order.name)" class="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>
                          </button>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    </div>
    
    <!-- Action Menu Modal -->
    <div v-if="activeMenuOrderId && activeOrder" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
        <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity" @click="closeMenu"></div>
        
        <div class="relative bg-white rounded-xl shadow-xl max-w-3xl w-full overflow-hidden flex flex-col max-h-[90vh]">
            <!-- Modal Header -->
            <div class="px-6 py-4 border-b flex flex-col sm:flex-row justify-between items-start bg-gray-50 gap-4 sm:gap-0">
                <div class="w-full sm:w-auto">
                    <div class="flex items-center gap-3 mb-1 flex-wrap">
                        <h3 class="text-lg font-bold text-gray-900">{{ activeOrder.name }}</h3>
                        <span :class="['px-2.5 py-0.5 rounded-full text-xs font-medium', getOrderStatusClasses(activeOrder.order_status)]">
                            {{ activeOrder.order_status }}
                        </span>
                        <span v-if="activeOrder.unresolved_push === 1" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            Unresolved
                        </span>
                    </div>
                    <div class="flex items-center gap-4 text-sm text-gray-500">
                        <div class="flex items-center gap-1.5">
                            <span class="text-gray-400">📅</span> {{ formatDate(activeOrder.order_date) }}
                        </div>
                        <div class="flex items-center gap-1.5">
                            <span class="text-gray-400">👤</span> {{ activeOrder.user }}
                        </div>
                    </div>
                </div>
                <div class="flex items-center gap-3 w-full sm:w-auto justify-end">
                    <Button variant="subtle" size="sm" @click="openCommentForm">
                        <template #prefix>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                        </template>
                        Add Comment
                    </Button>
                    <button @click="closeMenu" class="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-200 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Modal Body -->
            <div class="flex flex-col md:flex-row flex-1 overflow-hidden min-h-[400px]">
                <!-- Pane 1: Order Summary -->
                <div class="w-full md:w-1/2 p-6 pb-10 border-b md:border-b-0 md:border-r overflow-y-auto bg-white">
                    <h4 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Order Summary</h4>
                    
                    <div class="space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-medium text-gray-500 mb-1">Delivery Address</label>
                                <div class="text-sm text-gray-900 font-medium">{{ activeOrder.address_title }}</div>
                                <div class="text-sm text-gray-700 mt-1">
                                    {{ activeOrder.address_line1 }}<br>
                                    {{ activeOrder.city }}<span v-if="activeOrder.pincode"> - {{ activeOrder.pincode }}</span>
                                </div>
                                <div class="mt-2 pt-2 border-t border-gray-100">
                                    <label class="block text-xs font-medium text-gray-500 mb-1">Resolved Territory</label>
                                    <div class="text-sm font-medium text-gray-900 break-words mb-2">{{ activeOrder.custom_resolved_territory || 'N/A' }}</div>
                                    <div v-if="isTerritoryAdmin" class="flex gap-2">
                                        <button @click="openChangeTerritoryDialog" class="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded hover:bg-blue-100 font-medium transition-colors">Change</button>
                                        <button v-if="canRelease" @click="showReleaseDialog = true" class="text-xs bg-red-50 text-red-600 px-2 py-1 rounded hover:bg-red-100 font-medium transition-colors">Release</button>
                                    </div>
                                </div>
                            </div>

                            <div v-if="activeOrder.first_name">
                                <label class="block text-xs font-medium text-gray-500 mb-1">Contact Person</label>
                                <div class="text-sm text-gray-900 font-medium">{{ activeOrder.first_name }} {{ activeOrder.last_name }}</div>
                                <div class="text-sm text-gray-700 mt-1 flex items-center gap-2" v-if="activeOrder.mobile_no">
                                    <span class="text-gray-400 text-xs">📱</span> {{ activeOrder.mobile_no }}
                                </div>
                                <div class="text-sm text-gray-700 flex items-center gap-2" v-if="activeOrder.email_id">
                                    <span class="text-gray-400 text-xs">✉️</span> {{ activeOrder.email_id }}
                                </div>
                            </div>
                        </div>
    
                            <div v-if="orderDetails.data && orderDetails.data.items && orderDetails.data.items.length > 0">
                                <label class="block text-xs font-medium text-gray-500 mb-2">Items</label>
                                <div class="border rounded-lg overflow-hidden">
                                    <table class="w-full text-xs">
                                        <thead class="bg-gray-50 border-b">
                                            <tr>
                                                <th class="px-3 py-2 text-left font-medium text-gray-500">Item</th>
                                                <th class="px-3 py-2 text-right font-medium text-gray-500">Qty</th>
                                                <th class="px-3 py-2 text-right font-medium text-gray-500">Amt</th>
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y">
                                            <tr v-for="(item, idx) in orderDetails.data.items" :key="idx" class="bg-white">
                                                <td class="px-3 py-2 text-gray-900">{{ item.item }}</td>
                                                <td class="px-3 py-2 text-right text-gray-600">{{ item.quantity }}</td>
                                                <td class="px-3 py-2 text-right text-gray-600">{{ item.line_item_amount }}</td>
                                            </tr>
                                        </tbody>
                                        <tfoot class="bg-gray-50 border-t">
                                            <tr>
                                                <td colspan="2" class="px-3 py-2 font-bold text-gray-700 text-right">Total</td>
                                                <td class="px-3 py-2 font-bold text-gray-900 text-right">{{ orderTotal }}</td>
                                            </tr>
                                        </tfoot>
                                    </table>
                                </div>
                            </div>
                            <div v-else-if="orderDetails.loading" class="text-xs text-gray-500 italic">
                                Loading items...
                            </div>
    
                            <div>
                                <label class="block text-xs font-medium text-gray-500 mb-1">Service Category</label>
                                <div class="text-sm text-gray-900 mb-2">{{ getChannelName(activeOrder.service_category) }}</div>
                                <div v-if="isTerritoryAdmin" class="flex gap-2">
                                    <button @click="openChangeCategoryDialog" class="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded hover:bg-blue-100 font-medium transition-colors">Change</button>
                                </div>
                            </div>

                        <div v-if="activeOrder.channel_partner">
                            <label class="block text-xs font-medium text-gray-500 mb-1">Channel Partner</label>
                            <div class="text-sm text-gray-900">{{ getPartnerName(activeOrder.channel_partner) }}</div>
                        </div>
                    </div>
                </div>

                <!-- Pane 2: Action Center / Timeline -->
                <div class="w-full md:w-1/2 p-6 pb-10 bg-gray-50 custom-scrollbar">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-sm font-bold text-gray-900 uppercase tracking-wider" v-if="activePane === 'Action Center'">Action Center</h4>
                        <h4 class="text-sm font-bold text-gray-900 uppercase tracking-wider" v-else>Timeline</h4>
                        
                        <div class="flex bg-gray-200 rounded p-0.5" v-if="activeTab !== 'History'">
                             <button @click="activePane = 'Timeline'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', activePane === 'Timeline' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">Timeline</button>
                             <button @click="activePane = 'Action Center'" :class="['px-3 py-1 rounded text-xs font-medium transition-all', activePane === 'Action Center' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-800']">Action Center</button>
                        </div>
                    </div>

                    <div v-if="activePane === 'Action Center'">
                        <div v-if="currentAction" class="bg-white p-4 rounded-lg border shadow-sm">
                            <div class="flex items-center gap-2 mb-3">
                                <button @click="cancelAction" class="text-gray-400 hover:text-gray-600">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                                </button>
                                <h5 class="font-bold text-gray-800">{{ currentAction === 'Cancel Order' ? 'Cancellation Notes' : currentAction }}</h5>
                            </div>
                            
                            <div v-if="currentAction === 'Add Comment'" class="space-y-3">
                                <textarea
                                    v-model="commentText"
                                    class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                    rows="4"
                                    placeholder="Write your comment here..."
                                ></textarea>
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center gap-2">
                                        <input type="checkbox" v-model="makePublic" id="make_public" class="rounded text-blue-600 focus:ring-blue-500">
                                        <label for="make_public" class="text-sm text-gray-700 select-none">Make Public</label>
                                    </div>
                                    <div class="flex gap-2">
                                        <Button variant="subtle" size="sm" @click="cancelAction">Cancel</Button>
                                        <Button variant="solid" size="sm" @click="submitComment" :loading="submittingComment">Submit</Button>
                                    </div>
                                </div>
                            </div>
                            <div v-else-if="['Select Channel Partner', 'Change Channel Partner'].includes(currentAction)" class="space-y-3">
                                <div v-if="channelPartners.loading" class="flex justify-center py-8">
                                    <LoadingIndicator />
                                </div>
                                <div v-else-if="channelPartners.data && channelPartners.data.length > 0" class="space-y-2 max-h-[400px] overflow-y-auto">
                                    <div
                                        v-for="partner in channelPartners.data"
                                        :key="partner.name"
                                        class="border p-3 rounded-lg cursor-pointer hover:border-blue-500 transition-colors"
                                        :class="{'ring-2 ring-blue-500 bg-blue-50': selectedChannelPartner === partner.name}"
                                        @click="selectedChannelPartner = partner.name"
                                    >
                                        <div class="font-medium text-sm text-gray-900">{{ partner.partner_name }}</div>
                                        <div class="text-gray-600 text-xs mt-1" v-if="partner.description">{{ partner.description }}</div>
                                        <div class="text-gray-500 text-xs mt-2" v-if="partner.address_html" v-html="partner.address_html"></div>
                                        <div class="text-gray-500 text-xs mt-1" v-if="partner.contact_html" v-html="partner.contact_html"></div>
                                    </div>
                                </div>
                                <div v-else class="text-center py-8 text-gray-500">
                                    No Channel Partners found for this area.
                                </div>
                                
                                <div class="flex justify-end gap-2 pt-2 border-t">
                                    <Button variant="subtle" size="sm" @click="cancelAction">Cancel</Button>
                                    <Button variant="solid" size="sm" @click="submitChannelPartner" :loading="assigningPartner" :disabled="!selectedChannelPartner">
                                        {{ currentAction === 'Change Channel Partner' ? 'Change' : 'Assign' }} Partner
                                    </Button>
                                </div>
                            </div>
                            <div v-else-if="currentAction === 'Mark Delivered'" class="space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-gray-500 mb-1">Delivery Date</label>
                                    <Input type="date" v-model="deliveryDate" />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-gray-500 mb-1">Delivery Notes</label>
                                    <textarea
                                        v-model="deliveryNotes"
                                        class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        rows="3"
                                        placeholder="Enter delivery notes..."
                                    ></textarea>
                                </div>
                                <div class="flex justify-end gap-2 pt-2 border-t">
                                    <Button variant="subtle" size="sm" @click="cancelAction">Cancel</Button>
                                    <Button variant="solid" size="sm" @click="submitDelivery" :loading="submittingDelivery" :disabled="!deliveryDate || !deliveryNotes">Submit</Button>
                                </div>
                            </div>
                            <div v-else-if="currentAction === 'Accept Order'" class="space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-gray-500 mb-1">Notes</label>
                                    <textarea
                                        v-model="acceptanceNotes"
                                        class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        rows="3"
                                        placeholder="Enter acceptance notes..."
                                    ></textarea>
                                </div>
                                <div class="flex justify-end gap-2 pt-2 border-t">
                                    <Button variant="subtle" size="sm" @click="cancelAction">Cancel</Button>
                                    <Button variant="solid" size="sm" @click="submitAcceptance" :loading="acceptingOrder" :disabled="!acceptanceNotes">Accept Order</Button>
                                </div>
                            </div>
                            <div v-else-if="currentAction === 'Reject Order'" class="space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-gray-500 mb-1">Notes</label>
                                    <textarea
                                        v-model="rejectionNotes"
                                        class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        rows="3"
                                        placeholder="Enter rejection notes..."
                                    ></textarea>
                                </div>
                                <div class="flex justify-end gap-2 pt-2 border-t">
                                    <Button variant="subtle" size="sm" @click="cancelAction">Cancel</Button>
                                    <Button variant="solid" theme="red" size="sm" @click="submitRejection" :loading="rejectingOrder" :disabled="!rejectionNotes">Reject Order</Button>
                                </div>
                            </div>
                            <div v-else-if="currentAction === 'Cancel Order'" class="space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-gray-500 mb-1">Notes</label>
                                    <textarea
                                        v-model="cancellationNotes"
                                        class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                                        rows="3"
                                        placeholder="Enter cancellation notes..."
                                    ></textarea>
                                </div>
                                <div class="flex justify-end gap-2 pt-2 border-t">
                                    <Button variant="subtle" size="sm" @click="cancelAction">Cancel</Button>
                                    <Button variant="solid" theme="red" size="sm" @click="submitCancellation" :loading="cancellingOrder" :disabled="!cancellationNotes">Cancel Order</Button>
                                </div>
                            </div>
                            <div v-else>
                                <p class="text-sm text-gray-500 italic">Form for {{ currentAction }} is under construction.</p>
                            </div>
                        </div>
                        <div v-else-if="menuActions.length > 0" class="grid grid-cols-1 gap-3">
                            <button v-for="action in menuActions"
                                    :key="action"
                                    class="flex items-center justify-between w-full px-4 py-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md hover:border-blue-300 hover:bg-blue-50 transition-all group text-left"
                                    @click="handleAction(action)">
                                <span class="font-medium text-gray-700 group-hover:text-blue-700">{{ action }}</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 group-hover:text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                                </svg>
                            </button>
                        </div>
                        <div v-else class="text-center py-8 text-gray-500">
                            <p>No actions available for this order.</p>
                        </div>
                    </div>
                    
                    <div v-else-if="activePane === 'Timeline'">
                        <div v-if="orderDetails.data && orderDetails.data.timeline && orderDetails.data.timeline.length > 0" class="space-y-4">
                            <div v-for="(event, idx) in orderDetails.data.timeline" :key="idx" class="flex gap-3">
                                <div class="flex flex-col items-center">
                                    <div class="w-2 h-2 rounded-full bg-gray-300 mt-1.5"></div>
                                    <div class="w-0.5 flex-1 bg-gray-200 my-1" v-if="idx !== orderDetails.data.timeline.length - 1"></div>
                                </div>
                                <div class="pb-4">
                                    <div class="text-sm font-medium text-gray-900 flex items-center gap-2">
                                        {{ event.event_type }}
                                        <span v-if="event.is_internal" class="bg-gray-100 text-gray-600 text-xs px-1.5 py-0.5 rounded border border-gray-200">Internal</span>
                                        <span v-else class="bg-blue-100 text-blue-600 text-xs px-1.5 py-0.5 rounded border border-blue-200">Public</span>
                                    </div>
                                    <div class="text-xs text-gray-500">{{ formatDate(event.recorded_time) }} • {{ event.created_by }}</div>
                                    <div class="text-sm text-gray-700 mt-1" v-if="event.event_detail">{{ event.event_detail }}</div>
                                    <div v-if="isTerritoryAdmin && event.event_type === 'Comment'" class="mt-1">
                                        <button @click="toggleVisibility(event.name)" class="text-xs text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1" :disabled="togglingEventId === event.name">
                                            <span v-if="togglingEventId === event.name">Updating...</span>
                                            <span v-else>{{ event.is_internal ? 'Make Public' : 'Make Internal' }}</span>
                                        </button>
                                    </div>
                                    <div class="text-sm text-gray-700 mt-1" v-if="event.event_type === 'Field Change'">
                                        <span v-if="event.fieldname === 'resolved_territory'">
                                            Changed <b>Resolved Territory</b> from <span class="bg-red-50 text-red-600 px-1 rounded">{{ event.from_value || 'Empty' }}</span> to <span class="bg-green-50 text-green-600 px-1 rounded">{{ event.to_value || 'Empty' }}</span>
                                        </span>
                                        <span v-else-if="event.fieldname === 'service_category'">
                                            Changed <b>Service Category</b> from <span class="bg-red-50 text-red-600 px-1 rounded">{{ event.from_value || 'Empty' }}</span> to <span class="bg-green-50 text-green-600 px-1 rounded">{{ event.to_value || 'Empty' }}</span>
                                        </span>
                                        <span v-else-if="event.fieldname === 'channel_partner'">
                                            Changed <b>Channel Partner</b> from <span class="bg-red-50 text-red-600 px-1 rounded">{{ event.from_value || 'Empty' }}</span> to <span class="bg-green-50 text-green-600 px-1 rounded">{{ event.to_value || 'Empty' }}</span>
                                        </span>
                                        <span v-else>
                                            Changed <b>{{ event.fieldname }}</b> from <span class="bg-red-50 text-red-600 px-1 rounded">{{ event.from_value || 'Empty' }}</span> to <span class="bg-green-50 text-green-600 px-1 rounded">{{ event.to_value || 'Empty' }}</span>
                                        </span>
                                    </div>
                                    <div class="text-sm text-gray-700 mt-1" v-else-if="event.event_type === 'Status Update'">
                                        Order Status changed from <span class="bg-red-50 text-red-600 px-1 rounded">{{ event.from_value || 'Empty' }}</span> to <span class="bg-green-50 text-green-600 px-1 rounded">{{ event.to_value || 'Empty' }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else class="text-center py-8 text-gray-500">
                            No timeline events found.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Dialog v-model="showReleaseDialog">
        <template #body-title>
            <h3 class="text-lg font-bold">Release Territory</h3>
        </template>
        <template #body-content>
            <p class="text-gray-600">It will release the order from the current territory, its associated channel partner and move it to the parent territory and order may not be visible to you in future.</p>
        </template>
        <template #actions>
            <Button variant="subtle" @click="showReleaseDialog = false">Cancel</Button>
            <Button variant="solid" theme="red" @click="releaseTerritory" :loading="releasing">Confirm Release</Button>
        </template>
    </Dialog>

    <Dialog v-model="showChangeTerritoryDialog">
        <template #body-title>
            <h3 class="text-lg font-bold">Change Territory</h3>
        </template>
        <template #body-content>
            <div class="mt-2">
                <label class="block text-xs font-medium text-gray-500 mb-1">Select New Territory</label>
                <Autocomplete
                    v-model="editingTerritoryValue"
                    :options="territoryOptions"
                    placeholder="Select Territory"
                />
            </div>
        </template>
        <template #actions>
            <Button variant="subtle" @click="showChangeTerritoryDialog = false">Cancel</Button>
            <Button variant="solid" @click="saveTerritory" :loading="savingTerritory">Update</Button>
        </template>
    </Dialog>

    <Dialog v-model="showChangeCategoryDialog">
        <template #body-title>
            <h3 class="text-lg font-bold">Change Service Category</h3>
        </template>
        <template #body-content>
            <div class="mt-2">
                <label class="block text-xs font-medium text-gray-500 mb-1">Select New Category</label>
                <select v-model="editingCategoryValue" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white">
                    <option v-for="opt in serviceChannels.data" :key="opt.name" :value="opt.name">{{ opt.channel_name }}</option>
                </select>
            </div>
        </template>
        <template #actions>
            <Button variant="subtle" @click="showChangeCategoryDialog = false">Cancel</Button>
            <Button variant="solid" @click="saveCategory" :loading="savingCategory">Update</Button>
        </template>
    </Dialog>

    <!-- Overlay for filters -->
    <div v-if="showFilters" class="absolute inset-0 bg-black bg-opacity-20 z-10" @click="showFilters = false"></div>

    <!-- Filter Sidebar -->
    <div v-if="showFilters" class="absolute inset-y-0 right-0 w-80 bg-white shadow-2xl border-l z-20 flex flex-col transform transition-transform duration-300 ease-in-out">
        <div class="p-4 border-b flex justify-between items-center bg-gray-50">
            <h3 class="font-bold text-gray-800">Filters</h3>
            <button @click="showFilters = false" class="text-gray-500 hover:text-gray-700 text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-5 space-y-6">
            <!-- Filter Fields -->
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Service Category</label>
                <select v-model="filters.custom_address_category" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white">
                    <option value="">All Categories</option>
                    <option v-for="opt in serviceChannels.data" :key="opt.name" :value="opt.name">{{ opt.channel_name }}</option>
                </select>
            </div>
            
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Territory</label>
                <div class="relative">
                    <Autocomplete
                        v-model="filters.custom_resolved_territory"
                        :options="territoryOptions"
                        placeholder="Select Territory"
                    />
                </div>
                <div v-if="filters.custom_resolved_territory" class="mt-3 flex items-center gap-2 bg-blue-50 p-2 rounded border border-blue-100">
                    <input type="checkbox" v-model="filters.include_child_territories" id="inc_child" class="rounded text-blue-600 focus:ring-blue-500" />
                    <label for="inc_child" class="text-sm text-blue-800 cursor-pointer select-none">Include Child Territories</label>
                </div>
            </div>
            
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Channel Partner</label>
                <div class="relative">
                    <Autocomplete
                        v-model="tempSelectedPartner"
                        :options="partnerOptions"
                        placeholder="Select Partners"
                    />
                </div>
                <div class="flex flex-wrap gap-2 mt-2" v-if="filters.channel_partner && filters.channel_partner.length > 0">
                    <div v-for="pVal in filters.channel_partner" :key="pVal" class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full flex items-center gap-1">
                        {{ getPartnerName(pVal) }}
                        <button @click="removePartnerFilter(pVal)" class="hover:text-blue-900 font-bold">&times;</button>
                    </div>
                </div>
            </div>
            
            <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Order Status</label>
                <select v-model="filters.order_status" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white">
                    <option value="">All Statuses</option>
                    <option v-for="status in availableStatuses" :key="status" :value="status">{{ status }}</option>
                </select>
            </div>
        </div>
        <div class="p-4 border-t bg-gray-50 flex gap-3">
            <Button class="flex-1" variant="subtle" @click="clearFilters">Clear All</Button>
            <Button class="flex-1" appearance="primary" @click="applyFilters">Apply Filters</Button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue'
import { Button, Input, LoadingIndicator, createResource, createListResource, Autocomplete, Dialog, frappeRequest } from 'frappe-ui'

const tabs = ['Active', 'Unresolved', 'History']
const activeTab = ref('Active')
const initialTabSet = ref(false)
const currentView = ref('List')
const showFilters = ref(false)
const searchQuery = ref('')


const isTerritoryAdmin = computed(() => {
    return userInfo.data?.roles?.includes('Territory Admin')
})

const activeKanbanMenu = ref(null)
const activeMenuOrderId = ref(null)
const activePane = ref('Action Center')
const currentAction = ref(null)
const commentText = ref('')
const makePublic = ref(false)
const submittingComment = ref(false)

const activeOrder = computed(() => {
    if (!activeMenuOrderId.value || !orders.data) return null
    return orders.data.find(o => o.name === activeMenuOrderId.value)
})

const orderDetails = createResource({
    url: 'frappe.client.get',
    makeParams() {
        return {
            doctype: 'Connect Order',
            name: activeMenuOrderId.value
        }
    }
})

const orderTotal = computed(() => {
    if (!orderDetails.data || !orderDetails.data.items) return 0
    return orderDetails.data.items.reduce((sum, item) => sum + (item.line_item_amount || 0), 0)
})

watch(activeMenuOrderId, (newId) => {
    if (newId) {
        orderDetails.fetch()
    }
})

const menuActions = computed(() => {
    let actions = []
    if (isTerritoryAdmin.value) {
        if (activeTab.value === 'Active') actions = ['Action 21', 'Action 22', 'Action 23']
        else if (activeTab.value === 'Unresolved') actions = ['Action 24', 'Action 25']
    } else {
        if (activeTab.value === 'Active') actions = ['Action 1', 'Action 2', 'Action 3']
        else if (activeTab.value === 'Unresolved') actions = ['Action 4', 'Action 5']
    }

    if (activeOrder.value) {
        if (activeOrder.value.order_status === 'Submitted' ||
           (activeOrder.value.order_status === 'Rejected' && !activeOrder.value.channel_partner)) {
            actions = ['Select Channel Partner']
        } else {
            if (['Assigned', 'Accepted'].includes(activeOrder.value.order_status)) {
                actions = []
            }

            if (isTerritoryAdmin.value &&
                    ['Assigned', 'Accepted', 'Rejected'].includes(activeOrder.value.order_status) &&
                    activeOrder.value.channel_partner) {
                actions.push('Change Channel Partner')
            }
        }

        const status = activeOrder.value.order_status
        const hasPartner = !!activeOrder.value.channel_partner
        
        if (hasPartner) {
             let canMarkDelivered = false
             if (isTerritoryAdmin.value && ['Assigned', 'Accepted'].includes(status)) {
                 canMarkDelivered = true
             }
             if (isPartnerAdmin.value && status === 'Accepted') {
                 canMarkDelivered = true
             }
             
             if (canMarkDelivered) {
                 actions.push('Mark Delivered')
             }
        }

        if (isPartnerAdmin.value &&
            activeOrder.value.order_status === 'Assigned' &&
            activeOrder.value.channel_partner) {
            actions.push('Accept Order')
        }

        if (isPartnerAdmin.value &&
            ['Assigned', 'Accepted'].includes(activeOrder.value.order_status) &&
            activeOrder.value.channel_partner) {
            actions.push('Reject Order')
        }

        if (isTerritoryAdmin.value && ['Assigned', 'Accepted', 'Rejected'].includes(activeOrder.value.order_status)) {
            actions.push('Cancel Order')
        }
    }
    return actions
})

function toggleMenu(orderId) {
    activeMenuOrderId.value = orderId
    currentAction.value = null
    commentText.value = ''
    makePublic.value = false
    if (activeTab.value === 'History' || menuActions.value.length === 0) {
        activePane.value = 'Timeline'
    } else {
        activePane.value = 'Action Center'
    }
}

function closeMenu() {
    activeMenuOrderId.value = null
    currentAction.value = null
}

function openCommentForm() {
    activePane.value = 'Action Center'
    currentAction.value = 'Add Comment'
}

function cancelAction() {
    currentAction.value = null
    if (activeTab.value === 'History') {
        activePane.value = 'Timeline'
    }
}

function handleAction(action) {
    currentAction.value = action
    if (['Select Channel Partner', 'Change Channel Partner'].includes(action)) {
        fetchChannelPartners()
    }
    if (action === 'Mark Delivered') {
        deliveryDate.value = new Date().toISOString().split('T')[0]
        deliveryNotes.value = ''
    }
    if (action === 'Accept Order') {
        acceptanceNotes.value = ''
    }
    if (action === 'Reject Order') {
        rejectionNotes.value = ''
    }
    if (action === 'Cancel Order') {
        cancellationNotes.value = ''
    }
}

const deliveryDate = ref('')
const deliveryNotes = ref('')
const submittingDelivery = ref(false)
const acceptanceNotes = ref('')
const acceptingOrder = ref(false)
const rejectionNotes = ref('')
const rejectingOrder = ref(false)
const cancellationNotes = ref('')
const cancellingOrder = ref(false)

const markDeliveredResource = createResource({
    url: 'connect_master.api.mark_order_delivered'
})

const acceptOrderResource = createResource({
    url: 'connect_master.api.accept_order'
})

const rejectOrderResource = createResource({
    url: 'connect_master.api.reject_order'
})

const cancelOrderResource = createResource({
    url: 'connect_master.api.cancel_order'
})

function submitRejection() {
    rejectingOrder.value = true
    rejectOrderResource.submit({
        order_name: activeOrder.value.name,
        notes: rejectionNotes.value
    }, {
        onSuccess: () => {
            rejectingOrder.value = false
            currentAction.value = null
            orders.reload()
            orderCounts.reload()
            orderDetails.fetch()
            activePane.value = 'Timeline'
        },
        onError: () => {
            rejectingOrder.value = false
        }
    })
}

function submitAcceptance() {
    acceptingOrder.value = true
    acceptOrderResource.submit({
        order_name: activeOrder.value.name,
        notes: acceptanceNotes.value
    }, {
        onSuccess: () => {
            acceptingOrder.value = false
            currentAction.value = null
            orders.reload()
            orderCounts.reload()
            orderDetails.fetch()
            activePane.value = 'Timeline'
        },
        onError: () => {
            acceptingOrder.value = false
        }
    })
}

function submitCancellation() {
    cancellingOrder.value = true
    cancelOrderResource.submit({
        order_name: activeOrder.value.name,
        notes: cancellationNotes.value
    }, {
        onSuccess: () => {
            cancellingOrder.value = false
            currentAction.value = null
            orders.reload()
            orderCounts.reload()
            orderDetails.fetch()
            activePane.value = 'Timeline'
        },
        onError: () => {
            cancellingOrder.value = false
        }
    })
}

function submitDelivery() {
    if (!deliveryDate.value) return
    
    submittingDelivery.value = true
    markDeliveredResource.submit({
        order_name: activeOrder.value.name,
        delivery_date: deliveryDate.value,
        delivery_notes: deliveryNotes.value
    }, {
        onSuccess: () => {
            submittingDelivery.value = false
            currentAction.value = null
            orders.reload()
            orderCounts.reload()
            orderDetails.fetch()
            activePane.value = 'Timeline'
        },
        onError: () => {
            submittingDelivery.value = false
        }
    })
}

const channelPartners = reactive({ data: [], loading: false })
const selectedChannelPartner = ref(null)
const assigningPartner = ref(false)

const tempSelectedPartner = ref(null)

watch(tempSelectedPartner, (val) => {
    if (val) {
        const value = typeof val === 'object' && val !== null && 'value' in val ? val.value : val
        
        if (!filters.channel_partner.includes(value)) {
            filters.channel_partner.push(value)
        }
        
        nextTick(() => {
            tempSelectedPartner.value = null
        })
    }
})

function removePartnerFilter(val) {
    filters.channel_partner = filters.channel_partner.filter(p => p !== val)
}

async function fetchChannelPartners() {
    channelPartners.loading = true
    channelPartners.data = []
    selectedChannelPartner.value = null
    
    try {
        const res = await frappeRequest({
            url: 'connect_master.connect_master.doctype.connect_order.connect_order.get_channel_partners',
            params: {
                territory: activeOrder.value.custom_resolved_territory,
                channel: activeOrder.value.service_category
            }
        })
        channelPartners.data = res.message || res
    } catch (e) {
        console.error(e)
    } finally {
        channelPartners.loading = false
    }
}

const assignPartnerResource = createResource({
    url: 'connect_master.api.assign_channel_partner'
})

function submitChannelPartner() {
    if (!selectedChannelPartner.value) return
    
    assigningPartner.value = true
    assignPartnerResource.submit({
        order_name: activeOrder.value.name,
        channel_partner: selectedChannelPartner.value
    }, {
        onSuccess: () => {
            assigningPartner.value = false
            currentAction.value = null
            selectedChannelPartner.value = null
            // Refresh
            orders.reload()
            orderCounts.reload()
            orderDetails.fetch()
            activePane.value = 'Timeline'
        },
        onError: () => {
            assigningPartner.value = false
        }
    })
}

const addCommentResource = createResource({
    url: 'connect_master.api.add_comment'
})

function submitComment() {
    if (!commentText.value.trim()) return
    
    submittingComment.value = true
    addCommentResource.submit({
        order_name: activeOrder.value.name,
        comment: commentText.value,
        is_internal: makePublic.value ? 0 : 1
    }, {
        onSuccess: () => {
            submittingComment.value = false
            currentAction.value = null
            commentText.value = ''
            makePublic.value = false
            // Refresh timeline
            orderDetails.fetch()
            // Switch to timeline to show the new comment
            activePane.value = 'Timeline'
        },
        onError: () => {
            submittingComment.value = false
        }
    })
}

const togglingEventId = ref(null)

const toggleVisibilityResource = createResource({
    url: 'connect_master.api.toggle_timeline_event_visibility'
})

function toggleVisibility(eventName) {
    togglingEventId.value = eventName
    toggleVisibilityResource.submit({
        order_name: activeOrder.value.name,
        event_name: eventName
    }, {
        onSuccess: () => {
            orderDetails.fetch()
            togglingEventId.value = null
        },
        onError: () => {
            togglingEventId.value = null
        }
    })
}

const filters = reactive({
    custom_address_category: '',
    custom_resolved_territory: '',
    include_child_territories: false,
    channel_partner: [],
    order_status: ''
})

const allStatuses = ['Submitted', 'Assigned', 'Accepted', 'Rejected', 'Cancelled', 'Fulfilled']
const partnerAdminStatuses = ['Assigned', 'Accepted', 'Rejected', 'Cancelled', 'Fulfilled']

const userInfo = createResource({
    url: 'connect_master.api.get_user_info',
    auto: true
})

const isPartnerAdmin = computed(() => {
    return userInfo.data?.roles?.includes('Partner Admin')
})

const isSystemManager = computed(() => {
    return userInfo.data?.roles?.includes('System Manager')
})

const availableStatuses = computed(() => {
    if (isPartnerAdmin.value) {
        return partnerAdminStatuses
    }
    return allStatuses
})

// Set partner filter when user info loads
watch(() => userInfo.data, (info) => {
    if (info && info.partners && info.partners.length > 0 && isPartnerAdmin.value) {
        // Pre-select all assigned partners? Or let user choose?
        // User said "show a multi-select dropdown".
        // If I pre-select all, it filters by all.
        // If I select none, it filters by none (which means all for System Manager, but for Partner Admin it should mean "all assigned").
        // But get_compass_orders handles permission logic separately.
        // So if filter is empty, Partner Admin still only sees assigned partners' orders.
        // So I don't need to pre-select.
        // But the user might want to filter by specific one.
        filters.channel_partner = []
    }
})

const orderCounts = createResource({
    url: 'connect_master.api.get_order_counts',
    auto: true,
    makeParams() {
        return {
            filters: JSON.stringify(filters),
            search: searchQuery.value
        }
    },
    onSuccess(data) {
        if (!initialTabSet.value) {
            let newTab = 'Active'
            if (data.Active > 0) {
                newTab = 'Active'
            } else if (data.Unresolved > 0) {
                newTab = 'Unresolved'
            } else {
                newTab = 'History'
            }
            
            if (activeTab.value !== newTab) {
                activeTab.value = newTab
                orders.reload()
            }
            initialTabSet.value = true
        }
    }
})

const orders = createResource({
    url: 'connect_master.api.get_compass_orders',
    auto: true,
    makeParams() {
        return {
            tab: activeTab.value,
            filters: JSON.stringify(filters),
            search: searchQuery.value
        }
    }
})

// Watchers to reload data
// watch(activeTab, () => {
//     orders.reload()
// })

function applyFilters() {
    orders.reload()
    orderCounts.reload()
    showFilters.value = false
}

function clearFilters() {
    filters.custom_address_category = ''
    filters.custom_resolved_territory = ''
    filters.include_child_territories = false
    filters.channel_partner = []
    filters.order_status = ''
    applyFilters()
}

const treeRebuildResource = createResource({
    url: 'connect_master.api.rebuild_service_territory_tree'
})

function rebuildTree() {
    treeRebuildResource.submit({}, {
        onSuccess: () => {
            orders.reload()
            orderCounts.reload()
            territories.reload()
        }
    })
}

const hasActiveFilters = computed(() => {
    return filters.custom_address_category || 
           filters.custom_resolved_territory || 
           (filters.channel_partner && filters.channel_partner.length > 0) || 
           filters.order_status
})

// Helper Resources
const serviceChannels = createResource({
    url: 'connect_master.api.get_allowed_service_categories',
    auto: true
})

const territories = createResource({
    url: 'connect_master.api.get_allowed_territories',
    auto: true
})

const showReleaseDialog = ref(false)
const releasing = ref(false)

const showChangeTerritoryDialog = ref(false)
const editingTerritoryValue = ref(null)
const savingTerritory = ref(false)

function openChangeTerritoryDialog() {
    editingTerritoryValue.value = activeOrder.value.custom_resolved_territory
    showChangeTerritoryDialog.value = true
}

const updateTerritoryResource = createResource({
    url: 'connect_master.api.update_territory'
})

function saveTerritory() {
    if (!editingTerritoryValue.value) return
    
    savingTerritory.value = true
    
    let newVal = editingTerritoryValue.value
    if (typeof newVal === 'object' && newVal !== null && 'value' in newVal) {
        newVal = newVal.value
    }
    
    updateTerritoryResource.submit({
        order_name: activeOrder.value.name,
        new_territory: newVal
    }, {
        onSuccess: () => {
            savingTerritory.value = false
            showChangeTerritoryDialog.value = false
            closeMenu()
            orders.reload()
            orderCounts.reload()
        },
        onError: () => {
            savingTerritory.value = false
        }
    })
}

const showChangeCategoryDialog = ref(false)
const editingCategoryValue = ref(null)
const savingCategory = ref(false)

function openChangeCategoryDialog() {
    editingCategoryValue.value = activeOrder.value.service_category
    showChangeCategoryDialog.value = true
}

const updateCategoryResource = createResource({
    url: 'connect_master.api.update_service_category'
})

function saveCategory() {
    if (!editingCategoryValue.value) return
    
    savingCategory.value = true
    
    updateCategoryResource.submit({
        order_name: activeOrder.value.name,
        new_category: editingCategoryValue.value
    }, {
        onSuccess: () => {
            savingCategory.value = false
            showChangeCategoryDialog.value = false
            closeMenu()
            orders.reload()
            orderCounts.reload()
        },
        onError: () => {
            savingCategory.value = false
        }
    })
}

const activeOrderTerritory = createResource({
    url: 'frappe.client.get',
    makeParams() {
        return {
            doctype: 'Service Territory',
            name: activeOrder.value?.custom_resolved_territory
        }
    }
})

watch(() => activeOrder.value?.custom_resolved_territory, (newVal) => {
    if (newVal) {
        activeOrderTerritory.fetch()
    } else {
        activeOrderTerritory.data = null
    }
})

const canRelease = computed(() => {
    if (!activeOrder.value || !activeOrder.value.custom_resolved_territory) return false
    if (['Fulfilled', 'Cancelled'].includes(activeOrder.value.order_status)) return false
    return activeOrderTerritory.data && activeOrderTerritory.data.parent_service_territory
})

const releaseTerritoryResource = createResource({
    url: 'connect_master.api.release_territory',
    makeParams() {
        return {
            order_name: activeOrder.value?.name
        }
    }
})

function releaseTerritory() {
    releasing.value = true
    releaseTerritoryResource.submit({}, {
        onSuccess: () => {
            releasing.value = false
            showReleaseDialog.value = false
            closeMenu()
            orders.reload()
            orderCounts.reload()
        },
        onError: () => {
            releasing.value = false
        }
    })
}

const territoryOptions = computed(() => {
    if (!territories.data) return []
    return territories.data.map(t => ({
        label: t.territory_name,
        value: t.name
    }))
})

const partners = createResource({
    url: 'connect_master.api.get_allowed_partners',
    auto: true
})

const partnerOptions = computed(() => {
    if (!partners.data) return []
    return partners.data.map(p => ({
        label: p.partner_name,
        value: p.name
    }))
})

// Helpers
function getChannelName(name) {
    const c = serviceChannels.data?.find(x => x.name === name)
    return c ? c.channel_name : name
}

function getPartnerName(name) {
    const p = partners.data?.find(x => x.name === name)
    return p ? p.partner_name : name
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString() + ' ' + new Date(dateStr).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
}

function formatDateShort(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString()
}

function getDaysAgo(dateStr) {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    return `${diffDays} days ago`
}

function getOrderStatusClasses(status) {
    const map = {
        'Draft': 'bg-gray-100 text-gray-800',
        'Submitted': 'bg-blue-100 text-blue-800',
        'Assigned': 'bg-orange-100 text-orange-800',
        'Accepted': 'bg-purple-100 text-purple-800',
        'Completed': 'bg-green-100 text-green-800',
        'Fulfilled': 'bg-green-100 text-green-800',
        'Cancelled': 'bg-red-100 text-red-800',
        'Rejected': 'bg-red-100 text-red-800'
    }
    return map[status] || 'bg-gray-100 text-gray-800'
}

// Kanban Helpers
const kanbanStatuses = computed(() => {
    if (activeTab.value === 'History') return ['Fulfilled', 'Cancelled']
    return ['Submitted', 'Assigned', 'Accepted', 'Rejected']
})

function getOrdersByStatus(status) {
    if (!orders.data) return []
    return orders.data.filter(o => o.order_status === status)
}

function toggleKanbanMenu(status) {
    if (activeKanbanMenu.value === status) {
        activeKanbanMenu.value = null
    } else {
        activeKanbanMenu.value = status
    }
}

const downloadCsvResource = createResource({
    url: 'connect_master.api.download_orders_csv'
})

function downloadKanbanCsv(status) {
    downloadCsvResource.submit({
        tab: activeTab.value,
        filters: JSON.stringify(filters),
        search: searchQuery.value,
        status: status
    }, {
        onSuccess: (data) => {
            if (!data || data.length === 0) return
            
            const csvContent = data.map(row =>
                row.map(cell => `"${(cell || '').toString().replace(/"/g, '""')}"`).join(',')
            ).join('\n')
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
            const link = document.createElement('a')
            if (link.download !== undefined) {
                const url = URL.createObjectURL(blob)
                link.setAttribute('href', url)
                link.setAttribute('download', `${status}_orders.csv`)
                link.style.visibility = 'hidden'
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
            }
        }
    })
}
</script>

<style scoped>
.custom-scrollbar {
  overflow-y: auto;
  overflow-x: hidden;
  scroll-behavior: smooth;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db; /* gray-300 */
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #9ca3af; /* gray-400 */
}
</style>
