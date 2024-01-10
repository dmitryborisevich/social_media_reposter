import requests
import io


def get_source_data(request):
    url = request.POST.get('url')
    url_api = f"https://ab.api.onliner.by/adverts/{url.replace('https://ab.onliner.by/', '').split('/')[-1]}"
    try:
        response_json = requests.get(url_api).json()
        source_data = {
            'url': url,
            'post_id': response_json['id'],
            'name': response_json['title'],
            'description': f"{response_json['specs']['engine']['capacity']} "
                           f"{response_json['specs']['engine']['type']} - "
                           f"{response_json['specs']['engine']['power']['value']} h.p.",
            'price': response_json['price']['amount']
        }
        images = []

        for i in range(len(response_json['images']) if len(response_json['images']) <= 3 else 3):
            images.append(io.BytesIO(requests.get(response_json['images'][i]['1900x1180']).content))

        return {
            'source_data': source_data,
            'images': images,
        }
    except Exception as e:
        print(e)
        return {}
