# Homebrew Formula Template (for after PyPI release)
# This goes in homebrew-core or your own tap

class TokenCounter < Formula
  include Language::Python::Virtualenv

  desc "Fast CLI tool for counting tokens with LLM context limit comparison"
  homepage "https://github.com/puya/token-counter"
  url "https://files.pythonhosted.org/packages/source/t/token-counter/token-counter-0.1.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"  # Get this from: shasum -a 256 dist/token_counter-0.1.0.tar.gz
  license "MIT"

  depends_on "python@3.11"

  resource "inquirerpy" do
    url "https://files.pythonhosted.org/packages/source/i/inquirerpy/inquirerpy-0.3.4.tar.gz"
    sha256 "89d2ada0111f337483cb41ae31073108b2ec1e618a49d7110b0d7ade89fc197e"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.0.0.tar.gz"  
    sha256 "8260cda28e3db6bf04d2d1ef4dbc03ba80a824c88b0e7668a0f23126a424844a"
  end

  resource "tiktoken" do
    url "https://files.pythonhosted.org/packages/source/t/tiktoken/tiktoken-0.9.0.tar.gz"
    sha256 "99c65c1d9e21325e1a19d1d2d3b1beeca25e81ccddfd20dfcedb21e86bfcda48"
  end

  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.16.0.tar.gz"
    sha256 "6e5714e7e9c90b86ba253d85feb38feff56a2cbca3ea1a1be1ea10b9830a1c2b8"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Token Count Result", pipe_output("#{bin}/token-counter", "test text")
  end
end