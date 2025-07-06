from database import engine, Base, get_db
import models
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.responses import FileResponse
import shemas
import os
import random
import string
from pathlib import Path

Base.metadata.create_all(engine)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_DOC_TYPES = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
MAX_FILE_SIZE = 5 * 1024 * 1024 

app = FastAPI()

@app.get("/offres", response_model = list[shemas.OffreOut])
def get_by_search(db: Session = Depends(get_db), id_secteur_activite: Optional[int] = None, id_fonction: Optional[int] = None, id_ville: Optional[int] = None, min_exprerience: Optional[int] = None, type_offre: Optional[str] = None ):
    offres = db.query(models.OffreEmploi)
    if id_secteur_activite:
        offres = offres.filter(models.OffreEmploi.id_secteur_activite == id_secteur_activite)
    if id_fonction:
        offres = offres.filter(models.OffreEmploi.id_fonction == id_fonction)
    if id_ville: 
        offres = offres.filter(models.OffreEmploi.id_ville == id_ville)
    if min_exprerience:
        offres = offres.filter(models.OffreEmploi.annee_experience_min >= min_exprerience)
    if type_offre:
        offres = offres.filter(models.OffreEmploi.type_offre == type_offre)
    return offres.all()

@app.post("/offres")
def post_offre(offre: shemas.OffreIn, db: Session = Depends(get_db)):
    entreprise = models.Entreprise(nom_entreprise = offre.nom_entreprise, logo_id = offre.id_fichier, ville_id = offre.ville_id_entreprise, adresse = offre.adresse)
    db.add(entreprise)
    db.commit()
    db.refresh(entreprise)
    offre_enre = models.OffreEmploi(id_user = offre.id_user, titre = offre.titre, id_entreprise = entreprise.id_entreprise, teletravail = offre.teletravail, id_ville = offre.id_ville_offre, id_secteur_activite = offre.id_secteur_activite, id_fonction = offre.id_fonction, diplome_requis = offre.diplome_requis, niveau_etude_requis = offre.niveau_etude_requis, type_offre = offre.type_offre, annee_experience_min = offre.annee_experience_min, annee_experience_max = offre.annee_experience_max, nbr_employes_demande = offre.nbr_employes_demande, salaire_min = offre.salaire_min, salaire_max = offre.salaire_max, description = offre.description)
    db.add(offre_enre)
    db.commit()
    db.refresh(offre_enre)
    for competence in offre.competences:
        c = models.Competence(nom_competence = competence.nom_competence, niveau = competence.niveau_competence, id_offre = offre_enre.id_offre)
        db.add(c)
    db.commit()
    return {"message": "Offre insérée avec succès", "id_offre": offre_enre.id_offre}

@app.get("/offres/{id_user}", response_model = list[shemas.OffreOut])
def get_by_id(id_user:int, db: Session = Depends(get_db)):
    offres = db.query(models.OffreEmploi).filter(models.OffreEmploi.id_user == id_user)
    return offres

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content_type = file.content_type
    if content_type not in ALLOWED_IMAGE_TYPES.union(ALLOWED_DOC_TYPES):
        raise HTTPException(status_code=400, detail="Type de fichier non supporté")
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 5 Mo)")
    extension = Path(file.filename).suffix.lower()
    print(str(Path(__file__)))
    base_dir = Path(__file__).resolve().parent.parent 
    if content_type in ALLOWED_DOC_TYPES:
        upload_folder = base_dir / "uploads" / "cv"
    else:
        upload_folder = base_dir / "uploads" / "images"
    upload_folder.mkdir(parents=True, exist_ok=True)
    secure_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15)) + extension
    full_path = upload_folder / secure_name
    with open(full_path, "wb") as f:
        f.write(content)
    fichier = models.File(
        file_name=secure_name,
        file_type=content_type,
        file_path=str(full_path)
    )
    db.add(fichier)
    db.commit()
    db.refresh(fichier)
    return {"id_fichier": fichier.id_file}

@app.delete("offre/{id_offre}")
def delete_offre(id_offre: int, db: Session = Depends(get_db)):
    offre = db.query(models.OffreEmploi).get(id_offre)
    if not offre: 
        raise HTTPException(status_code = 404, detail = "offre_inexistant")
    db.delete(offre)
    db.commit()
    return {"message": "offre supprimé"}

@app.get("/file/{id_file}")
def get_file_by_id(id_file: int, db: Session = Depends(get_db)):
    file = db.query(models.File).get(id_file)
    if not file:
        raise HTTPException(status_code = 404, detail = "fichier_inexistant")
    return FileResponse(path = file.file_path, media_type = file.file_type, filename = file.file_name)

@app.get("/offre/{id_offre}", response_model = shemas.OffreOut)
def get_by_id(id_offre:int, db: Session = Depends(get_db)):
    offre = db.query(models.OffreEmploi).get(id_offre)
    if not offre:
        raise HTTPException(status_code = 404, detail = "offre_non_trouvé")
    return offre

@app.get("/refresh_database")
def refresh(db:Session = Depends(get_db)):
    db.query(models.Candidature).delete()
    db.query(models.Competence).delete()
    db.query(models.OffreEmploi).delete()
    db.query(models.User).delete()
    db.query(models.Entreprise).delete()
    db.query(models.Ville).delete()
    db.query(models.Fonction).delete()
    db.query(models.SecteurActivite).delete()
    db.query(models.File).delete()
    db.query(models.Role).delete()
    db.commit()
    return {"message": "Toutes les données ont été supprimées."}