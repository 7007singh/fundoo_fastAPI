from fastapi import FastAPI
from routers.user import user_router


app = FastAPI(debug=True)
app.include_router(user_router, prefix='/user')
