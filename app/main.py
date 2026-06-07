from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .database import get_db, engine, Base
from .models import MeterReading, MeterReadingIn, MeterReadingOut
from .websocket_manager import manager
from contextlib import asynccontextmanager
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Smart Grid Load Balancing API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Smart Grid API is running!"}

@app.post("/api/v1/meter/reading", response_model=MeterReadingOut)
async def ingest_meter_data(reading: MeterReadingIn, db: AsyncSession = Depends(get_db)):
    db_reading = MeterReading(**reading.model_dump())
    db.add(db_reading)
    await db.commit()
    await db.refresh(db_reading)

    if reading.voltage > 405:
        alert = json.dumps({
            "alert": "HIGH_CAPACITY",
            "zone": reading.city_zone,
            "voltage": reading.voltage,
            "meter_id": reading.meter_id
        })
        await manager.broadcast(alert)

    return db_reading

@app.get("/api/v1/meter/readings/{city_zone}")
async def get_zone_readings(city_zone: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM meter_readings WHERE city_zone = :zone ORDER BY timestamp DESC LIMIT 50"),
        {"zone": city_zone}
    )
    return result.mappings().all()

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Alert: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)