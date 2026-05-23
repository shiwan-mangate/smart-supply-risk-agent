import json
import time
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from main import run_risk_intelligence
from src.logger import logger


WATCHED_REGIONS_FILE = Path("watched_regions.json")


def load_watched_regions():
    try:
        if not WATCHED_REGIONS_FILE.exists():
            logger.warning("watched_regions.json not found")
            return []

        with open(WATCHED_REGIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger.error("watched_regions.json must contain a list")
            return []

        return data

    except Exception as e:
        logger.error(f"Failed to load watched regions: {e}")
        return []


def scheduled_analysis_job():
    logger.info("Scheduled daily supply chain analysis started")

    regions = load_watched_regions()

    if not regions:
        logger.warning("No watched regions configured")
        return

    for region in regions:
        try:
            logger.info(f"Running scheduled analysis for {region}")

            result = run_risk_intelligence(region)

            if result:
                logger.info(
                    f"Completed scheduled analysis for {region} "
                    f"(Risk Score: {result['risk_score']})"
                )

        except Exception as e:
            logger.error(
                f"Scheduled analysis failed for {region}: {e}"
            )

    logger.info("Scheduled daily supply chain analysis completed")


def schedule_daily_analysis():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        scheduled_analysis_job,
        trigger=IntervalTrigger(hours=24),
        max_instances=1,
        id="daily_supply_chain_analysis",
        replace_existing=True
    )

    scheduler.start()

    logger.info("Daily automated scheduler started")

    return scheduler


def run_scheduler_forever():
    scheduler = schedule_daily_analysis()

    try:
        while True:
            time.sleep(60)

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped")