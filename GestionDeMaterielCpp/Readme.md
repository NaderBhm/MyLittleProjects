# Application de Gestion de Matériel - CPU ISIMM  

## Description  
Ce projet est une application en C++ permettant de gérer les membres du club CPU ISIMM et l'inventaire des composants robotiques. Elle facilite l'organisation et la distribution du matériel pour le responsable technique.  

## Fonctionnalités  
### Gestion des Membres  
- **Ajout de membres** avec `addManyMembers(n)`.  
- **Suppression d'un membre** par ID avec `removeMemberById(id)`.  
- **Affichage des informations** d’un membre avec `displayMemberById(id)`.  
- **Recherche** par ID ou prénom.  

### Gestion des Composants  
- **Ajout d'un nouveau composant** avec `addComposantFirstTime(id, quantité)`.  
- **Ajout de stock** à un composant existant.  
- **Vérification de disponibilité** des composants.  

### Allocation des Composants  
- **Allocation d’un composant** à un membre.  
- **Vérification des allocations**.  
- **Affichage des membres ayant alloué un composant**.  

## Installation  
1. **Compiler le programme**  
   ```sh
   g++ -o gestion_materiel helpfahd.cpp
   ```
2. **Exécuter l'application**  
   ```sh
   ./gestion_materiel
   ```

## Utilisation  
L’application propose un **menu interactif** permettant d’ajouter, supprimer et gérer les membres et les composants de manière intuitive.  

## Auteur  
Développé par moi (Nader Ben Haj Messaoud) durant le workshop c++ du club CPU ISIMM
