"""
Script để tạo Molecule Cloud từ file CSV
Đọc: SMILES (cột A), Toxicity (cột B), Scaffold (cột C)
"""

import pandas as pd
from molecule_cloud import MoleculeCloud
import os
import sys

# ============ CẤU HÌNH ============
CSV_FILE = 'file tổng số lượng scaffold.csv'  # 👈 TÊN FILE CỦA BẠN
OUTPUT_PNG = 'molecule_cloud.png'
OUTPUT_SVG = 'molecule_cloud.svg'
RANDOM_SEED = 42

print("=" * 60)
print("🧬 MOLECULE CLOUD GENERATOR")
print("=" * 60)

# ============ KIỂM TRA FILE ============
if not os.path.exists(CSV_FILE):
    print(f"\n❌ Lỗi: File '{CSV_FILE}' không tìm thấy!")
    print(f"\n📂 Các file CSV trong thư mục hiện tại:")
    found = False
    for f in os.listdir('.'):
        if f.endswith('.csv'):
            print(f"   - {f} ✅")
            found = True
    if not found:
        print(f"   (Không tìm thấy file CSV nào)")
    print(f"\n💡 Hãy kiểm tra tên file hoặc copy vào thư mục này")
    sys.exit(1)

print(f"\n✅ Tìm thấy file: {CSV_FILE}")

# ============ ĐỌC DỮ LIỆU ============
try:
    print("\n📖 Đang đọc file CSV...")
    # Thử nhiều encoding khác nhau vì file CSV từ khác có thể dùng encoding khác
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
    except:
        try:
            df = pd.read_csv(CSV_FILE, encoding='latin-1')
        except:
            df = pd.read_csv(CSV_FILE, encoding='cp1252')
    
    print(f"   - Số rows: {len(df)}")
    print(f"   - Các cột: {list(df.columns)}")
    print(f"\n🔍 Dữ liệu mẫu (5 rows đầu):")
    print(df.head())
    print()
    
except Exception as e:
    print(f"❌ Lỗi khi đọc file: {e}")
    sys.exit(1)

# ============ CẤU TRÚC DỮ LIỆU ============
# Giả sử: Cột A = SMILES, Cột B = Toxicity, Cột C = Scaffold
# Lấy tên cột tự động
col_names = list(df.columns)

print(f"⚙️  Đang xử lý dữ liệu...")

# Lấy cột đầu tiên (SMILES)
col_smiles = col_names[0] if len(col_names) > 0 else 'SMILES'
# Lấy cột thứ 2 (Toxicity)
col_toxicity = col_names[1] if len(col_names) > 1 else 'Toxicity'
# Lấy cột thứ 3 (Scaffold)
col_scaffold = col_names[2] if len(col_names) > 2 else 'Scaffold'

print(f"   - Cột 1 (SMILES): {col_smiles}")
print(f"   - Cột 2 (Toxicity): {col_toxicity}")
print(f"   - Cột 3 (Scaffold): {col_scaffold}\n")

# ============ CHỌN DỮ LIỆU ============
print(f"💡 Chọn dữ liệu để vẽ cloud:")
print(f"   Option 1: Dùng Scaffold SMILES (cột 3) ✅ KHUYÊN DÙNG")
print(f"   Option 2: Dùng Original SMILES (cột 1)")

# Mặc định dùng Scaffold (vì đó là scaffold của tác dụng)
use_scaffold = True

if use_scaffold:
    print(f"\n✅ Sử dụng: Scaffold column (cột 3)\n")
    data_for_cloud = pd.DataFrame({
        'SMILES': df[col_scaffold],
        'Activity': df[col_toxicity]
    })
else:
    print(f"\n✅ Sử dụng: SMILES column (cột 1)\n")
    data_for_cloud = pd.DataFrame({
        'SMILES': df[col_smiles],
        'Activity': df[col_toxicity]
    })

# Xóa rows với SMILES rỗng
initial_count = len(data_for_cloud)
data_for_cloud = data_for_cloud.dropna(subset=['SMILES'])
data_for_cloud = data_for_cloud[data_for_cloud['SMILES'].astype(str).str.strip() != '']
removed_count = initial_count - len(data_for_cloud)

if removed_count > 0:
    print(f"   ⚠️  Bỏ qua {removed_count} rows có SMILES rỗng")

print(f"   📊 Valid rows: {len(data_for_cloud)}")
print(f"   🧬 Unique scaffolds: {data_for_cloud['SMILES'].nunique()}")

# Kiểm tra Activity
if 'Activity' in data_for_cloud.columns:
    activity_values = data_for_cloud['Activity'].unique()
    print(f"   🎯 Activity values: {sorted(activity_values)}")

# ============ LƯU TẠM THÀNH EXCEL ============
# Vì MoleculeCloud chỉ đọc Excel, nên convert CSV -> Excel tạm thời
temp_file = '__temp_cloud_data__.xlsx'
print(f"\n💾 Chuyển đổi CSV → Excel tạm thời...")
data_for_cloud.to_excel(temp_file, index=False)
print(f"   ✅ Lưu vào: {temp_file}")

# ============ TẠO MOLECULE CLOUD ============
try:
    print(f"\n🔄 Đang tạo Molecule Cloud...")
    print(f"   - Random seed: {RANDOM_SEED}")
    print(f"   - Canvas: 1200x800\n")
    
    cloud = MoleculeCloud(
        excel_file=temp_file,
        random_seed=RANDOM_SEED,
        canvas_width=1200,
        canvas_height=800
    )
    
    print(f"   ✅ Loaded: {len(cloud.scaffolds)} unique scaffolds")
    
    # In thống kê
    sizes = cloud.scaffolds.get_scaffolds_list()
    if sizes:
        freqs = [s.frequency for s in sizes]
        print(f"   📊 Frequency - Min: {min(freqs)}, Max: {max(freqs)}, Avg: {sum(freqs)/len(freqs):.1f}")
    
    # ============ GENERATE LAYOUT ============
    print(f"\n⚙️  Đang generate layout...")
    print(f"   [1/4] Spiral placement...")
    print(f"   [2/4] Collision avoidance...")
    print(f"   [3/4] Force-directed relaxation...")
    print(f"   [4/4] Compaction...")
    
    cloud.generate(
        use_force_relaxation=True,
        use_compaction=True
    )
    print(f"   ✅ Layout generated successfully")
    
    # ============ EXPORT PNG ============
    print(f"\n💾 Exporting...")
    print(f"   Generating PNG...")
    cloud.export_png(OUTPUT_PNG)
    file_size_png = os.path.getsize(OUTPUT_PNG) / 1024  # KB
    print(f"   ✅ PNG: {OUTPUT_PNG} ({file_size_png:.1f} KB)")
    
    # ============ EXPORT SVG ============
    print(f"   Generating SVG...")
    cloud.export_svg(OUTPUT_SVG)
    file_size_svg = os.path.getsize(OUTPUT_SVG) / 1024  # KB
    print(f"   ✅ SVG: {OUTPUT_SVG} ({file_size_svg:.1f} KB)")
    
    # Xóa file tạm
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"   🧹 Cleaned up temporary files")
    
    print(f"\n{'=' * 60}")
    print(f"🎉 HOÀN THÀNH!")
    print(f"{'=' * 60}")
    print(f"📁 Kết quả trong thư mục hiện tại:")
    print(f"   📌 PNG: {OUTPUT_PNG}")
    print(f"   📌 SVG: {OUTPUT_SVG}")
    print(f"{'=' * 60}\n")
    
    print(f"💡 Bước tiếp theo:")
    print(f"   1. Mở {OUTPUT_PNG} để xem hình ảnh")
    print(f"   2. Dùng {OUTPUT_SVG} trong Illustrator hoặc Inkscape để chỉnh sửa")
    print()
    
except Exception as e:
    print(f"\n❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    
    # Xóa file tạm nếu lỗi
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    sys.exit(1)
