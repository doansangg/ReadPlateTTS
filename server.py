from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
import uvicorn
from handleBienSoXe import HandleBSX

app = FastAPI()
handleBSXNam =HandleBSX('config/config.yaml')
origins = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def Redirect():
    return RedirectResponse('/docs')

@app.get("/tts/generate")
async def getTTS(text:str):
    pathFile=handleBSXNam.synthesize(text)    
    return FileResponse(pathFile)

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='127.0.0.1')