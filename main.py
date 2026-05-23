import asyncio

from src.graph_logic import create_supply_chain_graph
from src.database import save_analysis, save_critical_alert


def parse_risk_report(report_text: str):
    lines = report_text.splitlines()

    executive_summary = ""
    risk_score = 0.0
    confidence_level = "Unknown"

    for i, line in enumerate(lines):
        clean_line = line.strip().replace("*", "")

        if "Executive Summary:" in clean_line:
            if i + 1 < len(lines):
                executive_summary = lines[i + 1].strip()

        if "Risk Score" in clean_line:
            if i + 1 < len(lines):
                try:
                    risk_score = float(
                        lines[i + 1].strip().replace("*", "")
                    )
                except ValueError:
                    risk_score = 0.0

        if "Confidence Level:" in clean_line:
            if i + 1 < len(lines):
                confidence_level = (
                    lines[i + 1]
                    .strip()
                    .replace("*", "")
                )

    return executive_summary, risk_score, confidence_level


def build_initial_state(region: str):
    return {
        "query": region,
        "news_context": "",
        "market_risk_report": "",
        "logistics_impact": "",
        "inventory_risk_level": "",
        "final_recommendation": "",
        "competitor_status": "",
        "risk_report": "",
        "risk_score": 0.0,
        "confidence_level": "",
        "reanalysis_count": 0,
        "is_reanalysis": False,
        "recalled_memories": "",
        "history": []
    }


async def run_risk_intelligence_async(region: str):
    print(f"\n--- INITIALIZING AUTONOMOUS RISK INTELLIGENCE FOR: {region} ---")
    print(f"Analyzing {region} supply chain dependencies...")

    risk_graph = create_supply_chain_graph()
    inputs = build_initial_state(region)

    try:
        final_state = await risk_graph.ainvoke(inputs)

        report = final_state["risk_report"]

        executive_summary, risk_score, confidence_level = parse_risk_report(report)

        save_analysis(
            region=region,
            risk_score=risk_score,
            confidence_level=confidence_level,
            executive_summary=executive_summary
        )

        if risk_score >= 8:
            save_critical_alert(
                region=region,
                risk_score=risk_score,
                executive_summary=executive_summary
            )

        print("\n" + "=" * 60)
        print(f"AI RISK REPORT: {region}")
        print("=" * 60)
        print(report)
        print("=" * 60)

        return {
            "region": region,
            "risk_score": risk_score,
            "confidence": confidence_level,
            "summary": executive_summary,
            "state": final_state
        }

    except Exception as e:
        print(f"Error during orchestration for {region}: {e}")
        return None


def run_risk_intelligence(region: str):
    return asyncio.run(run_risk_intelligence_async(region))


async def run_parallel_analysis(
    regions: list[str],
    max_concurrency: int = 1
):
    print("\n=== STARTING PARALLEL MULTI-REGION ANALYSIS ===")

    semaphore = asyncio.Semaphore(max_concurrency)

    async def bounded_run(region: str):
        async with semaphore:
            return await run_risk_intelligence_async(region)

    tasks = [
        bounded_run(region)
        for region in regions
    ]

    results = await asyncio.gather(*tasks)

    print("\n=== PARALLEL ANALYSIS COMPLETE ===")

    return results


if __name__ == "__main__":
    regions = [
        "South China Sea",
        "Red Sea",
        "Taiwan Strait"
    ]

    asyncio.run(
        run_parallel_analysis(
            regions=regions,
            max_concurrency=1
        )
    )

    # run_risk_intelligence("South China Sea Logistics")