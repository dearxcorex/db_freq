from fastapi import FastAPI,Depends,status,HTTPException,Form,Request
from fastapi.templating import Jinja2Templates
import schemas,models,database
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/",response_class=HTMLResponse)
async def home(request:Request,db:Session=Depends(get_db)):
    frequencies = db.query(models.freq).all()
    return templates.TemplateResponse("index.html",{"request":request,"frequencies":frequencies})




@app.post("/add")
async def add(request:Request,freq:float=Form(...),institution:str=Form(...),usage:str=Form(...),db:Session=Depends(get_db)):
    new_freq = models.freq(freq = freq, institution = institution, usage = usage)
    db.add(new_freq)
    db.commit()
    db.refresh(new_freq)

    return RedirectResponse(url=app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)


@app.get("/addnew")
async def addnew(request:Request):
    return templates.TemplateResponse("addnew.html",{"request":request})


@app.get("/edit/{id}")
async def edit(request:Request,id:int,db:Session=Depends(get_db)):
    frequencies = db.query(models.freq).filter(models.freq.id==id).first()
    return templates.TemplateResponse("edit.html",{"request":request,"frequencies":frequencies})


@app.post("/update/{id}")
async def update(request:Request,id:int,freq:float=Form(...),institution:str=Form(...),usage:str=Form(...),db:Session=Depends(get_db)):
    frequencies = db.query(models.freq).filter(models.freq.id==id).first()
    frequencies.freq = freq
    frequencies.institution = institution
    frequencies.usage = usage
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)



@app.get("/delete/{id}")
async def delete(request:Request,id:int,db:Session=Depends(get_db)):
    frequencies = db.query(models.freq).filter(models.freq.id==id).first()
    db.delete(frequencies)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)
# find freq
# @app.get("/freq/{id}",response_model=schemas.freqResponse)
# def get_freq(id:float,db:Session=Depends(get_db)):
#     freq = db.query(models.freq).filter(models.freq.freq==id)

#     if not freq.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"freq with id {id} not found")
    

#     return freq.first()

# delete freq
# @app.delete("/freq/{id}")
# def delete_freq(id:float,db:Session=Depends(get_db)):
#     freq = db.query(models.freq).filter(models.freq.freq==id)

#     if not freq.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"freq with id {id} not found")
    
#     freq.delete(synchronize_session=False)
#     db.commit()
#     return {"detail":"done"}


#update freq
# @app.put("/freq/{id}")
# def update_freq(id:float,request:schemas.freqUpdateResponse,db:Session=Depends(get_db)):
#     freq = db.query(models.freq).filter(models.freq.freq==id).first()
     
#     if not freq:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"freq with id {id} not found")
    

#     if request.freq == 0:
#         freq.freq = request.freq
#     if request.institution  == "string":
#         freq.institution =  request.institution
#         # request.institution =  models.freq.institution
#     if request.usage == "string":
#         freq.usage = request.usage

#     freq.update(request.model_dump(),synchronize_session=False)
    
#     db.commit()
#     return {"detail":"done"}





