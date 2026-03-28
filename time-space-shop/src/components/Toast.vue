<template>
  <transition name="toast-slide">
    <div v-if="visible" class="fixed bottom-24 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white px-6 py-3 rounded-full shadow-lg z-50 flex items-center gap-2 min-w-max">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <span class="text-sm font-medium">{{ message }}</span>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')

let timer = null

const show = (msg, duration = 2000) => {
  message.value = msg
  visible.value = true
  
  if (timer) clearTimeout(timer)
  
  timer = setTimeout(() => {
    visible.value = false
  }, duration)
}

defineExpose({ show })
</script>

<style scoped>
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.3s ease;
}

.toast-slide-enter-from {
  opacity: 0;
  transform: translate(-50%, 20px);
}

.toast-slide-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}
</style>