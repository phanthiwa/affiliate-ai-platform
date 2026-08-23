'use client';

import React, { useState, useEffect } from 'react';
import {
  Sparkles, TrendingUp, DollarSign, Video, CheckCircle2,
  Download, Layers, Search, ChevronRight, Eye, RefreshCw, Zap, Flame, Compass, ShieldCheck,
  Share2, Play, Pause, Volume2, VolumeX, RotateCcw
} from 'lucide-react';
import {
  fetchDashboardOverview, fetchProducts, fetchProductIntelligence,
  triggerDailyBatchClips, batchApproveClips, API_BASE,
  Product, ProductIntelligenceCard, BatchGenerationResponse, DashboardOverview
} from '@/lib/api';

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<DashboardOverview | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedProductIntelligence, setSelectedProductIntelligence] = useState<ProductIntelligenceCard | null>(null);
  const [batchData, setBatchData] = useState<BatchGenerationResponse | null>(null);
  const [activeClipIndex, setActiveClipIndex] = useState<number>(0);
  const [isGeneratingBatch, setIsGeneratingBatch] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [isPlayingVideo, setIsPlayingVideo] = useState<boolean>(false);
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [currentPlaySec, setCurrentPlaySec] = useState<number>(0);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setIsLoading(true);
      const [dashData, prodsData] = await Promise.all([
        fetchDashboardOverview(),
        fetchProducts()
      ]);
      setDashboard(dashData);
      setProducts(prodsData);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearchAndFilter = async (category: string, query: string) => {
    setSelectedCategory(category);
    try {
      const params: Record<string, string> = {};
      if (category !== 'ALL') params.category = category;
      if (query) params.search = query;
      const filtered = await fetchProducts(params);
      setProducts(filtered);
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenIntelligence = async (productId: string) => {
    try {
      const intel = await fetchProductIntelligence(productId);
      setSelectedProductIntelligence(intel);
    } catch (err) {
      console.error(err);
    }
  };

  const handleGenerateDailyBatch = async (productIds?: string[]) => {
    try {
      setIsGeneratingBatch(true);
      const res = await triggerDailyBatchClips(productIds);
      setBatchData(res);
      setActiveClipIndex(0);
      showToast('🚀 สร้างชุด 10–15 คลิปสำหรับ Google Flow สำเร็จเรียบร้อย!');
    } catch (err) {
      console.error(err);
      showToast('เกิดข้อผิดพลาดในการสร้างชุดคลิป');
    } finally {
      setIsGeneratingBatch(false);
    }
  };

  const handleApproveAllClips = async () => {
    if (!batchData) return;
    try {
      const clipIds = batchData.clips.map(c => c.clip_id);
      await batchApproveClips(clipIds);
      showToast(`✅ อนุมัติสำเร็จทั้ง ${clipIds.length} คลิป! ตั้งเวลาลง TikTok Shop & Shopee เรียบร้อย`);
    } catch (err) {
      console.error(err);
    }
  };

  const handleExportGoogleFlowJson = () => {
    if (!batchData) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(batchData.google_flow_payload, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `google_flow_batch_${batchData.batch_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    showToast('📥 ดาวน์โหลด Google Flow JSON สำเร็จ!');
  };

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 pb-20">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-6 py-3 rounded-xl shadow-2xl flex items-center gap-3 border border-purple-400/30 animate-bounce">
          <Sparkles className="w-5 h-5" />
          <span className="font-medium text-sm">{toastMessage}</span>
        </div>
      )}

      {/* Top Navigation */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-xl sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
                  Affiliate Growth OS
                </span>
                <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  15 Clips/Day
                </span>
              </div>
              <p className="text-xs text-slate-400">ระบบ AI ผลิตและบริหารคอนเทนต์นายหน้าอัตโนมัติ (ตลาดไทย)</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-purple-950/60 hover:bg-purple-900/80 border border-purple-500/40 text-xs font-semibold text-purple-200 transition-all cursor-pointer shadow-sm"
            >
              <Share2 className="w-3.5 h-3.5 text-pink-400" />
              <span>ผูกบัญชีโซเชียล</span>
            </button>
            <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-slate-300 font-medium">Google Flow: พร้อมเชื่อมต่อ</span>
            </div>
            <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-semibold text-slate-200">K. Aom (Creator 1.2M)</p>
                <p className="text-[11px] text-purple-400">TikTok Shop & Shopee Pro</p>
              </div>
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center font-bold text-sm text-white shadow-md">
                A
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 space-y-8">
        
        {/* KPI Metrics Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-2xl relative overflow-hidden group hover:border-purple-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
              <span>ยอดขายสะสม (GMV)</span>
              <DollarSign className="w-4 h-4 text-emerald-400" />
            </div>
            <p className="text-2xl font-bold text-white tracking-tight">฿1,482,950</p>
            <div className="mt-2 flex items-center gap-1.5 text-xs text-emerald-400">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>+24.5% สัปดาห์นี้</span>
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-2xl relative overflow-hidden group hover:border-purple-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
              <span>ค่าคอมมิชชั่นสุทธิ</span>
              <Sparkles className="w-4 h-4 text-purple-400" />
            </div>
            <p className="text-2xl font-bold text-purple-300 tracking-tight">฿342,890</p>
            <div className="mt-2 text-xs text-slate-400">
              เฉลี่ย ฿23.1% ต่อออเดอร์
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-2xl relative overflow-hidden group hover:border-purple-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
              <span>ยอดวิว & CTR เฉลี่ย</span>
              <Eye className="w-4 h-4 text-blue-400" />
            </div>
            <p className="text-2xl font-bold text-white tracking-tight">1.24M วิว</p>
            <div className="mt-2 flex items-center gap-2 text-xs text-blue-400">
              <span>CTR: 4.82%</span>
              <span className="text-slate-500">•</span>
              <span>CVR: 5.41%</span>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/40 to-pink-900/30 border border-purple-500/30 p-4 rounded-2xl relative overflow-hidden">
            <div className="flex items-center justify-between text-purple-200 text-xs font-medium mb-1">
              <span>เป้าหมายคลิปวันนี้</span>
              <Video className="w-4 h-4 text-pink-400" />
            </div>
            <p className="text-2xl font-bold text-white tracking-tight">15 / 15 คลิป</p>
            <div className="mt-2 text-xs text-purple-300 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>พร้อมส่ง Google Flow & ตรวจอนุมัติ</span>
            </div>
          </div>
        </div>

        {/* "What Should I Do Today?" Directive Engine */}
        <section className="bg-gradient-to-r from-slate-900 via-purple-950/30 to-slate-900 border border-purple-500/30 rounded-3xl p-6 relative shadow-2xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="px-2.5 py-0.5 text-xs font-bold bg-pink-500 text-white rounded-full uppercase tracking-wider flex items-center gap-1 shadow-sm">
                  <Flame className="w-3 h-3" /> AI Directive
                </span>
                <h2 className="text-xl font-bold text-white">🎯 วันนี้ทำอะไรดี? (AI Recommendation)</h2>
              </div>
              <p className="text-sm text-slate-300">
                ระบบวิเคราะห์แนวโน้มตลาดและอัตราเปลี่ยนเป็นยอดขาย แนะนำแผนผลิตคลิปประจำวันเพื่อสร้างผลตอบแทนสูงสุด
              </p>
            </div>

            <button
              onClick={() => handleGenerateDailyBatch()}
              disabled={isGeneratingBatch}
              className="flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 hover:from-purple-500 hover:to-pink-500 text-white px-6 py-3.5 rounded-2xl font-bold text-sm shadow-xl shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer disabled:opacity-50"
            >
              {isGeneratingBatch ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  <span>กำลังสร้าง 15 คลิป...</span>
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  <span>⚡ สร้างชุด 10–15 คลิปประจำวันสำหรับ Google Flow</span>
                </>
              )}
            </button>
          </div>

          {/* 3 AI Recommendation Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {dashboard?.daily_recommendations?.map((rec, idx) => (
              <div key={rec.id || idx} className="bg-slate-900/80 border border-slate-800 hover:border-purple-500/40 p-4 rounded-2xl flex flex-col justify-between transition-all group">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      {rec.badge_label}
                    </span>
                    <span className="text-[11px] text-emerald-400 font-medium">
                      คาดการณ์ +฿{rec.estimated_daily_gmv_potential.toLocaleString()}
                    </span>
                  </div>
                  <h4 className="font-semibold text-sm text-slate-100 group-hover:text-purple-300 transition-colors mb-1.5">
                    {rec.headline_th}
                  </h4>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {rec.reasoning_th}
                  </p>
                </div>
                <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                  <button 
                    onClick={() => handleOpenIntelligence(rec.recommended_product_id)}
                    className="text-xs text-purple-400 hover:text-purple-300 font-medium flex items-center gap-1 cursor-pointer"
                  >
                    <span>ดูบทวิเคราะห์สินค้า</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() => handleGenerateDailyBatch([rec.recommended_product_id])}
                    className="text-xs bg-slate-800 hover:bg-purple-600/50 text-slate-200 px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                  >
                    สร้าง 5 คลิปสินค้านี้
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Batch Clips Studio View (When Generated) */}
        {batchData && (
          <section className="bg-slate-900/90 border border-purple-500/40 rounded-3xl p-6 shadow-2xl space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2.5 py-0.5 text-xs font-bold bg-purple-600 text-white rounded-full">
                    {batchData.total_generated} คลิปพร้อมใช้งาน
                  </span>
                  <h3 className="text-lg font-bold text-white">🎬 สตูดิโอตรวจอนุมัติ & ส่งเข้า Google Flow</h3>
                </div>
                <p className="text-xs text-slate-400">{batchData.summary_message_th}</p>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={handleExportGoogleFlowJson}
                  className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2.5 rounded-xl text-xs font-semibold border border-slate-700 transition-all cursor-pointer"
                >
                  <Download className="w-4 h-4 text-purple-400" />
                  <span>ส่งออก JSON สำหรับ Google Flow</span>
                </button>
                <button
                  onClick={handleApproveAllClips}
                  className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-lg shadow-emerald-600/20 transition-all cursor-pointer"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>อนุมัติทั้ง {batchData.total_generated} คลิป และตั้งเวลาลงทันที</span>
                </button>
              </div>
            </div>

            {/* Clips Grid & Inspector */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left List of 10-15 Clips */}
              <div className="lg:col-span-5 space-y-2.5 max-h-[560px] overflow-y-auto pr-2">
                {batchData.clips.map((clip, idx) => (
                  <div
                    key={clip.clip_id}
                    onClick={() => setActiveClipIndex(idx)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between gap-3 ${
                      activeClipIndex === idx
                        ? 'bg-purple-950/40 border-purple-500 shadow-md'
                        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-6 h-6 rounded-full bg-slate-800 text-xs font-bold text-purple-300 flex items-center justify-center">
                        {idx + 1}
                      </span>
                      <div className="space-y-0.5">
                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-semibold px-1.5 py-0.2 rounded bg-purple-500/20 text-purple-300">
                            {clip.duration_sec}s
                          </span>
                          <span className="text-xs font-medium text-slate-200 line-clamp-1">
                            {clip.angle_type}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 line-clamp-1">
                          ฮุก: {clip.hook_text_th}
                        </p>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full block mb-1">
                        อย./สคบ. PASS
                      </span>
                      <span className="text-[10px] text-slate-400">
                        {clip.scheduled_time_slot_th.split(' ')[0]}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Right Detail Preview of Active Clip */}
              {batchData.clips[activeClipIndex] && (
                <div className="lg:col-span-7 bg-slate-950/80 border border-slate-800 p-5 rounded-2xl space-y-4">
                  {(() => {
                    const activeClip = batchData.clips[activeClipIndex];
                    return (
                      <>
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="text-xs font-bold text-purple-400 uppercase tracking-wider">
                              คลิปที่ {activeClipIndex + 1} จาก {batchData.total_generated} • {activeClip.angle_type}
                            </span>
                            <h4 className="text-base font-bold text-white mt-0.5">
                              {activeClip.product_title_th}
                            </h4>
                          </div>
                          <span className="text-xs bg-purple-500/20 text-purple-300 px-2.5 py-1 rounded-lg border border-purple-500/30">
                            ตั้งเวลา: {activeClip.scheduled_time_slot_th}
                          </span>
                        </div>

                        {/* Video / Storyboard Visual Preview */}
                        <div className="grid grid-cols-1 sm:grid-cols-12 gap-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800/80">
                          {/* 9:16 Vertical TikTok Simulator Player */}
                          <div className="sm:col-span-5 relative rounded-2xl overflow-hidden bg-slate-950 aspect-[9/16] max-h-[420px] mx-auto border-2 border-purple-500/50 shadow-2xl flex flex-col justify-between p-3 select-none group">
                            {/* Background Image / Motion Simulator Video Layer */}
                            <div className="absolute inset-0 z-0 overflow-hidden">
                              {isPlayingVideo ? (
                                <video
                                  src={activeClip.preview_video_url || "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"}
                                  autoPlay
                                  loop
                                  playsInline
                                  muted={isMuted}
                                  className="w-full h-full object-cover brightness-90 scale-105"
                                />
                              ) : (
                                <img
                                  src={activeClip.product_thumbnail || "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&auto=format&fit=crop&q=60"}
                                  alt="Product Preview"
                                  className="w-full h-full object-cover brightness-75 scale-100 transition-all duration-700"
                                />
                              )}
                              <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/90 pointer-events-none"></div>
                            </div>

                            {/* Top Bar on Phone */}
                            <div className="relative z-10 flex items-center justify-between text-[11px] text-white">
                              <span className="px-2 py-0.5 rounded-full bg-black/60 backdrop-blur-md text-[10px] flex items-center gap-1">
                                <span className={`w-1.5 h-1.5 rounded-full ${isPlayingVideo ? 'bg-emerald-400 animate-ping' : 'bg-red-500'}`}></span>
                                {isPlayingVideo ? 'PLAYING VIDEO' : 'READY TO PLAY'}
                              </span>
                              <span className="px-2 py-0.5 rounded-full bg-purple-600/80 text-[10px] font-bold">
                                {activeClip.duration_sec}s
                              </span>
                            </div>

                            {/* Center Play Button & Dynamic Subtitles Overlay */}
                            <div className="relative z-10 space-y-3">
                              {/* Big Play / Pause Button */}
                              <div className="flex justify-center">
                                <button
                                  onClick={() => {
                                    if (isPlayingVideo) {
                                      setIsPlayingVideo(false);
                                      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
                                    } else {
                                      setIsPlayingVideo(true);
                                      const audioUrl = `${API_BASE}/video/tts-audio?text=${encodeURIComponent(activeClip.script.full_voiceover_th)}&voice=female`;
                                      const audio = new Audio(audioUrl);
                                      audio.muted = isMuted;
                                      audio.play().catch(() => {
                                        if ('speechSynthesis' in window) {
                                          const utterance = new SpeechSynthesisUtterance(activeClip.script.full_voiceover_th);
                                          utterance.lang = 'th-TH';
                                          utterance.onend = () => setIsPlayingVideo(false);
                                          window.speechSynthesis.speak(utterance);
                                        }
                                      });
                                      audio.onended = () => setIsPlayingVideo(false);
                                      showToast("🎬 กำลังเล่นวิดีโอ & เสียงพากย์ AI...");
                                    }
                                  }}
                                  className="w-16 h-16 rounded-full bg-gradient-to-tr from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white flex items-center justify-center shadow-2xl shadow-purple-600/60 hover:scale-110 active:scale-95 transition-all cursor-pointer border-2 border-white/40"
                                >
                                  {isPlayingVideo ? (
                                    <Pause className="w-8 h-8 fill-white text-white" />
                                  ) : (
                                    <Play className="w-8 h-8 fill-white text-white ml-1" />
                                  )}
                                </button>
                              </div>

                              {/* Kinetic Subtitles during playback */}
                              {isPlayingVideo && (
                                <div className="text-center px-3 py-2 bg-black/80 backdrop-blur-md rounded-xl border border-purple-500/50 mx-2 animate-bounce">
                                  <p className="text-[10px] text-pink-300 font-bold uppercase tracking-wider">🗣️ เสียงพากย์ AI (Real-time)</p>
                                  <p className="text-xs text-yellow-300 font-bold mt-0.5">
                                    "{activeClip.hook_text_th}"
                                  </p>
                                </div>
                              )}
                            </div>

                            {/* Bottom TikTok Style Overlay & Controls */}
                            <div className="relative z-10 space-y-2 text-left">
                              {/* Shopping Cart Yellow Basket */}
                              <div className="inline-flex items-center gap-1.5 bg-amber-400 text-slate-950 px-2.5 py-1 rounded-md text-[11px] font-bold shadow-md">
                                <span>🛒 ตะกร้าเหลือง ฿{activeClip.sale_price}</span>
                              </div>

                              {/* Creator Name & Thai Hook */}
                              <div className="text-white space-y-1">
                                <p className="text-xs font-bold text-slate-100">@aom_affiliate_pro</p>
                                <p className="text-[11px] text-slate-200 line-clamp-2 leading-tight bg-black/40 p-1.5 rounded backdrop-blur-sm">
                                  {activeClip.hook_text_th}
                                </p>
                              </div>

                              {/* Playback Controls & Sound Toggle */}
                              <div className="flex items-center justify-between pt-1 border-t border-white/10 text-[10px] text-slate-300">
                                <button
                                  onClick={() => setIsMuted(!isMuted)}
                                  className="flex items-center gap-1 text-slate-300 hover:text-white cursor-pointer"
                                >
                                  {isMuted ? <VolumeX className="w-3.5 h-3.5 text-red-400" /> : <Volume2 className="w-3.5 h-3.5 text-emerald-400" />}
                                  <span>{isMuted ? 'ปิดเสียง' : 'เปิดเสียง'}</span>
                                </button>
                                <span className="text-[10px] text-purple-300 font-medium">9:16 HD AI Video</span>
                              </div>
                            </div>
                          </div>

                          {/* Hook & Voiceover Script */}
                          <div className="sm:col-span-7 space-y-3 flex flex-col justify-between text-xs">
                            <div>
                              <label className="text-[11px] font-bold text-purple-400 uppercase tracking-wider block mb-1">
                                🎯 ข้อความฮุกหยุดนิ้ว (0-3 วินาทีแรก)
                              </label>
                              <p className="p-2.5 rounded-lg bg-slate-950 border border-purple-500/40 text-slate-200 font-medium text-xs leading-relaxed">
                                "{activeClip.hook_text_th}"
                              </p>
                            </div>

                            <div>
                              <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                                🎙️ เสียงพากย์และเนื้อหาทั้งหมด (Thai Natural Tone)
                              </label>
                              <p className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 leading-relaxed max-h-[140px] overflow-y-auto text-xs">
                                {activeClip.script.full_voiceover_th}
                              </p>
                            </div>

                            <div className="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-500/30 text-emerald-300">
                              <span className="font-bold flex items-center gap-1 text-[11px] mb-0.5">
                                <ShieldCheck className="w-3.5 h-3.5" /> ตรวจสอบความถูกต้องทางกฎหมาย (อย. / สคบ.)
                              </span>
                              <p className="text-[11px] text-emerald-400/90">
                                ผ่านเกณฑ์โฆษณา ไม่พบคำเคลมเกินจริง ใส่แท็ก #นายหน้า #affiliate ครบถ้วน
                              </p>
                            </div>
                          </div>
                        </div>

                        {/* Shot-by-Shot Storyboard for Google Flow */}
                        <div>
                          <h5 className="text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
                            <Layers className="w-3.5 h-3.5 text-purple-400" />
                            <span>สตอรี่บอร์ดแยกช็อตสำหรับ Google Flow Node</span>
                          </h5>
                          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                            {activeClip.script.storyboard_shots.map((shot) => (
                              <div key={shot.shot_number} className="bg-slate-900 p-2.5 rounded-lg border border-slate-800 text-[11px] space-y-1 hover:border-purple-500/40 transition-colors">
                                <div className="flex items-center justify-between text-purple-400 font-bold">
                                  <span>ช็อตที่ {shot.shot_number}</span>
                                  <span className="text-[10px] text-slate-400">{shot.start_sec}-{shot.end_sec}s</span>
                                </div>
                                <p className="text-slate-300 line-clamp-2">{shot.visual_description_th}</p>
                                <p className="text-slate-500 text-[10px] italic line-clamp-1">{shot.camera_direction}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      </>
                    );
                  })()}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Product Discovery & Opportunity Scoring Engine */}
        <section className="bg-slate-900/60 border border-slate-800 rounded-3xl p-6 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Compass className="w-5 h-5 text-purple-400" />
                <h3 className="text-lg font-bold text-white">สำรวจและคัดกรองสินค้าศักยภาพสูง (Product Discovery)</h3>
              </div>
              <p className="text-xs text-slate-400">
                โมเดล AI คำนวณคะแนนโอกาส (Opportunity Score) โดยไม่มองแค่ยอดขาย แต่วิเคราะห์ความต้องการ การแข่งขัน และค่าคอมมิชชั่นร่วมด้วย
              </p>
            </div>

            {/* Category Filter Tabs */}
            <div className="flex flex-wrap items-center gap-2">
              {[
                { id: 'ALL', label: 'ทั้งหมด' },
                { id: 'Skincare', label: 'สกินแคร์ / ความงาม' },
                { id: 'Kitchen', label: 'ของใช้ในบ้าน / ครัว' },
                { id: 'Gadgets', label: 'แกดเจ็ต / สุขภาพ' }
              ].map(cat => (
                <button
                  key={cat.id}
                  onClick={() => handleSearchAndFilter(cat.id, searchQuery)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                    selectedCategory === cat.id
                      ? 'bg-purple-600 text-white shadow-md'
                      : 'bg-slate-800/80 text-slate-400 hover:text-white'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="ค้นหาชื่อสินค้า, แบรนด์, หรือแท็ก เช่น เซรั่ม, หมอนนวด, แก้วเก็บความเย็น..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                handleSearchAndFilter(selectedCategory, e.target.value);
              }}
              className="w-full pl-10 pr-4 py-2.5 bg-slate-950/80 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-purple-500 transition-colors"
            />
          </div>

          {/* Products Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-3 px-3">สินค้า</th>
                  <th className="py-3 px-2">ราคาขาย</th>
                  <th className="py-3 px-2">ค่าคอม %</th>
                  <th className="py-3 px-2">รับต่อชิ้น (฿)</th>
                  <th className="py-3 px-2">ยอดขาย/เดือน</th>
                  <th className="py-3 px-2">เติบโต 7 วัน</th>
                  <th className="py-3 px-2">คะแนนโอกาส</th>
                  <th className="py-3 px-2">ระดับความสำคัญ</th>
                  <th className="py-3 px-3 text-right">ดำเนินการ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {products.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/30 transition-colors group">
                    <td className="py-3 px-3">
                      <div className="flex items-center gap-3">
                        <img
                          src={p.thumbnail_url}
                          alt={p.title_th}
                          className="w-10 h-10 rounded-lg object-cover bg-slate-800 shrink-0"
                        />
                        <div>
                          <p className="font-semibold text-slate-200 line-clamp-1 group-hover:text-purple-300 transition-colors">
                            {p.title_th}
                          </p>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-[10px] text-purple-400 font-medium">{p.category}</span>
                            <span className="text-[10px] text-slate-500">•</span>
                            <span className="text-[10px] text-amber-400 font-medium">★ {p.rating} ({p.review_count.toLocaleString()})</span>
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-2 font-semibold text-slate-200">฿{p.sale_price}</td>
                    <td className="py-3 px-2 text-purple-300 font-bold">{p.commission_rate}%</td>
                    <td className="py-3 px-2 text-emerald-400 font-bold">฿{p.estimated_commission.toFixed(2)}</td>
                    <td className="py-3 px-2 text-slate-300">{p.monthly_sales.toLocaleString()}</td>
                    <td className="py-3 px-2 font-semibold text-emerald-400">+{p.growth_rate_7d}%</td>
                    <td className="py-3 px-2">
                      <div className="flex items-center gap-1.5">
                        <div className="w-8 h-8 rounded-full bg-purple-900/60 border border-purple-500/40 flex items-center justify-center font-bold text-purple-200">
                          {p.opportunity_score.toFixed(0)}
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        p.classification === 'HIGH_PRIORITY'
                          ? 'bg-red-500/20 text-red-300 border border-red-500/30'
                          : p.classification === 'TEST'
                          ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                          : 'bg-slate-700 text-slate-300'
                      }`}>
                        {p.classification}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenIntelligence(p.id)}
                          className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-medium transition-colors cursor-pointer"
                        >
                          วิเคราะห์ AI
                        </button>
                        <button
                          onClick={() => handleGenerateDailyBatch([p.id])}
                          className="px-2.5 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-[11px] font-bold transition-all shadow-sm cursor-pointer"
                        >
                          สร้างคลิป
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Product Intelligence Modal / Card View */}
        {selectedProductIntelligence && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-purple-500/40 rounded-3xl max-w-3xl w-full max-h-[85vh] overflow-y-auto p-6 shadow-2xl space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-purple-400" />
                  <h3 className="text-lg font-bold text-white">Product Intelligence Card (11 Sections)</h3>
                </div>
                <button
                  onClick={() => setSelectedProductIntelligence(null)}
                  className="text-slate-400 hover:text-white text-lg font-bold px-2 py-1 cursor-pointer"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4 text-xs">
                <div>
                  <h4 className="font-bold text-purple-400 uppercase tracking-wider mb-1">1. สรุปภาพรวมสินค้า</h4>
                  <p className="text-slate-200 bg-slate-950 p-3 rounded-xl border border-slate-800">{selectedProductIntelligence.product_summary_th}</p>
                </div>

                <div>
                  <h4 className="font-bold text-purple-400 uppercase tracking-wider mb-1">2. กลุ่มเป้าหมายในไทย (Target Audience)</h4>
                  <p className="text-slate-300 bg-slate-950 p-3 rounded-xl border border-slate-800">{selectedProductIntelligence.target_audience_th}</p>
                </div>

                <div>
                  <h4 className="font-bold text-purple-400 uppercase tracking-wider mb-1">3. ปัญหาของลูกค้า (Customer Pain Points)</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {selectedProductIntelligence.customer_pain_points.map((pt, i) => (
                      <div key={i} className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                        <p className="font-semibold text-slate-200">{pt.issue_th}</p>
                        <p className="text-[10px] text-pink-400 mt-0.5">อารมณ์: {pt.emotional_trigger}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-bold text-purple-400 uppercase tracking-wider mb-1">4. จุดขายที่ไม่เหมือนใคร (USP)</h4>
                  <ul className="list-disc list-inside space-y-1 bg-slate-950 p-3 rounded-xl border border-slate-800 text-slate-300">
                    {selectedProductIntelligence.usp_th.map((u, i) => (
                      <li key={i}>{u}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="font-bold text-purple-400 uppercase tracking-wider mb-1">5. ฮุกแนะนำที่ผ่านการทดสอบ (Recommended Hooks)</h4>
                  <div className="space-y-2">
                    {selectedProductIntelligence.recommended_hooks.map((h, i) => (
                      <div key={i} className="bg-slate-950 p-2.5 rounded-lg border border-purple-500/30 flex items-center justify-between">
                        <div>
                          <span className="text-[10px] font-bold text-purple-400 uppercase">{h.hook_type}:</span>
                          <p className="text-slate-200 font-medium">"{h.hook_text_th}"</p>
                        </div>
                        <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">
                          คาดการณ์ค้างดู 3s: {h.estimated_retention_3s}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
                <button
                  onClick={() => setSelectedProductIntelligence(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold cursor-pointer"
                >
                  ปิด
                </button>
                <button
                  onClick={() => {
                    const pId = selectedProductIntelligence.product_id;
                    setSelectedProductIntelligence(null);
                    handleGenerateDailyBatch([pId]);
                  }}
                  className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold shadow-lg shadow-purple-600/30 cursor-pointer"
                >
                  สร้าง 5 คลิปทันที
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Social Accounts Connection Modal */}
        {isSettingsOpen && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <div className="bg-slate-900 border border-purple-500/40 rounded-3xl max-w-xl w-full p-6 shadow-2xl space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <Share2 className="w-5 h-5 text-pink-400" />
                  <h3 className="text-lg font-bold text-white">ผูกบัญชีโซเชียลสำหรับการโพสต์อัตโนมัติ</h3>
                </div>
                <button
                  onClick={() => setIsSettingsOpen(false)}
                  className="text-slate-400 hover:text-white text-lg font-bold px-2 py-1 cursor-pointer"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-3 text-xs">
                <p className="text-slate-300">
                  ระบบเชื่อมต่อผ่าน **Official Open API (OAuth 2.0)** อย่างปลอดภัย ไม่มีการขอรหัสผ่านส่วนตัว 100%
                </p>

                {/* TikTok Shop Account */}
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-pink-500/20 text-pink-400 flex items-center justify-center font-bold text-sm">
                      TK
                    </div>
                    <div>
                      <p className="font-bold text-slate-200">TikTok Shop Creator</p>
                      <p className="text-[11px] text-emerald-400">● เชื่อมต่อแล้ว: @aom_affiliate_pro</p>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-semibold transition-colors">
                    ตั้งค่าใหม่
                  </button>
                </div>

                {/* Shopee Video Account */}
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-orange-500/20 text-orange-400 flex items-center justify-center font-bold text-sm">
                      SP
                    </div>
                    <div>
                      <p className="font-bold text-slate-200">Shopee Video Channel</p>
                      <p className="text-[11px] text-emerald-400">● เชื่อมต่อแล้ว: Aom Review Official</p>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-semibold transition-colors">
                    ตั้งค่าใหม่
                  </button>
                </div>

                {/* Facebook Reels / Page */}
                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-sm">
                      FB
                    </div>
                    <div>
                      <p className="font-bold text-slate-200">Facebook Page / Reels</p>
                      <p className="text-[11px] text-emerald-400">● เชื่อมต่อแล้ว: Aom ป้ายยาของดี</p>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-semibold transition-colors">
                    ตั้งค่าใหม่
                  </button>
                </div>

                {/* Google Flow Direct Webhook */}
                <div className="p-3.5 rounded-xl bg-slate-950 border border-purple-500/30 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-purple-300 flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5" /> Google Flow Webhook URL
                    </span>
                    <span className="text-[10px] text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded">
                      Active
                    </span>
                  </div>
                  <input
                    type="text"
                    defaultValue="https://flow.google.internal/webhook/v1/generate-clips"
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-slate-300 text-[11px] focus:outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
                <button
                  onClick={() => setIsSettingsOpen(false)}
                  className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold shadow-lg shadow-purple-600/30 cursor-pointer"
                >
                  บันทึกการตั้งค่า
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
