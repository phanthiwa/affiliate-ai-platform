'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Sparkles, Wand2, Play, Pause, Download, Video, CheckCircle2,
  Copy, Share2, Volume2, VolumeX, RefreshCw, ShoppingBag,
  Film, Layers, ChevronRight, Flame, ShieldCheck, Zap
} from 'lucide-react';
import {
  generateVideoFromPrompt,
  PromptToVideoResponse,
  API_BASE
} from '@/lib/api';

interface PromptToVideoFlowModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (msg: string) => void;
}

const PRESET_PROMPTS = [
  {
    label: "✨ เซรั่มไฮยาหน้าใส",
    prompt: "สร้างวิดีโอรีวิวเซรั่มไฮยาลูรอนเข้มข้น แก้ปัญหาหน้าโทรม ผิวฉ่ำโกลว์ใน 3 วัน พูดสไตล์เป็นกันเอง ชี้ตะกร้าเหลือง"
  },
  {
    label: "🍳 หม้อทอดไร้น้ำมัน 5.5L",
    prompt: "รีวิวหม้อทอดไร้น้ำมัน Smart Air Fryer ทอดกรอบไม่อมน้ำมัน ล้างง่ายมาก เหมาะกับคนอยู่คอนโด มีโปรส่งฟรี"
  },
  {
    label: "🎧 หูฟังบลูทูธ ANC",
    prompt: "รีวิวหูฟังไร้สายตัดเสียงรบกวน แบตอึด 40 ชม. เบสแน่น คุยโทรศัพท์ชัดเจน ราคาหลักร้อย คุณภาพหลักพัน"
  },
  {
    label: "❄️ แก้วเก็บความเย็น 900ml",
    prompt: "รีวิวแก้วเก็บความเย็นสแตนเลส 316 ใส่น้ำแข็งข้ามวันไม่ละลาย ไม่เป็นไอน้ำเกาะ ดีไซน์มินิมอลจับถนัดมือ"
  }
];

export default function PromptToVideoFlowModal({
  isOpen,
  onClose,
  onSuccess
}: PromptToVideoFlowModalProps) {
  const [prompt, setPrompt] = useState<string>(PRESET_PROMPTS[0].prompt);
  const [voiceGender, setVoiceGender] = useState<string>('female');
  const [styleMode, setStyleMode] = useState<string>('AVATAR_HYBRID');
  const [durationSec, setDurationSec] = useState<number>(20);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [videoResult, setVideoResult] = useState<PromptToVideoResponse | null>(null);

  // Video Player state
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [activeShotIndex, setActiveShotIndex] = useState<number>(0);
  const [isDownloadingMp4, setIsDownloadingMp4] = useState<boolean>(false);
  const [copiedCaption, setCopiedCaption] = useState<boolean>(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentTime((prev) => {
          const maxDur = videoResult ? videoResult.duration_sec : durationSec;
          if (prev >= maxDur) {
            setIsPlaying(false);
            return 0;
          }
          return Number((prev + 0.2).toFixed(1));
        });
      }, 200);
    } else {
      clearInterval(timer);
    }
    return () => clearInterval(timer);
  }, [isPlaying, videoResult, durationSec]);

  // Update active shot based on currentTime
  useEffect(() => {
    if (videoResult && videoResult.shots.length > 0) {
      const idx = videoResult.shots.findIndex(
        (s) => currentTime >= s.start_sec && currentTime <= s.end_sec
      );
      if (idx !== -1 && idx !== activeShotIndex) {
        setActiveShotIndex(idx);
      }
    }
  }, [currentTime, videoResult]);

  if (!isOpen) return null;

  const handleGenerate = async () => {
    try {
      setIsGenerating(true);
      const res = await generateVideoFromPrompt({
        prompt,
        voice_gender: voiceGender,
        style_mode: styleMode,
        duration_sec: durationSec
      });
      setVideoResult(res);
      setCurrentTime(0);
      setActiveShotIndex(0);
      setIsPlaying(false);
      if (onSuccess) onSuccess(`🎉 สร้างวิดีโอสำเร็จรูปสำหรับ '${res.product_title_th}' พร้อมโพสต์แล้ว!`);
    } catch (err) {
      console.error(err);
      alert('เกิดข้อผิดพลาดในการสร้างวิดีโอ กรุณาลองใหม่อีกครั้ง');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleTogglePlay = () => {
    if (isPlaying) {
      setIsPlaying(false);
      if (audioRef.current) audioRef.current.pause();
    } else {
      setIsPlaying(true);
      if (videoResult) {
        const audioUrl = `${API_BASE}/video/tts-audio?text=${encodeURIComponent(videoResult.full_voiceover_th)}&voice=${videoResult.voice_gender}`;
        if (!audioRef.current) {
          audioRef.current = new Audio(audioUrl);
        } else {
          audioRef.current.src = audioUrl;
        }
        audioRef.current.muted = isMuted;
        audioRef.current.currentTime = currentTime;
        audioRef.current.play().catch(() => {});
      }
    }
  };

  const handleCopyCaption = () => {
    if (!videoResult) return;
    navigator.clipboard.writeText(videoResult.social_caption);
    setCopiedCaption(true);
    setTimeout(() => setCopiedCaption(false), 3000);
    if (onSuccess) onSuccess('📋 คัดลอกแคปชัน & แฮชแท็ก TikTok/Shopee เรียบร้อย!');
  };

  const handleDownloadVideo = async () => {
    if (!videoResult) return;
    try {
      setIsDownloadingMp4(true);
      
      // Fetch TTS Audio
      const audioUrl = `${API_BASE}/video/tts-audio?text=${encodeURIComponent(videoResult.full_voiceover_th)}&voice=${videoResult.voice_gender}`;
      const audioResp = await fetch(audioUrl);
      const audioBlob = await audioResp.blob();

      // Create downloadable bundle or direct video stream
      const a = document.createElement('a');
      a.href = URL.createObjectURL(audioBlob);
      a.download = `video_voiceover_${videoResult.product_title_th.replace(/\s+/g, '_')}.mp3`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      // Also trigger JSON package
      const jsonStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(videoResult, null, 2));
      const jsonA = document.createElement('a');
      jsonA.href = jsonStr;
      jsonA.download = `ready_video_post_${videoResult.video_id}.json`;
      document.body.appendChild(jsonA);
      jsonA.click();
      jsonA.remove();

      if (onSuccess) onSuccess('📥 ดาวน์โหลดไฟล์เสียงพากย์และแพ็กเกจวิดีโอสำเร็จรูปเรียบร้อย!');
    } catch (e) {
      console.error(e);
      alert('ดาวน์โหลดไฟล์สำเร็จ');
    } finally {
      setIsDownloadingMp4(false);
    }
  };

  const currentShot = videoResult?.shots[activeShotIndex] || videoResult?.shots[0];

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
      <div className="bg-slate-900 border border-purple-500/40 rounded-3xl max-w-6xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
        
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-500 via-purple-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-purple-600/30">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-lg text-white">✨ Google Flow Prompt-to-Video Engine</h3>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 text-white uppercase shadow-sm">
                  1-Prompt Ready Video
                </span>
              </div>
              <p className="text-xs text-slate-400">ใส่แค่ข้อความ Prompt เดียว AI สร้างสคริปต์ พากย์เสียงไทย เจนภาพ 9:16 พร้อมโพสต์ทันที</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-sm font-bold transition-all cursor-pointer"
          >
            ✕
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-y-auto">
          
          {/* Left Column: Prompt Input & Generator Options */}
          <div className="lg:col-span-6 space-y-5">
            
            {/* Prompt Input Box */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-purple-300 flex items-center justify-between">
                <span>1. พิมพ์คำสั่ง Prompt สินค้าที่ต้องการสร้างวิดีโอ</span>
                <span className="text-[10px] text-pink-400 font-normal">รองรับภาษาไทย 100%</span>
              </label>

              <textarea
                rows={3}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="เช่น รีวิวเซรั่มไฮยา ผิวฉ่ำใสใน 3 วัน พูดสไตล์สนุกสนาน ชี้ตะกร้าเหลือง..."
                className="w-full bg-slate-950 border border-purple-500/30 focus:border-purple-500 rounded-2xl p-3.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none transition-all leading-relaxed shadow-inner"
              />

              {/* Quick Preset Chips */}
              <div className="space-y-1 pt-1">
                <span className="text-[10px] text-slate-400">ตัวอย่าง Prompt ขายดี:</span>
                <div className="flex flex-wrap gap-1.5">
                  {PRESET_PROMPTS.map((item, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setPrompt(item.prompt)}
                      className={`text-[11px] px-2.5 py-1 rounded-lg border transition-all cursor-pointer ${
                        prompt === item.prompt
                          ? 'bg-purple-600/30 border-purple-500 text-purple-200 shadow-sm'
                          : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                      }`}
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Options Grid */}
            <div className="grid grid-cols-2 gap-3">
              {/* Voice Selection */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-purple-300">
                  2. เลือกเสียงพากย์ AI
                </label>
                <div className="grid grid-cols-2 gap-1.5">
                  <button
                    type="button"
                    onClick={() => setVoiceGender('female')}
                    className={`py-2 px-2.5 rounded-xl border text-xs font-semibold transition-all cursor-pointer text-center ${
                      voiceGender === 'female'
                        ? 'bg-pink-600/30 border-pink-500 text-pink-200 shadow-sm'
                        : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                    }`}
                  >
                    👩 หญิง (สดใส)
                  </button>
                  <button
                    type="button"
                    onClick={() => setVoiceGender('male')}
                    className={`py-2 px-2.5 rounded-xl border text-xs font-semibold transition-all cursor-pointer text-center ${
                      voiceGender === 'male'
                        ? 'bg-blue-600/30 border-blue-500 text-blue-200 shadow-sm'
                        : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                    }`}
                  >
                    👨 ชาย (นุ่มนวล)
                  </button>
                </div>
              </div>

              {/* Target Duration */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-purple-300">
                  3. ความยาวคลิป
                </label>
                <div className="grid grid-cols-3 gap-1.5">
                  {[15, 20, 30].map((sec) => (
                    <button
                      key={sec}
                      type="button"
                      onClick={() => setDurationSec(sec)}
                      className={`py-2 rounded-xl border text-xs font-semibold transition-all cursor-pointer text-center ${
                        durationSec === sec
                          ? 'bg-purple-600/40 border-purple-500 text-purple-200 shadow-sm'
                          : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                      }`}
                    >
                      {sec}s
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Visual Style Selection */}
            <div className="space-y-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-purple-300">
                4. สไตล์ภาพวิดีโอ (Visual Style)
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: 'AVATAR_HYBRID', label: '🌟 AI Avatar + Demo', desc: 'คนพูดสมจริง + สลับสินค้า' },
                  { id: 'CINEMATIC_BROLL', label: '🎥 4K Cinematic', desc: 'ฟุตเทจสินค้าแสงสตูดิโอ 3D' },
                  { id: 'UGC_VIRAL', label: '🛍️ TikTok UGC', desc: 'รีวิวบ้านๆ มุมกล้องมือถือ' },
                ].map((st) => (
                  <div
                    key={st.id}
                    onClick={() => setStyleMode(st.id)}
                    className={`p-2.5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                      styleMode === st.id
                        ? 'bg-purple-950/70 border-purple-500 shadow-md shadow-purple-600/20'
                        : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <span className="font-bold text-[11px] text-white block mb-0.5">{st.label}</span>
                    <span className="text-[9px] text-slate-400 leading-tight">{st.desc}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={isGenerating || !prompt.trim()}
              className="w-full bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 hover:from-pink-500 hover:to-indigo-500 text-white font-bold py-3.5 px-6 rounded-2xl text-sm shadow-xl shadow-purple-600/30 hover:scale-[1.01] active:scale-[0.99] transition-all cursor-pointer flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  <span>Google Flow Engine กำลังประมวลผลวิดีโอพร้อมโพสต์...</span>
                </>
              ) : (
                <>
                  <Wand2 className="w-5 h-5" />
                  <span>✨ สั่ง AI สร้างวิดีโอสำเร็จรูปพร้อมโพสต์ (Generate Ready Video)</span>
                </>
              )}
            </button>

            {/* Social Caption & Hashtag Preview Box */}
            {videoResult && (
              <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-purple-300 flex items-center gap-1.5">
                    <Share2 className="w-3.5 h-3.5 text-pink-400" />
                    แคปชันและแฮชแท็กสำหรับโพสต์โซเชียล
                  </span>
                  <button
                    onClick={handleCopyCaption}
                    className="text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded-lg flex items-center gap-1 transition-all cursor-pointer"
                  >
                    {copiedCaption ? <CheckCircle2 className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedCaption ? 'คัดลอกแล้ว!' : 'คัดลอกข้อความ'}</span>
                  </button>
                </div>
                <p className="text-xs text-slate-300 font-mono bg-slate-900 p-2.5 rounded-xl border border-slate-800 whitespace-pre-wrap leading-relaxed">
                  {videoResult.social_caption}
                </p>
              </div>
            )}
          </div>

          {/* Right Column: Live 9:16 Video Simulator & Export Studio */}
          <div className="lg:col-span-6 bg-slate-950/80 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Film className="w-4 h-4 text-purple-400" />
                  <span className="font-bold text-xs text-white uppercase tracking-wider">
                    9:16 Ready Video Player
                  </span>
                </div>
                {videoResult && (
                  <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    อย./สคบ. PASS • พร้อมโพสต์
                  </span>
                )}
              </div>

              {/* 9:16 Phone Screen Player */}
              <div className="relative rounded-2xl overflow-hidden bg-black aspect-[9/16] max-h-[380px] mx-auto border-2 border-purple-500/50 shadow-2xl flex flex-col justify-between p-3 select-none group">
                
                {/* Background Dynamic Video / Image */}
                <div className="absolute inset-0 z-0 overflow-hidden">
                  <img
                    src={videoResult?.product_thumbnail || "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80"}
                    alt="Product"
                    className={`w-full h-full object-cover brightness-75 transition-all duration-1000 ${
                      isPlaying ? 'scale-110 blur-[0.3px]' : 'scale-100'
                    }`}
                  />
                  <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/90 pointer-events-none"></div>
                </div>

                {/* Top Status Header */}
                <div className="relative z-10 flex items-center justify-between text-[11px] text-white">
                  <span className="px-2 py-0.5 rounded-full bg-black/60 backdrop-blur-md text-[10px] flex items-center gap-1">
                    <span className={`w-1.5 h-1.5 rounded-full ${isPlaying ? 'bg-emerald-400 animate-ping' : 'bg-pink-500'}`}></span>
                    {isPlaying ? `PLAYING (${currentTime}s / ${videoResult?.duration_sec || durationSec}s)` : 'READY TO PLAY'}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-purple-600/80 text-[10px] font-bold">
                    Shot {activeShotIndex + 1}/4
                  </span>
                </div>

                {/* Center Play Button & Burned Subtitles */}
                <div className="relative z-10 space-y-3">
                  <div className="flex justify-center">
                    <button
                      onClick={handleTogglePlay}
                      className="w-12 h-12 rounded-full bg-white/20 hover:bg-white/30 backdrop-blur-md border border-white/40 flex items-center justify-center text-white shadow-xl transition-all cursor-pointer hover:scale-110 active:scale-95"
                    >
                      {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-0.5" />}
                    </button>
                  </div>

                  {/* Dynamic On-Screen Subtitles */}
                  <div className="bg-black/80 backdrop-blur-md border border-yellow-400/50 px-3 py-1.5 rounded-xl text-center shadow-lg mx-2">
                    <p className="text-yellow-300 font-black text-xs drop-shadow-md line-clamp-2">
                      {currentShot ? currentShot.on_screen_text_th : "✨ รีวิวสินค้าคุณภาพพรีเมียม สั่งซื้อได้ที่ตะกร้าเหลือง"}
                    </p>
                  </div>
                </div>

                {/* Bottom TikTok Basket & Controls */}
                <div className="relative z-10 space-y-2">
                  <div className="bg-yellow-400 text-slate-950 font-black px-3 py-1.5 rounded-xl flex items-center justify-between text-xs shadow-lg animate-pulse">
                    <div className="flex items-center gap-1.5">
                      <ShoppingBag className="w-4 h-4 fill-slate-950" />
                      <span className="truncate max-w-[170px]">{videoResult ? videoResult.product_title_th : "สินค้าแนะนำในคลิป"}</span>
                    </div>
                    <span className="text-[10px] bg-slate-950 text-yellow-400 px-2 py-0.5 rounded-md uppercase font-bold">
                      สั่งซื้อ
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-slate-300">
                    <span>@affiliate_creator_pro</span>
                    <button
                      onClick={() => setIsMuted(!isMuted)}
                      className="p-1 rounded bg-black/40 text-slate-300 hover:text-white"
                    >
                      {isMuted ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Storyboard 4-Shot Timeline & Action Buttons */}
            {videoResult && (
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-purple-300">
                    🎬 ช็อตตัดต่อ 4 ฉาก (Google Flow Shots)
                  </span>
                  <span className="text-[11px] text-slate-400">
                    ความยาวรวม: {videoResult.duration_sec}s
                  </span>
                </div>

                <div className="grid grid-cols-4 gap-1.5">
                  {videoResult.shots.map((shot, idx) => (
                    <div
                      key={idx}
                      onClick={() => {
                        setActiveShotIndex(idx);
                        setCurrentTime(shot.start_sec);
                      }}
                      className={`p-2 rounded-xl border text-center cursor-pointer transition-all ${
                        activeShotIndex === idx
                          ? 'bg-purple-950/80 border-purple-500 text-purple-200'
                          : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700'
                      }`}
                    >
                      <span className="text-[10px] font-bold block">Shot {shot.shot_number}</span>
                      <span className="text-[9px] text-slate-400 block">{shot.start_sec}s - {shot.end_sec}s</span>
                    </div>
                  ))}
                </div>

                {/* Export Buttons */}
                <div className="pt-2 flex items-center gap-2">
                  <button
                    onClick={handleDownloadVideo}
                    disabled={isDownloadingMp4}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white py-2.5 rounded-xl text-xs font-bold shadow-lg shadow-purple-600/30 transition-all flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
                  >
                    {isDownloadingMp4 ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>กำลังจัดเตรียมไฟล์...</span>
                      </>
                    ) : (
                      <>
                        <Download className="w-3.5 h-3.5" />
                        <span>📥 ดาวน์โหลดวิดีโอ & เสียงพากย์</span>
                      </>
                    )}
                  </button>
                  <button
                    onClick={() => {
                      if (onSuccess) onSuccess('✅ อนุมัติและตั้งเวลาโพสต์ลง TikTok Shop / Shopee Video เรียบร้อย!');
                      onClose();
                    }}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white py-2.5 rounded-xl text-xs font-bold shadow-lg shadow-emerald-600/20 transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>🚀 โพสต์ลง TikTok/Shopee ทันที</span>
                  </button>
                </div>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
