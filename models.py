from enum import Enum
from pydantic import BaseModel,field_validator


class Risk(str,Enum):
    HIGH="HIGH"
    MEDIUM="MEDIUM"
    LOW="LOW"

class Review(str,Enum):
    NO="NO"
    YES="YES"    

class Assessment(BaseModel):
    model_name:str
    biz_unit:str
    risk:Risk
    review:Review = Review.NO
    
    @field_validator("model_name")
    @classmethod
    def model_name_validate(cls, model_name: str):

    # strip() removes leading/trailing whitespace
        clean_name = model_name.strip()
        if len(clean_name) < 3:
            raise ValueError("Model name must be at least 3 characters long")
        return clean_name
        
class AssessmentResponse(Assessment):
    id:int