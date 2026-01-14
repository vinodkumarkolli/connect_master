import { ref } from 'vue'
import { createResource } from 'frappe-ui'
import { useSession } from './useSession'

export function useConsumerValidation() {
    // UI State
    const showCommunication = ref(false)
    const communicationMode = ref('Address+Contact')
    const communicationAddress = ref(null)
    const communicationContact = ref(null)
    const isBlocking = ref(false)
    const isDefaultAddress = ref(false)

    const session = useSession()

    const userRoles = createResource({
        url: 'connect_master.utils.get_user_roles',
        auto: false
    })

    const addresses = createResource({
        url: 'frappe.client.get_list',
        makeParams(values) {
            return {
                doctype: 'Address',
                fields: [
                    'name',
                    'disabled',
                    'custom_is_default',
                    'address_title',
                    'address_line1',
                    'address_line2',
                    'city',
                    'pincode',
                    'state',
                    'country',
                    'custom_address_category',
                    'address_type'
                ],
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
                fields: ['name', 'address'],
                filters: [['Dynamic Link', 'link_name', '=', session.data], ['Dynamic Link', 'link_doctype', '=', 'User']]
            }
        },
        auto: false
    })

    async function validate() {
        try {
            if (!session.data) await session.fetch()
            if (!session.data || session.data === 'Guest') return { valid: true }

            // Check Role
            await userRoles.fetch()
            let roles = []
            if (Array.isArray(userRoles.data)) {
                roles = userRoles.data
            } else if (userRoles.data && Array.isArray(userRoles.data.message)) {
                roles = userRoles.data.message
            }
            
            if (!roles.includes('Consumer') && !roles.includes('Customer')) return { valid: true }

            // Check Data
            await addresses.fetch()
            await contacts.fetch()

            const addrList = addresses.data || []
            const contactList = contacts.data || []

            const addrContactMap = {}
            contactList.forEach(c => {
                if (c.address) {
                    if (!addrContactMap[c.address]) addrContactMap[c.address] = []
                    addrContactMap[c.address].push(c)
                }
            })

            // Filter for enabled addresses
            const enabledAddresses = addrList.filter(a => !a.disabled)

            // Scenario 1: No enabled addresses
            if (enabledAddresses.length === 0) {
                return { valid: false, missing: 'address', scenario: 1 }
            }

            // Find enabled addresses without contacts
            const addressesWithoutContact = enabledAddresses.filter(a => !addrContactMap[a.name] || addrContactMap[a.name].length === 0)

            if (addressesWithoutContact.length > 0) {
                // Prioritize default address if it's missing contact
                let targetAddress = addressesWithoutContact.find(a => a.custom_is_default) || addressesWithoutContact[0]

                // Scenario 2: Single enabled address, no contact
                if (enabledAddresses.length === 1) {
                     return { valid: false, missing: 'contact', address: targetAddress, scenario: 2 }
                }
                
                // Scenario 3: Multiple enabled addresses, at least one without contact
                return { valid: false, missing: 'contact', address: targetAddress, scenario: 3 }
            }

            return { valid: true }
        } catch (e) {
            console.error('Validation error:', e)
            return { valid: true }
        }
    }

    async function checkAndPrompt() {
        const result = await validate()
        if (!result.valid) {
            isBlocking.value = true
            
            if (result.scenario === 1) {
                // Scenario 1: Address+Contact, Default=1
                communicationMode.value = 'Address+Contact'
                communicationAddress.value = null
                communicationContact.value = null
                isDefaultAddress.value = true
                showCommunication.value = true
            } else if (result.scenario === 2 || result.scenario === 3) {
                // Scenario 2 & 3: Editable Address + Mandatory Contact
                communicationMode.value = 'Editable Address + Mandatory Contact'
                communicationAddress.value = result.address
                communicationContact.value = null
                // Set isDefaultAddress based on the address being edited
                isDefaultAddress.value = !!result.address.custom_is_default
                showCommunication.value = true
            }
            return false
        }
        return true
    }

    return {
        validate,
        checkAndPrompt,
        session,
        userRoles,
        showCommunication,
        communicationMode,
        communicationAddress,
        communicationContact,
        isBlocking,
        isDefaultAddress
    }
}
