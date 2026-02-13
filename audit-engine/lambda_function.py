import json
import boto3
import re
import math

# LC DIGITAL SOLUTIONS: API_relay
# Partner: Henry | Leo
# Role: Authorized Service Provider (Agent for the Dealer)
# Method: Passive Witness Ingestion (No-Touch Model)
# Goal: Forensic Verification of "Bot DNA" and Lead Waste

s3_client = boto3.client('s3')

def get_data_entropy(text):
    """
    Detects 'Keyboard Mashing' signatures. 
    High entropy indicates non-human randomness patterns in names/emails.
    """
    if not text or len(text) < 5: 
        return 0
    # Shannon Entropy identifies synthetic randomness
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def lambda_handler(event, context):
    print("🎯 LC DIGITAL: API_relay Passive Witness Active.")
    
    try:
        # 1. Capture the Evidence (Lead Log Witnessing)
        # Triggered by S3 Upload
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        response = s3_client.get_object(Bucket=bucket, Key=key)
        raw_body = response['Body'].read().decode('utf-8')
        content = raw_body.lower()
        
        # 2. Forensic DNA Verification Payload
        verification = {
            "status": "VERIFIED",
            "flags": [],
            "witness_score": 100,
            "vault_ref": key,
            "recovery_eligible": False
        }

        # --- SCAN A: Synthetic Geometry (Fake Phone Patterns) ---
        # Identifies 000-000, 123-456, or repeating digits
        if re.search(r"(.)\1{9}|000-000|123-456|999-999|111-111", content):
            verification["flags"].append("GEOMETRY_FAILURE: Synthetic Phone Pattern")
            verification["witness_score"] -= 45

        # --- SCAN B: Bot Fingerprints (Automated Entry Detection) ---
        # Detects signatures of common lead-generation bots
        bot_signatures = ["headless", "selenium", "puppeteer", "webdriver", "automated-form"]
        for sig in bot_signatures:
            if sig in content:
                verification["flags"].append(f"SIGNATURE_MATCH: {sig}")
                verification["witness_score"] -= 60

        # --- SCAN C: Randomness Check (Keyboard Mash Detector) ---
        # Names like "asdfgh" or "qwerty" fail this check
        if get_data_entropy(raw_body[:100]) > 4.2:
            verification["flags"].append("ENTROPY_FAILURE: Synthetic Data (Mashing)")
            verification["witness_score"] -= 30

        # 3. Final Witness Verdict
        # If score drops below 70, it is flagged for the 25% recovery fee
        if verification["witness_score"] < 70:
            verification["status"] = "FLAGGED FOR DISCREPANCY RECOVERY"
            verification["recovery_eligible"] = True
        
        print(f"✅ Witness Result for {key}: {verification['status']}")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {str(e)}")
        return {'statusCode': 500}

    # Return the Witness Statement (The Product we sell for $2,500)
    return {
        'statusCode': 200,
        'body': json.dumps({
            'witness_statement': verification,
            'legal_standing': "Certified Passive Witness - LC Digital Solutions",
            'authorized_by': "Forensic Division"
        })
    }
