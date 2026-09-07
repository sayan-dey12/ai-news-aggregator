from app.database.connection import get_session
from app.database.models import (
    Digest,
    AnthropicArticle,
    OpenAIArticle,
    YouTubeVideo,
)


def reset_database():

    session = get_session()

    try:
        session.query(Digest).delete()
        session.query(AnthropicArticle).delete()
        session.query(OpenAIArticle).delete()
        session.query(YouTubeVideo).delete()

        session.commit()

        print("Database data cleared successfully.")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    reset_database()
