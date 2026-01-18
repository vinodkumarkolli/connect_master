<template>
  <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Sastry Balm
        </h1>
        <div class="flex items-center gap-4">
            <button @click="showMedia = true" class="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                Media
            </button>
            <CustomDropdown :options="promotionOptions">
                <button class="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"></path></svg>
                    Promotions
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </button>
            </CustomDropdown>
        </div>
      </div>
      <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
        <div class="flex flex-col md:flex-row gap-8 mb-8">
            <div class="w-full md:w-1/3">
                <img src="https://zap.sravie.in/files/SB.jpeg" alt="Sastry Balm" class="w-full rounded-lg shadow-md" />
            </div>
            <div class="w-full md:w-2/3 prose prose-blue max-w-none">
                <h3>Description</h3>
                <p>Sri Kodandarama Ayurveda Nilayam is an Ayurvedic Pharmacy operated from 7 generations of Ayurvedic Specialists. The organisation started gaining popularity under the aegis of Sri. Vukkadapu Ram Mohan Rao. Sastry Balm was started manufacturing from 1993 and since then, it has been a household name in Andhra Pradesh.</p>
                <p>The Balm is thoroughly formulated using natural and tested ingredients that ensure to its optimum effectiveness. Sri Kodandarama Ayurveda Nilayam is a GMP certified Organisation by Dept. of Ayush, Govt of India. Owing to this, it is a reliable name in the market for the best herbal formulation in terms of Pain Balm</p>
            </div>
        </div>

        <div class="prose prose-blue max-w-none">
            <h3>Features</h3>
            <p>SASTRY BALM is a Premium Ayurvedic Medicine</p>
            <ul>
                <li>Provides Strong Ayurvedic Remedy</li>
                <li>Persons suffering from Severe Cold or Blocking of Nostrils or Uneasy Breathing are advised to keep small quantity of Sastry Balm in a tub of hot water and inhale the vapors</li>
                <li>Can be applied and massaged smoothly over Chest and Back region in Breathlessness followed by hot water fomentation</li>
                <li>Safe to use for children</li>
            </ul>

            <h3>Used for</h3>
            <ul>
                <li>Fast Relief from Headache</li>
                <li>Cold</li>
                <li>Back Pain</li>
                <li>Knee Joint Pain</li>
                <li>Neck Pain</li>
                <li>Sprains</li>
                <li>Joint Pains</li>
                <li>Muscle Spasm</li>
                <li>Frozen Shoulder and</li>
                <li>Rheumatic Pain</li>
            </ul>

            <h3>Basic Ingredients</h3>
            <ul>
                <li>Ajwan Ka Phool</li>
                <li>Karpura Powder</li>
                <li>Ganga Sindhuram</li>
                <li>Guggilam Powder</li>
                <li>Honeywax</li>
                <li>Lavanga Tailam</li>
                <li>Pudina Satwam</li>
                <li>Tarpent Tailam</li>
            </ul>
        </div>
      </div>
    </div>

    <!-- Media Modal -->
    <div v-if="showMedia" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75" @click.self="showMedia = false">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 overflow-hidden relative">
            <button @click="showMedia = false" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 z-10 bg-white rounded-full p-1">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            
            <div class="p-6">
                <h3 class="text-xl font-bold mb-4">Media Gallery</h3>
                
                <div class="flex justify-between items-center mb-4 relative z-10">
                    <button type="button" @click.stop.prevent="prevVideo" class="p-2 rounded-full hover:bg-gray-100 disabled:opacity-50 cursor-pointer" :disabled="currentVideoIndex === 0">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
                    </button>
                    <span class="text-sm text-gray-500">{{ currentVideoIndex + 1 }} / {{ videoIds.length }}</span>
                    <button type="button" @click.stop.prevent="nextVideo" class="p-2 rounded-full hover:bg-gray-100 disabled:opacity-50 cursor-pointer" :disabled="currentVideoIndex === videoIds.length - 1">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </button>
                </div>

                <div class="relative aspect-video bg-black rounded-lg overflow-hidden">
                    <iframe 
                        :key="currentVideoIndex"
                        :src="`https://www.youtube.com/embed/${videoIds[currentVideoIndex]}`" 
                        class="w-full h-full" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
            </div>
        </div>
    </div>

    <!-- Promotions Modal -->
    <div v-if="showPromotions" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75" @click.self="showPromotions = false">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl mx-4 overflow-hidden relative">
            <button @click="showPromotions = false" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 z-10 bg-white rounded-full p-1">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            
            <div class="p-6">
                <h3 class="text-xl font-bold mb-4">Backlit Boards</h3>
                
                <div class="flex justify-between items-center mb-4 relative z-10">
                    <button type="button" @click.stop.prevent="prevImage" class="p-2 rounded-full hover:bg-gray-100 disabled:opacity-50 cursor-pointer" :disabled="currentImageIndex === 0">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
                    </button>
                    <span class="text-sm text-gray-500">{{ currentImageIndex + 1 }} / {{ imageUrls.length }}</span>
                    <button type="button" @click.stop.prevent="nextImage" class="p-2 rounded-full hover:bg-gray-100 disabled:opacity-50 cursor-pointer" :disabled="currentImageIndex === imageUrls.length - 1">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </button>
                </div>

                <div class="relative aspect-video bg-black rounded-lg overflow-hidden flex items-center justify-center">
                    <img :src="imageUrls[currentImageIndex]" class="max-w-full max-h-full object-contain" />
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CustomDropdown from '../components/CustomDropdown.vue'

const showMedia = ref(false)
const currentVideoIndex = ref(0)
const videoIds = [
    'u91s5bmL_uM',
    '6zb489Rk3Xc',
    'veLlh6GHiDM',
    'VVDlTIMaedo',
    'eiYjnOSgeXI',
    'bsJuUa7Ox6k'
]

function nextVideo() {
    if (currentVideoIndex.value < videoIds.length - 1) {
        currentVideoIndex.value++
    }
}

function prevVideo() {
    if (currentVideoIndex.value > 0) {
        currentVideoIndex.value--
    }
}

const showPromotions = ref(false)
const currentImageIndex = ref(0)
const imageUrls = [
    'https://zap.sravie.in//files/1.jpeg',
    'https://zap.sravie.in//files/2.jpeg',
    'https://zap.sravie.in//files/3.jpeg',
    'https://zap.sravie.in//files/4.jpeg',
    'https://zap.sravie.in//files/5.jpeg',
    'https://zap.sravie.in//files/6.jpeg'
]

const promotionOptions = [
    {
        label: 'Backlit Boards',
        onClick: () => {
            showPromotions.value = true
            currentImageIndex.value = 0
        }
    }
]

function nextImage() {
    if (currentImageIndex.value < imageUrls.length - 1) {
        currentImageIndex.value++
    }
}

function prevImage() {
    if (currentImageIndex.value > 0) {
        currentImageIndex.value--
    }
}
</script>
