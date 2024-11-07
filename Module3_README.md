Data Ingestion Project with Azure Synapse Analytics.
This project involves designing and implementing a data pipeline in Azure Synapse Analytics to automate the ingestion, storage, and querying of data from a source system to Azure Data Lake Storage. The pipeline is built using Serverless SQL Pools for flexible querying and External Tables to read data stored in Azure Data Lake. The overall process is divided into multiple phases for efficient data handling, including the creation of external file formats, external data sources, and external tables, along with options for automated ingestion using Azure Data Synapse using parameters or Triggers.

Here are the steps I followed to create a data-driven workflow using Azure Synapse Analytics.  

--Pre-requisites for Data Ingestion Pipeline.  

Log in to the Azure portal using login credentials.   

Created a resource group, "sample_resource9" for the services to use in the Azure portal.  

Created an Azure SQL Database, "adventuredb97", Azure SQL server and used sample data “AdventureWorks” to ingest data into a storage account.  

Created an Azure Synapse Analytics workspace, "synapseworkspace97" along with storage account "storagesynapse97" and a container named “raw-data” to use.  
Create Azure Key Vault to ingest data from SQL DB.  

Created an Azure Key Vault with the name "keyvaultmodule3" using create resource. 
![image](https://github.com/user-attachments/assets/0a30c3f5-e6ee-4bae-8bbf-a68482e3367d)



Configure the key vault by generating a secret key for Azure Synapse.  
![image](https://github.com/user-attachments/assets/1b053210-444b-4a19-bf2c-f9b800d6908a)



Enable the access policies for the resources to use Azure Synapse analytics and add the managed identity object of Synapse workspace to the key vault.  
![image](https://github.com/user-attachments/assets/a501757f-edc5-424d-b219-235b3932cd48)



Enable the system-assigned managed identity in the SQL server so the SQL DB can use the Azure key vault security system. 
![image](https://github.com/user-attachments/assets/ec6785b8-b54b-4a22-87a3-9986dbdf0ae3)

#Step 1: Data Ingestion  
-Used a Copy Activity from the pipeline to ingest data from various sources into your data lake.  
-Created a Parameterized Data Pipeline in Azure Data Synapse from the source SQL Database to Data Lake Storage using key vault. We have also set the file name dynamically using functions like utcNow() and concat(). This approach allows to dynamically specify the source and destination of your data copy operation.  
  1.	Pipeline Parameters  
	Create two pipeline parameters:  
      1.	targetTable  
      2.	targetDB  
  2.	These parameters will be used for both your source (SQL DB) and sink (Storage Account) datasets.
       ![image](https://github.com/user-attachments/assets/2e071b25-3476-4e24-bd36-9f042deb7e3f)

  3.Source Dataset (Azure SQL DB) In your DB dataset:  
    Create two parameters:  
      1.	srcTable  
      2.	srcDB  
  4.For the connection:
    Set the Table to "Enter manually" and use @dataset().srcTable to reference the table parameter.  
    Set the Database to @dataset().srcDB.
     ![image](https://github.com/user-attachments/assets/311d4e01-fb29-4655-aa5a-eb71755682ad)

  5.This allows the pipeline to dynamically pass the table and database values from the pipeline parameters to the dataset(table).  
  6.Pipeline -> Copy Activity -> Source In the Copy Activity's Source section:  
    Choose the source dataset  
    You will see the two parameters (srcTable and srcDB).  
    Assign them values using expressions:  
      1.	srcTable = @pipeline().parameters.targetTable  
      2.	srcDB = @pipeline().parameters.targetDB  
     ![image](https://github.com/user-attachments/assets/b1da4151-2900-499b-888d-7960a57f2bf4)

  7.Target Dataset (Storage Account) In your Target dataset:  
    Create two parameters:  
      1.	targetTable  
      2.	targetFolder  
     ![image](https://github.com/user-attachments/assets/eddde674-9469-4176-927c-db3834353d6a)

  8.For the File path:  
    GoTo Connections in dataset  
    Set the Container name manually.  
    Set the Folder path using the expression:  
      @concat(dataset().targetFolder,'/',dataset().targetTable)  
    Set the File name using the expression:  
      @concat(dataset().targetTable, '_', utcNow())  
     ![image](https://github.com/user-attachments/assets/f228ea67-a82c-4f6e-8350-3bb817b82a10)  

  9.This dynamically builds the folder path and file name using the dataset parameters and the current timestamp.  
  10.Pipeline -> Copy Activity -> Sink In the Copy Activity's Sink section:  
    Choose the target dataset(Here storage account dataset)  
    You should see the parameters targetTable and targetFolder from the dataset.  
    Assign them values using expressions:  
      1.	targetTable = @pipeline().parameters.targetTable  
      2.	targetFolder = @pipeline().parameters.targetDB (because you're using targetDB as the folder name for the target).  
    ![image](https://github.com/user-attachments/assets/b85d311a-46b6-4101-82e0-fa1da030d32a)  
--This setup allows you to copy data from the targetDB and targetTable (which are the pipeline parameters) to the appropriate folder in the storage account.
   ![image](https://github.com/user-attachments/assets/dd0725dc-c5ba-4d09-965e-ce2e7fdd533d)  


--Pipeline is successful and copied the data from Azure SQL DB to the Storage account and created a file in the container for schema and table, which we passed as parameters.  
![image](https://github.com/user-attachments/assets/30af1f7b-6317-4d8a-84a0-3c8c68044256)  


  11.Trigger: Created a schedule event trigger to schedule the pipeline based on time intervals(eg: 5 minuites) to fetch the data. When triggering the pipeline manually or through a schedule, you only need to      provide values for the targetDB (the database name) and targetTable (the table name).  
  ![image](https://github.com/user-attachments/assets/10f5a256-19f1-4e28-9d41-541bcb683686)  
  ![image](https://github.com/user-attachments/assets/c25fc27f-d0bc-4d87-b795-7236ba7e2bc6)  


Step 2: Create a synapse external table using a serverless SQL pool.  
For raw staged data, a Synapse External Table was created. Specified the format, source, and table definition to make the data queryable.  

  1. Create External File Format.  
  The external file format defines the structure of the data files that Azure Synapse will read. We will use a delimited text format where commas separate the fields.  
  2. Create the external data source.  
  The external data source points to the storage account where the data files are located. In this case, it's an Azure Data Lake Storage Gen2 account.  
  ![image](https://github.com/user-attachments/assets/e80abf8d-34c4-4683-aedc-ccb1fa62129a)



  3.Create the external table.  
  The external table maps to the data files stored in Azure Data Lake. This allows us to query the data without physically loading it into the dedicated SQL pool.  
  ![image](https://github.com/user-attachments/assets/dbe4656b-3a9b-47cb-aa3a-a46053482d9d)  



Step 3: Data Exploration with external table.  
Refer to the query.sql for the queries.  
