import os,requests,time,json

API_BASE = "https://discord.com/api/v10"

print(f"Developed By : Britto")
time.sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')
print(f"[~~] GitHub : https://github.com/13shayan82 ") 
tokenlist = []

try:
    with open("tokens.txt", 'r') as f:
        tokenlist = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("\n[!!!] ERROR: 'tokens.txt' not found. Please create it and add your token(s).")
    input("\nPress Enter to exit...")
    exit()

if not tokenlist:
    print("\n[!!!] ERROR: 'tokens.txt' is empty. Please add your token(s) to the file.")
    input("\nPress Enter to exit...")
    exit()

for token in tokenlist:
    headers = {'Authorization': token}
    print(f"\n[+] Starting process for token: {token[:10]}...") 
    
    try:
        print(f"[*] Fetching all available guilds...")
        response = requests.get(f"{API_BASE}/users/@me/guilds", headers=headers)
        
        if response.status_code == 429:
            try:
                retry_after = response.json().get('retry_after', 5) 
            except json.JSONDecodeError:
                retry_after = 5
            print(f"[!!!] Global Rate limited on fetch! Waiting for {retry_after} seconds.")
            time.sleep(retry_after)
            response = requests.get(f"{API_BASE}/users/@me/guilds", headers=headers)
        if response.status_code == 200:
            guilds = response.json()
            
            if isinstance(guilds, dict) and 'message' in guilds and 'retry_after' in guilds:
                retry_after = guilds.get('retry_after', 5)
                print(f"[!!!] Rate limited on fetch (JSON body)! Waiting for {retry_after} seconds.")
                time.sleep(retry_after)
                continue 

            if not guilds:
                print(f"[!] Token: {token[:10]}... has no guilds to leave.")
                continue

            print(f"[+] Found {len(guilds)} guilds. Starting to leave them.")

            for guild in guilds:
                guild_id = guild['id']
                guild_name = guild.get('name', 'Unknown Server')
                
                print(f"\t[*] Attempting to leave/delete server: {guild_name} ({guild_id})")
                
                delete_response = requests.delete(
                    f'{API_BASE}/users/@me/guilds/{guild_id}',
                    headers=headers
                )
                
                if delete_response.status_code == 204:
                    print(f"\t[!] Successfully left/deleted server: {guild_name}")
                
                elif delete_response.status_code == 429:
                    try:
                        retry_after = delete_response.json().get('retry_after', 1)
                    except json.JSONDecodeError:
                        retry_after = 1
                    
                    print(f"\t[!!!] Rate limited! Waiting for {retry_after:.2f} seconds before continuing.")
                    time.sleep(retry_after)

                elif delete_response.status_code == 403:
                    print(f"\t[!] Forbidden (403): Cannot leave/delete server: {guild_name}. (May be owner)")
                
                elif delete_response.status_code == 401:
                     print(f"\t[!!!] Unauthorized (401): Token is invalid for server: {guild_name}.")
                
                else:
                    print(f"\t[!!!] Failed to leave server: {guild_name}. Status: {delete_response.status_code} | Response: {delete_response.text}")

                time.sleep(0.5) 

            print(f"\n[+] Finished processing all available guilds for this token: {token[:10]}...")
        
        elif response.status_code == 401:
            print("\n[!!!] ERROR: The token is invalid or unauthorized (401). Skipping.")

        else:
            print(f"\n[!!!] ERROR: Failed to fetch guilds. Status: {response.status_code} | Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"\t[!!!] Network/Request Error for token : {token[:10]}... | Error: {e}")
    except Exception as e:
        print(f"\t[!!!] Unhandled error for token : {token[:10]}... | Error: {e}")

input("\n[DONE] Press Enter to exit...")
