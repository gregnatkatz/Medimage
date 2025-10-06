"""
Organize multi-modal liver imaging datasets for demo (60%) and live testing (40%)
"""

import os
import shutil
import random
from pathlib import Path

KAGGLE_DATA_DIR = Path(__file__).parent / "data" / "kaggle"
ORGANIZED_DIR = Path(__file__).parent / "data" / "organized"
DEMO_RATIO = 0.6
RANDOM_SEED = 42

def organize_chaos_ct():
    """Organize CHAOS CT scans"""
    print("\n📊 Organizing CHAOS CT scans...")
    
    source_dir = KAGGLE_DATA_DIR / "chaos-ct-mr" / "CHAOS_Train_Sets" / "Train_Sets" / "CT"
    demo_dir = ORGANIZED_DIR / "demo" / "ct"
    live_dir = ORGANIZED_DIR / "live_testing" / "ct"
    
    demo_dir.mkdir(parents=True, exist_ok=True)
    live_dir.mkdir(parents=True, exist_ok=True)
    
    patients = sorted([d for d in source_dir.iterdir() if d.is_dir()])
    random.Random(RANDOM_SEED).shuffle(patients)
    
    split_idx = int(len(patients) * DEMO_RATIO)
    demo_patients = patients[:split_idx]
    live_patients = patients[split_idx:]
    
    print(f"   Total CT patients: {len(patients)}")
    print(f"   Demo (60%): {len(demo_patients)} patients")
    print(f"   Live testing (40%): {len(live_patients)} patients")
    
    for patient in demo_patients:
        dest = demo_dir / patient.name
        if not dest.exists():
            shutil.copytree(patient, dest)
    
    for patient in live_patients:
        dest = live_dir / patient.name
        if not dest.exists():
            shutil.copytree(patient, dest)
    
    print(f"   ✅ CT scans organized")
    return len(demo_patients), len(live_patients)


def organize_chaos_mri():
    """Organize CHAOS MRI scans"""
    print("\n📊 Organizing CHAOS MRI scans...")
    
    source_dir = KAGGLE_DATA_DIR / "chaos-ct-mr" / "CHAOS_Train_Sets" / "Train_Sets" / "MR"
    demo_dir = ORGANIZED_DIR / "demo" / "mri"
    live_dir = ORGANIZED_DIR / "live_testing" / "mri"
    
    demo_dir.mkdir(parents=True, exist_ok=True)
    live_dir.mkdir(parents=True, exist_ok=True)
    
    patients = sorted([d for d in source_dir.iterdir() if d.is_dir()])
    random.Random(RANDOM_SEED).shuffle(patients)
    
    split_idx = int(len(patients) * DEMO_RATIO)
    demo_patients = patients[:split_idx]
    live_patients = patients[split_idx:]
    
    print(f"   Total MRI patients: {len(patients)}")
    print(f"   Demo (60%): {len(demo_patients)} patients")
    print(f"   Live testing (40%): {len(live_patients)} patients")
    
    for patient in demo_patients:
        dest = demo_dir / patient.name
        if not dest.exists():
            shutil.copytree(patient, dest)
    
    for patient in live_patients:
        dest = live_dir / patient.name
        if not dest.exists():
            shutil.copytree(patient, dest)
    
    print(f"   ✅ MRI scans organized")
    return len(demo_patients), len(live_patients)


def organize_ultrasound():
    """Organize ultrasound images"""
    print("\n📊 Organizing ultrasound images...")
    
    source_base = KAGGLE_DATA_DIR / "liver-ultrasound" / "7272660"
    demo_dir = ORGANIZED_DIR / "demo" / "ultrasound"
    live_dir = ORGANIZED_DIR / "live_testing" / "ultrasound"
    
    demo_dir.mkdir(parents=True, exist_ok=True)
    live_dir.mkdir(parents=True, exist_ok=True)
    
    total_demo = 0
    total_live = 0
    
    for category in ["Benign", "Malignant", "Normal"]:
        source_dir = source_base / category / category / "image"
        if not source_dir.exists():
            print(f"   ⚠️ Skipping {category} - not found")
            continue
        
        images = sorted(list(source_dir.glob("*.jpg")))
        random.Random(RANDOM_SEED).shuffle(images)
        
        split_idx = int(len(images) * DEMO_RATIO)
        demo_images = images[:split_idx]
        live_images = images[split_idx:]
        
        print(f"   {category}: {len(images)} total, {len(demo_images)} demo, {len(live_images)} live")
        
        demo_category_dir = demo_dir / category
        live_category_dir = live_dir / category
        demo_category_dir.mkdir(parents=True, exist_ok=True)
        live_category_dir.mkdir(parents=True, exist_ok=True)
        
        for img in demo_images:
            dest = demo_category_dir / img.name
            if not dest.exists():
                shutil.copy2(img, dest)
        
        for img in live_images:
            dest = live_category_dir / img.name
            if not dest.exists():
                shutil.copy2(img, dest)
        
        total_demo += len(demo_images)
        total_live += len(live_images)
    
    print(f"   ✅ Ultrasound images organized")
    return total_demo, total_live


def create_summary():
    """Create a summary file with organization details"""
    summary_path = ORGANIZED_DIR / "DATA_ORGANIZATION.txt"
    
    with open(summary_path, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("Multi-Modal Liver Imaging Dataset Organization\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("Organization: 60% Demo / 40% Live Testing\n")
        f.write("Random Seed: 42 (for reproducibility)\n\n")
        
        f.write("Directory Structure:\n")
        f.write("  organized/\n")
        f.write("  ├── demo/              (60% - Pre-processed for demonstrations)\n")
        f.write("  │   ├── ct/            CHAOS CT scans\n")
        f.write("  │   ├── mri/           CHAOS MRI scans\n")
        f.write("  │   └── ultrasound/    Ultrasound images\n")
        f.write("  └── live_testing/      (40% - Raw data for live testing)\n")
        f.write("      ├── ct/\n")
        f.write("      ├── mri/\n")
        f.write("      └── ultrasound/\n\n")
        
        f.write("Dataset Sources:\n")
        f.write("  - CHAOS: Combined CT-MR Healthy Abdominal Organ Segmentation\n")
        f.write("  - Ultrasound: Annotated Ultrasound Liver Images Dataset\n\n")
        
        f.write("Modalities Available:\n")
        f.write("  ✅ CT (Computed Tomography)\n")
        f.write("  ✅ MRI (Magnetic Resonance Imaging)\n")
        f.write("  ✅ Ultrasound (B-mode)\n")
        f.write("  ❌ Pathology (Not available on Kaggle)\n\n")
    
    print(f"\n✅ Summary saved to: {summary_path}")


def main():
    print("=" * 70)
    print("Multi-Modal Dataset Organization Script")
    print("=" * 70)
    print(f"\nSource: {KAGGLE_DATA_DIR}")
    print(f"Destination: {ORGANIZED_DIR}")
    print(f"Split: {int(DEMO_RATIO * 100)}% demo / {int((1 - DEMO_RATIO) * 100)}% live testing\n")
    
    if ORGANIZED_DIR.exists():
        response = input(f"⚠️  {ORGANIZED_DIR} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("❌ Organization cancelled")
            return
        shutil.rmtree(ORGANIZED_DIR)
    
    ct_demo, ct_live = organize_chaos_ct()
    mri_demo, mri_live = organize_chaos_mri()
    us_demo, us_live = organize_ultrasound()
    
    create_summary()
    
    print("\n" + "=" * 70)
    print("Organization Complete!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  CT:         {ct_demo} demo, {ct_live} live testing")
    print(f"  MRI:        {mri_demo} demo, {mri_live} live testing")
    print(f"  Ultrasound: {us_demo} demo, {us_live} live testing")
    print(f"\n✅ All datasets organized and ready for use!")


if __name__ == "__main__":
    main()
