<template>
  <div class="flex flex-col h-full bg-gray-50">
    <!-- Chat Messages Area -->
    <div class="flex-1 overflow-y-auto p-4 space-y-6" ref="chatContainer">
      <div v-for="msg in shopStore.messages" :key="msg.id" class="flex w-full" :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'">
        
        <!-- AI Avatar -->
        <div v-if="msg.sender === 'ai'" class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-xl flex-shrink-0 mr-3 shadow-sm">
          {{ shopStore.currentCelebrity.avatar }}
        </div>
        
        <!-- Message Bubble -->
        <div class="flex flex-col max-w-[75%]">
          <!-- Name -->
          <div v-if="msg.sender === 'ai'" class="text-xs text-gray-500 mb-1 ml-1">{{ shopStore.currentCelebrity.name }}</div>
          
          <!-- Text content -->
          <div 
            class="px-4 py-3 rounded-2xl text-sm break-words shadow-sm"
            :class="msg.sender === 'user' ? 'bg-blue-500 text-white rounded-tr-none' : 'bg-white text-gray-800 rounded-tl-none'"
          >
            {{ msg.text }}
          </div>
          
          <!-- Product Recommendations -->
          <div v-if="msg.products && msg.products.length > 0" class="mt-3 space-y-2 w-full">
            <div 
              v-for="product in msg.products" 
              :key="product.id"
              class="bg-white rounded-lg shadow-sm border border-gray-100 p-2 flex items-center gap-3 w-64 cursor-pointer"
              @click="$emit('showProduct', product)"
            >
              <div class="w-14 h-14 bg-gray-100 rounded flex items-center justify-center text-3xl flex-shrink-0">
                {{ product.image }}
              </div>
              <div class="flex flex-col flex-1 overflow-hidden">
                <div class="text-sm font-medium text-gray-800 truncate">{{ product.title }}</div>
                <div class="text-xs text-red-500 font-bold mt-1">¥ {{ product.price }}</div>
                <div class="flex gap-1 mt-1">
                  <span v-for="tag in product.tags" :key="tag" class="text-[10px] bg-red-50 text-red-500 px-1 rounded">{{ tag }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- User Avatar -->
        <div v-if="msg.sender === 'user'" class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-xl flex-shrink-0 ml-3 shadow-sm">
          👤
        </div>
      </div>
      
      <!-- Loading Indicator -->
      <div v-if="isTyping" class="flex w-full justify-start">
        <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-xl flex-shrink-0 mr-3">
          {{ shopStore.currentCelebrity.avatar }}
        </div>
        <div class="bg-white px-4 py-3 rounded-2xl rounded-tl-none flex items-center space-x-1 shadow-sm h-10">
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="bg-white border-t p-3 flex items-center gap-2 pb-safe">
      <input 
        v-model="inputText" 
        @keyup.enter="sendMessage"
        type="text" 
        placeholder="输入您想买的商品..." 
        class="flex-1 bg-gray-100 rounded-full px-4 py-2 outline-none text-sm"
      />
      <button 
        @click="sendMessage"
        :disabled="!inputText.trim() || isTyping"
        class="bg-blue-500 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 disabled:bg-blue-300 transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useShopStore } from '@/stores/shop'

const shopStore = useShopStore()
const inputText = ref('')
const chatContainer = ref(null)
const isTyping = ref(false)

const emit = defineEmits(['showProduct'])

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

watch(() => shopStore.messages.length, () => {
  scrollToBottom()
})

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text) return
  
  // Add user message
  shopStore.addMessage({
    id: Date.now(),
    sender: 'user',
    text: text,
    timestamp: Date.now()
  })
  
  inputText.value = ''
  isTyping.value = true
  scrollToBottom()
  
  // Simulate network delay
  setTimeout(() => {
    generateReply(text)
  }, 1000)
}

const generateReply = (text) => {
  isTyping.value = false
  
  const celeb = shopStore.currentCelebrity
  const recommendations = shopStore.getRecommendations(text)
  
  let replyText = ''
  
  // Simple heuristic for "asking"
  const isQuestioning = text.includes('什么') || text.includes('推荐') || text.includes('不知道') || text.includes('看看')
  
  if (recommendations.length > 0) {
    replyText = celeb.templates.success
  } else if (isQuestioning) {
    replyText = celeb.templates.ask
  } else {
    replyText = celeb.templates.fail
  }
  
  shopStore.addMessage({
    id: Date.now(),
    sender: 'ai',
    text: replyText,
    timestamp: Date.now(),
    products: recommendations
  })
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 12px);
}
</style>