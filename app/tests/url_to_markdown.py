from app.services.content_converter import ContentConverter

converter = ContentConverter()

urls = {
    "openai": "https://openai.com/index/an-alien-mind",
    "anthropic": "https://www.anthropic.com/news/model-hardware-standard-research-preview",
}

for name, url in urls.items():
    print("\n" + "=" * 70)
    print(name.upper())
    print("=" * 70)

    content = converter.url_to_markdown(url)

    if content:
        print("SUCCESS")
        print("Markdown length:", len(content))
        print("\n--- PREVIEW ---")
        print(content[:2000])
    else:
        print("FAILED: converter returned None")