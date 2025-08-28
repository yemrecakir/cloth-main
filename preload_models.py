#!/usr/bin/env python3
"""
Model önyükleme scripti - Google Cloud Run deployment öncesi modelleri indir
"""

import os
import sys
from rembg import new_session, remove
import requests
from PIL import Image
import io
import time

def download_and_test_model(model_name, retry_count=3):
    """Model indir ve test et"""
    for attempt in range(retry_count):
        try:
            print(f"📥 {model_name} modeli indiriliyor... (deneme {attempt + 1}/{retry_count})")
            
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
            
            # Model dosya boyutunu kontrol et
            model_path = os.path.expanduser(f"~/.u2net/{model_name}")
            if os.path.exists(model_path):
                size = os.path.getsize(model_path) / (1024 * 1024)
                print(f"📊 {model_name} model boyutu: {size:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ {model_name} modeli yüklenemedi (deneme {attempt + 1}): {str(e)}")
            if attempt < retry_count - 1:
                print("⏳ 5 saniye bekleyip tekrar denenecek...")
                time.sleep(5)
            else:
                print(f"💥 {model_name} modeli {retry_count} denemede de başarısız oldu")
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