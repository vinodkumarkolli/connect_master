<template>
  <div class="max-w-4xl mx-auto py-12 px-4">
    <!-- Step 1: Welcome -->
    <div class="text-center space-y-6 py-20">
      <h1 class="text-5xl font-bold text-gray-900">Koda</h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        We make buying of Sastry Balm easy by connecting you with local vendors/distributors/wholesalers
      </p>
      <div class="pt-8">
        <Button :variant="'outline'" size="xl" @click="startOrdering" :loading="session.loading">
          Start Ordering
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { Button, frappeRequest } from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
const session = reactive({
    data: null,
    loading: true
})

onMounted(async () => {
    try {
        let res = await frappeRequest({ url: 'frappe.auth.get_logged_user' })
        if (res) {
            session.data = res.message || res
        }
    } catch (e) {
        session.data = null
    } finally {
        session.loading = false
    }
})

function startOrdering() {
    if (session.data && session.data !== 'Guest') {
        router.push('/order')
    } else {
        window.location.href = '/login?redirect-to=/koda/order'
    }
}
</script>
