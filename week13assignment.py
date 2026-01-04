import requests
import time

print("                  Welcome to URL + Crypto Checker                  ")
print("------------------------------------------------------------------------")

url_ = input("Enter a URL to check (VirusTotal): ").strip()
asset = input("Type the asset to check (BTC, USD, XAU): ").strip().upper()

url = "f5cef0b12607375a6b672ca04cfd20e93d6204428779318f51bd32de67b786f0"
header = {"apikey": url}

def virus_total_scan(url):
    try:
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers = header,
            data={"url": url}
        )
        if response.status_code == 200:
            analysis_id = response.json()["data"]["id"]
            time.sleep(5)
            result_response = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers = header
            )
            if result_response.status_code == 200:
                stats = result_response.json()
                stats = ["data"]["attributes"]["stats"]
                harmless = stats.get("harmless", 0)
                suspicious = stats.get("suspicious", 0)
                malicious = stats.get("malicious", 0)

                if malicious > 0:
                    status = "Dangerous"
                    advice = "Do NOT open this link."
                elif suspicious > 0:
                    status = "Suspicious"
                    advice = "Be careful before visiting."
                else:
                    status = "Safe"
                    advice = "This link appears safe."

                return {
                    "harmless": harmless,
                    "suspicious": suspicious,
                    "malicious": malicious,
                    "status": status,
                    "advice": advice
                }
            else:
                print(f"Error fetching VirusTotal result. Status code: {result_response.status_code}")
                return None
        else:
            print(f"Error submitting URL to VirusTotal. Status code: {response.status_code}")
            return None
    except:
        print("VirusTotal API error.")
        return None

def crypto_price(asset_symbol):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "", "vs_currencies": "usd"}
        if asset_symbol == "BTC":
            params["ids"] = "bitcoin"
        elif asset_symbol == "XAU":
            params["ids"] = "tether-gold"
        elif asset_symbol == "USD":
            params["ids"] = "usd-coin"
        else:
            print("Asset not supported.")
            return None

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            price = list(data.values())[0]["usd"]
            return price
        else:
            print(f"Error, Status code: {response.status_code}")
            return None
    except:
        print("Could not connect to CoinGecko.")
        return None

def display_results(vt_data, asset, price, url):
    print("\n--------------------- VirusTotal Result ---------------------")
    if vt_data:
        print(f"URL: {url}")
        print(f"Harmless:    {vt_data['harmless']}")
        print(f"Suspicious:  {vt_data['suspicious']}")
        print(f"Malicious:   {vt_data['malicious']}")
        print(f"Status:      {vt_data['status']}")
        print(f"Advice:      {vt_data['advice']}")
    else:
        print("No VirusTotal data.")

    print("\n--------------------- Crypto Price Result --------------------")
    if price is not None:
        print(f"{asset} price in USD: ${price}")
    else:
        print("No price data available.")

    try:
        with open("multi_api_report.txt", "w") as f:
            f.write("Multi API Report\n")
            f.write("-----------------\n")
            f.write("VirusTotal Result:\n")
            if vt_data:
                f.write(f"URL: {url}\n")
                f.write(f"Harmless: {vt_data['harmless']}\n")
                f.write(f"Suspicious: {vt_data['suspicious']}\n")
                f.write(f"Malicious: {vt_data['malicious']}\n")
                f.write(f"Status: {vt_data['status']}\n")
                f.write(f"Advice: {vt_data['advice']}\n")
            else:
                f.write("No VirusTotal data.\n")
            f.write("\nCrypto Price Result:\n")
            if price is not None:
                f.write(f"{asset} price in USD: {price}\n")
            else:
                f.write("No price data available.\n")
        print("\nSaved to multi_api_report.txt")
    except:
        print("Could not save file.")

result1 = virus_total_scan(url_)
price = crypto_price(asset)
display_results(result1, asset, price, url_)
