# AI-Powered Personalized News Aggregator

An AI-powered personalized news aggregation system that automatically collects AI content, processes it, generates concise digests, personalizes the content based on a user's technical profile, and delivers the final curated feed through email.

**Live Project:** [Sayan Builds — AI-Powered Personalized News Aggregator](https://sayanbuilds.online/project/ai-powered-personalized-news-aggregator?utm_source=chatgpt.com)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [System Architecture](#3-system-architecture)
4. [Content Sources](#4-content-sources)
5. [Complete Pipeline](#5-complete-pipeline)
6. [AI Agents](#6-ai-agents)
7. [YouTube Transcript Handling](#7-youtube-transcript-handling)
8. [Personalized Curation](#8-personalized-curation)
9. [Database Structure](#9-database-structure)
10. [Tech Stack](#10-tech-stack)
11. [Setup](#11-setup)
12. [Design Philosophy](#12-design-philosophy)

---

## 1. Overview

This project is an **AI-powered personalized news aggregation system** designed to turn a large amount of AI-related content into a concise and personalized knowledge feed.

Instead of manually checking multiple AI companies, blogs, research sources, and YouTube channels, the system automates the complete workflow:

```text
Discover
   ↓
Collect
   ↓
Process
   ↓
Understand
   ↓
Personalize
   ↓
Deliver
```

The system collects content from **16 RSS feeds and 6 YouTube channels**, stores the collected data in PostgreSQL, processes the content, generates AI-powered digests, ranks the content according to a user's profile, and finally delivers the curated digest through email. ([Sayan Builds][1])

The project is designed as a practical exploration of how **LLMs, AI agents, backend systems, databases, APIs, and automation** can work together as a complete application.

---

## 2. Features

### Multi-source content collection

* 16 RSS feeds
* 6 AI-focused YouTube channels
* Automated content discovery
* Centralized PostgreSQL storage

### Content processing

* RSS articles → clean Markdown
* YouTube videos → transcripts
* Transcript retry handling
* IP-block detection
* Title + description fallback

### AI-powered digest generation

* Concise titles
* Short summaries
* Technical insights
* Practical and actionable information
* Structured LLM output

### Personalized curation

* User-specific technical profile
* Interest-based relevance scoring
* Content ranking
* Technical and practical content prioritization

### Automated email delivery

* AI-generated email introduction
* Ranked articles
* Summaries and source links
* Email delivery through Resend

---

## 3. System Architecture

```text
                 ┌─────────────────────┐
                 │     RSS Sources     │
                 └──────────┬──────────┘
                            │
                 ┌──────────▼──────────┐
                 │  YouTube Channels   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Scrapers      │
                 │                     │
                 │   RSS Scraper       │
                 │   YouTube Scraper   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     PostgreSQL      │
                 │                     │
                 │ Articles / Videos   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Content Processing  │
                 │                     │
                 │ RSS → Markdown      │
                 │ YouTube → Transcript│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Digest Agent     │
                 │        LLM          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Curator Agent     │
                 │                     │
                 │ User Profile        │
                 │ Relevance Ranking   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Email Agent     │
                 │                     │
                 │ Personalized Email  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Resend        │
                 └──────────┬──────────┘
                            │
                            ▼
                       User Inbox
```

The architecture separates **scraping, processing, AI generation, curation, and delivery** into independent stages.

---

## 4. Content Sources

The system currently works with **22 content sources**:

* **16 RSS feeds**
* **6 YouTube channels**

### RSS Source Breakdown

| Source                      | RSS Feeds |
| --------------------------- | --------: |
| Anthropic                   |         3 |
| OpenAI                      |         3 |
| Hugging Face                |         1 |
| Google / DeepMind           |         2 |
| Meta AI                     |         1 |
| Mistral                     |         1 |
| xAI                         |         1 |
| Ollama                      |         1 |
| The Batch — DeepLearning.AI |         1 |
| Simon Willison              |         1 |
| Cohere                      |         1 |
| **Total**                   |    **16** |

### YouTube Sources

The project currently collects content from:

* Dave Ebbelaar
* Matthew Berman
* Matt Wolfe
* The AI Daily Brief
* AI Explained
* Two Minute Papers

This combination provides content from both **official AI sources and independent AI-focused creators**. ([Sayan Builds][1])

---

## 5. Complete Pipeline

The complete system follows this workflow:

```text
                     DISCOVER
                        │
                        ▼
               RSS + YouTube Sources
                        │
                        ▼
                    SCRAPING
                        │
                        ▼
                   PostgreSQL
                        │
                        ▼
                  PROCESSING
                 ┌──────┴──────┐
                 │             │
                RSS          YouTube
                 │             │
                 ▼             ▼
             Markdown      Transcript
                 │             │
                 └──────┬──────┘
                        ▼
                  UNDERSTAND
                        │
                        ▼
                  Digest Agent
                        │
                        ▼
                 PERSONALIZE
                        │
                        ▼
                 Curator Agent
                        │
                        ▼
                  Ranked Content
                        │
                        ▼
                     EMAIL
                        │
                        ▼
                  Email Agent
                        │
                        ▼
                     Resend
                        │
                        ▼
                   User Inbox
```

### Stage 1 — Discovery

The scrapers collect new content from configured RSS feeds and YouTube channels.

### Stage 2 — Storage

Metadata and source information are stored in PostgreSQL.

### Stage 3 — Content Processing

RSS content is converted into Markdown, while YouTube videos go through transcript extraction.

### Stage 4 — Digest Generation

The Digest Agent converts processed content into concise, structured digests.

### Stage 5 — Personalization

The Curator Agent evaluates the generated digests against the user's profile.

### Stage 6 — Email Generation

The Email Agent prepares the final personalized email.

### Stage 7 — Delivery

The final digest is sent through Resend.

---

## 6. AI Agents

The system contains three main AI agents.

### Digest Agent

The Digest Agent converts processed content into a concise technical digest.

```text
Processed Content
       │
       ▼
  Digest Agent
       │
       ▼
Title + Summary
```

It generates:

* A concise title
* A short summary
* Important technical information
* Practical insights
* Actionable information

The agent is also instructed to ignore irrelevant content such as navigation, promotional material, social links, and other unnecessary page elements. ([Sayan Builds][1])

---

### Curator Agent

The Curator Agent personalizes the content for the user.

```text
                  User Profile
                       │
                       ▼
                ┌─────────────┐
Generated ─────►│   Curator   │
Digests         │    Agent    │
                └──────┬──────┘
                       │
                       ▼
                Ranked Content
```

The user profile contains information such as:

* Technical background
* Areas of interest
* Preferred content style
* Expertise level
* Learning preferences

The agent evaluates each digest and assigns relevance scores and rankings.

This allows the system to prioritize content according to the user's specific interests rather than treating every article equally.

---

### Email Agent

The Email Agent handles the final email-generation stage.

```text
Ranked Content
      │
      ▼
 Email Agent
      │
      ▼
Personalized Email
      │
      ▼
    Resend
      │
      ▼
 User Inbox
```

It generates the personalized introduction and prepares the final email containing the curated content.

---

## 7. YouTube Transcript Handling

YouTube transcript retrieval is designed with a fallback mechanism so that the pipeline can continue even when a transcript cannot be obtained.

### Transcript Flow

```text
YouTube Video
      │
      ▼
Get Transcript
      │
      ▼
Transcript Available?
    /           \
  YES            NO
   │              │
   ▼              ▼
Use Transcript   Check Failure
                    │
              ┌─────┴─────┐
              │           │
         Temporary     IP Blocked
          Failure          │
              │             ▼
              ▼         Stop Retry
            Retry
              │
              ▼
            Retry
              │
              ▼
            Retry
              │
              ▼
       Continue Without
          Transcript
```

### Retry Logic

For temporary transcript retrieval failures, the system attempts retrieval up to **three times**.

```text
Attempt 1
   │
   ├── Success → Continue
   │
   └── Failure
          ↓
Attempt 2
   │
   ├── Success → Continue
   │
   └── Failure
          ↓
Attempt 3
   │
   ├── Success → Continue
   │
   └── Failure → Fallback
```

However, an **IP-blocked condition is handled differently**.

If the system detects that the IP is blocked, it immediately stops the retry loop instead of repeatedly making requests that are unlikely to succeed.

### Transcript Fallback

The system does not depend entirely on the transcript.

If a transcript cannot be retrieved, the Digest Agent can use the available **video title and meaningful description**.

```text
YouTube Video
      │
      ├── Title
      ├── Description
      └── Transcript
             │
             ▼
      Transcript Available?
         /           \
       YES            NO
        │              │
        ▼              ▼
   Full Content    Title +
                   Description
        │              │
        └──────┬───────┘
               ▼
         Digest Agent
               │
               ▼
            AI Digest
```

The fallback prevents the absence of a transcript from completely stopping the content pipeline.

The model is instructed to use only the available information and avoid inventing unsupported details. ([Sayan Builds][1])

---

## 8. Personalized Curation

Personalization is one of the central parts of the system.

Instead of simply collecting and summarizing AI news, the system maintains a structured user profile containing:

```text
User Profile
├── Name
├── Professional Background
├── Interests
├── Preferences
└── Expertise Level
```

The profile describes the user's technical interests and preferred type of content.

Examples include:

* LLM application development
* AI agents
* Agentic workflows
* RAG
* Generative AI
* Prompt engineering
* AI APIs and model providers
* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* MLOps
* Multimodal AI
* Practical AI engineering

The Curator Agent uses this profile to evaluate the relevance of generated digests and produce ranked content.

```text
                 User Profile
                      │
                      ▼
              Interest Matching
                      │
                      ▼
               Relevance Score
                      │
                      ▼
                  Ranking
                      │
                      ▼
             Personalized Feed
```

The result is a feed designed around **what the user is interested in learning**, rather than simply what is newest.

---

## 9. Database Structure

PostgreSQL acts as the persistent storage layer.

The primary data entities are:

```text
┌──────────────────────┐
│     YouTubeVideo     │
├──────────────────────┤
│ video_id             │
│ title                │
│ url                  │
│ channel_id           │
│ published_at         │
│ description          │
│ transcript           │
│ created_at           │
└──────────┬───────────┘
           │
           │
           ▼
┌──────────────────────┐
│       Digest         │
├──────────────────────┤
│ id                   │
│ article_type         │
│ article_id           │
│ url                  │
│ title                │
│ summary              │
│ created_at           │
└──────────────────────┘


┌──────────────────────┐
│      RSSArticle      │
├──────────────────────┤
│ guid                 │
│ source               │
│ title                │
│ url                  │
│ description          │
│ published_at         │
│ category             │
│ markdown             │
│ created_at           │
└──────────┬───────────┘
           │
           ▼
        Digest
```

### Main entities

**YouTubeVideo**

Stores YouTube metadata and transcript information.

**RSSArticle**

Stores RSS article metadata and processed Markdown content.

**Digest**

Stores the AI-generated title and summary associated with the original content.

SQLAlchemy is used as the ORM and repository layer, keeping database operations separate from the scraping and AI-processing logic.

---

## 10. Tech Stack

### Backend

- Python
- SQLAlchemy
- Pydantic
- PostgreSQL
- uv

### AI & Agents

- OpenRouter
- LLM APIs
- Structured LLM Outputs
- AI Agents

### Content Sources & Processing

- RSS Feeds
- YouTube
- YouTube Transcript API
- Markdown Processing

### Infrastructure & Delivery

- Docker — PostgreSQL container
- Resend — Email delivery
- Environment-based Configuration

---

## 11. Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/)
- Git

The project uses **uv** for Python environment and dependency management, while **Docker is used to run the PostgreSQL database**.

---

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ai-news-aggregator
````

---

### 2. Install Dependencies

This project uses `uv` to manage the Python environment and dependencies.

If the project already contains a `pyproject.toml`, run:

```bash
uv sync
```

This creates the required virtual environment and installs the project's dependencies.

---

### 3. Start the PostgreSQL Database

PostgreSQL runs inside Docker.

The project includes a `docker-compose.yml` configuration for the database.

Start the database with:

```bash
docker compose up -d
```

This starts the PostgreSQL container in the background.

To check whether the container is running:

```bash
docker ps
```

To stop the database:

```bash
docker compose down
```

The Docker setup is used for the **database infrastructure only**. The Python application itself runs directly through the `uv` environment.

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_openrouter_api_key

POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_news_aggregator

RESEND_API_KEY=your_resend_api_key
```

Add any additional credentials required by the configured content sources or external services.

---

### 5. Initialize the Database

After starting PostgreSQL, initialize the database tables using the project's database setup script.

```bash
uv run python -m app.database.create_tables
```

---

### 6. Run the Application

Run the application using `uv`:

```bash
uv run python -m app.runner
```

The pipeline then runs through the complete workflow:

```text
Scraping
   ↓
Content Processing
   ↓
Digest Generation
   ↓
Content Curation
   ↓
Email Generation
   ↓
Email Delivery
```

---

### 7. Useful Commands

Start the PostgreSQL database:

```bash
docker compose up -d
```

Stop the PostgreSQL database:

```bash
docker compose down
```

Install/sync Python dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run python -m app.runner
```

Run a Python command inside the project's environment:

```bash
uv run python <command>
```

---

### Project Runtime

The runtime architecture is intentionally simple:

```text
             Docker
               │
               ▼
        ┌──────────────┐
        │  PostgreSQL  │
        └───────┬──────┘
                │
                │
        ┌───────▼──────┐
        │ Python App   │
        │    via uv    │
        └───────┬──────┘
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
   AI Pipeline       External APIs
                       │
                       ├── OpenRouter
                       ├── YouTube
                       └── Resend
```

Docker is responsible for the **PostgreSQL database**, while `uv` manages and runs the Python application.

---

## 12. Design Philosophy

The project is built around a simple idea:

> **Don't just collect information. Transform it into personalized knowledge.**

The internet already contains an enormous amount of AI information. The problem is not simply finding information — it is processing the volume of information and identifying what is actually useful to a particular person.

This project approaches that problem as an automated pipeline:

```text
Discover
   ↓
Process
   ↓
Understand
   ↓
Personalize
   ↓
Deliver
```

The system combines:

```text
LLMs
 +
AI Agents
 +
Backend Engineering
 +
Databases
 +
APIs
 +
Automation
```

The goal is to build a complete AI-powered application where the LLM is only one component of a larger system.

The project demonstrates how AI can be integrated with conventional backend engineering to create an automated workflow that continuously transforms raw external information into a personalized knowledge feed. ([Sayan Builds][1])

[1]: https://sayanbuilds.online/project/ai-powered-personalized-news-aggregator "sayanbuilds.online"
