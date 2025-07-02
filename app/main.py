from database import engine, Base, get_db
import models
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/offres")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.OffreEmploi).all()

@app.get("/offre")
def get_by_search(db: Session = Depends(get_db), id_secteur_activite: Optional[int] = None, id_fonction: Optional[int] = None, id_ville: Optional[int] = None, min_exprerience: Optional[int] = None, type_offre: Optional[str] = None ):
    offres = []
    if id_secteur_activite:
        offres.extend(db.quey(models.OffreEmploi).filter(models.OffreEmploi.id_secteur_activite == id_secteur_activite))
    if id_fonction:
        offres.extend(db.query(models.OffreEmploi).filter(models.OffreEmploi.id_fonction == id_fonction))
    if id_ville: 
        offres.extend(db.query(models.OffreEmploi).filter(models.OffreEmploi.id_ville == id_ville))
    if min_exprerience:
        offres.extend(db.query(models.OffreEmploi).filter(models.OffreEmploi.annee_experience_min == min_exprerience))
    if type_offre:
        offres.extend(db.query(models.OffreEmploi).filter(models.OffreEmploi.type_offre == type_offre))

@app.post("/offre")
def post_offre(db: Session = Depends(get_db)):
    pass

@app.get("/offre/{id}")
def get_by_id(id:int, db: Session = Depends(get_db)):
    offre = db.query(models.OffreEmploi).get(id)
    if not offre:
        raise HTTPException(status_code = 404, detail = "offre_non_trouvé")
    return offre


@app.get("/refresh_database")
def refresh(db:Session = Depends(get_db)):
    db.query(models.Candidature).delete()
    db.query(models.CompetencesOffre).delete()
    
    db.query(models.OffreEmploi).delete()
    db.query(models.User).delete()
    db.query(models.Entreprise).delete()
    db.query(models.Ville).delete()
    db.query(models.Fonction).delete()
    db.query(models.SecteurActivite).delete()
    db.query(models.File).delete()

    db.query(models.Role).delete()
    db.query(models.Competence).delete()
    
    db.commit()
    return {"message": "Toutes les données ont été supprimées."}