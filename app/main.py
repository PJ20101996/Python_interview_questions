from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.register_routes import router as register_router
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_router)
if __name__ == "__main__":
    # uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, workers=10, timeout_keep_alive=600)