import { reactive } from 'vue'
import { frappeRequest } from 'frappe-ui'

const session = reactive({
    data: null,
    loading: false,
    error: null,
    fetch: null
})

let fetchPromise = null

session.fetch = async function() {
    if (session.data) return session.data
    if (fetchPromise) return fetchPromise

    session.loading = true
    fetchPromise = frappeRequest({ url: 'frappe.auth.get_logged_user' })
        .then(res => {
            let user = res.message || res
            session.data = user
            return user
        })
        .catch(error => {
            console.error('Failed to fetch session:', error)
            session.error = error
            session.data = 'Guest'
            return 'Guest'
        })
        .finally(() => {
            session.loading = false
            fetchPromise = null
        })
    return fetchPromise
}

export function useSession() {
    return session
}
