<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 lg:px-8">
    <div v-if="showDisclaimer" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      <div class="fixed inset-0 bg-gray-900 bg-opacity-50 transition-opacity"></div>
      
      <div class="relative bg-white rounded-xl shadow-xl max-w-2xl w-full overflow-hidden flex flex-col max-h-[90vh]">
        <!-- Modal Header -->
        <div class="px-6 py-4 border-b flex justify-between items-center bg-gray-50">
          <h3 class="text-lg font-bold text-red-600">Notice</h3>
        </div>

        <!-- Modal Body -->
        <div class="p-6 overflow-y-auto">
          <div class="space-y-4">
            <p class="text-sm text-gray-700">
              No money transaction is involved when you place order on our application. 
              This application doesn't collect payments from the customer nor does it pay for the channel partners. 
              Koda app from Sravi Enterprises is a informative app that aims to bring the customers and vendors closer. 
              We forward orders that you place, to our channel partners and the transaction is carried between you and channel partner.<br/>
              <b>Sravi Enterprises holds no responsibility for this transaction</b><br/>
              We advise user descretion in guaging the authenticity of the channel partners and therby carrying out the transaction
            </p>

            <p class="text-sm text-gray-700">
              Read our <router-link to="/terms" class="text-blue-600 hover:underline">Terms and Conditions</router-link>.
            </p>
            
            <h4 class="font-bold text-gray-900">Disclaimers</h4>
            <div class="space-y-2">
              <div class="flex items-start gap-2">
                <input type="checkbox" id="d1" v-model="accepted1" class="mt-1 rounded text-blue-600 focus:ring-blue-500">
                <label for="d1" class="text-sm text-gray-700">I understand that this application doesn't collect payments</label>
              </div>
              <div class="flex items-start gap-2">
                <input type="checkbox" id="d2" v-model="accepted2" class="mt-1 rounded text-blue-600 focus:ring-blue-500">
                <label for="d2" class="text-sm text-gray-700">I understand that placing an order doesn't guarantee the delivery of the product and I understand that I am just acknowledging my intention of buying</label>
              </div>
              <div class="flex items-start gap-2">
                <input type="checkbox" id="d3" v-model="accepted3" class="mt-1 rounded text-blue-600 focus:ring-blue-500">
                <label for="d3" class="text-sm text-gray-700">I understand that Sravi Enterprises and its Channel Partners holds the right to turn down the order as per their policies, <router-link to="/terms" class="text-blue-600 hover:underline">terms and conditions</router-link></label>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="px-6 py-4 border-t bg-gray-50 flex justify-end">
          <Button appearance="primary" :disabled="!canProceed" @click="acceptDisclaimer">I Agree</Button>
        </div>
      </div>
    </div>
    <div v-if="!showDisclaimer">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
      </div>

      <div class="mt-5 sm:mx-auto sm:w-full sm:max-w-sm">
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
                <!-- Wrapper with 2px horizontal margin (mx-[2px]) and responsive gap -->
                <div class="mt-2 grid grid-cols-6 gap-2 mx-[2px] justify-items-center">
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
                    class="w-full aspect-square text-center text-xl border rounded-md focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 border-gray-300 min-w-0"
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
  </div>
  <div class="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob"></div>
    <div class="absolute top-0 right-1/4 w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
    <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-4000"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, frappeRequest, Card, Dialog } from 'frappe-ui'
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

const showDisclaimer = ref(true)
const accepted1 = ref(false)
const accepted2 = ref(false)
const accepted3 = ref(false)

const canProceed = computed(() => accepted1.value && accepted2.value && accepted3.value)

function acceptDisclaimer() {
    showDisclaimer.value = false
}

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

<style scoped>
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}
</style>
