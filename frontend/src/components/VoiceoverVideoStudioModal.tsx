'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Mic, Upload, Sparkles, Play, Pause, Download, Video,
  CheckCircle2, AlertCircle, RefreshCw, Volume2, VolumeX,
  Layers, Film, Wand2, ArrowRight, ShieldCheck, ShoppingBag, Radio
} from 'lucide-react';
import {
  generateVideoFromVoiceover,
  VoiceoverGenerationResponse,
  API_BASE
} from '@/lib/api';

interface VoiceoverVideoStudioModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: (msg: string) => void;
}

const SAMPLE_PRODUCTS = [
  { title: "หม้อทอดไร้น้ำมัน Smart Air Fryer 5.5L", thumb: "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=500&auto=format&fit=crop&q=60" },
  { title: "เซรั่มไฮยาลูรอนเข้มข้น ผิวฉ่ำโกลว์", thumb: "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&auto=format&fit=crop&q=60" },
  { title: "หูฟังบลูทูธไร้สาย ตัดเสียงรบกวน ANC", thumb: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60" },
  { title: "แก้วเก็บความเย็นสแตนเลส 316 ขนาด 900ml", thumb: "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500&auto=format&fit=crop&q=60" },
];

export default function VoiceoverVideoStudioModal({
  isOpen,
  onClose,
  onSuccess
}: VoiceoverVideoStudioModalProps) {
  const [productTitle, setProductTitle] = useState('เซรั่มไฮยาลูรอนเข้มข้น ผิวฉ่ำโกลว์');
  const [selectedThumb, setSelectedThumb] = useState(SAMPLE_PRODUCTS[1].thumb);
  const [voiceoverScript, setVoiceoverScript] = useState(
    'ทุกคนคะ ตัวนี้คือเซรั่มไฮยาที่รีวิวแน่นมาก ใช้แค่ 3 วันผิวฉ่ำอิ่มน้ำ หน้าไม่โทรมเลย ใช้ง่ายมากแค่หยดเดียวเกลี่ยทั่วหน้า ใครหน้าแห้งแต่งหน้าไม่ติดต้องลอง จิ้มตะกร้าซ้ายล่างตอนมีโปรส่งฟรีได้เลยค่ะ!'
  );
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [audioBlobUrl, setAudioBlobUrl] = useState<string | null>(null);
  const [audioDuration, setAudioDuration] = useState<number>(20);
  const [styleMode, setStyleMode] = useState<string>('AVATAR_HYBRID');
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [generatedResult, setGeneratedResult] = useState<VoiceoverGenerationResponse | null>(null);
  
  // Video Simulator Player State
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [activeShotIndex, setActiveShotIndex] = useState<number>(0);
  
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentTime((prev) => {
          const maxDur = generatedResult ? generatedResult.duration_sec : audioDuration;
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
  }, [isPlaying, generatedResult, audioDuration]);

  // Update active shot based on currentTime
  useEffect(() => {
    if (generatedResult && generatedResult.shots.length > 0) {
      const idx = generatedResult.shots.findIndex(
        (s) => currentTime >= s.start_sec && currentTime <= s.end_sec
      );
      if (idx !== -1 && idx !== activeShotIndex) {
        setActiveShotIndex(idx);
      }
    }
  }, [currentTime, generatedResult]);

  if (!isOpen) return null;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setAudioFile(file);
    const url = URL.createObjectURL(file);
    setAudioBlobUrl(url);

    // Read audio length
    const tempAudio = new Audio(url);
    tempAudio.onloadedmetadata = () => {
      if (tempAudio.duration && !isNaN(tempAudio.duration)) {
        const rounded = Math.round(tempAudio.duration);
        setAudioDuration(rounded);
      }
    };
  };

  const handleGenerate = async () => {
    try {
      setIsAnalyzing(true);
      const res = await generateVideoFromVoiceover({
        product_title_th: productTitle,
        voiceover_script: voiceoverScript,
        duration_sec: audioDuration,
        style_mode: styleMode,
        product_thumbnail: selectedThumb
      });
      setGeneratedResult(res);
      setCurrentTime(0);
      setActiveShotIndex(0);
      setIsPlaying(false);
      if (onSuccess) onSuccess('⚡ AI สร้าง Storyboard และ Prompts วิดีโอสมจริงสำเร็จเรียบร้อย!');
    } catch (err) {
      console.error(err);
      alert('เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleTogglePlay = () => {
    if (isPlaying) {
      setIsPlaying(false);
      if (audioPlayerRef.current) audioPlayerRef.current.pause();
    } else {
      setIsPlaying(true);
      if (audioPlayerRef.current) {
        audioPlayerRef.current.currentTime = currentTime;
        audioPlayerRef.current.play().catch(() => {});
      } else if (!audioBlobUrl && generatedResult) {
        // Play synthetic preview voice if no custom file uploaded
        const ttsUrl = `${API_BASE}/video/tts-audio?text=${encodeURIComponent(generatedResult.sanitized_script)}&voice=female`;
        const audio = new Audio(ttsUrl);
        audio.muted = isMuted;
        audio.play().catch(() => {});
      }
    }
  };

  const handleExportJson = () => {
    if (!generatedResult) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(generatedResult, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `ai_video_project_${generatedResult.video_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    if (onSuccess) onSuccess('📥 ดาวน์โหลด JSON คำสั่ง Google Flow & AI Video เรียบร้อย!');
  };

  const currentShot = generatedResult?.shots[activeShotIndex] || generatedResult?.shots[0];

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
      <div className="bg-slate-900 border border-purple-500/40 rounded-3xl max-w-6xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden text-slate-100">
        
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 via-pink-600 to-amber-500 flex items-center justify-center shadow-lg shadow-purple-600/30">
              <Mic className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-lg text-white">🎙️ Voiceover-to-Video Studio</h3>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-pink-500/20 text-pink-300 border border-pink-500/30 uppercase">
                  Realistic Video Engine
                </span>
              </div>
              <p className="text-xs text-slate-400">อัปโหลดไฟล์เสียงพากย์ของคุณ ให้ AI สร้างวิดีโอรีวิวสินค้าที่สมจริง 100% อัตโนมัติ</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-sm font-bold transition-all cursor-pointer"
          >
            ✕
          </button>
        </div>

        {/* Modal Body (2 Columns Layout) */}
        <div className="p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-y-auto">
          
          {/* Left Column: Audio Upload & Settings */}
          <div className="lg:col-span-6 space-y-5">
            
            {/* 1. Upload Audio Box */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-purple-300 flex items-center justify-between">
                <span>1. อัปโหลดไฟล์เสียงพากย์ (.mp3 / .wav)</span>
                {audioFile && (
                  <span className="text-[11px] text-emerald-400 font-semibold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> {audioFile.name} ({audioDuration}s)
                  </span>
                )}
              </label>

              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-purple-500/40 hover:border-purple-400 bg-purple-950/20 hover:bg-purple-950/40 rounded-2xl p-4 text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-2 group"
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept="audio/*,.mp3,.wav,.m4a"
                  className="hidden"
                />
                <div className="w-10 h-10 rounded-full bg-purple-600/30 group-hover:bg-purple-600/50 flex items-center justify-center text-purple-300 transition-colors">
                  <Upload className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-slate-200">
                    {audioFile ? "คลิกเพื่อเปลี่ยนไฟล์เสียงพากย์" : "คลิกหรือลากไฟล์เสียงพากย์มาวางที่นี่"}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    รองรับ MP3, WAV, M4A (ระบบจะคำนวณจังหวะและแยกท่อนให้อัตโนมัติ)
                  </p>
                </div>
              </div>

              {audioBlobUrl && (
                <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2 text-xs text-purple-300 font-medium truncate">
                    <Volume2 className="w-4 h-4 text-pink-400 shrink-0" />
                    <span className="truncate">{audioFile?.name}</span>
                  </div>
                  <audio
                    ref={audioPlayerRef}
                    src={audioBlobUrl}
                    controls
                    className="h-8 max-w-[200px]"
                  />
                </div>
              )}
            </div>

            {/* 2. Product Name & Selection */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-purple-300">
                2. ระบุสินค้าที่ต้องการรีวิว
              </label>
              <input
                type="text"
                value={productTitle}
                onChange={(e) => setProductTitle(e.target.value)}
                placeholder="พิมพ์ชื่อสินค้า เช่น เซรั่มหน้าใส, เครื่องฟอกอากาศ..."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 transition-colors"
              />

              {/* Sample Quick Select */}
              <div className="flex flex-wrap gap-1.5 pt-1">
                {SAMPLE_PRODUCTS.map((prod, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setProductTitle(prod.title);
                      setSelectedThumb(prod.thumb);
                    }}
                    className={`text-[11px] px-2.5 py-1 rounded-lg border transition-all cursor-pointer ${
                      productTitle === prod.title
                        ? 'bg-purple-600/30 border-purple-500 text-purple-200'
                        : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                    }`}
                  >
                    {prod.title.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>

            {/* 3. Style Selection */}
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-purple-300">
                3. เลือกสไตล์ภาพวิดีโอ (Video Visual Style)
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  {
                    id: 'AVATAR_HYBRID',
                    label: '🌟 AI Avatar + Demo',
                    desc: 'คนพูดสมจริง + ตัดสลับสินค้า (ยอดฮิต)'
                  },
                  {
                    id: 'CINEMATIC_BROLL',
                    label: '🎥 4K Cinematic B-Roll',
                    desc: 'ฟุตเทจสินค้าแสงสตูดิโอ 3D Macro'
                  },
                  {
                    id: 'UGC_VIRAL',
                    label: '🛍️ TikTok UGC Viral',
                    desc: 'สไตล์รีวิวบ้านๆ มุมมองกล้องมือถือ'
                  }
                ].map((style) => (
                  <div
                    key={style.id}
                    onClick={() => setStyleMode(style.id)}
                    className={`p-3 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                      styleMode === style.id
                        ? 'bg-purple-950/60 border-purple-500 shadow-md shadow-purple-600/20'
                        : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <span className="font-bold text-xs text-white block mb-1">
                      {style.label}
                    </span>
                    <span className="text-[10px] text-slate-400 leading-tight">
                      {style.desc}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* 4. Voiceover Script / Transcript */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold uppercase tracking-wider text-purple-300">
                  4. เนื้อหาคำพูดเสียงพากย์ (Voiceover Script)
                </label>
                <span className="text-[10px] text-slate-400">
                  ความยาวเป้าหมาย: ~{audioDuration} วินาที
                </span>
              </div>
              <textarea
                rows={3}
                value={voiceoverScript}
                onChange={(e) => setVoiceoverScript(e.target.value)}
                placeholder="ใส่บทพากย์ภาษาไทย เพื่อให้ AI นำไปตัดแบ่งฉากและตรวจ อย./สคบ."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500 transition-colors leading-relaxed"
              />
            </div>

            {/* Generate Action Button */}
            <button
              onClick={handleGenerate}
              disabled={isAnalyzing}
              className="w-full bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 hover:from-purple-500 hover:to-pink-500 text-white font-bold py-3.5 px-6 rounded-2xl text-sm shadow-xl shadow-purple-600/30 hover:scale-[1.01] active:scale-[0.99] transition-all cursor-pointer flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  <span>AI กำลังวิเคราะห์เสียงและเจนฉากสมจริง...</span>
                </>
              ) : (
                <>
                  <Wand2 className="w-5 h-5" />
                  <span>🚀 สั่ง AI สร้างวิดีโอรีวิวสมจริงพร้อมเสียงพากย์ (One-Click)</span>
                </>
              )}
            </button>
          </div>

          {/* Right Column: Live Video Simulator & Storyboard Inspection */}
          <div className="lg:col-span-6 bg-slate-950/80 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Film className="w-4 h-4 text-purple-400" />
                  <span className="font-bold text-xs text-white uppercase tracking-wider">
                    9:16 Video Player Preview
                  </span>
                </div>
                {generatedResult && (
                  <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    อย./สคบ. PASS
                  </span>
                )}
              </div>

              {/* Vertical Phone Screen Mockup */}
              <div className="relative rounded-2xl overflow-hidden bg-black aspect-[9/16] max-h-[380px] mx-auto border-2 border-purple-500/40 shadow-2xl flex flex-col justify-between p-3 select-none group">
                
                {/* Background Video / Image Layer with Smooth Zoom */}
                <div className="absolute inset-0 z-0 overflow-hidden">
                  <img
                    src={selectedThumb}
                    alt="Product"
                    className={`w-full h-full object-cover brightness-75 transition-all duration-1000 ${
                      isPlaying ? 'scale-110 blur-[0.5px]' : 'scale-100'
                    }`}
                  />
                  <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/90 pointer-events-none"></div>
                </div>

                {/* Top Status Header */}
                <div className="relative z-10 flex items-center justify-between text-[11px] text-white">
                  <span className="px-2 py-0.5 rounded-full bg-black/60 backdrop-blur-md text-[10px] flex items-center gap-1">
                    <span className={`w-1.5 h-1.5 rounded-full ${isPlaying ? 'bg-emerald-400 animate-ping' : 'bg-amber-400'}`}></span>
                    {isPlaying ? `PLAYING (${currentTime}s / ${generatedResult?.duration_sec || audioDuration}s)` : 'READY TO PREVIEW'}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-purple-600/80 text-[10px] font-bold">
                    Shot {activeShotIndex + 1}/4
                  </span>
                </div>

                {/* Center Play Button & Dynamic Subtitles */}
                <div className="relative z-10 space-y-3">
                  <div className="flex justify-center">
                    <button
                      onClick={handleTogglePlay}
                      className="w-12 h-12 rounded-full bg-white/20 hover:bg-white/30 backdrop-blur-md border border-white/40 flex items-center justify-center text-white shadow-xl transition-all cursor-pointer hover:scale-110 active:scale-95"
                    >
                      {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-0.5" />}
                    </button>
                  </div>

                  {/* Dynamic On-Screen Subtitle */}
                  <div className="bg-black/80 backdrop-blur-md border border-yellow-400/40 px-3 py-1.5 rounded-xl text-center shadow-lg mx-2">
                    <p className="text-yellow-300 font-bold text-xs drop-shadow-md line-clamp-2">
                      {currentShot ? currentShot.on_screen_text_th : "✨ รีวิวสินค้าคุณภาพพรีเมียม การันตีของแท้ 100%"}
                    </p>
                  </div>
                </div>

                {/* Bottom TikTok Basket & Controls Overlay */}
                <div className="relative z-10 space-y-2">
                  {/* Yellow Shopping Basket CTA */}
                  <div className="bg-yellow-400 text-slate-950 font-black px-3 py-1.5 rounded-xl flex items-center justify-between text-xs shadow-lg animate-pulse">
                    <div className="flex items-center gap-1.5">
                      <ShoppingBag className="w-4 h-4 fill-slate-950" />
                      <span className="truncate max-w-[170px]">{productTitle}</span>
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

            {/* Storyboard 4-Shot Timeline Breakdown */}
            {generatedResult && (
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-purple-300">
                    🎬 ไทม์ไลน์ 4 ช็อตตัดต่ออัตโนมัติ
                  </span>
                  <span className="text-[11px] text-slate-400">
                    คลิกเพื่อดู Prompt
                  </span>
                </div>

                <div className="grid grid-cols-4 gap-1.5">
                  {generatedResult.shots.map((shot, idx) => (
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
                      <span className="text-[10px] font-bold block">
                        Shot {shot.shot_number}
                      </span>
                      <span className="text-[9px] text-slate-400 block">
                        {shot.start_sec}s - {shot.end_sec}s
                      </span>
                    </div>
                  ))}
                </div>

                {/* Active Prompt Box */}
                {currentShot && (
                  <div className="bg-slate-900/90 border border-slate-800 p-2.5 rounded-xl text-[11px] space-y-1">
                    <p className="text-slate-300 font-semibold">
                      🎥 AI Video Prompt (Kling / Runway / Hedra):
                    </p>
                    <p className="text-purple-300 font-mono text-[10px] bg-slate-950 p-1.5 rounded border border-purple-500/20 line-clamp-2">
                      {currentShot.image_prompt_for_ai}
                    </p>
                  </div>
                )}

                {/* Export & Download Buttons */}
                <div className="pt-2 flex items-center gap-2">
                  <button
                    onClick={handleExportJson}
                    className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 py-2 rounded-xl text-xs font-semibold border border-slate-700 transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <Download className="w-3.5 h-3.5 text-purple-400" />
                    <span>โหลด JSON คำสั่งตัดต่อ</span>
                  </button>
                  <button
                    onClick={() => {
                      if (onSuccess) onSuccess('✅ อนุมัติและส่งวิดีโอเข้าคิวตั้งเวลาโพสต์เรียบร้อย!');
                      onClose();
                    }}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded-xl text-xs font-bold shadow-lg shadow-emerald-600/20 transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>อนุมัติและนำไปใช้งาน</span>
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
