from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from router.project_route.project_router import router as project_router
from router.data_route.data_router import router as data_router

if __name__ == '__main__':
    app = FastAPI()
    app.include_router(prefix="/api/v1/projects", router=project_router)
    app.include_router(prefix="/api/v1/data", router=data_router)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.mount("/static", StaticFiles(directory="static"), name="static")

    uvicorn.run(app, host="0.0.0.0", port=3000)
