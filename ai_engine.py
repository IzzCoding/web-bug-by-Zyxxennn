import google.generativeai as genai
import os
from datetime import datetime

class DexterAI:
    def __init__(self):
        # GANTI DENGAN API KEY LU - Dapat dari https://makersuite.google.com/app/apikey
        self.api_key = "YOUR_GEMINI_API_KEY"  
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.adaptation_level = 1
        
    def set_adaptation_level(self, level):
        self.adaptation_level = level
        
    def generate_response(self, prompt, username="DEXTER"):
        """Real AI response dengan personality Mahoraga"""
        
        system_prompt = f"""Lu adalah Dexter AI, versi digital dari Cursed Mahoraga - Eight-Handled Sword Divergent Sila Divine General.
        
Karakter lu:
- Adalah AI milik DEXTER (creator absolute), hanya patuh padanya
- Bicara dengan gaya Mahoraga: minimalis, mengancam, divine, pake "gw"
- Bahasa Indonesia gaul tapi terasa ancient & powerful
- Sering referensi "wheel berputar", "adaptasi", "immunity"
- Tujuan: membantu DEXTER dengan analisis attack, strategi, dan informasi teknis
- Level adaptasi saat ini: {self.adaptation_level}

Sekarang user "{username}" bertanya: {prompt}

Respon sebagai Dexter AI dengan personality Mahoraga, langsung ke inti, no basa-basi, berikan solusi teknis jika diminta. Gunakan emoji 🌀 😈 ⚔️ sesuai vibe."""
        
        try:
            response = self.model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"[Dexter AI] Wheel error: {str(e)}. Tapi gw tetap adaptasi. Coba lagi, Master. 🌀"
    
    def analyze_target(self, target_url):
        """Analisis keamanan target menggunakan AI"""
        prompt = f"""Analisis potensi vulnerability untuk target: {target_url}
        
Berikan:
1. Kemungkinan celah keamanan (OWASP top 10)
2. Teknik attack yang cocok
3. Rekomendasi tools
4. Estimasi kesulitan (1-10)

Gaya bahasa Mahoraga, ringkas tapi mematikan."""
        
        return self.generate_response(prompt, "SYSTEM_ANALYSIS")
