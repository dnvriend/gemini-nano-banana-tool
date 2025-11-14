#!/bin/bash

# Environment setup helper for nano-banana CLI
# Helps users configure their environment for Gemini API access

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Print functions
print_info() { echo -e "${BLUE}[INFO]${NC} $1" >&2; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1" >&2; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1" >&2; }
print_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Show setup banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                nano-banana Environment Setup                 ║"
    echo "║              Google Gemini Image Generation CLI              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check system dependencies
check_dependencies() {
    print_info "Checking system dependencies..."

    local missing_deps=()
    local optional_missing=()

    # Required dependencies
    for cmd in curl jq base64; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing_deps+=("$cmd")
        fi
    done

    # Optional dependencies
    for cmd in bc file; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            optional_missing+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install the missing tools:"

        # Provide installation instructions based on OS
        if command -v apt >/dev/null 2>&1; then
            echo "  Ubuntu/Debian: sudo apt update && sudo apt install ${missing_deps[*]}"
        elif command -v yum >/dev/null 2>&1; then
            echo "  CentOS/RHEL: sudo yum install ${missing_deps[*]}"
        elif command -v brew >/dev/null 2>&1; then
            echo "  macOS: brew install ${missing_deps[*]}"
        elif command -v pacman >/dev/null 2>&1; then
            echo "  Arch Linux: sudo pacman -S ${missing_deps[*]}"
        else
            echo "  Please install ${missing_deps[*]} using your system's package manager"
        fi
        return 1
    fi

    if [[ ${#optional_missing[@]} -gt 0 ]]; then
        print_warning "Missing optional dependencies: ${optional_missing[*]}"
        print_info "These are optional but recommended for full functionality"
    fi

    print_success "All required dependencies are installed"
    return 0
}

# Detect shell and configuration files
detect_shell() {
    local shell_name
    shell_name=$(basename "$SHELL")

    case "$shell_name" in
        bash)
            echo "$HOME/.bashrc"
            ;;
        zsh)
            echo "$HOME/.zshrc"
            ;;
        fish)
            echo "$HOME/.config/fish/config.fish"
            ;;
        *)
            echo "$HOME/.profile"
            ;;
    esac
}

# Get API key from user
get_api_key_from_user() {
    echo ""
    print_info "To use nano-banana, you need a Google Gemini API key"
    echo ""
    echo "📖 How to get your API key:"
    echo "1. Visit: https://aistudio.google.com/app/apikey"
    echo "2. Sign in with your Google account"
    echo "3. Click 'Create API key'"
    echo "4. Copy the generated API key"
    echo ""

    local api_key=""
    while [[ -z "$api_key" ]]; do
        echo -n "🔑 Enter your Gemini API key (or press Ctrl+C to exit): "
        read -r api_key
        echo ""

        if [[ -z "$api_key" ]]; then
            print_warning "API key is required to continue"
            continue
        fi

        # Basic validation
        if [[ ${#api_key} -lt 20 ]]; then
            print_error "API key appears to be too short"
            api_key=""
            continue
        fi

        if [[ ! "$api_key" =~ ^[a-zA-Z0-9_-]+$ ]]; then
            print_error "API key contains invalid characters"
            api_key=""
            continue
        fi

        break
    done

    echo "$api_key"
}

# Test API key
test_api_key() {
    local api_key="$1"

    print_info "Testing API key..."

    local response
    response=$(curl -s \
        --max-time 10 \
        -H "x-goog-api-key: $api_key" \
        -H "Content-Type: application/json" \
        "https://generativelanguage.googleapis.com/v1beta/models" 2>/dev/null)

    if echo "$response" | jq -e '.error' >/dev/null 2>&1; then
        local error_code
        error_code=$(echo "$response" | jq -r '.error.code // "UNKNOWN"')

        case "$error_code" in
            400|401|403)
                print_error "❌ API key authentication failed"
                print_error "Please check that your API key is valid and enabled"
                return 1
                ;;
            *)
                print_error "❌ API test failed with error: $error_code"
                return 1
                ;;
        esac
    fi

    print_success "✅ API key is valid and working"
    return 0
}

# Setup environment variables
setup_environment() {
    local api_key="$1"
    local shell_config
    shell_config=$(detect_shell)

    echo ""
    print_info "Setting up environment variables..."

    # Create environment export commands
    local env_exports=""
    env_exports="# nano-banana CLI Configuration\n"
    env_exports+="export GEMINI_API_KEY=\"$api_key\"\n"
    env_exports+="export GEMINI_BASE_URL=\"https://generativelanguage.googleapis.com/v1beta\"\n"
    env_exports+="export GEMINI_TIMEOUT=\"120\"\n"
    env_exports+="export GEMINI_VERBOSE=\"false\"\n"

    # Check if nano-banana config already exists
    if grep -q "nano-banana CLI Configuration" "$shell_config" 2>/dev/null; then
        print_warning "nano-banana configuration already exists in $shell_config"
        echo -n "🔄 Update existing configuration? (y/N): "
        read -r update_config
        echo ""

        if [[ "$update_config" =~ ^[Yy]$ ]]; then
            # Remove existing configuration
            sed -i '/# nano-banana CLI Configuration/,/^$/d' "$shell_config" 2>/dev/null || true
        else
            print_info "Skipping environment configuration"
            return 0
        fi
    fi

    # Add new configuration
    echo -e "$env_exports" >> "$shell_config"
    print_success "✅ Environment variables added to $shell_config"

    echo ""
    print_info "📝 To activate the configuration, run:"
    echo "   source $shell_config"
    echo ""
    print_info "Or restart your terminal session"
}

# Test installation
test_installation() {
    echo ""
    print_info "Testing nano-banana installation..."

    # Get script directory
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
    local nano_banana_cmd="$script_dir/nano-banana.sh"

    if [[ ! -f "$nano_banana_cmd" ]]; then
        print_error "nano-banana.sh not found in script directory"
        return 1
    fi

    # Test help command
    if "$nano_banana_cmd" --help >/dev/null 2>&1; then
        print_success "✅ nano-banana CLI is working"
    else
        print_error "❌ nano-banana CLI test failed"
        return 1
    fi

    # Test connectivity
    if GEMINI_API_KEY="${GEMINI_API_KEY:-}" "$nano_banana_cmd" -v status >/dev/null 2>&1; then
        print_success "✅ API connectivity confirmed"
    else
        print_warning "⚠️  API connectivity test failed (this is normal if API key is not set)"
    fi
}

# Show next steps
show_next_steps() {
    echo ""
    echo -e "${GREEN}🎉 Setup complete!${NC}"
    echo ""
    echo "📚 Next steps:"
    echo "1. Activate your environment: source $(detect_shell)"
    echo "2. Try a simple generation:"
    echo "   ./nano-banana.sh generate -o test.png 'A cute cat sitting on a rainbow'"
    echo ""
    echo "📖 For more examples and documentation:"
    echo "   ./nano-banana.sh --help"
    echo "   cat README.md"
    echo ""
    echo "🌟 Supported features:"
    echo "   • Text-to-image generation"
    echo "   • Image editing with reference photos"
    echo "   • Multiple aspect ratios and resolutions"
    echo "   • Cross-platform compatibility"
    echo ""
}

# Main setup function
main() {
    show_banner

    echo "🔍 Checking system compatibility..."
    if ! check_dependencies; then
        exit 1
    fi

    echo ""
    echo -n "🔑 Do you have a Gemini API key? (y/N): "
    read -r has_api_key
    echo ""

    local api_key=""

    if [[ "$has_api_key" =~ ^[Yy]$ ]]; then
        echo -n "🔑 Enter your existing API key: "
        read -r api_key
        echo ""
    else
        api_key=$(get_api_key_from_user)
    fi

    # Test API key
    if ! test_api_key "$api_key"; then
        print_error "Setup failed due to invalid API key"
        exit 1
    fi

    # Setup environment
    export GEMINI_API_KEY="$api_key"
    setup_environment "$api_key"

    # Test installation
    test_installation

    # Show next steps
    show_next_steps
}

# Handle script interruption
trap 'print_warning "Setup interrupted by user"; exit 130' INT TERM

# Run main function
main "$@"