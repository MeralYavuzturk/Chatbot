import React, { useState, useEffect, useRef } from 'react';
import {
  FileText,
  Send,
  Bot,
  User,
  Circle,
  Loader2
} from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const App = () => {
  const [messages, setMessages] = useState([
    {
      id: 'init-1',
      type: 'bot',
      text: 'Merhaba! Ben T.C. Sağlık Bakanlığı dokümanları konusunda size yardımcı olacak asistanım. Size nasıl yardımcı olabilirim?',
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      text: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input }),
      });

      if (!response.ok) throw new Error('API hatası oluştu');

      const data = await response.json();

      const botMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: data.answer,
        sources: data.sources?.map(s => ({
          name: `${s.file_name} (Sayfa ${s.page})`,
          icon: 'check'
        })) || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Soru sorma hatası:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: 'Üzgünüm, bir hata oluştu. Lütfen backend servisinin çalıştığından emin olun.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const documents = [
    { id: 1, name: 'Diyabet Rehberi', active: true },
  ];

  const suggestions = [];

  return (
    <div className="flex h-screen bg-[#f8fafc] text-slate-800 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col p-6 space-y-8 hidden md:flex">
        <div>
          <h2 className="text-lg font-bold text-slate-700 mb-6">İndekslenen Belgeler</h2>
          <div className="space-y-3">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className={`flex items-center space-x-3 p-3 rounded-xl cursor-pointer transition-all duration-200 ${doc.active
                    ? 'bg-[#e0f7fa] text-[#00acc1] border border-[#00acc1]/20 shadow-sm'
                    : 'text-slate-500 hover:bg-slate-50'
                  }`}
              >
                <FileText size={18} />
                <span className="font-medium text-sm">{doc.name}</span>
                {doc.active && <div className="ml-auto w-1 h-4 bg-[#00acc1] rounded-full"></div>}
              </div>
            ))}
          </div>
        </div>

        <div className="mt-auto">
          <div className="rounded-2xl overflow-hidden shadow-lg aspect-square bg-white p-4 border border-slate-100">
            <img
              src="/heart-logo.png"
              alt="Medical context"
              className="w-full h-full object-contain"
            />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative">
        {/* Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 z-10">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-[#00acc1] rounded-lg flex items-center justify-center">
              <Bot size={20} className="text-white" />
            </div>
            <h1 className="text-sm font-semibold text-slate-500">T.C. Sağlık Bakanlığı Verileri ile Güçlendirilmiş</h1>
          </div>
          <div className="flex items-center space-x-2 text-xs font-bold text-emerald-500">
            <Circle size={8} fill="currentColor" className="animate-pulse" />
            <span>SİSTEM ÇEVRİMİÇİ</span>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 pb-40">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-4 duration-500`}
            >
              <div className={`flex max-w-[85%] md:max-w-[70%] ${msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'} items-start gap-4`}>
                <div className={`w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center ${msg.type === 'user' ? 'bg-[#00acc1]' : 'bg-[#e0f7fa] text-[#00acc1]'
                  }`}>
                  {msg.type === 'bot' ? <Bot size={20} /> : <User size={20} className="text-white" />}
                </div>

                <div className={`p-5 rounded-2xl shadow-sm ${msg.type === 'user'
                    ? 'bg-[#00acc1] text-white rounded-tr-none'
                    : 'bg-white border border-slate-100 rounded-tl-none'
                  }`}>
                  <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{msg.text}</p>

                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-4 flex flex-wrap gap-2">
                      {msg.sources.map((source, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 text-slate-500 rounded-full text-[11px] font-medium border border-slate-200"
                        >
                          <Circle size={10} fill="currentColor" />
                          <span>Kaynak: {source.name}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start animate-pulse">
              <div className="flex items-center gap-4 bg-white p-4 rounded-2xl border border-slate-100 shadow-sm">
                <Loader2 className="animate-spin text-[#00acc1]" size={20} />
                <span className="text-sm text-slate-500 font-medium">Asistan cevap hazırlıyor...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Bottom Input Area */}
        <div className="absolute bottom-0 left-0 right-0 p-8 bg-gradient-to-t from-[#f8fafc] via-[#f8fafc] to-transparent">
          <div className="max-w-4xl mx-auto space-y-4">
            {/* Input Box */}
            <div className="relative group">
              <div className="absolute inset-0 bg-[#00acc1]/10 blur-xl group-focus-within:bg-[#00acc1]/20 transition-all rounded-3xl"></div>
              <div className="relative bg-white rounded-2xl shadow-xl border border-slate-100 flex items-center p-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Sağlık sorunuzu buraya yazın..."
                  className="flex-1 bg-transparent border-none focus:ring-0 text-sm px-2 text-slate-700"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSend}
                  disabled={isLoading || !input.trim()}
                  className="w-12 h-12 bg-[#00acc1] text-white rounded-xl flex items-center justify-center hover:bg-[#0097a7] transition-all shadow-lg hover:scale-105 active:scale-95 disabled:bg-slate-300 disabled:scale-100"
                >
                  {isLoading ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
