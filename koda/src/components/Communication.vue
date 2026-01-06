<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md mx-4 overflow-hidden">
      <!-- Header -->
      <div class="px-6 py-4 border-b flex justify-between items-center">
        <h3 class="text-lg font-bold">{{ title }}</h3>
        <button v-if="canClose" @click="close" class="text-gray-500 hover:text-gray-700">&times;</button>
      </div>

      <!-- Body -->
      <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
        <!-- Address Form -->
        <div v-if="step === 'address'" class="space-y-4">
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">Store Name / Individual Name <span class="text-red-500">*</span></label>
                <Input v-model="addressForm.address_title" />
            </div>
            <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700">Address Type <span class="text-red-500">*</span></label>
                <div v-if="channels.loading" class="text-sm text-gray-500">Loading channels...</div>
                <div v-else class="space-y-2">
                    <div
                        v-for="channel in channels.data"
                        :key="channel.name"
                        class="flex items-start p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                        :class="{'border-blue-500 bg-blue-50': addressForm.custom_address_category === channel.name}"
                        @click="addressForm.custom_address_category = channel.name"
                    >
                        <div class="flex items-center h-5">
                            <input
                                type="radio"
                                :name="'channel-' + channel.name"
                                :checked="addressForm.custom_address_category === channel.name"
                                class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300"
                            />
                        </div>
                        <div class="ml-3 text-sm">
                            <label class="font-bold text-gray-900 cursor-pointer">{{ channel.channel_shorthand }}</label>
                            <p class="text-gray-500">{{ channel.channel_description }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">Address Line 1 <span class="text-red-500">*</span></label>
                <Input v-model="addressForm.address_line1" />
            </div>
            <Input label="Address Line 2 (Optional)" v-model="addressForm.address_line2" />
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">City <span class="text-red-500">*</span></label>
                <Input v-model="addressForm.city" />
            </div>
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">Pincode <span class="text-red-500">*</span></label>
                <Input v-model="addressForm.pincode" />
            </div>
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">State <span class="text-red-500">*</span></label>
                <Autocomplete
                    :options="indianStates"
                    :modelValue="addressForm.state"
                    @update:modelValue="val => addressForm.state = val?.value || val"
                    placeholder="Select State"
                />
            </div>
            <Input label="Country" v-model="addressForm.country" :disabled="true" />
        </div>

        <!-- Contact Form -->
        <div v-if="step === 'contact'" class="space-y-4">
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">First Name <span class="text-red-500">*</span></label>
                <Input v-model="contactForm.first_name" />
            </div>
            <Input label="Last Name" v-model="contactForm.last_name" />
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">Mobile Number <span class="text-red-500">*</span></label>
                <div class="flex items-center gap-2">
                    <div class="font-medium text-gray-700">+91</div>
                    <div class="flex-1">
                        <Input v-model="contactForm.mobile_no" type="text" maxlength="10" placeholder="10 digit mobile number" @blur="touched.mobile_no = true" />
                    </div>
                </div>
                <p v-if="touched.mobile_no && contactForm.mobile_no && !isValidMobile(contactForm.mobile_no)" class="text-xs text-red-500 mt-1">
                    Please enter a valid 10-digit Indian mobile number (starts with 6-9)
                </p>
            </div>
            <div class="space-y-1">
                <label class="block text-sm font-medium text-gray-700">Landline Number</label>
                <div class="flex items-center gap-2">
                    <div class="font-medium text-gray-700">+91</div>
                    <div class="flex-1">
                        <Input v-model="contactForm.landline" type="text" maxlength="10" placeholder="STD code + Number" @blur="touched.landline = true" />
                    </div>
                </div>
                <p v-if="touched.landline && contactForm.landline && !isValidLandline(contactForm.landline)" class="text-xs text-red-500 mt-1">
                    Please enter a valid 10-digit landline number
                </p>
            </div>
                    <Input label="Email" v-model="contactForm.email_id" />
                </div>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 border-t bg-gray-50 flex justify-end gap-2">
        <Button v-if="canClose" variant="subtle" @click="close">Cancel</Button>
        <Button :appearance="'primary'" @click="submit" :loading="loading" :disabled="!isFormValid">
            {{ submitLabel }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { Button, Input, Autocomplete, createResource, createListResource, frappeRequest } from 'frappe-ui'

const props = defineProps({
    show: Boolean,
    mode: {
        type: String,
        required: true,
        validator: (value) => ['Address+Contact', 'Address', 'Contact', 'Editable Address + Mandatory Contact', 'Editable Address', 'Editable Contact'].includes(value)
    },
    addressDoc: Object,
    contactDoc: Object,
    user: String,
    isDefaultAddress: {
        type: Boolean,
        default: false
    },
    blocking: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:show', 'success', 'close'])

// State
const step = ref('address') // 'address' or 'contact'
const loading = ref(false)
const createdAddressName = ref(null)
const originalPhoneNos = ref([])
const originalEmailIds = ref([])
const touched = reactive({
    mobile_no: false,
    landline: false
})

// Forms
const addressForm = reactive({
    address_title: '',
    address_line1: '',
    address_line2: '',
    city: '',
    pincode: '',
    state: '',
    country: 'India',
    custom_address_category: '',
    address_type: 'Current',
    custom_resolved_territory: ''
})

const contactForm = reactive({
    first_name: '',
    last_name: '',
    mobile_no: '',
    landline: '',
    email_id: ''
})

const indianStates = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
].map(s => ({ label: s, value: s }))

// Computed
const title = computed(() => {
    if (step.value === 'address') return props.mode.includes('Editable') ? 'Edit Address' : 'Add Address'
    return props.mode.includes('Editable') ? 'Edit Contact' : 'Add Contact'
})

const submitLabel = computed(() => {
    if (step.value === 'address' && (props.mode === 'Address+Contact' || props.mode === 'Editable Address + Mandatory Contact')) return 'Next'
    return 'Save'
})

const canClose = computed(() => {
    return !props.blocking
})

const isFormValid = computed(() => {
    if (step.value === 'address') {
        return addressForm.address_title && addressForm.address_line1 && addressForm.city && addressForm.pincode && addressForm.state && addressForm.custom_address_category
    } else {
        return contactForm.first_name &&
               contactForm.mobile_no &&
               isValidMobile(contactForm.mobile_no) &&
               (!contactForm.landline || isValidLandline(contactForm.landline))
    }
})

function isValidMobile(phone) {
    return /^[6-9]\d{9}$/.test(phone)
}

function isValidLandline(phone) {
    return /^\d{10}$/.test(phone)
}

const channels = createListResource({
    doctype: 'Service Channel',
    fields: ['name', 'channel_name', 'channel_description', 'channel_shorthand'],
    auto: true
})

// Watchers
watch(() => props.show, (val) => {
    if (val) init()
})

function init() {
    // Reset forms
    Object.keys(addressForm).forEach(k => addressForm[k] = '')
    addressForm.country = 'India'
    addressForm.address_type = 'Current'
    Object.keys(contactForm).forEach(k => contactForm[k] = '')
    touched.mobile_no = false
    touched.landline = false
    originalPhoneNos.value = []
    originalEmailIds.value = []
    
    createdAddressName.value = null

    // Determine initial step
    if (props.mode === 'Contact' || props.mode === 'Editable Contact') {
        step.value = 'contact'
    } else {
        step.value = 'address'
    }

    // Pre-fill if editing
    if (props.addressDoc) {
        Object.keys(addressForm).forEach(k => {
            if (props.addressDoc[k] !== undefined) addressForm[k] = props.addressDoc[k]
        })
    }
    if (props.contactDoc) {
        // Pre-fill basic info
        Object.keys(contactForm).forEach(k => {
            if (props.contactDoc[k] !== undefined) contactForm[k] = props.contactDoc[k]
        })
        // Fetch full details including phone_nos
        contactDetails.fetch()
    }
}

// Actions
const contactDetails = createResource({
    url: 'frappe.client.get',
    makeParams(values) {
        return {
            doctype: 'Contact',
            name: props.contactDoc.name
        }
    },
    onSuccess(data) {
        contactForm.first_name = data.first_name
        contactForm.last_name = data.last_name
        contactForm.email_id = data.email_id
        
        if (data.phone_nos) {
            originalPhoneNos.value = data.phone_nos
            
            const mobile = data.phone_nos.find(p => p.is_primary_mobile_no)
            if (mobile) contactForm.mobile_no = mobile.phone
            
            const landline = data.phone_nos.find(p => p.is_primary_phone)
            if (landline) contactForm.landline = landline.phone
        } else {
            originalPhoneNos.value = []
        }

        if (data.email_ids) {
            originalEmailIds.value = data.email_ids
            const primaryEmail = data.email_ids.find(e => e.is_primary)
            if (primaryEmail) contactForm.email_id = primaryEmail.email_id
        } else {
            originalEmailIds.value = []
        }
    }
})

function getUpdatedPhoneNos() {
    let phones = [...originalPhoneNos.value]
    
    // Update Mobile
    let mobileRow = phones.find(p => p.is_primary_mobile_no)
    if (contactForm.mobile_no) {
        if (mobileRow) {
            mobileRow.phone = contactForm.mobile_no
        } else {
            phones.push({ phone: contactForm.mobile_no, is_primary_mobile_no: 1 })
        }
    } else if (mobileRow) {
        // Keep it but maybe clear phone? Or remove?
        // Since mandatory, we assume it's there. If user cleared it, validation blocks.
    }

    // Update Landline
    let landlineRow = phones.find(p => p.is_primary_phone)
    if (contactForm.landline) {
        if (landlineRow) {
            landlineRow.phone = contactForm.landline
        } else {
            phones.push({ phone: contactForm.landline, is_primary_phone: 1 })
        }
    } else if (landlineRow) {
        phones = phones.filter(p => p !== landlineRow)
    }
    
    return phones
}

function getUpdatedEmailIds() {
    let emails = [...originalEmailIds.value]
    let primaryRow = emails.find(e => e.is_primary)

    if (contactForm.email_id) {
        if (primaryRow) {
            primaryRow.email_id = contactForm.email_id
        } else {
            let existing = emails.find(e => e.email_id === contactForm.email_id)
            if (existing) {
                existing.is_primary = 1
            } else {
                emails.push({ email_id: contactForm.email_id, is_primary: 1 })
            }
        }
    } else {
        if (primaryRow) {
            emails = emails.filter(e => e !== primaryRow)
        }
    }
    
    return emails
}

const createAddress = createResource({
    url: 'frappe.client.insert',
    makeParams(values) {
        return {
            doc: {
                doctype: 'Address',
                ...addressForm,
                custom_is_default: props.isDefaultAddress ? 1 : 0,
                links: [{ link_doctype: 'User', link_name: props.user }]
            }
        }
    },
    onSuccess(data) {
        createdAddressName.value = data.name
        if (props.mode === 'Address+Contact') {
            step.value = 'contact'
        } else {
            emit('success', { address: data.name })
            close()
        }
    }
})

const updateAddress = createResource({
    url: 'frappe.client.set_value',
    makeParams(values) {
        return {
            doctype: 'Address',
            name: props.addressDoc.name,
            fieldname: addressForm
        }
    },
    onSuccess(data) {
        if (props.mode === 'Editable Address + Mandatory Contact') {
             if (!props.contactDoc) {
                 createdAddressName.value = props.addressDoc.name
                 step.value = 'contact'
             } else {
                 emit('success', { address: props.addressDoc.name })
                 close()
             }
        } else {
            emit('success', { address: props.addressDoc.name })
            close()
        }
    }
})

const createContact = createResource({
    url: 'frappe.client.insert',
    makeParams(values) {
        return {
            doc: {
                doctype: 'Contact',
                first_name: contactForm.first_name,
                last_name: contactForm.last_name,
                email_ids: getUpdatedEmailIds(),
                phone_nos: getUpdatedPhoneNos(),
                is_primary: 1,
                address: createdAddressName.value || (props.addressDoc ? props.addressDoc.name : null),
                links: [{ link_doctype: 'User', link_name: props.user }]
            }
        }
    },
    onSuccess(data) {
        emit('success', { contact: data.name })
        close()
    }
})

const updateContact = createResource({
    url: 'frappe.client.set_value',
    makeParams(values) {
        return {
            doctype: 'Contact',
            name: props.contactDoc.name,
            fieldname: {
                first_name: contactForm.first_name,
                last_name: contactForm.last_name,
                email_ids: getUpdatedEmailIds(),
                phone_nos: getUpdatedPhoneNos()
            }
        }
    },
    onSuccess(data) {
        emit('success', { contact: props.contactDoc.name })
        close()
    }
})

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

async function submit() {
    loading.value = true
    try {
        if (step.value === 'address') {
            addressForm.custom_resolved_territory = await resolveTerritory(addressForm)

            if (props.mode.includes('Editable') && props.addressDoc) {
                await updateAddress.submit()
            } else {
                await createAddress.submit()
            }
        } else {
            if (props.mode.includes('Editable') && props.contactDoc) {
                await updateContact.submit()
            } else {
                await createContact.submit()
            }
        }
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

function close() {
    emit('update:show', false)
    emit('close')
}
</script>
