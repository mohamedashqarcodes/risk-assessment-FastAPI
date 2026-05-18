from fastapi import APIRouter,FastAPI,status,Request,HTTPException,Depends
from models import Assessment,AssessmentResponse
from dependencies import get_settings, verify_api_key, Settings
from fastapi.responses import JSONResponse

#create database
assessment_db=[]

router_with_auth = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
    dependencies=[Depends(verify_api_key)],   # applies to every route
)

@router_with_auth.get("/config")
def get_config(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name, "max_risk": settings.max_risk}

@router_with_auth.post("/",response_model=AssessmentResponse,status_code=status.HTTP_201_CREATED)
def create_assessment(a:Assessment):
    entry={"id":len(assessment_db)+1,**a.model_dump()}
    assessment_db.append(entry)
    return entry

@router_with_auth.get("/",response_model=list[AssessmentResponse]) # no need status code as 200 is automatic
def get_assessment():
    return assessment_db

@router_with_auth.get("/{id}",response_model=AssessmentResponse)
def getbyid(id:int):
    for f in assessment_db:
        if f["id"]==id:
            return f
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"engagement {id} not found")

@router_with_auth.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT) #why si there status code here and why no response model here  
def deletebyid(id:int):
    for i,f in enumerate(assessment_db):
        if f["id"]==id:
            assessment_db.pop(i) #it pops the index and not the item
            return None
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"engagement {id} not found")
