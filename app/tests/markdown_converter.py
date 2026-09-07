import requests


urls = [
    "https://openai.com/index/an-alien-mind",
    "https://www.anthropic.com/news/model-hardware-standard-research-preview",
]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}


for url in urls:
    print("\n" + "=" * 70)
    print(url)
    print("=" * 70)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=(10, 60),
        )

        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("content-type"))
        print("Content-Length:", len(response.content))
        print("Content:", response.content[:3000])

    except Exception as e:
        print(type(e).__name__, ":", e)