from app.agents.email_agent import EmailDigestResponse


def digest_to_html(digest: EmailDigestResponse) -> str:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AI News Digest</title>
    </head>

    <body>
        <h2>{digest.introduction.greeting}</h2>

        <p>{digest.introduction.introduction}</p>

        <hr>
    """

    for article in digest.articles:
        html += f"""
        <h2>{article.title}</h2>

        <p>{article.summary}</p>

        <p>
            <a href="{article.url}">
                Read more →
            </a>
        </p>

        <hr>
        """

    html += """
    </body>
    </html>
    """

    return html