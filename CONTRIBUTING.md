# Contributing to Entroplain

Thanks for your interest in contributing! 🎉

## Development Setup

```bash
# Clone the repo
git clone https://github.com/entroplain/entroplain.git
cd entroplain

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Project Structure

```
entroplain/
├── entroplain/
│   ├── __init__.py      # Package exports
│   ├── monitor.py       # Core entropy monitor
│   ├── providers.py     # LLM provider integrations
│   ├── hooks.py         # Agent framework hooks
│   └── cli.py           # Command-line interface
├── tests/
│   └── test_monitor.py  # Unit tests
├── pyproject.toml       # Package config
├── README.md            # Documentation
└── LICENSE              # MIT License
```

## Adding a New Provider

1. Create a new provider class in `providers.py`:

```python
class MyProvider(BaseProvider):
    def calculate_entropy(self, logprobs_data: Dict) -> float:
        # Parse provider-specific format
        ...
    
    def stream_with_entropy(self, **kwargs) -> Iterator[TokenWithEntropy]:
        # Stream tokens with entropy
        ...
```

2. Export it in `__init__.py`

3. Add tests in `tests/test_providers.py`

## Code Style

- Use **Black** for formatting
- Use **isort** for imports
- Use **mypy** for type checking

```bash
black entroplain/ tests/
isort entroplain/ tests/
mypy entroplain/
```

## Testing

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=entroplain
```

## Pull Request Process

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black .`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Questions?

Open an issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
