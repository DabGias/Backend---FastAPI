from fastapi import FastAPI

from database.db_config import setup_db
from controllers import (
    item_controller,
    sale_controller, 
    user_controller
)


setup_db()

app = FastAPI()

app.include_router(item_controller.router)
app.include_router(user_controller.router)
app.include_router(sale_controller.router)
