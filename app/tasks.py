from celery import Celery
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

celery_app = Celery(
    "smart_grid",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

celery_app.conf.beat_schedule = {
    "aggregate-every-5-min": {
        "task": "app.tasks.aggregate_load",
        "schedule": 300.0,
    },
}

SYNC_DB = os.getenv("DATABASE_URL").replace("+asyncpg", "")

@celery_app.task
def aggregate_load():
    engine = create_engine(SYNC_DB)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT city_zone,
                   SUM(voltage * current) / 1000000 AS total_megawatt
            FROM meter_readings
            WHERE timestamp > NOW() - INTERVAL '5 minutes'
            GROUP BY city_zone
        """))
        for row in result:
            print(f"Zone: {row.city_zone} | Load: {row.total_megawatt:.2f} MW")
        conn.commit()
    return "Aggregation complete"