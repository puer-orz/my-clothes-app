// 全局变量
const gameModal = document.getElementById('game-modal');
const modalBody = document.getElementById('modal-body');
const closeModal = document.getElementById('close-modal');

// 游戏数据
const gameData = {
  'seven-game': {
    title: '逢7必过',
    description: '逢7必过是一款考验反应速度和专注力的经典酒桌游戏。玩家依次报数，但遇到数字7或7的倍数时，不能说出该数字，而是要说"过"。如果有人出错，就需要接受惩罚。',
    rules: [
      '1. 玩家按顺时针顺序依次报数，从1开始',
      '2. 当遇到数字包含7或7的倍数时，不能说出该数字，必须说"过"',
      '3. 如果有人说错或反应太慢，就需要接受惩罚',
      '4. 游戏可以从任意数字重新开始'
    ],
    tips: '提示：可以先在心里默数，提前准备好"过"字，避免出错！'
  },
  'three-gardens': {
    title: '逛三园',
    description: '逛三园是一款考验知识面和反应速度的游戏。玩家围成一圈，从"逛三园"开始，然后指定一个"园子"，下一个玩家需要说出该园子里的一样东西，循环往复。',
    rules: [
      '1. 玩家围成一圈，第一个人说"逛三园"',
      '2. 第二个人说"什么园"',
      '3. 第三个人指定一个园子，如"动物园"、"植物园"等',
      '4. 下一个玩家需要说出该园子里的一样东西',
      '5. 游戏按顺时针顺序继续，每个人都要说出不同的东西',
      '6. 如果说不出来或重复，就需要接受惩罚'
    ],
    gardens: [
      {
        name: '动物园',
        items: ['狮子', '老虎', '大象', '长颈鹿', '猴子', '熊猫', '斑马', '河马', '犀牛', '鳄鱼', '孔雀', '鹦鹉', '海豚', '鲸鱼', '鲨鱼', '海龟', '企鹅', '北极熊', '考拉', '袋鼠']
      },
      {
        name: '植物园',
        items: ['玫瑰', '牡丹', '菊花', '荷花', '向日葵', '郁金香', '仙人掌', '竹子', '松树', '柳树', '樱花', '梅花', '兰花', '桂花', '薰衣草', '薄荷', '芦荟', '蕨类', '苔藓', '蘑菇']
      },
      {
        name: '水果园',
        items: ['苹果', '香蕉', '橙子', '葡萄', '草莓', '西瓜', '桃子', '梨', '芒果', '菠萝', '柠檬', '猕猴桃', '火龙果', '山竹', '荔枝', '龙眼', '椰子', '石榴', '蓝莓', '覆盆子']
      },
      {
        name: '蔬菜园',
        items: ['西红柿', '黄瓜', '土豆', '胡萝卜', '白菜', '青菜', '茄子', '辣椒', '洋葱', '大蒜', '生姜', '韭菜', '菠菜', '芹菜', '莴笋', '西兰花', '花椰菜', '南瓜', '冬瓜', '丝瓜']
      },
      {
        name: '饮料园',
        items: ['可乐', '雪碧', '芬达', '橙汁', '苹果汁', '西瓜汁', '牛奶', '酸奶', '咖啡', '茶', '啤酒', '红酒', '白酒', '伏特加', '威士忌', '朗姆酒', '龙舌兰', '鸡尾酒', '矿泉水', '苏打水']
      },
      {
        name: '运动园',
        items: ['足球', '篮球', '排球', '网球', '羽毛球', '乒乓球', '棒球', '橄榄球', '高尔夫', '游泳', '跑步', '跳绳', '瑜伽', '健身', '举重', '拳击', '摔跤', '柔道', '跆拳道', '武术']
      },
      {
        name: '电影园',
        items: ['阿凡达', '泰坦尼克号', '盗梦空间', '星际穿越', '肖申克的救赎', '阿甘正传', '千与千寻', '复仇者联盟', '变形金刚', '速度与激情', '哈利波特', '指环王', '星球大战', '黑客帝国', '无间道', '教父', '楚门的世界', '辛德勒名单', '机器人总动员', '疯狂动物城']
      },
      {
        name: '音乐园',
        items: ['流行音乐', '古典音乐', '摇滚音乐', '爵士音乐', '嘻哈音乐', '电子音乐', '民谣音乐', '乡村音乐', 'R&B音乐', '重金属音乐', '钢琴', '吉他', '小提琴', '大提琴', '萨克斯', '架子鼓', '长笛', '小号', '古筝', '琵琶']
      },
      {
        name: '国家园',
        items: ['中国', '美国', '英国', '法国', '德国', '俄罗斯', '日本', '韩国', '意大利', '加拿大', '澳大利亚', '巴西', '印度', '西班牙', '墨西哥', '阿根廷', '泰国', '埃及', '南非', '土耳其']
      },
      {
        name: '城市园',
        items: ['北京', '上海', '广州', '深圳', '成都', '杭州', '重庆', '武汉', '西安', '天津', '南京', '苏州', '长沙', '郑州', '青岛', '沈阳', '宁波', '昆明', '东莞', '佛山']
      },
      {
        name: '图书园',
        items: ['红楼梦', '西游记', '三国演义', '水浒传', '百年孤独', '活着', '三体', '哈利波特', '福尔摩斯', '小王子', '围城', '平凡的世界', '白鹿原', '追风筝的人', '解忧杂货店', '挪威的森林', '人间失格', '傲慢与偏见', '简爱', '了不起的盖茨比']
      }
    ]
  },
  'miss-card': {
    title: '小姐牌',
    description: '小姐牌是一款使用扑克牌的酒桌游戏，每张牌都有特定的规则和惩罚。游戏开始时，将扑克牌洗好后分发，玩家根据自己拿到的牌执行相应的动作。',
    rules: [
      '1. 将扑克牌洗好后，牌面向下放在桌子中央',
      '2. 玩家按顺时针顺序轮流抽牌',
      '3. 根据抽到的牌执行相应的规则',
      '4. 游戏可以根据玩家数量和喜好调整规则'
    ],
    cardRules: {
      'A': '指定一人喝一杯',
      '2': '小姐牌：抽到者成为"小姐"，当别人喊"小姐"时，"小姐"必须回应"唉"，否则罚酒一杯',
      '3': '逛三园：抽到者指定一个园子，下一个玩家开始轮流说出园子里的东西',
      '4': '照相机：抽到者喊"照相机"，所有人保持静止，最后一个静止的人罚酒',
      '5': '神经病：抽到者可以做任何奇怪的动作，别人不能笑，笑的人罚酒',
      '6': '逛大街：抽到者指定一个方向，所有人模仿逛街动作，最后一个做的人罚酒',
      '7': '逢7必过：从抽到者开始报数，遇到7或7的倍数说"过"',
      '8': '厕所牌：抽到者可以上厕所，其他人上厕所需要得到"厕所牌"拥有者的同意',
      '9': '自罚一杯',
      '10': '真心话大冒险：抽到者选择真心话或大冒险',
      'J': '左边的人喝一杯',
      'Q': '右边的人喝一杯',
      'K': '摸到K的人可以指定一个规则，直到下一个K出现',
      '小王': '王炸：可以指定任意两个人喝交杯酒',
      '大王': '国王：可以指定任意一个规则，所有人必须遵守'
    }
  }
};

// DOM 加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 初始化 GSAP 动画
  initAnimations();
  
  // 绑定游戏卡片点击事件
  document.querySelectorAll('.game-card').forEach(card => {
    card.addEventListener('click', function() {
      const gameId = this.dataset.game;
      showGameModal(gameId);
    });
  });
  
  // 绑定关闭模态框事件
  closeModal.addEventListener('click', hideGameModal);
  
  // 点击模态框外部关闭
  gameModal.addEventListener('click', function(e) {
    if (e.target === gameModal) {
      hideGameModal();
    }
  });
  
  // 键盘 ESC 关闭模态框
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && !gameModal.classList.contains('hidden')) {
      hideGameModal();
    }
  });
});

// 初始化 GSAP 动画
function initAnimations() {
  // Logo 动画
  gsap.from('.logo-animation', {
    y: -50,
    opacity: 0,
    duration: 1.5,
    ease: 'back.out(1.7)'
  });
  
  // 标题动画
  gsap.from('h1', {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.5,
    ease: 'power2.out'
  });
  
  // 副标题动画
  gsap.from('p', {
    y: 20,
    opacity: 0,
    duration: 1,
    delay: 0.8,
    ease: 'power2.out'
  });
  
  // 游戏卡片动画
  gsap.from('.game-card', {
    y: 50,
    opacity: 0,
    duration: 1,
    stagger: 0.2,
    delay: 1,
    ease: 'power2.out'
  });
  
  // 添加背景动画
  createBackgroundAnimation();
}

// 创建背景动画
function createBackgroundAnimation() {
  const bgAnimation = document.createElement('div');
  bgAnimation.className = 'bg-animation';
  document.body.appendChild(bgAnimation);
}

// 显示游戏模态框
function showGameModal(gameId) {
  try {
    const game = gameData[gameId];
    if (!game) return;
    
    // 根据游戏类型生成不同的内容
    let content = '';
    
    switch(gameId) {
      case 'seven-game':
        content = generateSevenGameContent(game);
        break;
      case 'three-gardens':
        content = generateThreeGardensContent(game);
        break;
      case 'miss-card':
        content = generateMissCardContent(game);
        break;
    }
    
    // 添加返回按钮到内容顶部
    const contentWithBackButton = `
      <div class="mb-6">
        <button id="back-button" class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded-full transition-all duration-300 flex items-center text-sm">
          <i class="fa fa-arrow-left mr-2"></i> 返回游戏列表
        </button>
      </div>
      ${content}
    `;
    
    modalBody.innerHTML = contentWithBackButton;
    
    // 显示模态框
    gameModal.classList.remove('hidden');
    
    // 强制设置模态框内容样式，确保可见
    const modalContent = document.querySelector('.modal-content');
    if (modalContent) {
      modalContent.style.opacity = '1';
      modalContent.style.display = 'block';
    }

    // 添加模态框动画
    gsap.fromTo('.modal-content', 
      {
        scale: 0.8,
        opacity: 0
      },
      {
        scale: 1,
        opacity: 1,
        duration: 0.3,
        ease: 'back.out(1.2)'
      }
    );
    
    // 绑定返回按钮事件 - 确保DOM元素已加载
    setTimeout(() => {
      const backButton = document.getElementById('back-button');
      if (backButton) {
        backButton.addEventListener('click', hideGameModal);
      }
    }, 100);
    
    // 绑定游戏特定的事件
    bindGameEvents(gameId);
  } catch (error) {
    console.error('Error in showGameModal:', error);
    // 如果出错，确保模态框可以关闭
    gameModal.classList.remove('hidden');
    modalBody.innerHTML = `
      <div class="text-center p-8">
        <h3 class="text-2xl font-bold mb-4">出现错误</h3>
        <p class="mb-6">加载游戏时出现问题，请尝试刷新页面或选择其他游戏。</p>
        <button id="error-back-button" class="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-full">
          返回游戏列表
        </button>
      </div>
    `;
    
    document.getElementById('error-back-button').addEventListener('click', hideGameModal);
  }
}

// 隐藏游戏模态框
function hideGameModal() {
  gsap.to('.modal-content', {
    scale: 0.8,
    opacity: 0,
    duration: 0.2,
    ease: 'power2.in',
    onComplete: function() {
      gameModal.classList.add('hidden');
      modalBody.innerHTML = '';
      // 清除动画留下的内联样式，避免下次打开时尺寸不正确
      gsap.set('.modal-content', { clearProps: 'all' });
    }
  });
}

// 生成逢7必过游戏内容
function generateSevenGameContent(game) {
  try {
    // 生成1-100的数字，标记出7的倍数和包含7的数字
    let numbersHtml = '<div class="grid grid-cols-5 sm:grid-cols-10 gap-2 my-6">';
    for (let i = 1; i <= 100; i++) {
      const isSeven = i % 7 === 0 || i.toString().includes('7');
      const className = isSeven ? 'number-highlight number-seven relative' : 'number-highlight number-normal relative';
      const text = isSeven ? '过' : i;
      const cornerMark = isSeven ? `<span class="absolute top-0 right-1 text-[10px] opacity-60">${i}</span>` : '';
      
      numbersHtml += `<div class="${className}">${text}${cornerMark}</div>`;
    }
    numbersHtml += '</div>';
  
    return `
      <div class="text-center mb-8">
        <h2 class="text-4xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-500">${game.title}</h2>
        <p class="text-lg text-gray-300">${game.description}</p>
      </div>
      
      <div class="mb-8">
        <h3 class="text-2xl font-bold mb-4 text-pink-400">游戏规则</h3>
        <ul class="list-none space-y-2 text-gray-300">
          ${game.rules.map(rule => `<li>${rule}</li>`).join('')}
        </ul>
      </div>
      
      <div class="mb-8">
        <h3 class="text-2xl font-bold mb-4 text-pink-400">数字表</h3>
        <p class="text-gray-400 mb-4">以下是1-100的数字表，标红的数字需要说"过"：</p>
        ${numbersHtml}
      </div>
      
      <div class="bg-gray-700 bg-opacity-30 p-4 rounded-lg">
        <p class="text-yellow-300"><i class="fa fa-lightbulb-o mr-2"></i>${game.tips}</p>
      </div>
    `;
  } catch (error) {
    console.error('Error in generateSevenGameContent:', error);
    return '<div class="text-center p-8"><p>加载游戏内容时出错</p></div>';
  }
}

// 生成逛三园游戏内容
function generateThreeGardensContent(game) {
  // 生成园子列表
  let gardensHtml = '';
  game.gardens.forEach(garden => {
    const itemsHtml = garden.items.map(item => `<span class="inline-block px-3 py-1 bg-blue-900 bg-opacity-50 rounded-full m-1 text-sm">${item}</span>`).join('');
    
    gardensHtml += `
      <div class="garden-card">
        <div class="flex justify-between items-center cursor-pointer garden-header">
          <h4 class="text-xl font-bold text-blue-400">${garden.name}</h4>
          <i class="fa fa-chevron-down text-blue-400 transition-transform duration-300"></i>
        </div>
        <div class="garden-items mt-4 hidden">
          <p class="text-gray-300 mb-2">${garden.name}里有：</p>
          <div class="flex flex-wrap">
            ${itemsHtml}
          </div>
        </div>
      </div>
    `;
  });
  
  return `
    <div class="text-center mb-8">
      <h2 class="text-4xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-cyan-500">${game.title}</h2>
      <p class="text-lg text-gray-300">${game.description}</p>
    </div>
    
    <div class="mb-8">
      <h3 class="text-2xl font-bold mb-4 text-blue-400">游戏规则</h3>
      <ul class="list-none space-y-2 text-gray-300">
        ${game.rules.map(rule => `<li>${rule}</li>`).join('')}
      </ul>
    </div>
    
    <div class="mb-8">
      <h3 class="text-2xl font-bold mb-4 text-blue-400">自定义园子</h3>
      <div class="bg-gray-700 bg-opacity-30 p-4 rounded-lg">
        <p class="text-gray-300 mb-4">输入你想逛的园子名称，自动生成园子里的物品：</p>
        <div class="flex gap-2">
          <input type="text" id="custom-garden-input" placeholder="例如：数码、动漫、零食..." class="flex-1 px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500">
          <button id="create-garden-btn" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-300">
            生成
          </button>
        </div>
        <div id="custom-garden-result" class="mt-4 hidden">
          <!-- 动态生成的内容将显示在这里 -->
        </div>
      </div>
    </div>
    
    <div class="mb-8">
      <h3 class="text-2xl font-bold mb-4 text-blue-400">园子列表</h3>
      <p class="text-gray-400 mb-4">点击园子名称展开/收起该园子里的物品：</p>
      ${gardensHtml}
    </div>
  `;
}

// 生成小姐牌游戏内容
function generateMissCardContent(game) {
  // 生成卡牌规则列表
  let cardRulesHtml = '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-6">';
  for (const [card, rule] of Object.entries(game.cardRules)) {
    cardRulesHtml += `
      <div class="bg-purple-900 bg-opacity-30 p-4 rounded-lg border border-purple-500 border-opacity-30">
        <h5 class="text-lg font-bold text-purple-400 mb-2">${card}</h5>
        <p class="text-gray-300">${rule}</p>
      </div>
    `;
  }
  cardRulesHtml += '</div>';
  
  return `
    <div class="text-center mb-8">
      <h2 class="text-4xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-pink-500">${game.title}</h2>
      <p class="text-lg text-gray-300">${game.description}</p>
    </div>
    
    <div class="mb-8">
      <h3 class="text-2xl font-bold mb-4 text-purple-400">游戏规则</h3>
      <ul class="list-none space-y-2 text-gray-300">
        ${game.rules.map(rule => `<li>${rule}</li>`).join('')}
      </ul>
    </div>
    
    <div class="mb-8">
      <div class="flex justify-center mb-6">
        <div class="card-container">
          <div class="card" id="miss-card-element">
            <div class="card-face card-front">
              <!-- 移除文字 -->
            </div>
            <div class="card-face card-back" id="card-back">
              <span id="card-value">?</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="text-center mb-6">
        <button id="draw-card-btn" class="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full text-lg font-bold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 neon-button-purple">
          抽牌
        </button>
        <div class="mt-4">
          <button id="view-rules-btn" class="px-3 py-1 bg-gray-700 text-white rounded-full text-xs hover:bg-gray-600 transition-all duration-300">
            查看规则
          </button>
        </div>
      </div>
      
      <div id="card-result" class="text-center hidden">
        <h4 class="text-2xl font-bold text-purple-400 mb-2">你抽到了：<span id="result-card-value" class="text-white"></span></h4>
        <p class="text-lg text-gray-300" id="result-card-rule"></p>
      </div>
    </div>
    
    <div id="rules-section" class="hidden">
      <h3 class="text-2xl font-bold mb-4 text-purple-400">卡牌规则</h3>
      <p class="text-gray-400 mb-4">每张牌的具体规则如下：</p>
      ${cardRulesHtml}
    </div>
  `;
}

// 绑定游戏特定的事件
function bindGameEvents(gameId) {
  try {
    // 使用setTimeout确保DOM元素已经完全加载
    setTimeout(() => {
      switch(gameId) {
        case 'three-gardens':
          // 绑定园子卡片点击事件
          const gardenHeaders = document.querySelectorAll('.garden-header');
          if (gardenHeaders.length > 0) {
            gardenHeaders.forEach(header => {
              header.addEventListener('click', function() {
                const card = this.parentElement;
                const icon = this.querySelector('i');
                const items = card.querySelector('.garden-items');
                
                card.classList.toggle('active');
                if (card.classList.contains('active')) {
                  icon.style.transform = 'rotate(180deg)';
                  items.classList.remove('hidden');
                } else {
                  icon.style.transform = 'rotate(0)';
                  items.classList.add('hidden');
                }
              });
            });
          }

          // 绑定自定义园子生成事件
          const createGardenBtn = document.getElementById('create-garden-btn');
          const customGardenInput = document.getElementById('custom-garden-input');
          const customGardenResult = document.getElementById('custom-garden-result');

          if (createGardenBtn && customGardenInput && customGardenResult) {
            createGardenBtn.addEventListener('click', function() {
              const keyword = customGardenInput.value.trim();
              if (!keyword) return;

              // 预定义词库
              const gardenDict = {
                '数码': ['手机', '电脑', '平板', '耳机', '键盘', '鼠标', '显示器', '充电宝', '数据线', '相机', '无人机', '路由器', '显卡', '硬盘', '音箱'],
                '动漫': ['海贼王', '火影忍者', '死神', '龙珠', '灌篮高手', '名侦探柯南', '进击的巨人', '鬼灭之刃', '咒术回战', '哆啦A梦', '蜡笔小新', '樱桃小丸子', '千与千寻', '你的名字', '天空之城'],
                '零食': ['薯片', '巧克力', '饼干', '果冻', '糖果', '牛肉干', '辣条', '瓜子', '花生', '核桃', '开心果', '腰果', '碧根果', '夏威夷果', '巴旦木'],
                '汽车': ['奔驰', '宝马', '奥迪', '大众', '丰田', '本田', '日产', '福特', '马自达', '现代', '起亚', '别克', '雪佛兰', '特斯拉', '比亚迪']
              };

              // 1. 优先搜索现有的园子列表
              const existingGarden = gameData['three-gardens'].gardens.find(g => g.name.includes(keyword) || keyword.includes(g.name.replace('园', '')));
              
              if (existingGarden) {
                items = existingGarden.items;
                // 如果用户输入的是简称（如"动物"），我们用完整的名字（"动物园"）
                if (!keyword.includes('园') && existingGarden.name.includes('园')) {
                   // 保持用户输入的关键词，或者使用匹配到的标准名称，这里选择展示匹配到的标准名称更友好
                   // 但为了保持逻辑一致，我们还是显示"自定义"区域，内容取自现有园子
                }
              } else {
                // 2. 搜索预定义扩展词库
                const matchedKey = Object.keys(gardenDict).find(key => keyword.includes(key));
                
                if (matchedKey) {
                  items = gardenDict[matchedKey];
                } else {
                  // 3. 通用/随机生成 (Mock)
                  items = [
                    keyword + '一号', keyword + '大王', '超级' + keyword, '小' + keyword,
                    keyword + '之星', keyword + '侠', keyword + '宝', keyword + '精灵',
                    '金' + keyword, '银' + keyword, '铜' + keyword, '铁' + keyword,
                    keyword + '世界', keyword + '乐园', keyword + '之家'
                  ];
                }
              }

              // 生成HTML
              const itemsHtml = items.map(item => `<span class="inline-block px-3 py-1 bg-green-900 bg-opacity-50 rounded-full m-1 text-sm text-green-300 border border-green-700">${item}</span>`).join('');
              
              customGardenResult.innerHTML = `
                <div class="garden-card active border-green-500 shadow-[0_0_15px_rgba(0,255,0,0.3)] relative">
                  <div class="flex justify-between items-center cursor-default p-0">
                    <h4 class="text-xl font-bold text-green-400">${keyword}园 (自定义)</h4>
                    <button id="close-custom-garden" class="text-gray-400 hover:text-white transition-colors duration-300">
                      <i class="fa fa-times"></i>
                    </button>
                  </div>
                  <div class="garden-items mt-4 block">
                    <p class="text-gray-300 mb-2">${keyword}园里有：</p>
                    <div class="flex flex-wrap">
                      ${itemsHtml}
                    </div>
                  </div>
                </div>
              `;
              customGardenResult.classList.remove('hidden');
              
              // 绑定关闭按钮事件
              document.getElementById('close-custom-garden').addEventListener('click', function() {
                customGardenResult.classList.add('hidden');
                customGardenInput.value = ''; // 可选：清空输入框
              });
              
              // 动画效果
              gsap.from(customGardenResult.firstElementChild, {
                y: 20,
                opacity: 0,
                duration: 0.5,
                ease: 'back.out(1.7)'
              });
            });
          }
          break;
          
        case 'miss-card':
          // 绑定抽牌按钮事件
          const drawCardBtn = document.getElementById('draw-card-btn');
          const viewRulesBtn = document.getElementById('view-rules-btn');
          
          if (drawCardBtn && viewRulesBtn) {
            const rulesSection = document.getElementById('rules-section');
            const cardResult = document.getElementById('card-result');
            const cardElement = document.getElementById('miss-card-element');
            const cardValue = document.getElementById('card-value');
            const resultCardValue = document.getElementById('result-card-value');
            const resultCardRule = document.getElementById('result-card-rule');
            
            // 卡牌数组
            const cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', '小王', '大王'];
            
            drawCardBtn.addEventListener('click', function() {
              try {
                // 重置卡牌状态
                cardElement.classList.remove('flipped');
                cardResult.classList.add('hidden');
                
                // 随机抽取一张牌
                setTimeout(() => {
                  const randomCard = cards[Math.floor(Math.random() * cards.length)];
                  cardValue.textContent = randomCard;
                  cardElement.classList.add('flipped');
                  
                  // 显示结果
                  setTimeout(() => {
                    resultCardValue.textContent = randomCard;
                    resultCardRule.textContent = gameData['miss-card'].cardRules[randomCard];
                    cardResult.classList.remove('hidden');
                    
                    // 添加结果动画
                    gsap.from('#card-result', {
                      y: 20,
                      opacity: 0,
                      duration: 0.5,
                      ease: 'power2.out'
                    });
                  }, 600);
                }, 300);
              } catch (error) {
                console.error('Error in draw card:', error);
              }
            });
            
            viewRulesBtn.addEventListener('click', function() {
              try {
                rulesSection.classList.toggle('hidden');
                
                if (!rulesSection.classList.contains('hidden')) {
                  // 添加规则区域动画
                  gsap.from('#rules-section', {
                    y: 20,
                    opacity: 0,
                    duration: 0.5,
                    ease: 'power2.out'
                  });
                }
              } catch (error) {
                console.error('Error in view rules:', error);
              }
            });
          }
          break;
      }
    }, 200);
  } catch (error) {
    console.error('Error in bindGameEvents:', error);
  }
}