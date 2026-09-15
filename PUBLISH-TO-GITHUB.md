# Publish to GitHub

```bash
cd ~/Downloads
unzip numerical-methods-practicals.zip
cd numerical-methods-practicals
git init
git add .
git commit -m "Initial commit: numerical methods practicals"
gh repo create numerical-methods-practicals --public --source=. --remote=origin --push
gh repo view --web
```

