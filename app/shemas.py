from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoleIn(BaseModel):
    nom_role: Optional[str]

class UserIn(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    id_role: Optional[int]
    
class UserOut(BaseModel):
    username: Optional[str]
    
    class Config:
        from_attributes = True

class VilleOut(BaseModel):
    nom_ville: Optional[str]
    
    class Config:
        from_attributes = True

class SecteurActiviteOut(BaseModel):
    nom_secteur: Optional[str]
    
    class Config:
        from_attributes = True

class FonctionOut(BaseModel):
    nom_fonction: Optional[str]
    
    class Config:
        from_attributes = True

class FileOut(BaseModel):
    file_path: Optional[str]
    file_name: Optional[str]
    file_type: Optional[str]

    class Config:
        from_attributes = True

class EntrepriseOut(BaseModel):
    nom_entreprise: Optional[str]
    adresse: Optional[str]
    logo: Optional[FileOut]
    ville: Optional[VilleOut]

    class Config:
        from_attributes = True

class CompetencesOut(BaseModel):
    nom_competence: Optional[str]
    niveau: Optional[str]

    class Config:
        from_attributes = True

class OffreOut(BaseModel):
    titre: Optional[str]
    teletravail: Optional[str]
    diplome_requis: Optional[str]
    niveau_etude_requis: Optional[str]
    type_offre: Optional[str]
    annee_experience_min: Optional[int]
    annee_experience_max: Optional[int]
    nbr_employes_demande: Optional[int]
    salaire_min: Optional[int]
    salaire_max: Optional[int]
    description: Optional[str]
    nbr_de_candidats: Optional[int]
    created_at: Optional[datetime]
    user: Optional[UserOut]
    entreprise: Optional[EntrepriseOut]
    ville: Optional[VilleOut]
    secteur_activite: Optional[SecteurActiviteOut]
    fonction: Optional[FonctionOut]
    competences: Optional[list[CompetencesOut]]

    class Config:
        from_attributes = True

class CompetencesIn(BaseModel):
    nom_competence: Optional[str]
    niveau_competence: Optional[str]

class OffreIn(BaseModel):
    id_fichier: Optional[int] 
    nom_entreprise: Optional[str] 
    adresse: Optional[str] 
    ville_id_entreprise: Optional[int] 
    id_user: Optional[int] 
    titre: Optional[str] 
    teletravail: Optional[str] 
    diplome_requis: Optional[str] 
    niveau_etude_requis: Optional[str] 
    type_offre: Optional[str] 
    annee_experience_min: Optional[int] 
    annee_experience_max: Optional[int] 
    nbr_employes_demande: Optional[int]
    salaire_min: Optional[int]
    salaire_max: Optional[int]
    id_secteur_activite: Optional[int]
    id_fonction: Optional[int]
    description: Optional[str]
    id_ville_offre: Optional[int]
    competences: Optional[list[CompetencesIn]]


class CompetencesUpdate(BaseModel):
    nom_competence: Optional[str] = None
    niveau_competence: Optional[str] = None

class imageUpdate(BaseModel):
    logo_id: int

class EntrepriseUpdate(BaseModel):
    nom_entreprise: Optional[str] = None
    adresse: Optional[str] = None
    id_ville: Optional[int] = None

class OffreUpdate(BaseModel):
    id_user: Optional[int] = None
    titre: Optional[str] = None
    teletravail: Optional[str] = None
    diplome_requis: Optional[str] = None
    niveau_etude_requis: Optional[str] = None
    type_offre: Optional[str] = None
    annee_experience_min: Optional[int] = None
    annee_experience_max: Optional[int] = None
    nbr_employes_demande: Optional[int] = None
    salaire_min: Optional[int] = None
    salaire_max: Optional[int] = None
    id_secteur_activite: Optional[int] = None
    id_fonction: Optional[int] = None
    description: Optional[str] = None
    id_ville: Optional[int] = None
    entreprise: Optional[EntrepriseUpdate] = None
    competences: Optional[list[CompetencesUpdate]] = None