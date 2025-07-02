from sqlalchemy import Column, Integer, LargeBinary, String, Text, DateTime, ForeignKey
from  sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Role(Base):
    __tablename__ = "roles"

    id_role = Column(Integer, primary_key = True, index = True)
    nom_role = Column(String)

    users = relationship("User", back_populates = "role")

class OffreEmploi(Base):
    __tablename__ = "offres_emploi"

    id_offre = Column(Integer, primary_key = True, index = True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    titre = Column(String)
    id_entreprise = Column(Integer ,ForeignKey("entreprises.id_entreprise"))
    teletravail = Column(String)
    id_ville = Column(Integer ,ForeignKey("villes.id_ville"))
    id_secteur_activite = Column(Integer ,ForeignKey("secteurs_activite.id_secteur_activite"))
    id_fonction = Column(Integer ,ForeignKey("fonctions.id_fonction"))
    diplome_requis = Column(String)
    niveau_etude_requis = Column(String)
    type_offre = Column(String)
    annee_experience_min = Column(Integer)
    annee_experience_max = Column(Integer)
    nbr_employes_demande = Column(Integer)
    salaire_min  = Column(Integer)
    salaire_max = Column(Integer)
    description = Column(Text)
    nbr_de_candidats = Column(Integer, default = 0 )
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime)

    user = relationship("User", back_populates = "offres_emploi")
    entreprise = relationship("Entreprise", back_populates = "offre")
    ville = relationship("Ville", back_populates = "offres_emploi")
    secteur_activite = relationship("SecteurActivite", back_populates = "offres_emploi")
    fonction = relationship("Fonction", back_populates = "offres_emploi")
    competences = relationship("CompetencesOffre", back_populates = "offre")
    candidatures = relationship("Candidature", back_populates = "offre")

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True)
    email = Column(String, unique = True)
    password = Column(String)
    id_role = Column(Integer, ForeignKey("roles.id_role"))
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime)

    role = relationship("Role", back_populates = "users")
    offres_emploi = relationship("OffreEmploi", back_populates = "user")

class Competence(Base):
    __tablename__ = "competences"
    
    id_competence = Column(Integer, primary_key = True, index = True)
    nom_competence = Column(String)

    offres = relationship("CompetencesOffre", back_populates = "competence")

class CompetencesOffre(Base): 
    __tablename__ = "competence_offre"

    id_competence_offre = Column(Integer, primary_key = True, index = True)
    id_offre = Column(Integer, ForeignKey("offres_emploi.id_offre"), )
    id_competence = Column(Integer, ForeignKey("competences.id_competence"))
    niveau = Column(String)

    offre = relationship("OffreEmploi", back_populates = "competences")
    competence = relationship("Competence", back_populates = "offres")

class Fonction(Base):
    __tablename__ = "fonctions"

    id_fonction = Column(Integer, primary_key = True, index = True)
    nom_fonction = Column(String)

    offres_emploi = relationship("OffreEmploi", back_populates = "fonction")

class SecteurActivite(Base):
    __tablename__ = "secteurs_activite"

    id_secteur_activite = Column(Integer, primary_key = True, index = True)
    nom_secteur = Column(String)

    offres_emploi = relationship("OffreEmploi", back_populates = "secteur_activite")

class Ville(Base):
    __tablename__ = "villes"

    id_ville = Column(Integer, primary_key = True, index = True)
    nom_ville = Column(String)

    offres_emploi = relationship("OffreEmploi", back_populates = "ville")
    entreprises = relationship("Entreprise", back_populates = "ville")

class Candidature(Base):
    __tablename__ = "candidatures"

    id_candidature = Column(Integer, primary_key = True, index = True)
    id_offre = Column(Integer, ForeignKey("offres_emploi.id_offre"))
    nom = Column(String)
    prenom = Column(String)
    email = Column(String)
    numero_tel = Column(String)
    cv_id = Column(Integer, ForeignKey(("files.id_file")))
    date_postulation = Column(DateTime, default = datetime.now)

    offre = relationship("OffreEmploi", back_populates = "candidatures")
    cv = relationship("File", back_populates = "candidature")

class File(Base):
    __tablename__ = "files"

    id_file =Column(Integer, primary_key = True, index = True)
    file_path = Column(String)
    file_name = Column(String)
    file_type = Column(String)
    file = Column(LargeBinary)

    candidature = relationship("Candidature", back_populates = "cv")
    entreprise = relationship("Entreprise", back_populates = "logo") 

class Entreprise(Base):
    __tablename__ = "entreprises"

    id_entreprise =Column(Integer, primary_key = True)
    nom_entreprise = Column(String)
    logo_id = Column(Integer, ForeignKey(("files.id_file")))
    ville_id = Column(Integer, ForeignKey(("villes.id_ville")))
    adresse = Column(String)

    offre = relationship("OffreEmploi", back_populates = "entreprise") 
    logo = relationship("File", back_populates = "entreprise")
    ville = relationship("Ville", back_populates = "entreprises")