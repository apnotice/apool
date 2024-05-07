import requests
import json
import time

# Your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1237003749747064842/p8dQivLi8ZBOPYc0Z8Pczw9JUUyOeqXoeRb8kICQvDGOYRiQ4M2CPqCG__0a312tc-hC'
# Your Discord user ID
YOUR_USER_ID = '963432108934725742'

# Function to send a notification to Discord
def send_discord_notification(message):
    # Mention yourself using your user ID
    mention = f"<@{YOUR_USER_ID}>"
    # Construct the notification message with mention
    message_with_mention = f"{mention} {message}"
    # Prepare the payload
    payload = {'content': message_with_mention}
    headers = {'Content-Type': 'application/json'}
    # Send the notification
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an error for non-200 status codes
        print("Notification sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")

# Function to get mining statistics from the pool API
def get_mining_stats():
    api_url = 'https://client.apool.io/mining/shares?currency=qubic&account=CP_7cqdjrvl2n&tag=day'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch mining statistics")
        return None

# Main function
def main():
    # Initialize previous share count
    prev_share_count = 0
    
    while True:
        # Get mining statistics
        mining_stats = get_mining_stats()
        if mining_stats:
            current_share_count = mining_stats['result']['accept']
            # Compare with previous share count
            if current_share_count > prev_share_count:
                # Calculate the increase in shares
                share_increase = current_share_count - prev_share_count
                # Send notification to Discord
                message = f"New share found! Total shares: {current_share_count}, Share increase: {share_increase}"
                send_discord_notification(message)
                # Update previous share count
                prev_share_count = current_share_count
        
        # Wait for 5 minutes before checking again (adjust as needed)
        time.sleep(300)

if __name__ == "__main__":
    main()
