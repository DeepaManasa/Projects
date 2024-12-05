# Project Overview
This repository documents the creation and configuration of an Azure Data Factory (ADF) pipeline integrated with Databricks for an end-to-end ETL process. It leverages Azure Storage Accounts for Medallion architecture, Databricks notebooks for transformations, and Azure Key Vault for secure integration.  
# Step-by-Step Process  
Step 1: Setting Up Storage Accounts for Medallion Architecture  
1.	Source Storage Account (sourceingestion):  
o	Create a storage account named sourceingestion.  
o	Inside this account, create a container (e.g., sales-data).  
o	Upload your source file (e.g., sales_data.csv) to this container.  
2.	Destination Storage Account (projectstorage997):  
o	Create another storage account named projectstorage997.  
o	Add three containers:  
     -  raw-data for storing unprocessed data.  
     -  curated for storing processed intermediate data.  
     -  staging for storing the final, transformed data.  
Explanation:  
This structure follows the Medallion Architecture (Raw → Curated → Staging), which organizes data flow into layers for better processing and management.  

# Step 2: Creating and Configuring ADF  
1.	Create the ADF Instance:  
o	Go to the Azure Portal and create an instance of Azure Data Factory.  
o	Launch the Data Factory Studio for designing pipelines.  
2.	Linked Services Configuration:  
o	In ADF Studio, navigate to Manage > Linked Services.  
o	Add linked services for:  
    -   Source Storage: Connect to source ingestion.  
    -   Destination Storage: Connect to projectstorage997.  
    -   Databricks: Use Azure Key Vault for secrets (explained in Step 5).  
Explanation:  
Linked Services act as connectors, allowing ADF to interact with storage accounts, Databricks, and other resources.  

3.	Pipeline Design - Copy Data Activity:   
o	Add a Copy Data activity to copy sales_data.csv from the sourceingestion storage to the raw-data container in projectstorage997.  
o	Configure dynamic parameters for the source and sink paths, enabling reusability of the pipeline.  
Explanation:
Copy Data is the initial step that moves raw data into the raw layer for further processing.

![image](https://github.com/user-attachments/assets/9c411a98-08da-4ae5-8687-018383893fcf)  

# Step 3: Setting Up Databricks Notebooks  
1.	Prepare Databricks Workspaces:  
o	Create a Databricks workspace in Azure.  
o	Inside Databricks, create two notebooks:  
  -  Curated Notebook: For intermediate processing.  
  -  Staging Notebook: For final transformations.  
2.	Notebook for Curated Data:  
o	Applied data cleaning activities and transformations such as:  
-   Handling null values using isnull().
-   Used abs() to convert quantity values to positive.
-   Capitalizing column data with initcap().
-   Data cleansing with regexp().  
-  	Date conversion with to_date() and coalesce() for converting different date formats in transaction date to one format.	
-   Used coulmnrenamed() to change the column name 	
o	Write the transformed data back to the curated container in CSV format.  
3.	Notebook for Staging Data:  
o	Additional transformations:  
-  	Utlilized StructType() to define schema for reading the data.
-   Extract year from date fields.
-  	Create a new column (e.g., total_quantity).  
-  	Partition data based on product type for efficient querying.  
o	Write the final output to the staging container in Parquet format.  
Explanation:  
Each notebook processes the data to refine and enhance its usability as it moves through the Medallion Architecture.

![image](https://github.com/user-attachments/assets/ddb4449b-9811-4552-ac32-02ca6226735e)  
                 ..........
![image](https://github.com/user-attachments/assets/07e07e49-a4e7-4e31-b46b-c342e06c6e33)

# Step 4: Pipeline Integration with Databricks  
1.	Databricks Linked Service:  
o	Use Azure Key Vault (explained in Step 5) to securely store credentials (access token and scope details).  
o	Create a Databricks linked service in ADF referencing these secrets.  
2.	Pipeline Design:  
o	Add two Databricks Notebook activities to the pipeline:  
-  	First for the curated stage.  
-  	Second for the staging stage.  
o	Configure the activities to call the respective Databricks notebooks.  
Explanation:  
This step integrates Databricks with ADF, allowing it to execute the transformations defined in the notebooks.  
Add Screenshot Here for Pipeline with Databricks Integration

![image](https://github.com/user-attachments/assets/6a593265-5c15-4540-a6bf-fdd69a36d068)  


# Step 5: Setting Up Azure Key Vault  
1.	Microsoft Entra ID (AAD) Creation:  
o	Create an app using app registrations  
o	Create the secret for the app and copy the value.  
o	Add a role assignment as storage Blob contributor and attach the above app for storage account(projectstorage997).  
2.	Key Vault Creation:  
o	Create an Azure Key Vault.  
o	Add secrets for:  
- 	Copy the secret value from the app and create a secret.  
- 	Databricks access token.  
3.	Access Policies:  
o	Grant access to:  
- 	APP to configure storage account with databricks.  
- 	ADF: To fetch secrets  
- 	Databricks: To use these secrets.  
Explanation:  
Key Vault ensures secure and centralized management of sensitive information like credentials and tokens.

![image](https://github.com/user-attachments/assets/7a7c2e30-fec0-4bdf-85c2-bc158473d23a)  


![image](https://github.com/user-attachments/assets/97bf93c0-14ec-4f2e-ac33-b5f0c0ec8a46)   


# Step 6: Implementing Dynamic Parameters  
1.	Create Parameters in the Pipeline:  
o	Add parameters for dynamic source and sink paths in the Copy Data activity.  
o	Use these parameters in the Databricks Notebook activities for flexibility.  
2.	Parameterize Linked Services:  
o	Use parameterized Linked Services to allow easy changes in storage or Databricks configurations without modifying the pipeline.  
Explanation:  
Dynamic parameters make the pipeline reusable and adaptable to different datasets and configurations.


![image](https://github.com/user-attachments/assets/b32eb2f5-2887-4686-a18c-2a7757bd2503)  

![image](https://github.com/user-attachments/assets/314395f7-6a50-4eda-8102-42d19fc3a44e)   


# Step 7: Testing and Validation  
1.	Run the Pipeline:  
o	Test the pipeline by triggering it with the source file (sales_data.csv).  
o	Verify that the data flows through the raw, curated, and staging containers as expected.  
2.	Validate Outputs:  
o	Check the curated container for processed CSV files.  
o	Check the staging container for Parquet files with applied transformations and partitions.

![image](https://github.com/user-attachments/assets/e8205083-3427-47aa-a5a6-56a7a5056965)  



![image](https://github.com/user-attachments/assets/6577299e-a40d-4bf5-971f-c5a989c7b470)   


# Conclusion
This detailed pipeline demonstrates the integration of ADF and Databricks to implement a robust ETL process based on Medallion Architecture. It ensures scalability, flexibility, and secure management of credentials.




























