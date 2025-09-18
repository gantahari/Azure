# Azure SQL

## Usecase1: Provisioning Azure SQL Server and Database with IaC tools like Terrafrom or ARM Templetes

## Usecase2: Set up CICD pipeline for Azure SQL Servers

**CI Pipeline:** 
-   Choose trigger and windows server agent
-   Build using VSBuild Task
-   Publish the build created DacPac File
-   Create a Service Connection to ARM or SQL Server using SQL Authentication or Managed Identity

**CI Pipeline:** 
-   Get the Artifact(dacpac file) created earlier
-   Add Stage and Job as Azure SQL Deployment [ Choose the sub, SQL Server and Database or Give Connection String]
-   Choose deployement type as dacpac and action as publish

<!-- ## Usecase3: Story about  -->

# Azure Databricks

## Usecase1: Provisioning Azure Databricks with IaC tools like Terrafrom or ARM Templetes

## Usecase2: Set up CICD pipeline for Azure Databricks

**CICD Pipeline:** 
-   Choose trigger, variables and variable groups
-   Stage to Deploy to Dev/Uat [ It call deploy.yaml file which has code with parameters like StageID, Env, Envname, RG, SCName, Notebook Path and Dependson (optional) ]
- Call the custom powershell script to get the databricks Bearer Token by passing Workspace ResourceID and Workspace URL as parameters.
-   Install Azure Databricks CICD tools for PS modules
-   Import Local Databricks notebooks folder into the databricks workspace by using the Bearer Token, Region, LocalPath, Databricks Path and -Clean 

# Azure Data Factory

## Usecase1: To migrate databases from On Prem to Azure SQL Servers at Commerce Bank

## Usecase2: To CSV files on Client Servers and Load them to Azure SQL Server Databases

## Usecase3: To connect with Share Point Files and copy them into the ADLS

## Usecase4: To transform the ADLS data and store cleaned files in ADLS






    