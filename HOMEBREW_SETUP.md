# Homebrew Distribution Guide

This guide covers two approaches for distributing your `token-counter-cli` package via Homebrew.

## 🚀 Option 1: Create Your Own Tap (Recommended First)

Creating your own tap is faster and gives you full control. Users can install with:
```bash
brew tap puya/tools
brew install token-counter-cli
```

### Step 1: Create the Homebrew Tap Repository

1. **Create a new GitHub repository** named `homebrew-tools` (must start with `homebrew-`)
   ```bash
   # On GitHub, create: puya/homebrew-tools
   ```

2. **Clone and set up the repository:**
   ```bash
   git clone https://github.com/puya/homebrew-tools.git
   cd homebrew-tools
   
   # Copy your formula
   cp /path/to/token-counter/token-counter-cli.rb ./
   
   # Create initial commit
   git add token-counter-cli.rb
   git commit -m "Add token-counter-cli formula"
   git push origin main
   ```

### Step 2: Test Your Tap Locally

```bash
# Add your tap locally
brew tap puya/tools

# Install from your tap
brew install puya/tools/token-counter-cli

# Test the installation
token-counter --help
```

### Step 3: Verify Formula Quality

```bash
# Audit your formula for issues
brew audit --strict puya/tools/token-counter-cli

# Test the formula thoroughly
brew test puya/tools/token-counter-cli
```

### Step 4: Documentation for Users

Add this to your main README.md:

```markdown
## Installation via Homebrew

```bash
brew tap puya/tools
brew install token-counter-cli
```
```

---

## 🏆 Option 2: Submit to Homebrew Core

This gets your package into the main Homebrew repository. More visibility but requires review.

### Prerequisites for Homebrew Core

1. **Package Requirements:**
   - ✅ Stable, well-tested software 
   - ✅ Notable/popular enough (your tool qualifies!)
   - ✅ Maintained and supported
   - ✅ No duplicate functionality (checked - your tool is unique)

2. **Technical Requirements:**
   - ✅ Formula passes `brew audit --strict`
   - ✅ Has working tests
   - ✅ Builds successfully on macOS

### Step 1: Fork homebrew-core

```bash
# Fork the repository on GitHub: https://github.com/Homebrew/homebrew-core
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/homebrew-core.git
cd homebrew-core
```

### Step 2: Create the Formula

```bash
# Add your formula to the correct location
cp /path/to/token-counter/token-counter-cli.rb Formula/

# Test locally
brew install --build-from-source ./Formula/token-counter-cli.rb
brew test token-counter-cli
brew audit --strict token-counter-cli
```

### Step 3: Create Pull Request

```bash
# Create a new branch
git checkout -b token-counter-cli

# Add and commit
git add Formula/token-counter-cli.rb
git commit -m "token-counter-cli 0.1.0 (new formula)

Fast CLI tool for counting tokens with LLM context limit comparison.
Uses tiktoken library for accurate token counting.
Supports multiple file types, directory scanning, and LLM limit comparison."

# Push and create PR
git push origin token-counter-cli
```

### Step 4: PR Requirements

Your PR description should include:

```markdown
## New Formula: token-counter-cli

**Description:** Fast CLI tool for counting tokens with LLM context limit comparison

**Features:**
- Accurate token counting using tiktoken (same as OpenAI)
- Support for multiple file formats
- LLM context window limit comparison
- Rich CLI interface with progress bars
- Directory scanning with exclusion patterns

**Testing:**
- [x] `brew install --build-from-source ./Formula/token-counter-cli.rb` succeeds
- [x] `brew test token-counter-cli` passes  
- [x] `brew audit --strict token-counter-cli` passes
- [x] Formula builds on macOS

**Justification:**
This tool fills a gap for developers working with LLMs who need accurate token counting
for prompt engineering and staying within context limits. It's actively maintained
and has unique features not found in existing tools.
```

### Step 5: Review Process

- Homebrew maintainers will review your PR
- They may request changes or improvements
- Typical review time: 1-7 days for new formulas
- Be responsive to feedback

---

## 🛠 Local Testing Commands

Before submitting anywhere, test thoroughly:

```bash
# Test installation from source
brew install --build-from-source ./token-counter-cli.rb

# Run built-in tests
brew test token-counter-cli

# Audit for issues
brew audit --strict token-counter-cli

# Test uninstall/reinstall
brew uninstall token-counter-cli
brew install token-counter-cli

# Test actual functionality
echo "test" | token-counter
token-counter --help
token-counter /path/to/some/file.txt
```

---

## 📋 Checklist

### Before Creating Tap:
- [ ] Formula file renamed to `token-counter-cli.rb`
- [ ] All SHA256 hashes verified and correct
- [ ] Tests pass locally
- [ ] Formula passes audit

### Before Submitting to Core:
- [ ] Tool is stable and well-maintained
- [ ] Formula follows all Homebrew guidelines
- [ ] Comprehensive testing completed
- [ ] PR description is detailed and informative

---

## 🎯 Recommendation

**Start with your own tap** (`puya/tools`) to:
1. Get immediate distribution
2. Gather user feedback
3. Prove stability
4. Build confidence in the formula

**Then consider homebrew-core** after your tool gains traction and you have evidence of its usefulness and stability. 