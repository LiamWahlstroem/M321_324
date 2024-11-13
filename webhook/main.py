from flask import Flask, request, jsonify
import subprocess
import hmac
import hashlib
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# GitHub secret for verifying payloads (optional but recommended)
GITHUB_SECRET = os.getenv("GITHUB_SECRET")

@app.route('/deploy', methods=['POST'])
def github_webhook():
    # Verify GitHub secret, if provided
    if GITHUB_SECRET:
        signature = request.headers.get('X-Hub-Signature-256')
        if not is_valid_signature(request.data, signature):
            return "Invalid signature", 403

    # Parse payload JSON
    payload = request.get_json()
    if not payload:
        return "Invalid JSON", 400
    
    if payload.get("action") == "completed" and payload["workflow_job"]["conclusion"] == "success":
        job_name = payload["workflow_job"]["name"]
        
        # Check if the job name corresponds to one of our image builds
        image = job_name.split('-')[0]
        if not image:
            return jsonify({"status": "ignored", "reason": "unknown job"}), 200
    
    try:
        subprocess.run(["docker-compose", "down", "{image}"])
        subprocess.run(["docker-compose", "pull", "{image}"])
        subprocess.run(["docker-compose", "up", "{image}"])
        
        return jsonify({"status": "success", "image": image}), 200
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def is_valid_signature(payload_body, signature):
    """
    Validate the request signature using the GitHub secret.
    """
    if not signature:
        return False
    sha_name, signature_hash = signature.split('=')
    if sha_name != 'sha256':
        return False
    
    # Compute HMAC digest
    mac = hmac.new(GITHUB_SECRET.encode(), payload_body, hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature_hash)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
