'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Sparkles, Layers, Wand2, Play, Pause, Copy, CheckCircle2,
  Download, Film, Eye, Flame, ChevronRight, ShieldCheck,
  ShoppingBag, Volume2, VolumeX, RefreshCw, Upload, ArrowRight, ExternalLink, Video
} from 'lucide-react';
import {
  generateFlowOmniStoryboard,
  FlowOmniStoryboardResponse,
  Product,
  API_BASE
} from '@/lib/api';

interface FlowOmniStudioModalProps {
  isOpen: boolean;
  onClose: () => void;
  products?: Product[];
  initialProductId?: string;
  onSuccess?: (msg: string) => void;
}

export default function FlowOmniStudioModal({
  isOpen,
  onClose,
  products = [],
  initialProductId,
  onSuccess
}: FlowOmniStudioModalProps) {
  const [selectedProductId, setSelectedProductId] = useState<string>(initialProductId || '');
  const [customTitle, setCustomTitle] = useState<string>('เซรั่มใบบัวบก Cica Intense Calming');
  const [customThumb, setCustomThumb] = useState<string>('https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [result, setResult] = useState<FlowOmniStoryboardResponse | null>(null);

  // 10s Video Player State
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [activeShotIndex, setActiveShotIndex] = useState<number>(0);
  const [copiedPrompt, setCopiedPrompt] = useState<boolean>(false);
  const [isDownloadingVideo, setIsDownloadingVideo] = useState<boolean>(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (initialProductId) {
      setSelectedProductId(initialProductId);
    }
  }, [initialProductId]);

  // Auto-generate on open if not generated yet
  useEffect(() => {
    if (isOpen && !result) {
      handleGenerate(selectedProductId || undefined);
    }
  }, [isOpen]);

  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= 10.0) {
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
  }, [isPlaying]);

  // Sync active shot (5 shots: 0-2s, 2-4s, 4-6s, 6-8s, 8-10s)
  useEffect(() => {
    if (result && result.shots.length > 0) {
      const idx = result.shots.findIndex(
        (s) => currentTime >= s.start_sec && currentTime <= s.end_sec
      );
      if (idx !== -1 && idx !== activeShotIndex) {
        setActiveShotIndex(idx);
      }
    }
  }, [currentTime, result]);

  if (!isOpen) return null;

  const handleGenerate = async (pId?: string) => {
    try {
      setIsGenerating(true);
      const prod = products.find((p) => p.id === pId);
      const res = await generateFlowOmniStoryboard({
        product_id: pId,
        product_title_th: prod ? prod.title_th : customTitle,
        product_thumbnail: prod ? prod.thumbnail_url : customThumb,
        category: prod ? prod.category : 'สกินแคร์ / ความงาม'
      });
      setResult(res);
      setCurrentTime(0);
      setActiveShotIndex(0);
      setIsPlaying(false);
      if (onSuccess) onSuccess(`🌟 สร้าง Storyboard 5 ช่อง และ Flow Omni Prompt สำหรับ '${res.product_title_th}' สำเร็จ!`);
    } catch (err) {
      console.error(err);
      alert('เกิดข้อผิดพลาดในการสร้าง Storyboard กรุณาลองใหม่อีกครั้ง');
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
      if (result) {
        const audioUrl = `${API_BASE}/video/tts-audio?text=${encodeURIComponent(result.full_voiceover_th)}&voice=female`;
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

  const handleCopyPrompt = () => {
    if (!result) return;
    navigator.clipboard.writeText(result.universal_flow_omni_prompt);
    setCopiedPrompt(true);
    setTimeout(() => setCopiedPrompt(false), 3000);
    if (onSuccess) onSuccess('📋 คัดลอก Universal Prompt สำหรับ Flow Omni สำเร็จแล้ว!');
  };

  const handleDownloadVideoPackage = async () => {
    if (!result) return;
    try {
      setIsDownloadingVideo(true);
      
      // 1. Download voiceover audio
      const audioUrl = `${API_BASE}/video/tts-audio?text=${encodeURIComponent(result.full_voiceover_th)}&voice=female`;
      const audioResp = await fetch(audioUrl);
      const audioBlob = await audioResp.blob();

      const a = document.createElement('a');
      a.href = URL.createObjectURL(audioBlob);
      a.download = `flow_omni_10s_voiceover_${result.product_title_th.replace(/\s+/g, '_')}.mp3`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      // 2. Download Flow Omni JSON metadata package
      const jsonStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(result, null, 2));
      const jsonA = document.createElement('a');
      jsonA.href = jsonStr;
      jsonA.download = `flow_omni_project_${result.video_id}.json`;
      document.body.appendChild(jsonA);
      jsonA.click();
      jsonA.remove();

      if (onSuccess) onSuccess('📥 ดาวน์โหลดไฟล์เสียงพากย์ 10 วิ และชุดคำสั่ง Flow Omni เรียบร้อย!');
    } catch (e) {
      console.error(e);
    } finally {
      setIsDownloadingVideo(false);
    }
  };

  const currentShot = result?.shots[activeShotIndex] || result?.shots[0];

  // Motion CSS classes per shot
  const getMotionClass = (idx: number) => {
    if (!isPlaying) return 'scale-100';
    switch (idx) {
      case 0: return 'scale-115 translate-y-[-2%] duration-[2000ms]';
      case 1: return 'scale-110 translate-x-[3%] duration-[2000ms]';
      case 2: return 'scale-125 duration-[2000ms]';
      case 3: return 'scale-108 rotate-[1deg] duration-[2000ms]';
      case 4: return 'scale-115 rotate-[-1deg] duration-[2000ms]';
      default: return 'scale-110 duration-[2000ms]';
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
      <div className="bg-slate-900 border border-purple-500/40 rounded-3xl max-w-7xl w-full max-h-[94vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/70 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-400 via-pink-500 to-purple-600 flex items-center justify-center shadow-lg shadow-pink-500/30">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-lg text-white">🌟 Flow Omni 5-Scene POV Studio</h3>
                <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-gradient-to-r from-amber-400 to-pink-500 text-slate-950 uppercase font-black tracking-wider">
                  10s BRIGHT PREMIUM
                </span>
              </div>
              <p className="text-xs text-slate-400">
                ดึงข้อมูลสินค้าฮิตอัตโนมัติ → สร้าง Storyboard 5 ช่อง POV → ได้ Universal Prompt สำหรับ Flow Omni (Omni Flash 10s)
              </p>
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
          
          {/* Left Column: Winning Products Quick-Select & Universal Prompt */}
          <div className="lg:col-span-6 space-y-5">
            
            {/* 1. Winning Products Quick Select */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold uppercase tracking-wider text-amber-300 flex items-center gap-1.5">
                  <Flame className="w-3.5 h-3.5 text-amber-400" />
                  1. ดึงข้อมูลจากสินค้ายอดฮิต (Opportunity Radar)
                </label>
                <span className="text-[10px] text-slate-400">คลิกเพื่อสลับสินค้าทันที</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {products.slice(0, 6).map((prod) => {
                  const isSelected = (selectedProductId === prod.id) || (result?.product_title_th === prod.title_th);
                  return (
                    <div
                      key={prod.id}
                      onClick={() => {
                        setSelectedProductId(prod.id);
                        setCustomTitle(prod.title_th);
                        setCustomThumb(prod.thumbnail_url);
                        handleGenerate(prod.id);
                      }}
                      className={`p-2.5 rounded-xl border cursor-pointer transition-all flex items-center gap-2.5 ${
                        isSelected
                          ? 'bg-purple-950/80 border-purple-400 shadow-md shadow-purple-600/30 ring-1 ring-amber-400/50'
                          : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                      }`}
                    >
                      <img
                        src={prod.thumbnail_url}
                        alt={prod.title_th}
                        className="w-10 h-10 rounded-lg object-cover shrink-0 border border-slate-700"
                      />
                      <div className="overflow-hidden">
                        <p className="text-[11px] font-semibold text-slate-200 line-clamp-1">
                          {prod.title_th.split(' ')[0]}
                        </p>
                        <p className="text-[10px] text-emerald-400 font-medium">
                          เรตติ้ง {prod.rating}★
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* 2. Universal Flow Omni Prompt Box */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold uppercase tracking-wider text-amber-300 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-pink-400" />
                  2. Universal Prompt สำหรับ Flow Omni (Copy ครั้งเดียวใช้งานได้เลย)
                </label>
                <span className="text-[10px] text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded">
                  Omni Flash (10s) Ready
                </span>
              </div>

              <div className="relative group">
                <textarea
                  readOnly
                  rows={8}
                  value={result ? result.universal_flow_omni_prompt : 'กำลังประมวลผล Universal Prompt สำหรับ Flow Omni...'}
                  className="w-full bg-slate-950 border border-purple-500/30 rounded-2xl p-3.5 text-[11px] font-mono text-purple-200 leading-relaxed focus:outline-none resize-none shadow-inner"
                />
                
                <button
                  onClick={handleCopyPrompt}
                  className="absolute top-3 right-3 bg-gradient-to-r from-amber-400 via-pink-500 to-purple-600 hover:from-amber-300 hover:to-pink-400 text-slate-950 font-black px-4 py-2 rounded-xl text-xs shadow-xl transition-all cursor-pointer flex items-center gap-1.5 hover:scale-105 active:scale-95"
                >
                  {copiedPrompt ? <CheckCircle2 className="w-4 h-4 text-emerald-950" /> : <Copy className="w-4 h-4" />}
                  <span>{copiedPrompt ? 'คัดลอกสำเร็จแล้ว!' : '📋 Copy Prompt สำหรับ Flow Omni'}</span>
                </button>
              </div>
            </div>

            {/* 3-Step Execution Workflow Guide */}
            <div className="bg-slate-950/90 border border-slate-800 rounded-2xl p-3.5 space-y-2">
              <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block">
                🚀 วิธีนำไปเปิดรันใน Flow Omni (STEP 1 → STEP 2 → STEP 3)
              </span>
              <div className="grid grid-cols-3 gap-2 text-[10px] text-slate-400">
                <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="font-bold text-amber-400 block mb-0.5">1. คัดลอก Prompt</span>
                  กดปุ่ม Copy สีทองด้านบน
                </div>
                <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="font-bold text-pink-400 block mb-0.5">2. แนบรูป Storyboard</span>
                  ใส่ภาพ 5 ช่องใน Flow Omni
                </div>
                <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="font-bold text-purple-400 block mb-0.5">3. กด Generate</span>
                  เลือกโมเดล Omni Flash 10s
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: 5-Scene Storyboard Visuals & 10s Multi-Shot Video Simulator */}
          <div className="lg:col-span-6 space-y-4">
            
            {/* Top Bar on Right */}
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Film className="w-4 h-4 text-pink-400" />
                🎬 Storyboard 5 ฉาก (สลับภาพและมุมกล้องทุก 2 วินาที)
              </span>
              <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                ไม่มีตัวละคร • POV มือเท่านั้น
              </span>
            </div>

            {/* 5-Scene Visual Cards Strip with Actual Images */}
            {result && (
              <div className="grid grid-cols-5 gap-1.5">
                {result.shots.map((shot, idx) => (
                  <div
                    key={idx}
                    onClick={() => {
                      setActiveShotIndex(idx);
                      setCurrentTime(shot.start_sec);
                    }}
                    className={`p-1.5 rounded-xl border text-center cursor-pointer transition-all flex flex-col items-center justify-between ${
                      activeShotIndex === idx
                        ? 'bg-gradient-to-b from-purple-900/90 to-slate-950 border-amber-400 shadow-md shadow-amber-400/20 ring-1 ring-amber-400'
                        : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="w-full h-12 rounded-lg overflow-hidden mb-1 relative">
                      <img
                        src={shot.scene_image_url || result.product_thumbnail}
                        alt={`Scene ${shot.shot_number}`}
                        className="w-full h-full object-cover"
                      />
                      <span className="absolute top-0.5 left-0.5 text-[8px] font-bold bg-black/70 px-1 py-0.2 rounded text-white">
                        {shot.start_sec}s
                      </span>
                    </div>
                    <span className="text-[10px] font-bold text-amber-300 block">
                      ฉาก {shot.shot_number}
                    </span>
                    <span className="text-[9px] font-medium text-slate-300 line-clamp-1 leading-tight">
                      {shot.on_screen_text_th}
                    </span>
                  </div>
                ))}
              </div>
            )}

            {/* 10s Multi-Shot 9:16 Video Player Simulator */}
            <div className="bg-slate-950/90 border border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center gap-4">
              
              {/* Phone Mockup with DYNAMIC MULTI-SCENE VIDEO VISUALS */}
              <div className="relative rounded-2xl overflow-hidden bg-black aspect-[9/16] w-full sm:w-[220px] h-[350px] border-2 border-amber-400/60 shadow-2xl flex flex-col justify-between p-3 select-none shrink-0 group">
                
                {/* Dynamic Multi-Shot Scene Background Image with Smooth Crossfade & Camera Motion */}
                <div className="absolute inset-0 z-0 overflow-hidden">
                  <img
                    key={activeShotIndex}
                    src={currentShot?.scene_image_url || result?.product_thumbnail || customThumb}
                    alt="Current Scene Visual"
                    className={`w-full h-full object-cover brightness-90 transition-all ease-out ${getMotionClass(activeShotIndex)}`}
                  />
                  <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/85 pointer-events-none"></div>
                </div>

                {/* Top Status */}
                <div className="relative z-10 flex items-center justify-between text-[10px] text-white">
                  <span className="px-2 py-0.5 rounded-full bg-black/60 backdrop-blur-md flex items-center gap-1">
                    <span className={`w-1.5 h-1.5 rounded-full ${isPlaying ? 'bg-emerald-400 animate-ping' : 'bg-amber-400'}`}></span>
                    {isPlaying ? `${currentTime}s / 10.0s` : '10s PREVIEW'}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-pink-600/90 font-bold text-[9px]">
                    Scene {activeShotIndex + 1}/5
                  </span>
                </div>

                {/* Center Play Button & Dynamic Burned Subtitles */}
                <div className="relative z-10 space-y-2">
                  <div className="flex justify-center">
                    <button
                      onClick={handleTogglePlay}
                      className="w-12 h-12 rounded-full bg-white/25 hover:bg-white/35 backdrop-blur-md border border-white/40 flex items-center justify-center text-white shadow-xl transition-all cursor-pointer hover:scale-110 active:scale-95"
                    >
                      {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
                    </button>
                  </div>

                  <div className="bg-black/85 backdrop-blur-md border border-yellow-400/60 px-2.5 py-1.5 rounded-xl text-center shadow-lg animate-fade-in">
                    <p className="text-yellow-300 font-black text-[11px] drop-shadow-md line-clamp-2">
                      {currentShot ? currentShot.on_screen_text_th : "✨ ผิวฉ่ำโกลว์ใน 3 วัน!"}
                    </p>
                  </div>
                </div>

                {/* Bottom Basket & Audio Control */}
                <div className="relative z-10 space-y-1.5">
                  <div className="bg-yellow-400 text-slate-950 font-black px-2.5 py-1.5 rounded-xl flex items-center justify-between text-[11px] shadow-lg animate-pulse">
                    <div className="flex items-center gap-1 truncate max-w-[130px]">
                      <ShoppingBag className="w-3.5 h-3.5 fill-slate-950 shrink-0" />
                      <span className="truncate">{result ? result.product_title_th : customTitle}</span>
                    </div>
                    <span className="text-[9px] bg-slate-950 text-yellow-400 px-1.5 py-0.5 rounded font-bold uppercase">
                      สั่งซื้อ
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[10px] text-slate-300">
                    <span className="text-[9px]">@affiliate_creator_pro</span>
                    <button
                      onClick={() => setIsMuted(!isMuted)}
                      className="p-0.5 rounded bg-black/40 text-slate-300 hover:text-white"
                    >
                      {isMuted ? <VolumeX className="w-3 h-3" /> : <Volume2 className="w-3 h-3" />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Active Scene Detailed Information & Export Buttons */}
              {currentShot && (
                <div className="flex-1 space-y-3 text-xs">
                  <div className="flex items-center justify-between pb-1.5 border-b border-slate-800">
                    <span className="font-bold text-amber-300">
                      รายละเอียดฉากที่ {currentShot.shot_number} ({currentShot.start_sec}s - {currentShot.end_sec}s)
                    </span>
                    <span className="text-[10px] text-purple-300 font-medium bg-purple-500/20 px-2 py-0.5 rounded">
                      {currentShot.camera_direction}
                    </span>
                  </div>

                  <div className="space-y-1.5 text-[11px]">
                    <p className="text-slate-300">
                      <span className="text-slate-400 font-semibold">มุมกล้อง:</span> {currentShot.camera_direction}
                    </p>
                    <p className="text-slate-300">
                      <span className="text-slate-400 font-semibold">การกระทำของมือ:</span> {currentShot.visual_description_th}
                    </p>
                    <p className="text-slate-300">
                      <span className="text-slate-400 font-semibold">Sound Effect (SFX):</span> 🔊 {currentShot.sound_effect_cue}
                    </p>
                    <p className="text-slate-300">
                      <span className="text-slate-400 font-semibold">ข้อความบนจอ:</span> <span className="text-yellow-400 font-bold">"{currentShot.on_screen_text_th}"</span>
                    </p>
                  </div>

                  <div className="pt-2 space-y-2">
                    <button
                      onClick={handleCopyPrompt}
                      className="w-full bg-gradient-to-r from-amber-400 via-pink-500 to-purple-600 hover:from-amber-300 hover:to-pink-400 text-slate-950 font-black py-2.5 px-4 rounded-xl text-xs shadow-lg shadow-purple-600/30 transition-all cursor-pointer flex items-center justify-center gap-1.5"
                    >
                      <Copy className="w-3.5 h-3.5" />
                      <span>{copiedPrompt ? 'คัดลอกสำเร็จแล้ว!' : 'คัดลอก Universal Prompt ไปใส่ใน Flow Omni'}</span>
                    </button>

                    <button
                      onClick={handleDownloadVideoPackage}
                      disabled={isDownloadingVideo}
                      className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-2 px-4 rounded-xl text-[11px] border border-slate-700 transition-all cursor-pointer flex items-center justify-center gap-1.5 disabled:opacity-50"
                    >
                      {isDownloadingVideo ? (
                        <>
                          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                          <span>กำลังเตรียมไฟล์ดาวน์โหลด...</span>
                        </>
                      ) : (
                        <>
                          <Download className="w-3.5 h-3.5 text-purple-400" />
                          <span>📥 ดาวน์โหลดไฟล์เสียงพากย์ 10 วิ & แพ็กเกจ Storyboard</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
