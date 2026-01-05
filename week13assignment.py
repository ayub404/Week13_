import requests

urll = "https://sandbox.lithic.com/v1/cards"
json__url = "https://jsonplaceholder.typicode.com/posts"

def add_cardds(url):
    card_name = input("Enter a card name: ")
    card_type = input("Enter your card type: ").strip().upper()
    spend_limit = int(input("Enter a limit (Spend limit): "))

    data = {
        'memo': card_name,
        'type': card_type,
        'spend_limit': spend_limit
    }

    headers = {
        "Authorization": "b208e6eb-0394-4641-aa63-e1e1c77c4124",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        
        card = response.json()  
        print(f"\nCard created successfully!")
        print(f"Card_token: {card['token']}")
        print(f"Last four: {card['last_four']}")
        print(f"Card type: {card['type']}")
        print(f"Status(Open or Closed): {card['state']}")
        return card
    else:
        print("We could not create a card!")
        print(response.status_code)
        return None


def json_fake_card(url):
    name = input("Which name you put to your card: ")
    data = {
        "title": f"New card created: {name}",
        "body": f"Card {name} was created in Lithic Sandbox",
        "userId": 1
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Logged card to JSONPlaceholder:", response.json()['title'])
        return response.json()
    else:
        print("Failed to log card!")
        return None


def card_info(url):
    headers = {
        "Authorization": "b208e6eb-0394-4641-aa63-e1e1c77c4124",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("-" * 60)
        print("                     Card details ")
        for card in data['data']:
            print(f"\nCard name is {card['memo']}")
            print(f"Card type: {card['type']}")
            print(f"Card currency: {card['cardholder_currency']}")
            print(f"card_token: {card['token']}")
        print(f"\nAccount token: {data['data'][0]['account_token']}")
        print("-" * 50)
        print(f"Total number of cards: {len(data['data'])}")
        return data['data']
    else:
        print("Failed to fetch cards:", response.status_code)
        return []

def save_to_txt(cards, fake_cards, filename="Total_information.txt"):
    with open(filename, "a") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write("\nHere you find All the card details")
        f.write("=" * 50 + "\n")
        for card in cards:
            f.write("Source: Lithic\n")
            f.write(f"Card Name: {card.get('memo','')}\n")
            f.write(f"Card Type: {card.get('type','')}\n")
            f.write(f"Last Four: {card.get('last_four','')}\n")
            f.write(f"Token: {card.get('token','')}\n")
            f.write(f"Status: {card.get('state','')}\n")
            f.write(f"Currency: {card.get('cardholder_currency','')}\n")
            f.write("-"*30 + "\n")

        for log in fake_cards:
            f.write("Source: JSONPlaceholder\n")
            f.write(f"Title: {log.get('title','')}\n")
            f.write(f"Body: {log.get('body','')}\n")
            f.write(f"ID: {log.get('id','')}\n")
            f.write("-"*30 + "\n")

    print(f"\nSaved all data to {filename}")

card = add_cardds(urll)
fake_card = json_fake_card(json__url)
total_cards = card_info(urll)
fake_card_list = []

if fake_card:
    fake_card_list.append(fake_card)
save_to_txt(total_cards, fake_card_list)
with open("Total_information.txt", "r") as f:
    print(f.read())

with open("Total_information.txt", "r") as f:
    print(f.read())
