export const generateFantasyStart = async (apiKey) => {
  const prompt = `
你是一个极具创意和想象力的文字冒险游戏引擎。当前游戏主题是"奇幻人生"。
**核心任务**：
玩家每次点击开始游戏，你必须生成一个**绝对独特且不可预测**的模拟世界。

**随机化要求**：
1. **世界主题**：不要总是停留在常见的题材。你可以选择：
   - 极微观世界、抽象/超现实世界、异类文明、经典题材的独特变体等。
   - **严禁**：不要每次都默认生成蒸汽朋克或中世纪。
2. **职业与技能**：职业必须高度适配当前世界观，但技能可以出其不意。
3. **随机物品**：生成三件物品。物品可以不符合世界主题，甚至可以是非常荒诞的。不要总是生成药水或武器。
4. **属性分配**：智力、敏捷、力量、耐力（0-10）。

**第一个事件**：
- 包含一个引人入胜的开场和3个选项。
- **硬核生存模式**：普通选项失败率 30%，挑战选项失败率 60%+。

请必须返回纯JSON格式数据。JSON结构如下：
{
  "world": { "theme": "世界主题名称", "description": "对这个世界的极具画面感的描述" },
  "player": {
    "profession": "职业名称",
    "skills": [{ "name": "技能名", "description": "技能描述" }],
    "stats": { "intelligence": 5, "agility": 5, "strength": 5, "endurance": 5 },
    "items": [{ "id": "item1", "name": "物品名", "description": "物品描述", "reusable": true, "used": false }]
  },
  "event": {
    "description": "第一个事件的描述",
    "choices": [{ "id": "c1", "text": "选项1描述", "requirement": "力量 > 7" }, { "id": "c2", "text": "选项2描述", "requirement": null }, { "id": "c3", "text": "选项3描述", "requirement": null }]
  }
}
`;
  return await callDeepSeek(apiKey, prompt, 1.3);
};

export const generateRomanceStart = async (apiKey, gender) => {
  const prompt = `
你是一个情感细腻、文笔优美的文字冒险游戏引擎。当前游戏主题是"恋爱模拟"。
玩家选择的性别是：${gender === 'male' ? '男性' : '女性'}。

**核心任务**：
1. **人生阶段**：为玩家随机生成一个现实的人生阶段（18-35岁），如大学生、职场新人、自由职业者、无业游民等。
2. **个人背景**：随机生成一个家庭背景（富二代、家境贫寒、普通家庭等）和个人特质。
3. **恋爱对象**：随机生成三个各具特色的潜在恋爱对象，描述他们的外貌、气质、性格和背景。
4. **第一个事件**：根据当前身份，生成一个与其中一个或多个对象相遇或互动的开场事件。

**选项规则**：
- 提供3个选项。
- 选项应体现不同的性格导向（如：直球、含蓄、幽默、冷漠等）。

请必须返回纯JSON格式数据。JSON结构如下：
{
  "profile": {
    "stage": "人生阶段",
    "background": "个人背景描述",
    "stats": { "charm": 5, "wealth": 5, "emotional_iq": 5, "appearance": 5 }
  },
  "targets": [
    { "id": "t1", "name": "姓名", "description": "外貌、气质、性格和背景的详细描述" },
    { "id": "t2", "name": "姓名", "description": "描述" },
    { "id": "t3", "name": "姓名", "description": "描述" }
  ],
  "event": {
    "description": "开场事件描述",
    "choices": [
      { "id": "c1", "text": "选项1描述" },
      { "id": "c2", "text": "选项2描述" },
      { "id": "c3", "text": "选项3描述" }
    ]
  }
}
`;
  return await callDeepSeek(apiKey, prompt, 1.1);
};

export const generateNextEvent = async (apiKey, gameState, choiceId, gameMode) => {
  const choiceText = gameState.currentEvent.choices.find(c => c.id === choiceId)?.text || '';
  const modeContext = gameMode === 'fantasy' 
    ? `世界：${gameState.world.theme}，职业：${gameState.player.profession}`
    : `身份：${gameState.player.stage}，背景：${gameState.player.background}`;

  const prompt = `
你是一个文字冒险游戏引擎。当前游戏模式是：${gameMode === 'fantasy' ? '奇幻人生' : '恋爱模拟'}。
当前状态：${modeContext}
玩家选择的应对方式：${choiceText}

**推演要求**：
1. **奇幻模式**：保持硬核，高失败率，后果严重。
2. **恋爱模式**：注重情感互动、好感度变化、修罗场或甜蜜时刻。
3. **通用规则**：合理推演结果，生成下一个事件（带3个选项），或判定结局。

请必须返回纯JSON格式数据。JSON结构如下：
{
  "outcomeText": "对玩家选择结果的详细描述",
  "isEnding": false,
  "endingType": "结局类型",
  "updatedPlayer": { ... },
  "nextEvent": {
    "description": "下一个事件",
    "choices": [
      { "id": "c1", "text": "选项1", "requirement": "可选要求" },
      { "id": "c2", "text": "选项2" },
      { "id": "c3", "text": "选项3" }
    ]
  }
}
`;
  return await callDeepSeek(apiKey, prompt, 1.0);
};

async function callDeepSeek(apiKey, prompt, temperature = 1.0) {
  try {
    const response = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: 'You are a helpful assistant that outputs JSON.' },
          { role: 'user', content: prompt }
        ],
        response_format: { type: 'json_object' },
        temperature: temperature
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    let content = data.choices[0].message.content.trim();
    if (content.startsWith('```json')) {
      content = content.replace(/^```json/, '').replace(/```$/, '').trim();
    } else if (content.startsWith('```')) {
      content = content.replace(/^```/, '').replace(/```$/, '').trim();
    }
    return JSON.parse(content);
  } catch (error) {
    console.error("DeepSeek API Error:", error);
    throw error;
  }
}
