from fastapi import FastAPI

from app.routes import (lines, auth, logs)
#from contextlib import asynccontextmanager  # Uncomment if you need to create tables on app start >>>
#from app.db import init_database
#
#@asynccontextmanager
#async def lifespan(app: FastAPI):
#    init_database()
#    yield                                   # <<< Uncomment if you need to create tables on app start


app = FastAPI(
    #lifespan=lifespan,  # Uncomment if you need to create tables on app start
    title="Сервис работы с простоями на производстве",
    description="Система работы с логами о простоях на проиводственной линии, "
                "основанная на фреймворке FastAPI.",
    version="0.0.2",
    contact={
        "name": "Зенькович Алексей Алексеевич",
        "url": "https://mipt.ru",
        "email": "zenkovich.aa@phystech.edu",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router(lines.router)
app.include_router(auth.router)
app.include_router(logs.router)
