import asyncio
import random
import threading
import time
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext, ModbusSequentialDataBlock

# Création du datastore avec 100 registres holding
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0] * 100)  # registres 40001-40100
)
context = ModbusServerContext(slaves=store, single=True)

# Fonction pour mettre à jour les registres (dans un thread séparé)
def update_registers():
    while True:
        value = random.randint(0, 100)  # valeur simulée
        context[0x00].setValues(3, 0, [value])  # registre 40001
        print(f"[SIMULATION] Code erreur mis à jour = {value}")
        time.sleep(5)

# Fonction principale (asyncio)
async def run_server():
    # lancer la boucle d’update dans un thread
    threading.Thread(target=update_registers, daemon=True).start()

    print("🚀 Simulation Modbus TS1500 en cours (localhost:5020)...")
    await StartAsyncTcpServer(context, address=("127.0.0.1", 5020))

if __name__ == "__main__":
    asyncio.run(run_server())



