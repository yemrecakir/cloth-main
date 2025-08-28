#!/usr/bin/env python3
"""
Model önyükleme scripti - Render.com deployment öncesi modelleri indir
"""

import os
import sys
from rembg import new_session, remove
import requests
from PIL import Image
import io

def download_and_test_model(model_name):
    """Model indir ve test et"""
    try:
        print(f"📥 {model_name} modeli indiriliyor...")
        
        # Model session oluştur (bu modeli indirir)
        session = new_session(model_name)
        print(f"✅ {model_name} modeli başarıyla indirildi")
        
        # Basit bir test resmi oluştur
        test_image = Image.new('RGB', (100, 100), color='red')
        test_bytes = io.BytesIO()
        test_image.save(test_bytes, format='PNG')
        test_bytes.seek(0)
        
        # Modeli test et
        result = remove(test_bytes.getvalue(), session=session)
        print(f"✅ {model_name} modeli test edildi ve çalışıyor")
        
        return True
        
    except Exception as e:
        print(f"❌ {model_name} modeli yüklenemedi: {str(e)}")
        return False

def main():
    """Ana modelleri önceden yükle"""
    print("🤖 AI Modelleri önyükleniyor...")
    print("=" * 50)
    
    # Kullanılan ana modeller
    models_to_preload = [
        'u2net',           # Varsayılan model
        'u2net_cloth_seg', # Kıyafet özel model
        'isnet-general-use', # DIS model  
        'dis-general-use',   # DIS genel
    ]
    
    success_count = 0
    
    for model in models_to_preload:
        if download_and_test_model(model):
            success_count += 1
        print("-" * 30)
    
    print(f"\n🎯 Sonuç: {success_count}/{len(models_to_preload)} model başarıyla yüklendi")
    
    if success_count > 0:
        print("✅ Modeller hazır! Server başlatılabilir.")
        return 0
    else:
        print("❌ Hiçbir model yüklenemedi!")
        return 1

if __name__ == "__main__":
    sys.exit(main())