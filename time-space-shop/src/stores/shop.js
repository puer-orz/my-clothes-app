import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useShopStore = defineStore('shop', () => {
  // --- 名人数据 ---
  const celebrities = ref([
    {
      id: 'hepburn',
      name: '奥黛丽·赫本',
      avatar: '👗',
      tags: ['优雅', '时尚', '经典'],
      description: '温柔、有品位、说话文艺',
      category: 'fashion',
      welcome: '亲爱的，很高兴遇见你。优雅永不过时。',
      templates: {
        success: '亲爱的，这些单品非常适合你，简约优雅，永不过时。',
        fail: '亲爱的，能多告诉我一些你的需求吗？比如场合、风格或预算？',
        ask: '你喜欢什么风格呢？是简约、复古还是时尚？'
      }
    },
    {
      id: 'wusong',
      name: '武松',
      avatar: '🐯',
      tags: ['豪爽', '户外', '硬汉'],
      description: '直率、粗犷、讲义气',
      category: 'sports',
      welcome: '兄弟，想买啥直接说！俺老孙帮你挑！', // user prompt says "俺老孙" which is a bit weird for Wu Song, but sticking to user requirements
      templates: {
        success: '兄弟，这些装备杠杠的，结实耐用，买不了吃亏！',
        fail: '兄弟，想买啥直接说！俺老孙帮你挑！',
        ask: '你要干嘛用？户外徒步还是日常训练？'
      }
    },
    {
      id: 'doraemon',
      name: '哆啦A梦',
      avatar: '🐱',
      tags: ['可爱', '奇趣', '科技'],
      description: '活泼、热心、喜欢分享',
      category: 'toys',
      welcome: '你好呀！我有很多神奇道具哦，想看看吗？',
      templates: {
        success: '这些好东西一定会让你开心的！我都想买呢！',
        fail: '还有其他想要的吗？我的口袋里有很多好东西哦！',
        ask: '是为了自己用还是送朋友呢？'
      }
    }
  ])

  const currentCelebrityId = ref('hepburn')
  
  const currentCelebrity = computed(() => {
    return celebrities.value.find(c => c.id === currentCelebrityId.value) || celebrities.value[0]
  })

  // --- 商品数据 ---
  const products = ref([
    // 时尚服饰类 (赫本)
    { id: 'f1', title: '法式复古赫本风黑色连衣裙', price: 299, category: 'fashion', image: '👗', tags: ['优雅', '经典'], matchKeywords: ['裙子', '连衣裙', '衣服', '黑色', '复古'] },
    { id: 'f2', title: '简约真丝丝巾', price: 129, category: 'fashion', image: '🧣', tags: ['百搭', '气质'], matchKeywords: ['配饰', '丝巾', '围巾', '简约'] },
    { id: 'f3', title: '经典款珍珠项链', price: 599, category: 'fashion', image: '📿', tags: ['饰品', '高贵'], matchKeywords: ['项链', '配饰', '珍珠'] },
    { id: 'f4', title: '时尚百搭高跟鞋', price: 359, category: 'fashion', image: '👠', tags: ['鞋靴', '显瘦'], matchKeywords: ['鞋子', '高跟鞋', '单鞋'] },
    { id: 'f5', title: '高级感哑光口红', price: 199, category: 'fashion', image: '💄', tags: ['美妆', '显白'], matchKeywords: ['美妆', '口红', '化妆品'] },
    
    // 运动户外类 (武松)
    { id: 's1', title: '专业户外登山背包', price: 459, category: 'sports', image: '🎒', tags: ['耐磨', '大容量'], matchKeywords: ['背包', '包', '户外', '登山'] },
    { id: 's2', title: '减震透气跑步鞋', price: 399, category: 'sports', image: '👟', tags: ['运动', '舒适'], matchKeywords: ['鞋子', '跑鞋', '运动鞋'] },
    { id: 's3', title: '防风防水冲锋衣', price: 599, category: 'sports', image: '🧥', tags: ['保暖', '防雨'], matchKeywords: ['衣服', '外套', '冲锋衣', '户外'] },
    { id: 's4', title: '便携式户外折叠帐篷', price: 299, category: 'sports', image: '⛺', tags: ['露营', '快开'], matchKeywords: ['帐篷', '露营', '户外'] },
    { id: 's5', title: '高强度碳纤维登山杖', price: 159, category: 'sports', image: '🦯', tags: ['轻量', '坚固'], matchKeywords: ['登山杖', '户外', '装备'] },
    
    // 零食玩具类 (哆啦A梦)
    { id: 't1', title: '铜锣烧大礼包', price: 59, category: 'toys', image: '🥞', tags: ['零食', '甜点'], matchKeywords: ['零食', '吃的', '铜锣烧', '甜点'] },
    { id: 't2', title: '智能伴睡机器人', price: 299, category: 'toys', image: '🤖', tags: ['数码', '智能'], matchKeywords: ['玩具', '机器人', '数码'] },
    { id: 't3', title: '竹蜻蜓飞行玩具', price: 39, category: 'toys', image: '🚁', tags: ['玩具', '创意'], matchKeywords: ['玩具', '竹蜻蜓', '飞'] },
    { id: 't4', title: '任意门造型储物盒', price: 89, category: 'toys', image: '🚪', tags: ['家居', '收纳'], matchKeywords: ['盒子', '收纳', '周边'] },
    { id: 't5', title: '记忆面包抱枕', price: 69, category: 'toys', image: '🍞', tags: ['抱枕', '毛绒'], matchKeywords: ['抱枕', '玩具', '软'] }
  ])

  // --- 聊天记录 ---
  const messages = ref([
    {
      id: Date.now(),
      sender: 'ai',
      text: celebrities.value[0].welcome,
      timestamp: Date.now()
    }
  ])

  const changeCelebrity = (id) => {
    currentCelebrityId.value = id
    // 切换名人时，清空历史记录，或者添加一条欢迎语
    messages.value = [{
      id: Date.now(),
      sender: 'ai',
      text: currentCelebrity.value.welcome,
      timestamp: Date.now()
    }]
  }

  const addMessage = (message) => {
    messages.value.push(message)
  }

  // --- 推荐逻辑 ---
  const getRecommendations = (text) => {
    const celeb = currentCelebrity.value
    // 过滤出当前名人负责的商品
    const availableProducts = products.value.filter(p => p.category === celeb.category)
    
    // 寻找匹配的商品
    let matchedProducts = []
    
    // 简单关键词匹配
    for (const product of availableProducts) {
      if (product.matchKeywords.some(keyword => text.includes(keyword))) {
        matchedProducts.push(product)
      }
    }
    
    // 限制最多3个
    return matchedProducts.slice(0, 3)
  }

  return {
    celebrities,
    currentCelebrityId,
    currentCelebrity,
    products,
    messages,
    changeCelebrity,
    addMessage,
    getRecommendations
  }
})