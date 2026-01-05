<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <Card class="p-6">
        <div class="space-y-6">
          <div v-if="step === 'email'">
            <div>
              <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
              <div class="mt-2">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autocomplete="email"
                  required
                  v-model="email"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                />
              </div>
            </div>

            <div v-if="showFullNameInput" class="mt-4">
              <label for="fullName" class="block text-sm font-medium leading-6 text-gray-900">Full Name</label>
              <div class="mt-2">
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  required
                  v-model="fullName"
                  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                />
              </div>
            </div>

            <div class="mt-6">
              <Button
                :loading="loading"
                :appearance="'primary'"
                class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                @click="sendOtp"
              >
                {{ showFullNameInput ? 'Create Account & Send OTP' : 'Send OTP' }}
              </Button>
            </div>
          </div>

          <div v-else>
             <div>
              <label for="otp" class="block text-sm font-medium leading-6 text-gray-900">One Time Password</label>
              <div class="mt-2 flex gap-2 justify-center">
                <input
                  v-for="(digit, index) in 6"
                  :key="index"
                  :ref="el => otpInputs[index] = el"
                  type="text"
                  inputmode="numeric"
                  maxlength="1"
                  v-model="otpDigits[index]"
                  @input="handleOtpInput(index, $event)"
                  @keydown="handleOtpKeydown(index, $event)"
                  @paste="handleOtpPaste"
                  class="w-12 h-12 text-center text-xl border rounded-md focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 border-gray-300"
                />
              </div>
            </div>

            <div class="mt-6">
              <Button
                :loading="loading"
                :appearance="'primary'"
                class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                @click="verifyOtp"
              >
                Verify & Login
              </Button>
            </div>
            
            <div class="mt-4 text-center">
               <a href="#" @click.prevent="step = 'email'" class="font-semibold text-indigo-600 hover:text-indigo-500 text-sm">Change Email</a>
            </div>
          </div>
          
          <div v-if="errorMessage" class="text-red-500 text-sm text-center mt-2">
              {{ errorMessage }}
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, frappeRequest, Card } from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()
const step = ref('email')
const email = ref('')
const otpDigits = ref(['', '', '', '', '', ''])
const otpInputs = ref([])
const fullName = ref('')
const showFullNameInput = ref(false)
const loading = ref(false)
const errorMessage = ref('')

function handleOtpInput(index, event) {
    const value = event.target.value
    if (!/^\d*$/.test(value)) {
        otpDigits.value[index] = ''
        return
    }
    
    otpDigits.value[index] = value.slice(-1)

    if (value && index < 5) {
        otpInputs.value[index + 1].focus()
    }
}

function handleOtpKeydown(index, event) {
    if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
        otpInputs.value[index - 1].focus()
    }
}

function handleOtpPaste(event) {
    event.preventDefault()
    const pastedData = event.clipboardData.getData('text').slice(0, 6)
    if (/^\d+$/.test(pastedData)) {
        pastedData.split('').forEach((digit, i) => {
            if (i < 6) otpDigits.value[i] = digit
        })
        const focusIndex = Math.min(pastedData.length, 5)
        otpInputs.value[focusIndex].focus()
    }
}

async function sendOtp() {
  if (!email.value) {
    errorMessage.value = 'Please enter your email'
    return
  }

  if (showFullNameInput.value && !fullName.value) {
      errorMessage.value = 'Please enter your full name'
      return
  }
  
  loading.value = true
  errorMessage.value = ''
  
  try {
    let res = await frappeRequest({
      url: 'connect_master.api.send_otp',
      params: {
        email: email.value,
        full_name: fullName.value
      }
    })

    if (res.status === 'user_not_found') {
        showFullNameInput.value = true
        errorMessage.value = res.message
    } else {
        step.value = 'otp'
    }
  } catch (error) {
    errorMessage.value = error.message || 'Failed to send OTP'
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function verifyOtp() {
  const otp = otpDigits.value.join('')
  if (otp.length !== 6) {
    errorMessage.value = 'Please enter complete OTP'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    await frappeRequest({
      url: 'connect_master.api.verify_otp',
      params: {
        email: email.value,
        otp: otp
      }
    })
    // Redirect to home or intended page
    window.location.href = '/koda'
  } catch (error) {
    errorMessage.value = error.message || 'Invalid OTP'
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>
