import io
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import EmailStr
from app.core.helper import AppHelper
from app.core.security import get_current_admin, get_current_user
from app.features.cards.dependencies import get_cards_service
from app.features.cards.services import CardService
from app.features.cards.schemas import CardSchema, CreateCardSchema, UpdateCardSchema
from app.features.users.models import UserModel
from app.core.config import settings

router = APIRouter(prefix="/card", tags=["cards"])

@router.get("/all", response_model=list[CardSchema])
async def get_all_cards(
  service: CardService = Depends(get_cards_service), 
  # admin: UserModel = Depends(get_current_admin)
):
  return await service.get_all()

@router.get("/{id}", response_model=CardSchema)
async def get_card_by_id(id: uuid.UUID, service: CardService = Depends(get_cards_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_by_id(id)

@router.post("/", response_model=CardSchema)
async def create_card(
  image: UploadFile = File(..., description="Profile image"),
  first_name: str = Form(..., max_length=50, min_length=3, description="Card first name"),
  last_name: str = Form(..., max_length=50, min_length=3, description="Card last name"),
  contact: str = Form(..., max_length=50, min_length=3, description="Card contact"),
  status: str = Form("Member", max_length=50, min_length=3, description="Card status"),
  department_id: uuid.UUID = Form(...),
  municipality_id: uuid.UUID = Form(...),
  email: EmailStr = Form(...) , 
  service: CardService = Depends(get_cards_service),
  current_user: UserModel = Depends(get_current_user)
):
  image_url = AppHelper.save_file(image, settings.PROFILE_IMAGE_DIR, image.filename)
  is_admin = current_user.is_admin
  return await service.create(CreateCardSchema(
    first_name=first_name,
    last_name=last_name,
    contact=contact,
    status=status,
    department_id=department_id,
    municipality_id=municipality_id,
    email=email,
    is_active=True if is_admin else False,
  ), image_url=image_url, creator_id=current_user.id)

@router.get("/pdf/{card_id}", response_class=StreamingResponse)
async def get_card_pdf_endpoint(
    card_id: uuid.UUID,
    current_admin: UserModel = Depends(get_current_admin),
    service: CardService = Depends(get_cards_service)
):
    try:
        pdf_bytes = await service.generate_card_pdf_bytes(card_id)
        if not pdf_bytes:
            raise HTTPException(status_code=404, detail="Carte PDF introuvable.")
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=carte_membre_{card_id}.pdf"
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.post("/send-email/{card_id}", status_code=status.HTTP_200_OK)
async def send_card_email_endpoint(
    card_id: uuid.UUID,
    recipient_email: Optional[str] = None,
    current_admin: UserModel = Depends(get_current_admin),
    service: CardService = Depends(get_cards_service)
):
    try:
        await service.send_card_by_email(card_id, recipient_email)
        return {"message": "Membership card email sent successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in send_card_email_endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Could not send card email: {str(e)}")

@router.get("/{card_id}", response_model=CardSchema)
async def get_card_by_id_endpoint(card_id: uuid.UUID, service: CardService = Depends(get_cards_service)):
    return await service.get_by_id(card_id)


@router.put("/", response_model=CardSchema)
async def update_cards(
  id: uuid.UUID = Form(...),
  image: Optional[UploadFile] = File(None),
  first_name: Optional[str] = Form(None),
  last_name: Optional[str] = Form(None),
  email: Optional[str] = Form(None),
  contact: Optional[str] = Form(None),
  status: Optional[str] = Form(None),
  department_id: Optional[uuid.UUID] = Form(None),
  municipality_id: Optional[uuid.UUID] = Form(None),
  service: CardService = Depends(get_cards_service),
  admin: UserModel = Depends(get_current_admin)
):
  image_url = None
  if image: 
    image_url = AppHelper.save_file(image, settings.PROFILE_IMAGE_DIR, image.filename)
  return await service.update(schema=UpdateCardSchema(
    id=id,
    first_name=first_name,
    last_name=last_name,
    email=email,
    contact=contact,
    status=status,
    department_id=department_id,
    municipality_id=municipality_id,
    is_active=True,
  ), image_url=image_url)

@router.delete("/{id}")
async def delete_cards(id: uuid.UUID, service: CardService = Depends(get_cards_service), admin: UserModel = Depends(get_current_admin)):
  return await service.delete(id)

