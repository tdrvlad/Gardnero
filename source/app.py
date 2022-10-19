from fastapi import FastAPI
import uvicorn
from source.circuit_scheduler import CircuitScheduler


def server(circuit_scheduler: CircuitScheduler):

    app = FastAPI()

    @app.post("/add_circuit")
    async def add_circuit(circuit_name: str, pump_id: int, time_period_days: int, time_duration_seconds: int):
        return circuit_scheduler.add_circuit(circuit_name, pump_id, time_period_days, time_duration_seconds)

    @app.post("/change_circuit")
    async def change_circuit(circuit_name: str, time_period_days: int = 0, time_duration_seconds: int = 0):
        return circuit_scheduler.change_circuit(circuit_name, time_period_days, time_duration_seconds)

    @app.get("/circuits")
    async def get_circuits():
        return circuit_scheduler.get_circuits()

    @app.get("/circuit_names")
    async def get_circuit_names():
        circuits = circuit_scheduler.get_circuits()
        if len(circuits):
            return list(circuits.keys())
        else:
            return []

    @app.get("/circuit/{circuit_name}")
    async def get_circuit(circuit_name:str):
        return circuit_scheduler.get_circuit(circuit_name)

    @app.get("/circuit/{circuit_name}/time_until_next_run")
    async def get_circuit(circuit_name: str):
        return circuit_scheduler.get_circuit_time_until_nex_run(circuit_name)

    @app.post('/mode/{mode}')
    async def change_mode(mode:int):
        return circuit_scheduler.change_mode(mode)

    @app.get('/mode')
    async def get_mode():
        return circuit_scheduler.get_mode()

    @app.post('/start_pump/{pump_id}')
    async def start_pump(pump_id: int, time_duration_seconds: int = 2):
        return circuit_scheduler.start_pump(pump_id, time_duration_seconds)

    @app.post('/start_circuit/{circuit_name}')
    async def start_circuit(circuit_name: str, time_duration_seconds: int = 2):
        return circuit_scheduler.start_circuit(circuit_name, time_duration_seconds)

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")