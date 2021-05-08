#!/bin/bash
location="East US2"
resourceIdentifier=cloudcomputing4

resource="resource-$resourceIdentifier"
server="server-$resourceIdentifier"
database="database-$resourceIdentifier"
webappname="webapp-$resourceIdentifier"

login="sampleLogin"
password="samplePassword123!"

startIP=0.0.0.0
endIP=255.255.255.255

echo "Creating $resource..."
az group create --name $resource --location "$location"

echo "Creating $server in $location..."
az sql server create --name $server --resource-group $resource --location "$location" --admin-user $login --admin-password $password

echo "Configuring firewall..."
az sql server firewall-rule create --resource-group $resource --server $server -n AllowYourIp --start-ip-address $startIP --end-ip-address $endIP

echo "Creating $database on $server..."
az sql db create --resource-group $resource --server $server --name $database --sample-name AdventureWorksLT -e GeneralPurpose -f Gen5 -c 2 --zone-redundant false

echo "Creating $webappname..."
az webapp up --resource-group $resource --location "$location" --plan denis-first-lab-django-plan --sku B1 --name $webappname

echo "Configuring $webappname..."
az webapp config appsettings set -g $resource -n $webappname --settings DBNAME=$database DBHOST=$database DBUSER=$login DBPASS=$password DBSERVER="$server.database.windows.net"

