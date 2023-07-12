# oVirt gestion des utilisateurs 

## Pour un LDAP
### Prérequis
Vérifier que dans ovirt, on a bien ce package d'installé.

```yum install ovirt-engine-extension-aaa-ldap-setup```
### Modification à apporter au code source python

On modifie les fichier dans le répertoire : /usr/share/ovirt-engine-extension-aaa-ldap/setup/plugins/ovirt-engine-extension-aaa-ldap/ldap

On a modifié dans le fichier ad.py à la ligne 52:

```what='_ldap._tcp.gc._msdcs.%s' % (

  #en 

  what='_ldap._tcp.%s' % (
```

### Configuration
```> 8 - OpenLDAP RFC-2307 Schema
> Use DNS : Yes
> 1 - Single server
> host address : exemple.fr
> Please select protocol to use (startTLS, ldaps, plain) [startTLS]:plain
> Enter search user DN (for example uid=username,dc=example,dc=com or leave empty for anonymous): cn=Manager,dc=exemple,dc=fr
> Please enter base DN (dc=exemple,dc=fr) [dc=exemple,dc=fr]:
> Are you going to use Single Sign-On for Virtual Machines (Yes, No) [Yes]: Yes
> Please specify profile name that will be visible to users [exemple.fr]:
```
### Connection 

Se connecter à oVirt en sélectionnant le profile name et en rentrant le bon login et le bon mot de passe.

## Pour l'AD (Active directory)

### Prérequis
Vérifier que dans ovirt, on a bien ce package d'installé.

```yum install ovirt-engine-extension-aaa-ldap-setup```
### Modification à apporter au code source python

On modifie les fichier dans le répertoire : /usr/share/ovirt-engine-extension-aaa-ldap/setup/plugins/ovirt-engine-extension-aaa-ldap/ldap

On a modifié dans le fichier ad.py à la ligne 52:

```what='_ldap._tcp.gc._msdcs.%s' % (

  #en 

  what='_ldap._tcp.%s' % (
```
### Configuration
```> 9 - OpenLDAP Standard Schema
> Use DNS : Yes
> 2 - DNS domain LDAP SRV record
> host address : exemple.fr
> Please select protocol to use (startTLS, ldaps, plain) [startTLS]:plain
> Enter search user DN (for example uid=username,dc=example,dc=com or leave empty for anonymous): Nom du compte de consultation de l'AD
> Please enter base DN (dc=exemple,dc=fr) [dc=exemple,dc=fr]:
> Are you going to use Single Sign-On for Virtual Machines (Yes, No) [Yes]: Yes
> Please specify profile name that will be visible to users [exemple.fr]:
```
Après, on passe le test de login qui va échouer même si les informations sont correctes.

On doit donc modifier le fichier de configuration :

```nano /etc/ovirt-engine/aaa/pfvd.nt.bnf.fr.properties```
On rajoute alors les lignes suivantes : 

```
attrmap.map-principal-record.attr.PrincipalRecord_PRINCIPAL.map = cn
attrmap.map-principal-record.attr.PrincipalRecord_ID.map = mail

sequence.openldap-init-vars.010.description = set base dn
sequence.openldap-init-vars.010.type = var-set
sequence.openldap-init-vars.010.var-set.variable = simple_attrsBaseDN
sequence.openldap-init-vars.010.var-set.value = DC=MYDOMAIN,DC=com
sequence.openldap-init-vars.020.var-set.value = cn
sequence.openldap-init-vars.040.var-set.value = 
(objectClass=Person)(${seq:simple_attrsUserName}=*)
```

### Connection 

Se connecter à oVirt en sélectionnant le profile name et en rentrant le bon login et le bon mot de passe.

On peut tester la connection avec : ```ovirt-engine-extensions-tool aaa login-user --profile={Adresse url définie} --user-name={CN de l'utilisateur}```
