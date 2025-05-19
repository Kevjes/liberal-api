from io import BytesIO
import io
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import EmailStr
from app.core.helper import AppHelper
from app.core.security import get_current_admin, get_current_user
from app.features.cards.dependencies import get_cards_service
from app.features.cards.services import CardService
from app.features.cards.schemas import CardSchema, CreateCardSchema
from app.features.users.models import UserModel
from app.core.config import settings

router = APIRouter(prefix="/card", tags=["cards"])

@router.get("/all", response_model=list[CardSchema])
async def get_all_cards(service: CardService = Depends(get_cards_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_all()

@router.get("/{id}", response_model=CardSchema)
async def get_card_by_id(id: uuid.UUID, service: CardService = Depends(get_cards_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_by_id(id)

@router.post("/", response_model=CardSchema)
async def create_card(
  image: UploadFile = Form(..., description="Profile image"),
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
  return await service.create(CreateCardSchema(
    first_name=first_name,
    last_name=last_name,
    contact=contact,
    status=status,
    department_id=department_id,
    municipality_id=municipality_id,
    email=email,
  ), image_url=image_url, creator_id=current_user.id)

@router.get("/{card_id}/pdf", response_class=StreamingResponse)
async def get_card_pdf_endpoint(
    card_id: uuid.UUID,
    service: CardService = Depends(get_cards_service)
):
    try:
        pdf_bytes = await service.generate_card_pdf_bytes(card_id)
        return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=carte_membre_{card_id}.pdf"})
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log l'erreur e
        raise HTTPException(status_code=500, detail="Could not generate PDF card.")


@router.post("/{card_id}/send-email", status_code=status.HTTP_200_OK)
async def send_card_email_endpoint(
    card_id: uuid.UUID,
    recipient_email: Optional[str] = None, # Permet de spécifier un e-mail différent
    service: CardService = Depends(get_cards_service)
):
    try:
        await service.send_card_by_email(card_id, recipient_email)
        return {"message": "Membership card email sent successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log l'erreur e
        print(f"Error in send_card_email_endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Could not send card email: {str(e)}")

# ... vos autres routes (GET, PUT, DELETE)
@router.get("/", response_model=List[CardSchema])
async def get_all_cards_endpoint(service: CardService = Depends(get_cards_service)):
    return await service.get_all()

@router.get("/{card_id}", response_model=CardSchema)
async def get_card_by_id_endpoint(card_id: uuid.UUID, service: CardService = Depends(get_cards_service)):
    return await service.get_by_id(card_id)


# @router.put("/", response_model=CardSchema)
# async def update_cards(
#   schema: UpdateCardSchema,
#   service: CardService = Depends(get_cards_service),
#   admin: UserModel = Depends(get_current_admin)
# ):
#   return await service.update(schema)

@router.delete("/{id}")
async def delete_cards(id: uuid.UUID, service: CardService = Depends(get_cards_service), admin: UserModel = Depends(get_current_admin)):
  return await service.delete(id)

