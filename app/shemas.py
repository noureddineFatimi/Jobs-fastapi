from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    username: str
    
    class Config:
        from_attributes = True

class VilleOut(BaseModel):
    nom_ville: str
    
    class Config:
        from_attributes = True

class SecteurActiviteOut(BaseModel):
    nom_secteur: str
    
    class Config:
        from_attributes = True

class FonctionOut(BaseModel):
    nom_fonction: str
    
    class Config:
        from_attributes = True

class FileOut(BaseModel):
    file_path: str
    file_name: str
    file_type: str

    class Config:
        from_attributes = True

class EntrepriseOut(BaseModel):
    nom_entreprise: str
    adresse: str
    logo: Optional[FileOut]
    ville: Optional[VilleOut]

    class Config:
        from_attributes = True

class CompetencesOut(BaseModel):
    nom_competence: str
    niveau_competence: str

    class Config:
        from_attributes = True

class OffreOut(BaseModel):
    titre: str
    teletravail: str
    diplome_requis: str
    niveau_etude_requis: str
    type_offre: str
    annee_experience_min: int
    annee_experience_max: int
    nbr_employes_demande: int
    salaire_min: int
    salaire_max: int
    description: int
    nbr_candidats: int
    created_at: datetime
    user: Optional[UserOut]
    entreprise: Optional[EntrepriseOut]
    ville: Optional[VilleOut]
    secteur_actvite: Optional[SecteurActiviteOut]
    fonction: Optional[FonctionOut]
    competences: Optional[list[CompetencesOut]]

    class Config:
        from_attributes = True

class CompetencesIn(BaseModel):
    nom_competence: str
    niveau_competence: str

class OffreIn(BaseModel):
    id_fichier:int
    nom_entreprise: int
    adresse: int
    ville_id_entreprise: int
    id_user: int
    titre: str
    teletravail: str
    diplome_requis: str
    niveau_etude_requis: str
    type_offre: str
    annee_experience_min: int
    annee_experience_max: int
    nbr_employes_demande: int
    salaire_min: int
    salaire_max: int
    id_secteur_activite: int
    id_fonction: int
    description: str
    nbr_de_candidats: int
    id_ville_offre: int
    competences: list[CompetencesIn]