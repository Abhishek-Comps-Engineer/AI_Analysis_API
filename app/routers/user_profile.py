import os
import uuid
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile, Depends,status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models import UserProfile
from app.schemas import UserProfileOutSchema, UserProfileSchema
from app.database import get_db

router = APIRouter(prefix="/user",tags=["UserProfile"])


PROFILES_DIR = "profiles"
os.makedirs(PROFILES_DIR, exist_ok=True)

@router.post("/",response_model=UserProfileSchema)
async def addUser(
    background_tasks: BackgroundTasks,
    email: EmailStr = Form(...),
    image: UploadFile = File(...),
    db :Session = Depends(get_db)):
   
   image_path = None

   if image:
      if not image.content_type.startswith("image/"):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail="Upload valid image File")
   
      _, ext = os.path.splitext(image.filename)
      unique_filename = f"{uuid.uuid4().hex}{ext}"
      image_path = os.path.join(PROFILES_DIR,unique_filename)

      contents = await image.read()

      background_tasks.add_task(save_image,contents,image_path)


   db_user = UserProfile(email=email, profileImage_url=image_path)
   db.add(db_user)
   db.commit()
   db.refresh(db_user)

   return db_user


@router.get("/", response_model=UserProfileOutSchema)
def get_image_path(email: str, db: Session = Depends(get_db)):
    print(email)
    user = db.query(UserProfile).filter(UserProfile.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def save_image(contents: bytes, path: str):
    with open(path, "wb") as buffer:
        buffer.write(contents)
