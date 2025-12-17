#!/usr/bin/env python
"""Demo script for running the agentic e-commerce system from command line."""
import asyncio
import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic_commerce import generate_recommendations


async def run_demo(query: str, budget: float = None, must_have: list = None, 
                   nice_to_have: list = None, category: str = None, top_k: int = 5):
    """Run a demo query."""
    print(f"\n🔍 Searching for: {query}")
    if budget:
        print(f"💰 Budget: ${budget:.2f}")
    if must_have:
        print(f"✅ Must have: {', '.join(must_have)}")
    
    print("\n⏳ Processing...\n")
    
    result = await generate_recommendations(
        raw_query=query,
        budget=budget,
        must_have=must_have or [],
        nice_to_have=nice_to_have or [],
        category=category,
        top_k=top_k
    )
    
    print("=" * 80)
    print(f"📊 Found {len(result.recommendations)} recommendations")
    print("=" * 80)
    
    for i, rec in enumerate(result.recommendations, 1):
        print(f"\n#{i} • {rec.title}")
        print(f"   Score: {rec.score:.2f}")
        
        if rec.best_offer:
            print(f"   Price: ${rec.best_offer.price.amount:.2f} at {rec.best_offer.retailer}")
            print(f"   Link: {rec.best_offer.url}")
        
        print(f"   Why: {rec.rationale}")
    
    print("\n" + "=" * 80)


async def run_all_demos():
    """Run all predefined demo scenarios."""
    scenarios = [
        {
            "query": "wireless noise cancelling headphones under $200 for travel",
            "budget": 200.0,
            "must_have": ["wireless", "noise_cancelling"],
            "category": "audio"
        },
        {
            "query": "robot vacuum for pet hair with mapping",
            "budget": 300.0,
            "must_have": ["pet"],
            "nice_to_have": ["mapping"],
            "category": "home"
        },
        {
            "query": "4k monitor for photo editing",
            "budget": 400.0,
            "must_have": ["4k"],
            "nice_to_have": ["wide_gamut"],
            "category": "monitors"
        }
    ]
    
    for scenario in scenarios:
        await run_demo(**scenario)
        print("\n" + "=" * 80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic E-Commerce Demo - Product Recommendation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "wireless headphones under $200"
  %(prog)s --query "gaming laptop" --budget 1500 --must-have "RTX,16GB"
  %(prog)s --demo-all
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Search query (e.g., 'wireless headphones under $200')"
    )
    
    parser.add_argument(
        "--budget", "-b",
        type=float,
        help="Budget in USD (e.g., 200.0)"
    )
    
    parser.add_argument(
        "--must-have", "-m",
        type=str,
        help="Comma-separated must-have features (e.g., 'wireless,noise_cancelling')"
    )
    
    parser.add_argument(
        "--nice-to-have", "-n",
        type=str,
        help="Comma-separated nice-to-have features"
    )
    
    parser.add_argument(
        "--category", "-c",
        type=str,
        help="Product category (e.g., 'audio', 'electronics')"
    )
    
    parser.add_argument(
        "--top-k", "-k",
        type=int,
        default=5,
        help="Number of recommendations to return (default: 5)"
    )
    
    parser.add_argument(
        "--demo-all",
        action="store_true",
        help="Run all predefined demo scenarios"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    
    args = parser.parse_args()
    
    if args.demo_all:
        asyncio.run(run_all_demos())
    elif args.query:
        must_have = [x.strip() for x in args.must_have.split(",")] if args.must_have else None
        nice_to_have = [x.strip() for x in args.nice_to_have.split(",")] if args.nice_to_have else None
        
        if args.json:
            async def run_json():
                result = await generate_recommendations(
                    raw_query=args.query,
                    budget=args.budget,
                    must_have=must_have or [],
                    nice_to_have=nice_to_have or [],
                    category=args.category,
                    top_k=args.top_k
                )
                print(json.dumps(result.model_dump(), indent=2, default=str))
            
            asyncio.run(run_json())
        else:
            asyncio.run(run_demo(
                query=args.query,
                budget=args.budget,
                must_have=must_have,
                nice_to_have=nice_to_have,
                category=args.category,
                top_k=args.top_k
            ))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
