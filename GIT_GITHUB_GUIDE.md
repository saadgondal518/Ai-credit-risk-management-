# 🐙 Git & GitHub Quick Reference Guide

## 📋 First Time Setup

### 1. Create a GitHub Account
- Go to [github.com](https://github.com)
- Sign up for a free account
- Verify your email

### 2. Configure Git Locally
```bash
# Set your name (shows on commits)
git config --global user.name "Your Name"

# Set your email (must match GitHub account)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

### 3. Create a New Repository on GitHub
- Click "New" button
- Repository name: `ai-credit-risk-management`
- Add description: "AI-powered credit risk assessment system"
- Choose Public (for portfolio)
- Click "Create repository"

---

## 🚀 First Time Push to GitHub

### Step 1: Copy Your Repository Link
On GitHub, click the green "Code" button and copy the HTTPS link

### Step 2: In Your Project Folder
```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AI Credit Risk Management System"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/ai-credit-risk-management.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## 📝 Daily Git Workflow

### After Making Changes
```bash
# Check what changed
git status

# Add files to commit
git add .

# Or add specific file
git add filename.py

# Create a commit
git commit -m "Describe your changes"

# Push to GitHub
git push
```

### Commit Message Examples
```
git commit -m "Add password validation feature"
git commit -m "Fix bug in credit calculation"
git commit -m "Update documentation"
git commit -m "Refactor API endpoints"
git commit -m "Add batch prediction functionality"
```

---

## 🔍 Common Git Commands

### Checking Status
```bash
# See what changed
git status

# See changes in detail
git diff

# See commit history
git log

# See last 5 commits
git log -5

# See commit with changes
git log -p
```

### Making Changes
```bash
# Add all files
git add .

# Add specific file
git add path/to/file

# Undo add (before commit)
git reset filename.py

# Undo all adds
git reset
```

### Commits
```bash
# Create commit
git commit -m "Your message"

# Commit with detailed message
git commit

# Amend last commit
git commit --amend

# See what's in last commit
git show HEAD
```

### Pushing & Pulling
```bash
# Push to GitHub
git push

# Push specific branch
git push origin main

# Pull latest changes
git pull

# Fetch without merging
git fetch
```

---

## 🌿 Branching (For Advanced Users)

### Create a New Branch
```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Or use newer syntax
git switch -c feature/new-feature

# Push new branch to GitHub
git push -u origin feature/new-feature
```

### Switch Branches
```bash
# Switch to existing branch
git checkout main

# Or use newer syntax
git switch main
```

### Merge Branches
```bash
# Switch to main
git checkout main

# Merge feature branch
git merge feature/new-feature

# Push merged changes
git push
```

### Delete Branch
```bash
# Delete locally
git branch -d feature/new-feature

# Delete on GitHub
git push origin --delete feature/new-feature
```

---

## ❌ Undo Changes

### Before Committing
```bash
# Discard changes in working directory
git checkout -- filename.py

# Discard all changes
git checkout -- .

# Or use newer syntax
git restore filename.py
git restore .
```

### After Committing
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo specific commit
git revert commit_hash
```

### View Previous Versions
```bash
# See file at previous commit
git show commit_hash:path/to/file

# Checkout file from previous commit
git checkout commit_hash -- path/to/file
```

---

## 🔄 Sync with GitHub

### Pull Latest Changes
```bash
# Get latest from GitHub
git pull

# Or fetch + merge
git fetch
git merge origin/main
```

### Update Your Branch
```bash
# Rebase (cleaner history)
git rebase origin/main

# Or merge
git merge origin/main
```

---

## 📦 .gitignore Reference

Already included in your project:
```
__pycache__/
*.pyc
.env
venv/
.vscode/
.idea/
*.pkl
backend/models/
backend/data/
```

Add more files by editing `.gitignore`

---

## 🐛 Troubleshooting

### Authentication Error
```bash
# If you get authentication error, use GitHub token instead of password
# Generate token at: https://github.com/settings/tokens
# Use token as password when prompted
```

### Wrong Commit Message
```bash
# Fix last commit message
git commit --amend -m "Correct message"

# Push with force (only if not pushed yet)
git push --force-with-lease
```

### Accidentally Committed Wrong Files
```bash
# Undo last commit (keep files)
git reset --soft HEAD~1

# Remove the wrong files
git reset path/to/wrong/file

# Recommit without those files
git commit -m "Correct commit"
```

### Can't Push (Rejected)
```bash
# Pull latest changes first
git pull --rebase

# Then push
git push
```

---

## 📊 GitHub Features

### Create a Pull Request (PR)
1. Push your branch to GitHub
2. Click "Compare & pull request"
3. Add description
4. Click "Create pull request"
5. Merge after review

### Track Issues
- Click "Issues" tab
- Create new issue
- Assign to yourself
- Link to pull request

### Star & Fork Others
- **Star**: Bookmark projects you like
- **Fork**: Copy to your account to contribute

---

## 💡 Best Practices

### Good Commit Messages
✅ `Add feature to calculate debt ratio`
✅ `Fix bug in credit calculation`
✅ `Update documentation for setup`
❌ `fix` or `update` or `asdfjkl`

### Commit Frequency
- Commit when feature is complete
- Commit when bug is fixed
- Don't commit every tiny change
- Aim for 2-5 commits per day

### Push Frequency
- Push at end of day
- Push after completing feature
- Don't push unfinished work

### Branch Naming
- `feature/new-feature-name`
- `fix/bug-description`
- `docs/update-readme`
- `refactor/clean-up-code`

---

## 📚 Learn More

### Official Resources
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)
- [Git Cheat Sheet](https://github.github.com/training-kit/)

### Useful Commands Cheatsheet
```bash
# Show all configured remotes
git remote -v

# Change remote URL
git remote set-url origin NEW_URL

# See unpushed commits
git log origin/main..HEAD

# See total commits
git rev-list --count HEAD

# See who changed what
git blame filename.py
```

---

## 🎯 Workflow Summary

### Every Work Session
```bash
# 1. Start of day - get latest
git pull

# 2. During work - make commits
git add .
git commit -m "Your message"

# 3. End of day - push to GitHub
git push
```

### When Publishing to GitHub
```bash
# 1. First time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin URL
git push -u origin main

# 2. After that, just push
git push
```

---
