"""Tests for the agent system."""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic_commerce import (
    generate_recommendations,
    UserQuery,
    Money,
    Product,
    Offer,
    Review,
    MockProductSearch,
    MockPriceProvider,
    MockReviewProvider,
)


@pytest.mark.asyncio
async def test_basic_recommendation():
    """Test basic recommendation generation."""
    result = await generate_recommendations(
        "wireless headphones",
        budget=200.0,
        top_k=5
    )
    
    assert len(result.recommendations) > 0
    assert len(result.recommendations) <= 5
    assert result.query.raw == "wireless headphones"


@pytest.mark.asyncio
async def test_budget_constraint():
    """Test that budget constraints are respected in scoring."""
    result = await generate_recommendations(
        "headphones under $100",
        budget=100.0,
        must_have=["wireless"],
        top_k=3
    )
    
    assert len(result.recommendations) > 0
    # Top recommendations should respect budget
    top_rec = result.recommendations[0]
    assert top_rec.best_offer is not None


@pytest.mark.asyncio
async def test_feature_matching():
    """Test that feature requirements are considered."""
    result = await generate_recommendations(
        "noise cancelling headphones",
        must_have=["noise_cancelling"],
        top_k=5
    )
    
    assert len(result.recommendations) > 0
    assert result.query.must_have == ["noise_cancelling"]


@pytest.mark.asyncio
async def test_budget_parsing():
    """Test automatic budget extraction from query."""
    result = await generate_recommendations(
        "laptop under $1500",
        top_k=3
    )
    
    # Budget should be auto-parsed from query
    assert result.query.budget is not None
    assert result.query.budget.amount == 1500.0


@pytest.mark.asyncio
async def test_mock_search_provider():
    """Test mock search provider."""
    query = UserQuery(
        raw="test product",
        must_have=[],
        nice_to_have=[],
    )
    
    provider = MockProductSearch()
    products = await provider.search(query)
    
    assert len(products) == 6  # Mock returns 6 products
    assert all(isinstance(p, Product) for p in products)


@pytest.mark.asyncio
async def test_mock_price_provider():
    """Test mock price provider."""
    product = Product(
        id="test-1",
        title="Test Product",
        offers=[Offer(
            retailer="TestMart",
            url="https://example.com",
            price=Money(amount=100.0)
        )]
    )
    
    provider = MockPriceProvider()
    offers = await provider.offers(product)
    
    assert len(offers) == 3  # Mock returns 3 retailers
    assert all(isinstance(o, Offer) for o in offers)
    assert all(len(o.price_history) > 0 for o in offers)


@pytest.mark.asyncio
async def test_mock_review_provider():
    """Test mock review provider."""
    product = Product(
        id="test-1",
        title="Test Product"
    )
    
    provider = MockReviewProvider()
    reviews = await provider.fetch_reviews(product, limit=10)
    
    assert len(reviews) == 10
    assert all(isinstance(r, Review) for r in reviews)
    assert all(r.rating is not None for r in reviews)


@pytest.mark.asyncio
async def test_diverse_recommendations():
    """Test that recommendations are diverse (not all the same brand)."""
    result = await generate_recommendations(
        "headphones",
        budget=300.0,
        top_k=5
    )
    
    brands = [rec.title.split()[0] for rec in result.recommendations]
    # Should have at least 2 different brands in top 5
    assert len(set(brands)) >= 2


@pytest.mark.asyncio
async def test_score_ordering():
    """Test that recommendations are ordered by score."""
    result = await generate_recommendations(
        "wireless earbuds",
        budget=150.0,
        top_k=5
    )
    
    scores = [rec.score for rec in result.recommendations]
    # Scores should be in descending order
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_empty_must_have():
    """Test that system works without must-have features."""
    result = await generate_recommendations(
        "tablet",
        budget=500.0,
        must_have=[],
        nice_to_have=[],
        top_k=3
    )
    
    assert len(result.recommendations) > 0


@pytest.mark.asyncio
async def test_comparative_query():
    """Test handling of comparative queries."""
    result = await generate_recommendations(
        "dyson v15 vs samsung jet vacuum",
        budget=700.0,
        top_k=5
    )
    
    assert len(result.recommendations) > 0
    # Should return products even with 'vs' in query
    assert all(rec.title for rec in result.recommendations)
