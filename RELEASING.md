# 🚀 Automated Release Process

This repository is set up with automated releases using GitHub Actions. Here's how it works and how to use it.

## ⚡ Quick Release (Recommended)

Use the release script to automatically bump version and trigger release:

```bash
# For bug fixes (0.1.2 → 0.1.3)
python scripts/release.py patch

# For new features (0.1.2 → 0.2.0)  
python scripts/release.py minor

# For breaking changes (0.1.2 → 1.0.0)
python scripts/release.py major
```

That's it! The script will:
1. ✅ Bump version in `pyproject.toml`
2. ✅ Commit and tag the changes
3. ✅ Push to GitHub
4. ✅ Trigger automated release workflow

## 🤖 What Happens Automatically

When you push a git tag (e.g., `v0.1.3`), GitHub Actions automatically:

1. **Builds** the Python package
2. **Tests** the package integrity
3. **Publishes** to PyPI using trusted publishing
4. **Creates** a GitHub release with auto-generated changelog
5. **Uploads** release artifacts

## 🔧 Manual Release (Alternative)

If you prefer manual control:

```bash
# 1. Update version in pyproject.toml
vim pyproject.toml

# 2. Commit changes
git add pyproject.toml
git commit -m "Bump version to 0.1.3"

# 3. Create and push tag
git tag v0.1.3
git push origin main --tags
```

The GitHub Actions workflow will still handle PyPI publishing and GitHub release creation.

## 📋 Prerequisites

### One-time setup required:

1. **Enable trusted publishing on PyPI**:
   - Go to https://pypi.org/manage/account/publishing/
   - Add publisher: `puya/token-counter-cli` (GitHub repo)
   - Workflow: `release.yml`
   - Environment: leave blank

2. **Verify GitHub permissions**:
   - Repository Settings → Actions → General
   - Ensure "Read and write permissions" is enabled for `GITHUB_TOKEN`

## 🛠 Troubleshooting

### PyPI Publishing Fails
- Check that trusted publishing is configured correctly on PyPI
- Verify the workflow has `id-token: write` permission

### GitHub Release Fails  
- Ensure `GITHUB_TOKEN` has sufficient permissions
- Check that you're pushing tags, not just commits

### Version Conflicts
- Make sure the version doesn't already exist on PyPI
- Use `--skip-existing` in the workflow (already configured)

## 🎯 Benefits of This Setup

- **Zero manual PyPI uploads** - no more `twine upload`
- **Consistent releases** - standardized changelog and formatting  
- **Secure** - uses GitHub's trusted publishing (no API keys to manage)
- **Fast** - entire release process takes ~2 minutes
- **Reliable** - automated testing before publishing

## 📚 More Information

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/) 