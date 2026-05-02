# Git and Version Control Documentation

Run these commands after copying the project files into your repository folder.

```bash
git init
git add .gitignore README.md requirements.txt
git commit -m "Initial project setup with documentation and dependencies"

git add schema.sql NORMALIZATION.md
git commit -m "Add 3NF schema and normalization audit"

git add app/__init__.py app/models.py run.py
git commit -m "Build Flask app factory and SQLAlchemy models"

git add app/routes.py app/templates app/static
git commit -m "Implement CRUD views dashboard validation and transaction flow"

git add AI_LOG.md GIT_VERSION_CONTROL.md
git commit -m "Add AI disclosure and version control notes"
```

## Push to GitHub
```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## Final Repository Checklist
- At least 5 commits are visible on GitHub
- `.gitignore` excludes `venv/`, `.env`, and `__pycache__/`
- `README.md` explains setup and usage
- `NORMALIZATION.md` contains the 3NF audit
- `AI_LOG.md` honestly discloses AI assistance
- `schema.sql` contains the final 3NF SQL schema
- Source code folders contain Python, HTML, and CSS files
