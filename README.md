

# Agentic E-Commerce Assistant

AI-powered product recommendation system using multi-agent architecture to search, compare prices, analyze reviews, and deliver personalized recommendations.

## Features

- **Multi-Agent System**: Search → Price Comparison → Review Analysis → Smart Recommendations
- **Natural Language Queries**: "wireless headphones under $200 for travel"
- **AI Review Analysis**: Sentiment scoring using HuggingFace transformers
- **Price History Tracking**: Identifies good deals vs historical prices
- **Diverse Results**: MMR algorithm ensures variety in recommendations

## Steps to Start

```bash
# Clone and setup
git clone https://github.com/yourusername/agentic-ecommerce.git
cd agentic-ecommerce
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Add your HUGGINGFACE_API_TOKEN to .env


**Command Line:**
```bash
python scripts/run_demo.py --query "robot vacuum under $300" --must-have "pet,mapping"
```

**Python API:**
```python
from src.agentic_commerce import generate_recommendations

result = await generate_recommendations(
    "noise cancelling headphones under $150",
    budget=150.0,
    must_have=["wireless", "noise_cancelling"]
)

for rec in result.recommendations:
    print(f"{rec.title}: ${rec.best_offer.price.amount} - Score: {rec.score:.2f}")
```

## API Keys

Required for full functionality:
- **HuggingFace API Token** ([Get here](https://huggingface.co/settings/tokens)) - For sentiment analysis
- **Icecat Token** (Optional) - For product enrichment
- **RapidAPI Key** (Optional) - Fallback sentiment API

Add to `.env`:
```env
HUGGINGFACE_API_TOKEN=your_token_here
```

## Architecture

```
User Query → ProductSearchAgent → PriceComparisonAgent → ReviewAnalysisAgent → RecommendationEngine
```

**Scoring Factors:**
- Budget fit (38%)
- Review sentiment (22%)
- Feature matching (22%)
- Price history/deals (13%)
- Availability (5%)

## Testing

```bash
pytest tests/                    # Run all tests
python scripts/run_demo.py --demo-all  # Run demo scenarios
```

## Project Structure

```
├── src/agentic_commerce.py     # Core agent pipeline
├── app/streamlit_app.py        # Web interface
├── scripts/run_demo.py         # CLI tool
├── tests/test_agents.py        # Test suite
└── notebooks/                  # Development notebooks
```

## Deployment

**Streamlit Cloud** (Easiest):
1. Push to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add secrets in dashboard

**Docker**:
```bash
docker build -t agentic-ecommerce .
docker run -p 8501:8501 -e HUGGINGFACE_API_TOKEN=your_token agentic-ecommerce
```

See [docs/deployment.md](docs/deployment.md) for AWS, Heroku, and GCP options.

## Example Queries

- "wireless noise cancelling headphones for travel under $200"
- "robot vacuum with mapping and pet hair under $300"
- "4k monitor for photo editing"
- "gaming laptop with RTX 4070"

## Contributing

Contributions welcome! Fork, create a feature branch, and submit a PR.

## License

MIT License - See [LICENSE](LICENSE) for details.


**Note**: Currently uses mock providers for demonstration. Integrate real APIs (eBay, Amazon, Best Buy) for production use.
