# Completion Command

Generate shell completion scripts for bash, zsh, or fish shells.

## Usage

```bash
gemini-nano-banana-tool completion SHELL
```

## Arguments

- `SHELL` - Shell type (bash, zsh, or fish)

## Examples

### Bash Completion

```bash
# Generate completion script
gemini-nano-banana-tool completion bash

# Add to ~/.bashrc
eval "$(gemini-nano-banana-tool completion bash)"
```

### Zsh Completion

```bash
# Generate completion script
gemini-nano-banana-tool completion zsh

# Add to ~/.zshrc
eval "$(gemini-nano-banana-tool completion zsh)"
```

### Fish Completion

```bash
# Generate completion script
gemini-nano-banana-tool completion fish

# Save to completions directory
gemini-nano-banana-tool completion fish > \
  ~/.config/fish/completions/gemini-nano-banana-tool.fish
```

## What Shell Completion Does

Shell completion provides:

- **Command Completion**: Tab to complete command names
- **Argument Completion**: Tab to complete option names
- **Value Completion**: Tab to complete option values (file paths, choices)
- **Help Integration**: Shows available options while typing

## Installation

### Bash

Add to `~/.bashrc`:

```bash
eval "$(gemini-nano-banana-tool completion bash)"
```

Then reload:
```bash
source ~/.bashrc
```

### Zsh

Add to `~/.zshrc`:

```bash
eval "$(gemini-nano-banana-tool completion zsh)"
```

Then reload:
```bash
source ~/.zshrc
```

### Fish

Save to completions directory:

```bash
gemini-nano-banana-tool completion fish > \
  ~/.config/fish/completions/gemini-nano-banana-tool.fish
```

Then reload (automatic in most cases):
```bash
exec fish
```

## Verification

Test completion by typing:

```bash
gemini-nano-banana-tool <TAB>
```

You should see available commands:
- `completion`
- `generate`
- `generate-conversation`
- `list-aspect-ratios`
- `list-models`
- `promptgen`

## Troubleshooting

If completion doesn't work:

1. **Check Installation**: Verify completion script is loaded
2. **Reload Shell**: Close and reopen terminal or source config file
3. **Check Permissions**: Ensure completion file is readable
4. **Check Path**: Verify `gemini-nano-banana-tool` is in PATH

## Pattern

This follows the industry-standard pattern used by:
- `kubectl completion`
- `helm completion`
- `docker completion`
- `gh completion`

## Benefits

- **Faster Typing**: Tab completion reduces typing
- **Discover Options**: See available options without `--help`
- **Reduce Errors**: Autocomplete prevents typos
- **Better UX**: Professional CLI experience
