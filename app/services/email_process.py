import logging
import os

from dotenv import load_dotenv

load_dotenv()

from app.agents.email_agent import EmailAgent, RankedArticleDetail, EmailDigestResponse
from app.agents.curator_agent import CuratorAgent
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository
from app.services.email import EmailService
from app.services.email_template import digest_to_html


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def generate_email_digest(
    hours: int = 24,
    top_n: int = 10,
) -> EmailDigestResponse:

    curator = CuratorAgent(USER_PROFILE)
    email_agent = EmailAgent(USER_PROFILE)
    repo = Repository()

    # --------------------------------
    # 1. Get recent digests
    # --------------------------------

    digests = repo.get_recent_digests(hours=hours)
    total = len(digests)

    if total == 0:
        logger.warning(
            f"No digests found from the last {hours} hours"
        )
        raise ValueError("No digests available")

    logger.info(
        f"Ranking {total} digests for email generation"
    )

    # --------------------------------
    # 2. Curate / rank the digests
    # --------------------------------

    ranked_articles = curator.rank_digests(digests)

    if not ranked_articles:
        logger.error("Failed to rank digests")
        raise ValueError("Failed to rank articles")

    logger.info(
        f"Successfully ranked {len(ranked_articles)} articles"
    )

    # --------------------------------
    # 3. Match ranked articles with
    #    their database information
    # --------------------------------

    digest_by_id = {
        digest["id"]: digest
        for digest in digests
    }

    article_details = []

    for article in ranked_articles:

        digest = digest_by_id.get(article.digest_id)

        if not digest:
            logger.warning(
                f"Digest not found: {article.digest_id}"
            )
            continue

        article_details.append(
            RankedArticleDetail(
                digest_id=article.digest_id,
                rank=article.rank,
                relevance_score=article.relevance_score,
                reasoning=article.reasoning,
                title=digest["title"],
                summary=digest["summary"],
                url=digest["url"],
                article_type=digest["article_type"],
            )
        )

    if not article_details:
        raise ValueError(
            "No ranked articles could be matched with digests"
        )

    # --------------------------------
    # 4. Generate email content
    # --------------------------------

    logger.info(
        f"Generating email digest with top {top_n} articles"
    )

    email_digest = email_agent.create_email_digest_response(
        ranked_articles=article_details,
        total_ranked=len(ranked_articles),
        limit=top_n,
    )

    logger.info("Email digest generated successfully")

    return email_digest


def send_digest_email(
    hours: int = 24,
    top_n: int = 10,
) -> dict:

    try:

        # --------------------------------
        # Generate digest
        # --------------------------------

        result = generate_email_digest(
            hours=hours,
            top_n=top_n,
        )

        # --------------------------------
        # Convert digest to email formats
        # --------------------------------

        body_text = result.to_markdown()
        body_html = digest_to_html(result)

        # --------------------------------
        # Subject
        # --------------------------------

        subject = (
            f"Daily AI News Digest - "
            f"{result.top_n} Articles"
        )

        # --------------------------------
        # Send through Resend
        # --------------------------------

        email_service = EmailService()

        recipient = os.getenv("EMAIL_TO")

        if not recipient:
            raise ValueError(
                "EMAIL_TO is not set"
            )

        email_service.send_email(
            to=recipient,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
        )

        logger.info("Email sent successfully!")

        return {
            "success": True,
            "subject": subject,
            "articles_count": len(result.articles),
        }

    except ValueError as e:

        logger.error(
            f"Error sending email: {e}"
        )

        return {
            "success": False,
            "error": str(e),
        }

    except Exception as e:

        logger.exception(
            "Unexpected error while sending email"
        )

        return {
            "success": False,
            "error": str(e),
        }


if __name__ == "__main__":

    result = send_digest_email(
        hours=24,
        top_n=10,
    )

    if result["success"]:

        print("\n=== Email Digest Sent ===")
        print(f"Subject: {result['subject']}")
        print(f"Articles: {result['articles_count']}")

    else:

        print(f"Error: {result['error']}")