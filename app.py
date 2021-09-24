import requests
from flask import Flask, request


app = Flask(__name__)
open_weather_token = 'b0a16eae7f582a7eb398dcd65a6db52b'


class Store:
    def __init__(self):
        self.current_city = ''
        self.set_city = False

    def start_city_select(self):
        self.set_city = True

    def select_city(self, city):
        self.current_city = city
        self.set_city = False


store = Store()


def get_weather():
    params = {"access_key": "fbee8a919a1f75c5038493c53ccc0bbf", "query": store.current_city or 'New York'}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    return (u'Current temperature in %s is %d℃' % (api_response['location']['name'], api_response['current']['temperature']))


def send_message(chat_id, text):
    method = "sendMessage"
    token = "1956766208:AAGRuBSzYp7Rr15GBnLJYJqD_WYv-AIIIbs"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def get_city_by_location(location):
    lon = location['longitude']
    lat = location['latitude']
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={open_weather_token}')
    if resp.status_code == 200:
        return resp.json()[0]['name']
    else:
        print('sasi')
        return None


@app.route("/", methods=["GET", "POST"])
def receive_update():
    data = request.json
    print(data)

    if request.method == "POST" and data.get('message'):
        message = data['message']

        if message.get('text'):
            command = data["message"]["text"]
            chat_id = message["chat"]["id"]

            if command == '/start':
                print(request.json)
                weather = get_weather()
                send_message(chat_id, weather)
            elif command == '/city':
                send_message(chat_id, 'Please enter the city')
                store.start_city_select()
            else:
                if store.set_city:
                    store.select_city(command)
                    send_message(chat_id, 'City selected')

        elif message.get('location'):
            if store.set_city:
                city = get_city_by_location(message['location'])
                store.select_city(city)

    return {"ok": True}


if __name__ == '__main__':
    app.run(port=5000, debug=True)