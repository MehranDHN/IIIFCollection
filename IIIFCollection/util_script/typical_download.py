import requests
import os
from tqdm import tqdm

# ================== CONFIGURATION ==================
start_idr = 4147896
end_idr   = 4148433
max_seq_per_idr = 600          # safety limit
save_folder = "D:\\www.ResanehAfzar.ir\\FlorenceShahnama"

os.makedirs(save_folder, exist_ok=True)

print(f"Downloading Florence Shahnameh from IDR {start_idr} to {end_idr}...\n")

total_downloaded = 0


    
for seq in range(1, max_seq_per_idr + 1):
        idr_num = start_idr
        idr = f"BNCF000{idr_num}"
        url = f"https://teca.bncf.firenze.sbn.it/ImageViewer/servlet/ImageViewer?idr={idr}&azione=showImg&sequence={seq}"
        
        try:
            response = requests.get(url, timeout=25)
            
            if response.status_code == 200 and len(response.content) > 8000:  # filter out error/empty images
                filename = f"{idr}_p{seq:04d}.jpg"
                filepath = os.path.join(save_folder, filename)
                idr_num += 1  # increment IDR for next attempt
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                total_downloaded += 1
            else:
                # No more pages in this IDR → move to next IDR
                break
                
        except Exception:
            break  # network issue or timeout → skip to next IDR

print(f"\n✅ Download completed!")
print(f"   Total images saved: {total_downloaded}")
print(f"   Folder: ./{save_folder}")