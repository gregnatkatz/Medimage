"""
Generate synthetic patient EHR data for medical imaging datasets
Uses faker to create realistic patient demographics and medical backgrounds
"""

import json
import random
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

ORGANIZED_DIR = Path(__file__).parent / "data" / "organized"
DEMO_DIR = ORGANIZED_DIR / "demo"
LIVE_DIR = ORGANIZED_DIR / "live_testing"

LIVER_CONDITIONS = [
    "Hepatocellular Carcinoma (HCC)",
    "Liver Cirrhosis (Alcoholic)",
    "Liver Cirrhosis (Viral Hepatitis C)",
    "Non-Alcoholic Steatohepatitis (NASH)",
    "Hepatitis B Chronic Infection",
    "Hepatitis C Chronic Infection",
    "Fatty Liver Disease (NAFLD)",
    "Liver Metastases (Colorectal origin)",
    "Autoimmune Hepatitis",
    "Primary Biliary Cholangitis"
]

RISK_FACTORS = [
    "Chronic alcohol use",
    "Type 2 Diabetes Mellitus",
    "Obesity (BMI > 30)",
    "Hepatitis B vaccination history",
    "Previous hepatitis infection",
    "Family history of liver disease",
    "Metabolic syndrome",
    "History of blood transfusions"
]

def generate_patient_record(patient_id, modality, category=None):
    """Generate a single patient record"""
    Faker.seed(hash(patient_id) % 2**32)
    random.seed(hash(patient_id) % 2**32)
    
    age = random.choices(
        range(35, 85),
        weights=[1]*10 + [3]*35 + [1]*5
    )[0]
    
    gender = random.choice(["Male", "Female"])
    
    if gender == "Male":
        name = fake.name_male()
    else:
        name = fake.name_female()
    
    if category:
        if category == "Malignant":
            primary_condition = random.choice([
                "Hepatocellular Carcinoma (HCC)",
                "Liver Metastases (Colorectal origin)"
            ])
        elif category == "Benign":
            primary_condition = random.choice([
                "Liver Cirrhosis (Viral Hepatitis C)",
                "Fatty Liver Disease (NAFLD)",
                "Autoimmune Hepatitis"
            ])
        else:
            primary_condition = "No significant liver pathology"
    else:
        primary_condition = random.choice(LIVER_CONDITIONS)
    
    risk_factors = random.sample(RISK_FACTORS, k=random.randint(1, 2))
    
    medical_background = f"{primary_condition}. "
    if risk_factors:
        medical_background += f"Risk factors: {', '.join(risk_factors)}. "
    
    if "Cirrhosis" in primary_condition or "Hepatitis" in primary_condition:
        medical_background += f"Elevated ALT/AST. "
    if "HCC" in primary_condition:
        medical_background += f"Elevated AFP (Alpha-fetoprotein). "
    
    return {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "ethnicity": random.choice([
            "Caucasian", "African American", "Hispanic/Latino", 
            "Asian", "Native American", "Mixed"
        ]),
        "medical_background": medical_background.strip(),
        "study_date": fake.date_between(start_date="-2y", end_date="today").isoformat()
    }

def generate_ct_mri_patients(base_dir, split_name):
    """Generate patient records for CT and MRI patients"""
    patients = {}
    
    ct_dir = base_dir / "ct"
    if ct_dir.exists():
        for patient_dir in sorted(ct_dir.iterdir()):
            if patient_dir.is_dir():
                patient_id = f"CT-{split_name}-{patient_dir.name}"
                patients[patient_id] = generate_patient_record(
                    patient_id, "CT"
                )
                patients[patient_id]["image_directory"] = str(patient_dir.relative_to(base_dir))
    
    mri_dir = base_dir / "mri"
    if mri_dir.exists():
        for patient_dir in sorted(mri_dir.iterdir()):
            if patient_dir.is_dir():
                patient_id = f"MRI-{split_name}-{patient_dir.name}"
                patients[patient_id] = generate_patient_record(
                    patient_id, "MRI"
                )
                patients[patient_id]["image_directory"] = str(patient_dir.relative_to(base_dir))
    
    return patients

def generate_ultrasound_patients(base_dir, split_name):
    """Generate virtual patients for ultrasound images (group 3-5 images per patient)"""
    patients = {}
    ultrasound_dir = base_dir / "ultrasound"
    
    if not ultrasound_dir.exists():
        return patients
    
    patient_counter = 1
    
    for category in ["Benign", "Malignant", "Normal"]:
        category_dir = ultrasound_dir / category
        if not category_dir.exists():
            continue
        
        image_files = sorted(list(category_dir.glob("*.jpg")))
        
        images_per_patient = 4
        for i in range(0, len(image_files), images_per_patient):
            patient_images = image_files[i:i+images_per_patient]
            
            patient_id = f"US-{split_name}-{patient_counter:03d}"
            patient_record = generate_patient_record(
                patient_id, "Ultrasound", category
            )
            patient_record["images"] = [
                str(img.relative_to(base_dir)) for img in patient_images
            ]
            patient_record["category"] = category
            
            patients[patient_id] = patient_record
            patient_counter += 1
    
    return patients

def main():
    print("=" * 70)
    print("Generating Synthetic Patient EHR Data")
    print("=" * 70)
    
    print("\n📋 Generating demo patient records...")
    demo_patients = {}
    demo_patients.update(generate_ct_mri_patients(DEMO_DIR, "DEMO"))
    demo_patients.update(generate_ultrasound_patients(DEMO_DIR, "DEMO"))
    
    demo_output = DEMO_DIR / "patients.json"
    with open(demo_output, "w") as f:
        json.dump(demo_patients, f, indent=2)
    
    print(f"✅ Generated {len(demo_patients)} demo patient records")
    print(f"   Saved to: {demo_output}")
    
    print("\n📋 Generating live testing patient records...")
    live_patients = {}
    live_patients.update(generate_ct_mri_patients(LIVE_DIR, "LIVE"))
    live_patients.update(generate_ultrasound_patients(LIVE_DIR, "LIVE"))
    
    live_output = LIVE_DIR / "patients.json"
    with open(live_output, "w") as f:
        json.dump(live_patients, f, indent=2)
    
    print(f"✅ Generated {len(live_patients)} live testing patient records")
    print(f"   Saved to: {live_output}")
    
    print("\n" + "=" * 70)
    print("Patient Data Generation Complete!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    
    demo_ct = len([p for p in demo_patients.keys() if p.startswith("CT-")])
    demo_mri = len([p for p in demo_patients.keys() if p.startswith("MRI-")])
    demo_us = len([p for p in demo_patients.keys() if p.startswith("US-")])
    
    print(f"  Demo: {demo_ct} CT patients, {demo_mri} MRI patients, {demo_us} ultrasound patients")
    
    live_ct = len([p for p in live_patients.keys() if p.startswith("CT-")])
    live_mri = len([p for p in live_patients.keys() if p.startswith("MRI-")])
    live_us = len([p for p in live_patients.keys() if p.startswith("US-")])
    
    print(f"  Live: {live_ct} CT patients, {live_mri} MRI patients, {live_us} ultrasound patients")
    print(f"\n✅ Patient data ready for use!")

if __name__ == "__main__":
    main()
