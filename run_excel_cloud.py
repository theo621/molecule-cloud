"""
Script để tạo Molecule Cloud từ file Excel
Đọc: SMILES (cột A), Toxicity (cột B), Scaffold (cột C)
"""

from molecule_cloud import MoleculeCloud
import os
import sys

# ============ CẤU HÌNH ============
EXCEL_FILE = 'file tổng số lượng scaffold.xlsx'  # 👈 TÊN FILE CỦA BẠN
OUTPUT_PNG = 'molecule_cloud.png'
OUTPUT_SVG = 'molecule_cloud.svg'
RANDOM_SEED = 42

print("=" * 60)
print("🧬 MOLECULE CLOUD GENERATOR")
print("=" * 60)

# ============ KIỂM TRA FILE ============
if not os.path.exists(EXCEL_FILE):
    print(f"\n❌ Lỗi: File '{EXCEL_FILE}' không tìm thấy!")
    print(f"\n📂 Các file Excel trong thư mục hiện tại:")
    found = False
    for f in os.listdir('.'):
        if f.endswith(('.xlsx', '.xls')):
            print(f"   - {f} ✅")
            found = True
    if not found:
        print(f"   (Không tìm thấy file Excel nào)")
    sys.exit(1)

print(f"\n✅ Tìm thấy file: {EXCEL_FILE}")

# ============ TẠO MOLECULE CLOUD ============
try:
    print(f"\n🔄 Đang tạo Molecule Cloud...")
    print(f"   - Random seed: {RANDOM_SEED}")
    print(f"   - Canvas: 1200x800\n")
    
    cloud = MoleculeCloud(
        excel_file=EXCEL_FILE,
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
    sys.exit(1)
