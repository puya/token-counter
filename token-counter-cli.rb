# Homebrew Formula for Token Counter CLI
# This goes in homebrew-core or your own tap

class TokenCounterCli < Formula
  include Language::Python::Virtualenv

  desc "Fast CLI tool for counting tokens with LLM context limit comparison"
  homepage "https://github.com/puya/token-counter"
  url "https://files.pythonhosted.org/packages/source/t/token-counter-cli/token_counter_cli-0.1.0.tar.gz"
  sha256 "bb0dc11a3efcd26582f784a74165e2f32946b6755c3c97c8758df0c3afe30702"
  license "MIT"

  depends_on "rust" => :build
  depends_on "python@3.12"

  resource "inquirerpy" do
    url "https://files.pythonhosted.org/packages/source/i/inquirerpy/inquirerpy-0.3.4.tar.gz"
    sha256 "89d2ada0111f337483cb41ae31073108b2ec1e618a49d7110b0d7ade89fc197e"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-14.0.0.tar.gz"
    sha256 "82f1bc23a6a21ebca4ae0c45af9bdbc492ed20231dcb63f297d6d1021a9d5725"
  end

  resource "tiktoken" do
    url "https://files.pythonhosted.org/packages/source/t/tiktoken/tiktoken-0.9.0.tar.gz"
    sha256 "d02a5ca6a938e0490e1ff957bc48c8b078c88cb83977be1625b1fd8aac792c5d"
  end

  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.16.0.tar.gz"
    sha256 "af377ffaee1dbe37ae9440cb4e8f11686ea5ce4e9bae01b84ae7c63b87f1dd3b"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Token Count Result", pipe_output("#{bin}/token-counter", "test text")
    assert_match "Usage:", shell_output("#{bin}/token-counter --help")
  end
end