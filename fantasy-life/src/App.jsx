import React, { useState, useEffect } from 'react';
import { generateFantasyStart, generateRomanceStart, generateNextEvent } from './api';
import { 
  Settings, Play, Skull, Trophy, Star, ChevronRight, 
  Shield, Sword, Brain, Activity, Copy, Check, 
  Heart, User, Sparkles, Wand2, Users
} from 'lucide-react';

function App() {
  const [apiKey, setApiKey] = useState(localStorage.getItem('deepseek_api_key') || '');
  const [completedLives, setCompletedLives] = useState(parseInt(localStorage.getItem('completed_lives') || '0'));
  const [showSettings, setShowSettings] = useState(false);
  const [gameState, setGameState] = useState('idle'); // idle, picking_gender, playing, gameover
  const [gameMode, setGameMode] = useState(null); // fantasy, romance
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [world, setWorld] = useState(null);
  const [player, setPlayer] = useState(null);
  const [currentEvent, setCurrentEvent] = useState(null);
  const [storyHistory, setStoryHistory] = useState([]);
  const [ending, setEnding] = useState(null);
  const [copied, setCopied] = useState(false);
  const [targets, setTargets] = useState([]);

  useEffect(() => {
    const anchor = document.getElementById('scroll-anchor');
    if (anchor) {
      anchor.scrollIntoView({ behavior: 'smooth' });
    }
  }, [storyHistory, loading]);

  const saveApiKey = (key) => {
    setApiKey(key);
    localStorage.setItem('deepseek_api_key', key);
    setShowSettings(false);
  };

  const initGameMode = (mode) => {
    if (!apiKey) {
      setShowSettings(true);
      return;
    }
    setGameMode(mode);
    if (mode === 'romance') {
      setGameState('picking_gender');
    } else {
      startFantasyGame();
    }
  };

  const startFantasyGame = async () => {
    setLoading(true);
    setError(null);
    setGameState('playing');
    setStoryHistory([]);
    setEnding(null);
    setCopied(false);

    try {
      const data = await generateFantasyStart(apiKey);
      setWorld(data.world);
      setPlayer(data.player);
      setCurrentEvent(data.event);
      setStoryHistory([
        { type: 'system', text: '你穿越到了' + data.world.theme + '。这里' + data.world.description },
        { type: 'system', text: '你的身份是：' + data.player.profession },
        { type: 'event', text: data.event.description }
      ]);
    } catch (err) {
      setError(err.message || '生成游戏失败，请检查API Key或网络。');
      setGameState('idle');
    } finally {
      setLoading(false);
    }
  };

  const startRomanceGame = async (gender) => {
    setLoading(true);
    setError(null);
    setGameState('playing');
    setStoryHistory([]);
    setEnding(null);
    setCopied(false);

    try {
      const data = await generateRomanceStart(apiKey, gender);
      setPlayer(data.profile);
      setTargets(data.targets);
      setCurrentEvent(data.event);
      setStoryHistory([
        { type: 'system', text: '你出生在现实世界的某个角落。当前阶段：' + data.profile.stage },
        { type: 'system', text: '你的背景：' + data.profile.background },
        { type: 'event', text: data.event.description }
      ]);
    } catch (err) {
      setError(err.message || '生成游戏失败，请检查API Key或网络。');
      setGameState('idle');
    } finally {
      setLoading(false);
    }
  };

  const handleChoice = async (choiceId) => {
    if (loading || gameState !== 'playing') return;

    const choiceText = currentEvent.choices.find(c => c.id === choiceId)?.text || '';
    setStoryHistory(prev => [...prev, { type: 'choice', text: '> 你选择了：' + choiceText }]);
    setLoading(true);
    setError(null);

    try {
      const data = await generateNextEvent(apiKey, { world, player, currentEvent, targets }, choiceId, gameMode);
      
      setStoryHistory(prev => [...prev, { type: 'outcome', text: data.outcomeText }]);
      
      if (data.updatedPlayer) {
        setPlayer(prev => ({
          ...prev,
          ...data.updatedPlayer
        }));
      }

      if (data.isEnding) {
        setGameState('gameover');
        setEnding(data.endingType);
        setStoryHistory(prev => [...prev, { type: 'ending', text: '结局达成：' + data.endingType }]);
        
        const newLives = completedLives + 1;
        setCompletedLives(newLives);
        localStorage.setItem('completed_lives', newLives.toString());
      } else {
        setCurrentEvent(data.nextEvent);
        setStoryHistory(prev => [...prev, { type: 'event', text: data.nextEvent.description }]);
      }
    } catch (err) {
      setError(err.message || '生成后续剧情失败，请重试。');
      setStoryHistory(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const copyStory = () => {
    const fullStory = storyHistory.map(line => line.text).join('\n\n');
    navigator.clipboard.writeText(fullStory);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-sans p-4 md:p-8">
      <div className="max-w-5xl mx-auto relative">
        
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 flex items-center gap-2 cursor-pointer" onClick={() => setGameState('idle')}>
            <Sparkles className="text-yellow-400" />
            模拟人生
          </h1>
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-1.5 bg-gray-900 px-3 py-1 rounded-full border border-gray-800">
              <span className="text-xs text-gray-500">已历经轮回:</span>
              <span className="text-sm font-bold text-purple-400">{completedLives}</span>
            </div>
            <button onClick={() => setShowSettings(true)} className="p-2 rounded-full hover:bg-gray-800 transition-colors">
              <Settings className="text-gray-500 hover:text-white" />
            </button>
          </div>
        </header>

        {error && (
          <div className="bg-red-900/20 border border-red-500/50 text-red-200 p-4 rounded-xl mb-6 flex items-center gap-3">
            <Activity className="w-5 h-5 text-red-500" />
            {error}
          </div>
        )}

        {gameState === 'idle' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 py-10">
            {/* Fantasy Card */}
            <div className="group bg-gray-900 rounded-3xl border border-gray-800 p-8 hover:border-purple-500/50 transition-all cursor-pointer shadow-2xl relative overflow-hidden" onClick={() => initGameMode('fantasy')}>
              <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/10 blur-3xl -mr-10 -mt-10 group-hover:bg-purple-600/20 transition-all"></div>
              <div className="bg-purple-900/30 p-4 rounded-2xl w-fit mb-6">
                <Wand2 className="w-8 h-8 text-purple-400" />
              </div>
              <h2 className="text-3xl font-bold mb-4">奇幻人生</h2>
              <p className="text-gray-400 leading-relaxed mb-8">
                穿越到未知的模拟世界。可能是微观细胞都市，也可能是由书籍构成的图书馆位面。在硬核的生存挑战中，利用荒诞的物品改写命运。
              </p>
              <div className="flex items-center text-purple-400 font-bold group-hover:translate-x-2 transition-transform">
                开启轮回 <ChevronRight className="w-5 h-5" />
              </div>
            </div>

            {/* Romance Card */}
            <div className="group bg-gray-900 rounded-3xl border border-gray-800 p-8 hover:border-pink-500/50 transition-all cursor-pointer shadow-2xl relative overflow-hidden" onClick={() => initGameMode('romance')}>
              <div className="absolute top-0 right-0 w-32 h-32 bg-pink-600/10 blur-3xl -mr-10 -mt-10 group-hover:bg-pink-600/20 transition-all"></div>
              <div className="bg-pink-900/30 p-4 rounded-2xl w-fit mb-6">
                <Heart className="w-8 h-8 text-pink-400" />
              </div>
              <h2 className="text-3xl font-bold mb-4">恋爱模拟</h2>
              <p className="text-gray-400 leading-relaxed mb-8">
                在现实的平行时空中，体验不同人生阶段的情感羁绊。与各具特色的对象相遇，在心动与抉择之间，书写属于你的浪漫篇章。
              </p>
              <div className="flex items-center text-pink-400 font-bold group-hover:translate-x-2 transition-transform">
                寻找真爱 <ChevronRight className="w-5 h-5" />
              </div>
            </div>
          </div>
        )}

        {gameState === 'picking_gender' && (
          <div className="flex flex-col items-center justify-center py-20 bg-gray-900 rounded-3xl border border-gray-800 shadow-xl">
            <h2 className="text-2xl font-bold mb-8">选择你的身份性别</h2>
            <div className="flex gap-6">
              <button onClick={() => startRomanceGame('male')} className="flex flex-col items-center gap-4 p-8 bg-gray-800 hover:bg-blue-900/30 border border-gray-700 hover:border-blue-500 rounded-3xl transition-all group">
                <div className="p-4 bg-blue-900/20 rounded-2xl group-hover:scale-110 transition-transform"><User className="w-10 h-10 text-blue-400" /></div>
                <span className="font-bold text-lg">男性视角</span>
              </button>
              <button onClick={() => startRomanceGame('female')} className="flex flex-col items-center gap-4 p-8 bg-gray-800 hover:bg-pink-900/30 border border-gray-700 hover:border-pink-500 rounded-3xl transition-all group">
                <div className="p-4 bg-pink-900/20 rounded-2xl group-hover:scale-110 transition-transform"><User className="w-10 h-10 text-pink-400" /></div>
                <span className="font-bold text-lg">女性视角</span>
              </button>
            </div>
          </div>
        )}

        {(gameState === 'playing' || gameState === 'gameover') && player && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            {/* Sidebar */}
            <div className="lg:col-span-1 space-y-6">
              <div className="bg-gray-900 p-6 rounded-3xl border border-gray-800 sticky top-8">
                {gameMode === 'fantasy' ? (
                  <>
                    <h3 className="text-xl font-bold mb-1 text-purple-400">{world?.theme}</h3>
                    <p className="text-sm text-gray-500 mb-6">{player.profession}</p>
                    <div className="grid grid-cols-2 gap-3 mb-6">
                      <StatItem icon={<Brain />} label="智力" value={player.stats.intelligence} color="blue" />
                      <StatItem icon={<Activity />} label="敏捷" value={player.stats.agility} color="green" />
                      <StatItem icon={<Sword />} label="力量" value={player.stats.strength} color="red" />
                      <StatItem icon={<Shield />} label="耐力" value={player.stats.endurance} color="yellow" />
                    </div>
                  </>
                ) : (
                  <>
                    <h3 className="text-xl font-bold mb-1 text-pink-400">{player.stage}</h3>
                    <p className="text-xs text-gray-500 mb-6 line-clamp-2 hover:line-clamp-none cursor-help transition-all" title={player.background}>
                      {player.background}
                    </p>
                    <div className="grid grid-cols-2 gap-3 mb-6">
                      <StatItem icon={<Sparkles />} label="魅力" value={player.stats.charm} color="pink" />
                      <StatItem icon={<Trophy />} label="财富" value={player.stats.wealth} color="yellow" />
                      <StatItem icon={<Brain />} label="情商" value={player.stats.emotional_iq} color="purple" />
                      <StatItem icon={<User />} label="颜值" value={player.stats.appearance} color="blue" />
                    </div>
                  </>
                )}

                {gameMode === 'fantasy' && player.skills?.length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-[10px] font-black text-gray-600 uppercase tracking-widest mb-3">技能</h4>
                    <div className="space-y-2">
                      {player.skills.map((s, i) => (
                        <div key={i} className="bg-gray-800/50 p-3 rounded-xl border border-gray-800">
                          <div className="font-bold text-xs text-purple-300">{s.name}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {gameMode === 'romance' && targets?.length > 0 && (
                  <div className="mb-6">
                    <h4 className="text-[10px] font-black text-gray-600 uppercase tracking-widest mb-3 flex items-center gap-1">
                      <Users className="w-3 h-3" /> 潜在对象
                    </h4>
                    <div className="space-y-2">
                      {targets.map((t, i) => (
                        <div key={i} className="bg-gray-800/50 p-3 rounded-xl border border-gray-800 group relative">
                          <div className="font-bold text-xs text-pink-300">{t.name}</div>
                          <div className="hidden group-hover:block absolute left-0 lg:left-full top-full lg:top-0 mt-2 lg:mt-0 lg:ml-4 w-64 p-4 bg-gray-900 border border-pink-500/30 rounded-2xl z-50 text-xs text-gray-300 shadow-2xl pointer-events-none backdrop-blur-xl">
                            <div className="text-pink-400 font-bold mb-1">{t.name}</div>
                            {t.description}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Main Content */}
            <div className="lg:col-span-3 flex flex-col h-[75vh] lg:h-auto lg:min-h-[80vh]">
              <div className="bg-gray-900 rounded-t-3xl border border-gray-800 p-8 flex-1 overflow-y-auto space-y-6">
                {storyHistory.map((line, i) => (
                  <div key={i} className={`p-5 rounded-2xl transition-all ${
                    line.type === 'system' ? 'bg-blue-500/5 text-blue-300/80 text-sm italic text-center border border-blue-500/10' :
                    line.type === 'event' ? 'bg-gray-800/40 text-gray-100 text-lg leading-relaxed border-l-4 border-purple-500 shadow-sm' :
                    line.type === 'choice' ? 'text-gray-500 pl-4 border-l border-gray-800 ml-2' :
                    line.type === 'outcome' ? 'bg-purple-500/5 text-purple-200 border border-purple-500/10' :
                    'bg-gradient-to-r from-yellow-900/20 to-amber-900/20 text-yellow-400 text-center font-black text-2xl py-10 rounded-3xl border border-yellow-500/20'
                  }`}>
                    {line.text}
                  </div>
                ))}
                
                {loading && (
                  <div className="flex items-center gap-3 text-gray-600 p-5 animate-pulse">
                    <Activity className="animate-spin w-5 h-5" />
                    <span className="text-sm font-medium tracking-widest uppercase">命运推演中...</span>
                  </div>
                )}

                {gameState === 'gameover' && (
                  <div className="mt-10 pt-10 border-t border-gray-800">
                    <div className="flex items-center justify-between mb-6">
                      <h4 className="text-lg font-bold text-gray-500 flex items-center gap-2">
                        <Sparkles className="w-5 h-5" /> 人生回忆录
                      </h4>
                      <button onClick={copyStory} className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-xl text-xs font-bold text-gray-300 transition-all">
                        {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
                        {copied ? '已存入档案' : '备份这段人生'}
                      </button>
                    </div>
                    <div className="bg-gray-950 p-8 rounded-3xl text-gray-500 text-sm leading-loose whitespace-pre-wrap max-h-80 overflow-y-auto italic border border-gray-800 shadow-inner">
                      {storyHistory.map(line => line.text).join('\n\n')}
                    </div>
                  </div>
                )}
                <div id="scroll-anchor" />
              </div>

              <div className="bg-gray-900 p-8 rounded-b-3xl border border-gray-800 border-t-0 shadow-2xl">
                {gameState === 'playing' && currentEvent && !loading && (
                  <div className="grid grid-cols-1 gap-3">
                    {currentEvent.choices.map((choice) => (
                      <button
                        key={choice.id}
                        onClick={() => handleChoice(choice.id)}
                        className="w-full text-left p-5 rounded-2xl bg-gray-800/50 hover:bg-gray-800 border border-gray-800 hover:border-purple-500/50 transition-all flex items-center justify-between group shadow-sm"
                      >
                        <div className="flex flex-col gap-1">
                          <span className="text-gray-300 group-hover:text-white transition-colors">{choice.text}</span>
                          {choice.requirement && (
                            <span className="text-[10px] font-black text-amber-500/60 uppercase tracking-widest">
                              Requirement: {choice.requirement}
                            </span>
                          )}
                        </div>
                        <ChevronRight className="w-5 h-5 text-gray-700 group-hover:text-purple-400 group-hover:translate-x-1 transition-all shrink-0" />
                      </button>
                    ))}
                  </div>
                )}

                {gameState === 'gameover' && (
                  <div className="flex flex-col items-center gap-6 pt-4">
                    <div className="flex items-center gap-3 text-3xl font-black text-yellow-500 drop-shadow-lg">
                      {ending?.includes('失败') || ending?.includes('死亡') ? <Skull className="w-10 h-10" /> : <Trophy className="w-10 h-10" />}
                      {ending || '尘埃落定'}
                    </div>
                    <button onClick={() => setGameState('idle')} className="px-10 py-4 bg-white text-black rounded-full font-black hover:scale-105 transition-transform shadow-xl">
                      重返轮回
                    </button>
                  </div>
                )}
              </div>
            </div>

          </div>
        )}

        {showSettings && (
          <div className="fixed inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-gray-900 rounded-3xl p-8 w-full max-w-md border border-gray-800 shadow-2xl">
              <h2 className="text-2xl font-black mb-8 flex items-center gap-3">
                <Settings className="text-gray-500" /> 系统设置
              </h2>
              <div className="space-y-6">
                <div>
                  <label className="block text-xs font-black text-gray-500 uppercase tracking-widest mb-3">DeepSeek API Key</label>
                  <input
                    type="password"
                    defaultValue={apiKey}
                    id="apikey-input"
                    className="w-full bg-gray-950 border border-gray-800 rounded-2xl px-5 py-4 text-white focus:outline-none focus:border-purple-500 transition-all font-mono"
                    placeholder="sk-..."
                  />
                </div>
                <div className="flex justify-end gap-3 pt-4">
                  <button onClick={() => setShowSettings(false)} className="px-6 py-3 rounded-2xl text-gray-500 font-bold hover:text-white transition-colors">取消</button>
                  <button onClick={() => saveApiKey(document.getElementById('apikey-input').value)} className="px-8 py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-2xl transition-all font-bold shadow-lg shadow-purple-900/20">应用配置</button>
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

function StatItem({ icon, label, value, color }) {
  const colorMap = {
    blue: 'text-blue-400 bg-blue-400/10',
    green: 'text-green-400 bg-green-400/10',
    red: 'text-red-400 bg-red-400/10',
    yellow: 'text-yellow-400 bg-yellow-400/10',
    pink: 'text-pink-400 bg-pink-400/10',
    purple: 'text-purple-400 bg-purple-400/10',
  };
  
  return (
    <div className="bg-gray-800/30 p-3 rounded-2xl border border-gray-800/50 flex items-center gap-3">
      <div className={`p-2 rounded-xl ${colorMap[color]}`}>
        {React.cloneElement(icon, { size: 16 })}
      </div>
      <div>
        <div className="text-[10px] text-gray-600 font-black uppercase tracking-tighter">{label}</div>
        <div className="font-bold text-sm leading-none">{value}</div>
      </div>
    </div>
  );
}

export default App;
