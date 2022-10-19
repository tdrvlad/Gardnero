from source.app import server
from source.circuit_scheduler import CircuitScheduler

if __name__ == "__main__":
    circuit_scheduler = CircuitScheduler()
    server(circuit_scheduler)



