

from fastapi import APIRouter,FastAPI,status,Request,HTTPException
from fastapi.responses import JSONResponse
from routers.assessments import router_with_auth as assessments_router





# fastapi dev main.py



app=FastAPI(title="AI model risk assessments tracker",description="internal API to track AI model risk assessments,completion statuses, the liason officers and the risk of project involved")
app.include_router(assessments_router)

#GLOBAL EXCEPTION HANDLER

@app.exception_handler(Exception)
async def global_exception_handler(request:Request,exception:Exception):
    print(f"unhandled error on {request.url}:{exception}")
    return JSONResponse(status_code=500,content={"message":"internal error logged"})#content from json repsonse must be dictionary #json is the language spoken by API to computer and 500 error shows internal server error and content or description always in dictionairies??



# the response model is to indicate what format i want from the api to me


        
            

        
