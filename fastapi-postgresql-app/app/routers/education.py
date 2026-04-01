from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db import get_session
from app.models.user import User
from app.models.education import Education
from app.schemas.education import EducationCreate, EducationUpdate, EducationOut

router = APIRouter(prefix="/education", tags=["educations"])
bearer = HTTPBearer(auto_error=True)

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_session),
) -> User:
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(sub)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/create", response_model=EducationOut, status_code=201)
async def create_education(
    payload: EducationCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    edu = Education(
        degree=payload.degree,
        field=payload.field,
        institute=payload.institute,
        user_id=current_user.id,
    )
    db.add(edu)
    await db.commit()
    await db.refresh(edu)
    return edu

@router.get("/read", response_model=list[EducationOut])
async def read_my_educations(
    db: AsyncSession = Depends(get_session),
):
    res = await db.execute(select(Education).where())
    return list(res.scalars().all())

@router.put("/update/{education_id}", response_model=EducationOut)
async def update_my_education(
    education_id: int,
    payload: EducationUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(select(Education).where(Education.id == education_id))
    edu = res.scalar_one_or_none()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    if edu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this education")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(edu, k, v)

    await db.commit()
    await db.refresh(edu)
    return edu

@router.delete("/delete/{education_id}", status_code=204)
async def delete_my_education(
    education_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(select(Education).where(Education.id == education_id))
    edu = res.scalar_one_or_none()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    if edu.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this education")

    await db.delete(edu)
    await db.commit()
    return None
