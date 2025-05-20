# app/features/cards/services.py
from io import BytesIO
import os
import uuid
from typing import Optional, List

from fastapi import HTTPException, status
from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A8, landscape # A8 est une petite taille, comme une carte de crédit
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode

from app.core.config import settings
from app.core.email import send_email
from app.features.cards.models import CardModel
from app.features.cards.repository import CardRepository
from app.features.cards.schemas import CardSchema, CreateCardSchema, UpdateCardSchema


# Définir les dimensions de la carte (ex: format carte de crédit 85.6mm x 53.98mm)
CARD_WIDTH, CARD_HEIGHT = 85.6 * mm, 53.98 * mm


class CardService:
    def __init__(self, repository: CardRepository):
        self.repository = repository

    async def get_all(self) -> List[CardSchema]:
        res = await self.repository.get_all()
        return list(CardSchema.model_validate(card) for card in res)

    async def get_by_id(self, id: uuid.UUID) -> CardSchema:
        res = await self.repository.get_by_id(id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found"
            )
        return CardSchema.model_validate(res)

    async def create(self, schema: CreateCardSchema, image_url: str, creator_id: uuid.UUID) -> CardSchema:
        model_data = schema.model_dump()
        model = CardModel(**model_data)
        model.creator_id = creator_id 
        model.image_url = image_url
        created_card = await self.repository.create(model)
        qr_data_url = f"{settings.DOMAIN_URL}/cards/view/{created_card.id}"
        created_card.qr_code_url = qr_data_url
        updated_card_with_qr = await self.repository.update(created_card)
        return CardSchema.model_validate(updated_card_with_qr)


    async def update(self, card_id: uuid.UUID, schema: UpdateCardSchema, image_url: Optional[str]) -> CardSchema:
        db_card = await self.repository.get_by_id(card_id)
        if not db_card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found"
            )
        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(db_card, key, value)
        
        if image_url is not None:
            db_card.image_url = image_url

        updated_card = await self.repository.update(db_card)
        return CardSchema.model_validate(updated_card)

    async def delete(self, id: uuid.UUID) -> None:
        model = await self.repository.get_by_id(id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found"
            )
        await self.repository.delete(model)
        return None


    async def _generate_qr_code_image(self, data: str) -> ImageReader:
        """Génère une image QR Code à partir des données fournies."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10, # Taille de chaque "boîte" du QR code
            border=2,    # Épaisseur de la bordure
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_buffer = BytesIO()
        img.save(img_buffer, "PNG")
        img_buffer.seek(0)
        return ImageReader(img_buffer)

    async def _get_member_photo(self, image_url: str) -> ImageReader:
        try:
            base_url = settings.DOMAIN_URL
            file_path = image_url.replace(f"{base_url}/", "")
            return ImageReader(file_path)
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )

    async def generate_card_pdf_bytes(self, card_id: uuid.UUID) -> bytes:
        """Génère la carte de membre en PDF et retourne les bytes."""
        card_data_model = await self.repository.get_by_id_model(card_id)
        if not card_data_model:
            raise HTTPException(status_code=404, detail="Card not found")

        buffer = BytesIO()
        # Utiliser landscape(A8) ou vos dimensions personnalisées
        # p = canvas.Canvas(buffer, pagesize=landscape(A8))
        p = canvas.Canvas(buffer, pagesize=(CARD_WIDTH, CARD_HEIGHT))

        # 1. Fond d'écran
        try:
            if os.path.exists(settings.CARD_BACKGROUND_IMAGE_PATH):
                p.drawImage(settings.CARD_BACKGROUND_IMAGE_PATH, 0, 0, width=CARD_WIDTH, height=CARD_HEIGHT, preserveAspectRatio=True, anchor='c')
            else:
                print(f"Attention : Fond d'écran non trouvé à {settings.CARD_BACKGROUND_IMAGE_PATH}")
                p.setFillColorRGB(0.9, 0.9, 0.9) # Un fond gris clair par défaut
                p.rect(0,0, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)

        except Exception as e:
            print(f"Erreur lors du chargement du fond d'écran : {e}")
            p.setFillColorRGB(0.9, 0.9, 0.9)
            p.rect(0,0, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)


        # 2. Photo du membre (Ex: coin supérieur gauche)
        photo_size = 20 * mm # Taille de la photo
        photo_x = CARD_WIDTH - photo_size - (8 * mm)
        photo_y = CARD_HEIGHT - photo_size - (8 * mm)
        
        member_photo = await self._get_member_photo(card_data_model.image_url)
        if member_photo:
            try:
                p.drawImage(member_photo, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"Erreur lors du dessin de la photo du membre : {e}")
                p.setFillColorRGB(0.7, 0.7, 0.7)
                p.rect(photo_x, photo_y, photo_size, photo_size, fill=1) # Placeholder gris

        # 3. Informations textuelles
        p.setFillColorRGB(1, 1, 1) # Couleur du texte (noir)
        
        # Nom et Prénom
        text_start_x = (7*mm) # A droite de la photo
        current_y = CARD_HEIGHT - (15 * mm)
        p.setFont(settings.CARD_DEFAULT_FONT + "-Bold", 8) # Taille 10
        p.drawString(photo_x, current_y + (8 * mm), f"N°: {card_data_model.number:04d}")
        p.drawString(text_start_x, current_y, f"Nom: {card_data_model.first_name}")
        p.drawString(text_start_x, current_y - (5 * mm), f"Prénom: {card_data_model.last_name}")
        
        current_y -= (10 * mm)
        # Numéro de membre
        
        # Statut
        p.drawString(text_start_x, current_y, f"Statut: {card_data_model.status}")
        current_y -= (5 * mm)
        # Contact
        p.drawString(text_start_x, current_y, f"Contact: {card_data_model.contact}")
        current_y -= (5 * mm)
        # Département (Assurez-vous que department est chargé)
        department_name = card_data_model.department.name if card_data_model.department else "N/A"
        p.drawString(text_start_x, current_y, f"Département: {department_name}") # En bas à gauche
        current_y -= (5 * mm)
        # Municipalité (Assurez-vous que municipality est chargé)
        municipality_name = card_data_model.municipality.name if card_data_model.municipality else "N/A"
        p.drawString(text_start_x, current_y, f"Commune: {municipality_name}")


        # 4. QR Code (Ex: coin inférieur droit)
        qr_code_size = 15 * mm
        qr_x = CARD_WIDTH - qr_code_size - (7 * mm)
        qr_y = 4 * mm
        if card_data_model.qr_code_url: # L'URL des données du QR Code
            try:
                qr_image = await self._generate_qr_code_image(card_data_model.qr_code_url)
                p.drawImage(qr_image, qr_x, qr_y, width=qr_code_size, height=qr_code_size, preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"Erreur lors de la génération ou du dessin du QR code : {e}")
        
        p.showPage()
        p.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    async def send_card_by_email(self, card_id: uuid.UUID, recipient_email: Optional[str] = None) -> None:
        """Génère la carte PDF et l'envoie par e-mail."""
        card = await self.repository.get_by_id_model(card_id) # Utiliser get_by_id_model pour avoir l'objet modèle
        if not card:
            raise HTTPException(status_code=404, detail="Card not found for emailing.")

        pdf_bytes = await self.generate_card_pdf_bytes(card_id)
        
        to_email = recipient_email if recipient_email else card.email
        if not to_email:
            raise HTTPException(status_code=400, detail="No recipient email address found for the card.")

        subject = f"Votre carte de membre - {card.first_name} {card.last_name}"
        
        # Formatter le numéro de carte avec des zéros en tête (par exemple, pour avoir 6 chiffres)
        formatted_card_number = f"{card.number:06d}"

        body = (
            f"Bonjour {card.first_name},\n\n"
            f"Veuillez trouver ci-joint votre carte de membre (Numéro: {formatted_card_number}).\n\n"
            f"Cordialement,\n"
            f"L'équipe de {settings.APP_NAME}"
        )
        html_body = (
            f"<p>Bonjour {card.first_name},</p>"
            f"<p>Veuillez trouver ci-joint votre carte de membre (Numéro: <strong>{formatted_card_number}</strong>).</p>"
            f"<p>Cordialement,<br>"
            f"L'équipe de {settings.APP_NAME}</p>"
        )
        
        attachments = [
            (f"carte_membre_{card.last_name}_{card.first_name}.pdf", pdf_bytes, "application/pdf")
        ]
        
        try:
            await send_email(
                to=to_email,
                subject=subject,
                body=body,
                html_body=html_body,
                attachments=attachments
            )
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail à {to_email}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")