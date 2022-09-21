import requests
import shutil
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


def download_metadata(url, token_id):
    r = requests.get(url.replace("{}", str(token_id)), headers=headers)
    data = r.json()
    with open(f"output/{token_id}.json", 'w') as out_file:
        json.dump(data, out_file)
    return data


def download_image(url, token_id, attempts_remaining = 5):
    url = url.replace('ipfs://', 'https://ipfs.io/ipfs/')
    ext = url.split(".")[-1]
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code != 200:
        if attempts_remaining == 0:
            print('Unable to download image')
            exit(1)
        print('Got ' + str(response.status_code) + '. Retrying...')
        return download_image(url, token_id, attempts_remaining - 1)
    with open(f"output/{token_id}.{ext}", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


if __name__ == "__main__":
    # e.g. "https://oddoneoutlabs.mypinata.cloud/ipfs/Qme8vhhD3LW9uq9oGiPGMWonvXndesEQhYNrM7ZP4Euskp/{}.json"
    url_template = input("URL template: ")
    start_id = int(input("First token id: "))
    last_id = int(input("Last token id: "))
    if not url_template or not last_id:
        exit()
    for i in range(start_id, last_id + 1):
        print(f"Fetching token {i}")
        try:
            data = download_metadata(url_template, i)
            # FIXME Uncomment to enable image downloading 
            # download_image(data["image"], i)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            print(f"Downloading {i} failed")
