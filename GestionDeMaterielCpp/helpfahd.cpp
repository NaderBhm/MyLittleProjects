#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <string>
#include <algorithm>

using namespace std;

struct Membre{
        string nom;
        string prenom;
        int id;
        bool operator<(const Membre& other) const {
        return id < other.id;
        }
};

vector<Membre> tabMem;
map<int,pair <int,int>> tabComp;
set<Membre> listeAllocation;

bool searchById(int id){
    for(Membre someone:tabMem){
        if(someone.id==id)
            return true;
    }
    return false;
}

Membre createMember(){
    Membre newMember;
    bool memberExist=false;
    do{
        cout << "Donner le nom du nouveau membre: " ;
        getline(cin,newMember.nom);
        getline(cin,newMember.nom);
        cout << "Donner le prenom du nouveau membre: " ;
        getline(cin,newMember.prenom);
        cout << "Donner l'id du nouveau membre: " ;
        cin >> newMember.id;
        memberExist=searchById(newMember.id);
        if(memberExist){
            cout << "membre existe deja";
        }
    }while(memberExist);
    return newMember;

}

void addManyMembers(int n){
    for(int i=0;i<n;i++){
        tabMem.push_back(createMember());
    }
    cout << "Members added successfully";
}

void removeLastMmember(){
    if (!tabMem.empty()) {
        tabMem.pop_back();
        cout << "Last member removed successfully";
    } else {
        cout << "No members to remove";
    }    
}

void removeMemberById(int id){
    auto iter= tabMem.begin();
    for(iter;iter != tabMem.end();iter++){
        if (iter->id == id) {
            tabMem.erase(iter);
            cout << "Member removed successfully";
            return;
        }
    }
    cout << "Member non existent";
}

void displayMemberById(int id){
    auto iter= tabMem.begin();
    for(iter;iter != tabMem.end();iter++){
        if ((*iter).id==id){
            cout << "Nom de member: " << (*iter).nom << endl;
            cout << "Prenom de member: " << (*iter).prenom << endl;
            return;
        }
    }
    cout << "Member non existent";
}

void displayMemberByFirstName(string prenom){
    auto iter= tabMem.begin();
    bool thereIsnt=true;
    for(iter;iter != tabMem.end();iter++){
        if ((*iter).prenom==prenom){
            cout << "Nom de member: " << (*iter).nom << endl;
            cout << "Prenom de member: " << (*iter).prenom << endl;
            cout << "Id de member: " << (*iter).id << endl;
            thereIsnt=false;

        }
    }
    if(thereIsnt)
        cout << "Member non existent";
}

void addComposantFirstTime(int id,int total){
    tabComp[id].first=total;
    tabComp[id].second=0;
    cout << "Component added successfully";
}

void addComposant(int id,int quantity){
    tabComp[id].first+=quantity;
    cout << "Component added successfully";
}

bool composantIsAvailable(int id){
    return tabComp.count(id);
}
bool isMemberAllocated(int id){
    for(Membre someone:listeAllocation){
        if(someone.id==id)
            return true;
    }
    return false;
}
void allocateComposant(int idM,int idC){
    if(tabComp.count(idC)==0)
        cout << "component not available";
    else
        if(tabComp[idC].first==tabComp[idC].second)
            cout << "component out of stock";
        else
            if(searchById(idM)==false)
                cout << "id inexistant";
            else
                if(isMemberAllocated(idM))
                    cout << "membre  a alloue deja";
                else{
                    tabComp[idC].second++;
                    auto iter= tabMem.begin();
                    for(iter;iter != tabMem.end();iter++){
                        if ((*iter).id==idM)
                           listeAllocation.insert(*iter);
                    }
                    cout << "allocation added successfully";
                }
}

void displayAllocatedMembers(){
    cout << "Liste des membres avec composants alloues:" << endl;
    for(Membre someone:listeAllocation){
            cout << "Nom de member: " << someone.nom << endl;
            cout << "Prenom de member: " << someone.prenom << endl;
            cout << "Id de member: " << someone.id << endl;

    }
}

void displayMenu() {
    cout << endl;
    cout << "----- Gestion des membres --------------------" << endl;
    cout << "1- Ajouter des membre" << endl;
    cout << "2- supprimer le dernier membre" << endl;
    cout << "3- supprimer un membre par son id" << endl;
    cout << "4- afficher les information d'un membre" << endl;
    cout << "5- rechercher un membre par son id" << endl;
    cout << "6- rechercher un membre par son prenom" << endl;
    cout << "----- Gestion des composants --------------------" << endl;
    cout << "7- Ajouter un nouveau composant" << endl;
    cout << "8- Ajouter au composant existant" << endl;
    cout << "9- Verifier la disponibilite d'un composant" << endl;
    cout << "----- Gestion des allocations --------------------" << endl;
    cout << "10- Allouer un composant" << endl;
    cout << "11- Verifier si un membre a deja alloue un composant" << endl;
    cout << "12- Afficher les membres avec composants alloues" << endl;
    cout << "----- -1 pour quitter -----" << endl;
}

void handleMemberManagement(int choix) {
    int n, id;
    string prenom;
    switch(choix) {
        case 1:
            cout << "Donner le nombre des membres a ajouter: ";
            cin >> n;
            addManyMembers(n);
            break;
        case 2:
            removeLastMmember();
            break;
        case 3:
            cout << "Donner l'id de nombre a supprimer: ";
            cin >> id;
            removeMemberById(id);
            break;
        case 4:
            cout << "Donner l'id de nombre a afficher: ";
            cin >> id;
            displayMemberById(id);
            break;
        case 5:
            cout << "Donner l'id de nombre a rechercher: ";
            cin >> id;
            if(searchById(id))
                cout << "membre " << id << " existe";
            else
                cout << "membre inexistant";
            break;
        case 6:
            cout << "Donner le prenom de nombre a rechercher: ";
            cin.ignore();
            getline(cin, prenom);
            displayMemberByFirstName(prenom);
            break;
        default:
            cout << "wrong number! pick again";
    }
}

void handleComponentManagement(int choix) {
    int id, total, add;
    switch(choix) {
        case 7:
            cout << "Donner l'id de nouveau composant: ";
            cin >> id;
            cout << "Donner le quantite de composant: ";
            cin >> total;
            if(composantIsAvailable(id))
                cout << "component already available";
            else
                addComposantFirstTime(id, total);
            break;
        case 8:
            cout << "Donner l'id de composant: ";
            cin >> id;
            cout << "Donner le quantite a ajouter: ";
            cin >> add;
            if(!composantIsAvailable(id))
                cout << "component not available";
            else
                addComposant(id, add);
            break;
        case 9:
            cout << "Donner l'id de composant: ";
            cin >> id;
            if(!composantIsAvailable(id))
                cout << "component not available";
            else
                cout << tabComp[id].first - tabComp[id].second << " available";
            break;
        default:
            cout << "wrong number! pick again";
    }
}

void handleAllocationManagement(int choix) {
    int idM, idC;
    switch(choix) {
        case 10:
            cout << "Donner l'id de membre: ";
            cin >> idM;
            cout << "Donner l'id de composant: ";
            cin >> idC;
            allocateComposant(idM, idC);
            break;
        case 11:
            cout << "Donner l'id de membre: ";
            cin >> idM;
            if(isMemberAllocated(idM))
                cout << "Membre a deja alloue";
            else
                cout << "Membre n'a pas allouer";
            break;
        case 12:
            displayAllocatedMembers();
            break;
        default:
            cout << "wrong number! pick again";
    }
}

int main() {
    cout << "Bonjour Fehd Fehri au application de gestion des materiels" << endl;
    int choix;
    do {
        displayMenu();
        cin >> choix;
        if (choix >= 1 && choix <= 6) {
            handleMemberManagement(choix);
        } else if (choix >= 7 && choix <= 9) {
            handleComponentManagement(choix);
        } else if (choix >= 10 && choix <= 12) {
            handleAllocationManagement(choix);
        } else if (choix == -1) {
            cout << "Au revoir, Fehd Fehri <3";
            break;
        } else {
            cout << "wrong number! pick again";
        }
    } while (true);
    return 0;
}




