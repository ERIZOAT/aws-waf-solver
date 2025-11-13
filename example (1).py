import capsolver
import requests
import os

# --- Configuration ---
# Replace with your actual CapSolver API Key
CAPSOLVER_API_KEY = os.environ.get("CAPSOLVER_API_KEY", "YOUR_CAPSOLVER_API_KEY")
TARGET_URL = "https://www.amazon.com/protected-endpoint"

# --- Main Logic ---

def solve_aws_waf_challenge(api_key: str, target_url: str):
    """
    Solves the AWS WAF challenge using the CapSolver API and returns the WAF token.
    
    NOTE: The awsKey, awsIv, and awsContext parameters must be dynamically
    scraped from the target page's source code before calling this function.
    """
    if api_key == "YOUR_CAPSOLVER_API_KEY":
        print("Error: Please set your CAPSOLVER_API_KEY.")
        return None

    capsolver.api_key = api_key

    # 1. Define the task payload
    # Placeholder values are used here. In a real scenario, these must be scraped.
    payload = {
        "type": "AntiAwsWafTask",
        "websiteURL": target_url,
        "proxy": "http://user:pass@proxy.example.com:port", # Recommended proxy format
        "awsKey": "PLACEHOLDER_AWS_KEY",
        "awsIv": "PLACEHOLDER_AWS_IV",
        "awsContext": "PLACEHOLDER_AWS_CONTEXT",
    }

    # 2. Execute the challenge resolution task
    print(f"Submitting AWS WAF challenge for {target_url}...")
    try:
        solution = capsolver.solve(payload)
        waf_token = solution.get("token")
        print(f"WAF Token Acquired: {waf_token}")
        return waf_token
    except Exception as e:
        print(f"An error occurred during CapSolver execution: {e}")
        return None

def make_protected_request(target_url: str, waf_token: str):
    """
    Makes the final request to the protected resource using the acquired WAF token.
    """
    if not waf_token:
        print("Cannot make request without a valid WAF token.")
        return

    # The token is passed in the Cookie header
    headers = {
        "Cookie": f"aws-waf-token={waf_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Attempting final request to {target_url}...")
    final_response = requests.get(target_url, headers=headers, timeout=15)

    # Verification
    if "challenge" not in final_response.text and final_response.status_code == 200:
        print("SUCCESS: WAF successfully circumvented. Status 200.")
        # print(final_response.text[:500] + "...") # Print first 500 chars of content
    else:
        print(f"FAILURE: Bypass failed. Status: {final_response.status_code}")
        print("Response likely still contains a WAF challenge.")

if __name__ == "__main__":
    token = solve_aws_waf_challenge(CAPSOLVER_API_KEY, TARGET_URL)
    if token:
        make_protected_request(TARGET_URL, token)
