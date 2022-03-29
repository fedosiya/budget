import asyncio

from PyQt5.QtWidgets import QApplication

from ui import widget, app
import sys
import httpx


def startUI():
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:5000/')
        print(r.json())
    startUI()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
