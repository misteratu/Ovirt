import logging
import ovirtsdk4 as sdk
import ovirtsdk4.types as types

def create_connection(url, mdp):

    # Crée et retourne une instance de la connexion ovirtsdk4
    return sdk.Connection(
        url=url,
        username='admin@internal',
        password=mdp,
        debug=False,
        log=logging.getLogger()
    )

def find_user(connection, USERNAME):
    # Obtient le service des utilisateurs à partir de la connexion
    users_service = connection.system_service().users_service()

    # Recherche et retourne le premier utilisateur correspondant au nom d'utilisateur donné
    user = users_service.list(search='usrname=%s' % USERNAME)[0]
    return user

def add_permission_to_network(networks_service, network, user):
    # Demande à l'utilisateur d'entrer le nom de la nouvelle permission à attribuer
    ROLENAME = input("Entrez le nom de la nouvelle permission à attribuer (anglais) : ")

    # Obtient le service des permissions pour le réseau spécifié
    permissions_service = networks_service.network_service(network.id).permissions_service()

    # Ajoute une nouvelle permission en utilisant l'ID de l'utilisateur et le nom du rôle
    permissions_service.add(
        types.Permission(
            user=types.User(
                id=user.id,
            ),
            role=types.Role(
                name=ROLENAME
            ),
        ),
    )

def add_permission_to_virtual_machines(connection, user):
    # Demande à l'utilisateur d'entrer les noms des machines virtuelles sur lesquelles l'utilisateur doit avoir la permission
    VMPERM = input("Entrez le nom des machines virtuelles sur lesquelles l'utilisateur doit avoir la permission voulue :")

    # Divise les noms des machines virtuelles en une liste
    MY_VMS = VMPERM.split(',')

    # Demande à l'utilisateur d'entrer le nom de la nouvelle permission à attribuer
    ROLENAME = input("Entrez le nom de la nouvelle permission à attribuer (anglais) : ")

    # Obtient le service des machines virtuelles à partir de la connexion
    vms_service = connection.system_service().vms_service()

    # Parcourt les noms des machines virtuelles et ajoute une nouvelle permission pour chaque machine virtuelle
    for vm_name in MY_VMS:
        # Recherche la machine virtuelle correspondante au nom donné
        vm = vms_service.list(search='name=%s' % vm_name)[0]

        # Obtient le service des permissions pour la machine virtuelle spécifiée
        permissions_service = vms_service.vm_service(vm.id).permissions_service()

        # Ajoute une nouvelle permission en utilisant l'ID de l'utilisateur et le nom du rôle
        permissions_service.add(
            types.Permission(
                user=types.User(
                    id=user.id,
                ),
                role=types.Role(
                    name=ROLENAME,
                ),
            ),
        )

def display_networks(url, mdp):
    # Crée une nouvelle connexion à l'ovirt engine pour afficher les réseaux disponibles
    connection2 = sdk.Connection(
        url=url,
        username='admin@internal',
        password=mdp,
        debug=False,
        log=logging.getLogger(),
    )

    # Obtient le service des réseaux à partir de la connexion
    networks_service = connection2.system_service().networks_service()

    # Obtient la liste des réseaux disponibles
    networks = networks_service.list()

    # Parcourt les réseaux et affiche leur nom
    for network in networks:
        print(network.name)

    # Ferme la connexion à l'ovirt engine
    connection2.close()

def display_vm(connection):
    # Obtient le service des machines virtuelles à partir de la connexion
    vms_service = connection.system_service().vms_service()

    # Obtient la liste de toutes les machines virtuelles du système
    vms = vms_service.list()

    # Parcourt les machines virtuelles et affiche leur nom et identifiant
    for vm in vms:
        print("%s: %s" % (vm.name, vm.id))

def display_vm_ask(connection):
    # Demande à l'utilisateur s'il souhaite afficher les machines virtuelles disponibles
    display = input("Afficher les machines virtuelles disponibles ? [y/N]")

    if display == 'y' or display == 'Y':
        # Affiche les machines virtuelles disponibles
        display_vm(connection)

def main():
    print("-------------------------------------------------------------------")
    print("                           Début du script")
    print("-------------------------------------------------------------------")

    # Demande à l'utilisateur d'entrer l'URL de l'ovirt engine et le mot de passe de l'administrateur
    adresse = input("Entrez l'url de l'ovirt engine (https://VotreAdresse) : ")
    mdp = input("Entrez le mot de passe de l'administrateur : ")

    # Construit l'URL complète pour la connexion
    url = '%s/ovirt-engine/api' % adresse

    # Connecte à l'ovirt engine
    connection = create_connection(url, mdp)
    print("\033[92mConnection créée\033[0m")

    # Demande à l'utilisateur si la permission est pour une machine virtuelle ou un réseau
    ModeVM = input("La permission est pour une vm ? [Y/n] ")

    if ModeVM == 'n' or ModeVM == 'N':
        # Affiche les réseaux disponibles
        print("Affichage des réseaux disponibles")
        display_networks(url, mdp)

        # Demande à l'utilisateur de fournir le nom du réseau
        RESEAU = input("Entrez le nom du réseau : ")

        # Obtient le service des réseaux à partir de la connexion
        networks_service = connection.system_service().networks_service()

        # Recherche le réseau correspondant au nom donné
        network = networks_service.list(search='name=%s' % RESEAU)[0]

        print("\033[92mNetwork créé\033[0m")

        # Demande à l'utilisateur de fournir le nom de l'utilisateur pour la nouvelle permission
        USERNAME = input("Entrez le nom de l'utilisateur qui doit recevoir une nouvelle permission : ")

        # Recherche l'utilisateur correspondant au nom donné
        user = find_user(connection, USERNAME)
        print("\033[92mUser trouvé\033[0m")

        # Ajoute la permission au réseau pour l'utilisateur
        add_permission_to_network(networks_service, network, user)
        print("\033[92mPermission ajoutée à l'utilisateur\033[0m")

    else:
        # Demande à l'utilisateur s'il souhaite afficher les machines virtuelles disponibles
        display_vm_ask(connection)

        # Demande à l'utilisateur de fournir le nom de l'utilisateur pour la nouvelle permission
        USERNAME = input("Entrez le nom de l'utilisateur qui doit recevoir une nouvelle permission : ")

        # Recherche l'utilisateur correspondant au nom donné
        user = find_user(connection, USERNAME)

        print("\033[92mUser trouvé\033[0m")

        # Ajoute la permission aux machines virtuelles pour l'utilisateur
        add_permission_to_virtual_machines(connection, user)
        print("\033[92mPermissions ajoutées aux machines virtuelles\033[0m")

    # Ferme la connexion au serveur
    connection.close()
    print("\033[92mConnection fermée\033[0m")

    print("-------------------------------------------------------------------")
    print("                            Fin du script")
    print("-------------------------------------------------------------------")

main()

