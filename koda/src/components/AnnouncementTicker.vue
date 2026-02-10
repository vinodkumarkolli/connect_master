<template>
    <div v-if="announcements && announcements.length > 0" :class="['relative h-12 overflow-hidden mb-6 bg-white border border-gray-100 rounded-lg shadow', containerClass]" style="max-width: 100%;">
        <div class="whitespace-nowrap animate-marquee absolute top-0 left-0 h-full flex items-center hover:pause">
            <span v-for="announcement in announcements" :key="announcement.name" class="inline-flex items-center mx-8">
                <span v-if="announcement.announcement_type === 'Offer'" class="flex-shrink-0 bg-red-100 text-red-700 text-xs font-bold px-2 py-0.5 rounded mr-2 border border-red-200">OFFER</span>
                <span v-else-if="announcement.announcement_type === 'Event'" class="flex-shrink-0 bg-purple-100 text-purple-700 text-xs font-bold px-2 py-0.5 rounded mr-2 border border-purple-200">EVENT</span>
                <div class="text-sm text-red-600 font-medium whitespace-nowrap" v-html="announcement.display_html"></div>
            </span>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    location: {
        type: String,
        required: true
    },
    announcements: {
        type: Array,
        default: () => []
    },
    containerClass: {
        type: String,
        default: 'w-full max-w-full'
    }
})
</script>

<style scoped>
.animate-marquee {
    animation: marquee 30s linear infinite;
    padding-left: 100%;
}

.hover\:pause:hover {
    animation-play-state: paused;
}

@keyframes marquee {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-100%);
    }
}
</style>
