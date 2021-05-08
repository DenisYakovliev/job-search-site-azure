az extension add --name db-up
az postgres up --resource-group denis-first-lab-django --location westus2 --sku-name B_Gen5_1 --server-name django-job-site-postgresdb --database-name pollsdb --admin-user denisYakovliev --admin-password Ws1Dden19sen4O --ssl-enforcement Enabled
az webapp up --resource-group denis-first-lab-django --location westus2 --plan denis-first-lab-django-plan --sku B1 --name deniyakovlievwebappfirstlab
az webapp config appsettings set --settings DBHOST=django-job-site-postgresdb DBNAME="pollsdb" DBUSER=denisYakovliev DBPASS=Ws1Dden19sen4O
