<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Access Restricted</h1>
      <p class="text-lg text-gray-600">Your access to the Koda app is restricted.</p>
      <div class="mt-8">
        <a href="/app" class="text-blue-600 hover:text-blue-800 font-medium">Go to Desk</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
})
</script>
