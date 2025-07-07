from database import engine, Base, get_db
import models
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.responses import FileResponse
import shemas
import random
import string
import os
from pathlib import Path

Base.metadata.create_all(engine)

UPLOAD_PATH = Path(__file__).resolve().parent.parent / "uploads"
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

@app.post("/offres", status_code = 201)
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

@app.post("/upload", status_code = 201)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content_type = file.content_type
    if content_type not in ALLOWED_IMAGE_TYPES.union(ALLOWED_DOC_TYPES):
        raise HTTPException(status_code=400, detail="Type de fichier non supporté")
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 5 Mo)")
    extension = Path(file.filename).suffix.lower()
    if content_type in ALLOWED_DOC_TYPES:
        upload_folder = UPLOAD_PATH / "cv"
    else:
        upload_folder = UPLOAD_PATH / "images"
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

@app.patch("/update-image/{id_entreprise}")
def update_image(id_entreprise: int, image: shemas.imageUpdate,  db: Session = Depends(get_db)):
    e = db.query(models.Entreprise).get(id_entreprise)
    if not e: 
        raise HTTPException(status_code = 404, detail = "entreprise_inexistant")
    
    for k, v in image.model_dump(exclude_defaults = True).items():
        setattr(e, k, v)
    return {"message": "success"}

@app.patch("/update/{id_offre}")
def update(id_offre: int, offre: shemas.OffreUpdate, db: Session = Depends(get_db)):
    offre_db = db.query(models.OffreEmploi).get(id_offre)
    if not offre_db: 
        raise HTTPException(status_code=404, detail="offre_inexistant")
    update_data = offre.model_dump(exclude_defaults=True)
    for k, v in update_data.items():
        if k not in ("entreprise", "competences"):
            setattr(offre_db, k, v)
    if "entreprise" in update_data and update_data["entreprise"]:
        e = offre_db.entreprise
        for k, v in update_data["entreprise"].items():
            setattr(e, k, v)
    if "competences" in update_data and update_data["competences"]:
        db.query(models.Competence).filter(models.Competence.id_offre == id_offre).delete()
        for competence in update_data["competences"]:
            c = models.Competence(
                nom_competence=competence.nom_competence,
                niveau=competence.niveau_competence,
                id_offre=id_offre
            )
            db.add(c)
    db.commit()
    db.refresh(offre_db)
    return offre_db

@app.delete("offre/{id_offre}")
def delete_offre(id_offre: int, db: Session = Depends(get_db)):
    offre = db.query(models.OffreEmploi).get(id_offre)
    if not offre: 
        raise HTTPException(status_code = 404, detail = "offre_inexistant")
    candidatures = db.query(models.Candidature).filter(models.Candidature.id_offre == offre.id_offre)
    competences = db.query(models.Competence).filter(models.Competence.id_offre == offre.id_offre)
    for competence in competences:
        db.delete(competence)
    for candidature in candidatures:
        db.delete(candidature)
    db.delete(offre)
    db.commit()
    return {"message": "offre supprimé"}

@app.delete("/file/{id_file}")
def delete_file_by_id(id_file: int, db: Session = Depends(get_db)):
    file = db.query(models.File).get(id_file)
    if not file:
        raise HTTPException(status_code = 404, detail = "fichier_inexistant")
    
    Path(file.file_path).unlink()
    db.delete(file)
    db.commit()
    return {"message": "fichier_supprimé"}

@app.post("/user", status_code = 201)
def inscription(user: shemas.UserIn, db: Session = Depends(get_db)):
    u = models.User(username = user.username, email = user.email, password = user.password, id_role = user.id_role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"message": "user_crée"}

@app.post("/role", status_code = 201)
def inscription(role: shemas.RoleIn, db: Session = Depends(get_db)):
    r = models.Role(nom_role = role.nom_role)
    db.add(r)
    db.commit()
    db.refresh(r)
    return {"message": "role_crée"}

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
    dir1 = UPLOAD_PATH / "images"
    dir2 = UPLOAD_PATH / "cv"
    for file in os.listdir(dir1):
        os.remove(dir1 / file)
    for file in os.listdir(dir2):
        os.remove(dir2 / file)
    return {"message": "Toutes les données ont été supprimées."}