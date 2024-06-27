from freeswitchESL import ESL
import xml.etree.ElementTree as ET
import websockets
import datetime
import psycopg2
import asyncio
import ast
import json

# Global set to store all connected websockets
my_sockets = set()

con = ESL.ESLconnection("138.201.188.127", "8021", "ClueCon")
con.events("plain", "ALL")
    
async def websocket_handler(websocket, path):
    # Add the new websocket to our global set
    my_sockets.add(websocket)

    try:
        # Send a greeting to the new connection
        # await websocket.send(f"Hello, your ID is {global_id + 1}")

        # Listen for incoming messages from the frontend
        async for message in websocket:
            
            print ("MESSAGE: ", message)

        # If the connection is closed, remove it from our set
        my_sockets.remove(websocket)

    except websockets.exceptions.ConnectionClosedError:
        my_sockets.remove(websocket)

async def send_message():
    
    while True:
        event = await asyncio.to_thread(con.recvEvent)
        
        if event:
            # Handle the event
            event_name = event.getHeader("Event-Name")
            
            print(f"EVENT: {event_name}")


async def main():
    # Start the server
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8001)

    # Start the message sending loop
    await send_message()

    # Serve the websockets indefinitely
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
