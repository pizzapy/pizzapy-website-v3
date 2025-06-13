# Flask Markdown Blog File Structure

```
pizzapy-website-v3/
├── app/
│   ├── services/
│   │   ├── meetup.py
│   │   └── blog.py                # Blog service for markdown processing
│   ├── templates/
│   │   ├── about.html             # About template
│   │   ├── blog_index.html        # Blog listing page
│   │   └── blog_post.html         # Individual post template
│   │   ├── index.html             # Index template
│   ├── static/
│   │   └── css/
│   │       └── style.css          # Basic styling
│   ├── posts/                     # Markdown blog posts
│   │   ├── 2025-06-10-first-post.md
│   │   ├── 2025-06-10-second-post.md
│   │   └── 2025-06-10-latest-post.md
│   └── routes.py                  # All routes including blog
├── .gitignore
└── requirements.txt
```