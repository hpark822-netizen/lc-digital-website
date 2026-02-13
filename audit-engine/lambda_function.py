import json
import boto3
import re
import math

# LC DIGITAL SOLUTIONS: THE IMPENETRABLE WITNESS
# Role: Authorized Service Provider (Agent for the Dealer)
# Method: Forensic Audit of Email Logs (No-Touch Model)
# Goal: 25% Recovery Fee on Flagged Waste

s3_client = boto3.client('s3')

def get_entropy(text):
    """Detects 'Keyboard Mashing' signatures (e.g. 'asdfjkl')"""
    if not text: return 0
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in prob])

def lambda_handler(event, context):
    print("🎯 LC DIGITAL: Forensic Extraction Initiated.")
    
    try:
        # 1. Capture the Evidence (Lead Data)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        response = s3_client.get_object(Bucket=bucket, Key=key)
        raw_body = response['Body'].read().decode('utf-8')
        content = raw_body.lower()
        
        # 2. Forensic Scan: Deep Pattern Analysis
        report = {
            "status": "PASS",
            "flags": [],
            "risk_score": 0
        }

        # SCAN A: Synthetic Phone Geometry
        # Flags repeating digits, sequences, or invalid area codes (000, 111, etc.)
        if re.search(r"(.)\1{9}|000-000|123-456|999-999", content):
            report["flags"].append("GEOMETRY_FAILURE: Synthetic Phone Pattern")
            report["risk_score"] += 45

        # SCAN B: Bot Fingerprints (Detecting "Headless" markers)
        bot_signatures = ["headless", "selenium", "puppeteer", "webdriver", "automated-form"]
        for sig in bot_signatures:
            if sig in content:
                report["flags"].append(f"SIGNATURE_MATCH: {sig}")
                report["risk_score"] += 60

        # SCAN C: Data Randomness (Detects 'Mashed' fake names)
        if get_entropy(raw_body[:200]) > 4.5:
            report["flags"].append("ENTROPY_FAILURE: Synthetic Data Detected")
            report["risk_score"] += 30

        # 3. Final Verdict
        if report["risk_score"] >= 60:
            report["status"] = "FLAGGED FOR CREDIT RECOVERY"
        
        print(f"✅ Audit Result for {key}: {report['status']}")

    except Exception as e:
        print(f"❌ System Error: {str(e)}")
        return {'statusCode': 500}

    return {
        'statusCode': 200,
        'body': json.dumps({'forensic_witness_report': report})
        'body': json.dumps({'forensic_witness_report': report})
