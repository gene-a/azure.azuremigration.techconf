# TechConf Registration Website
http://techconf-app.azurewebsites.net

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

This project was created in order to practice applied learnings for migrating azure web apps, long-calling functions, and databases.
Requires the use of a azure app service, azure function app, azure service bus, sendgrid api, and azure postgresdb.

## Dependencies

- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Monthly Cost Analysis
Month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database*|Basic|$0.034/hour|
| *Azure Service Bus*|Basic|$0.05/month|
| *Azure Function App*|Consumption Plan|Pay-As-You-Go|
| *Azure Storage Account*|Standard (GPv2)|$0.0184 per GB|
| *Azure App Service*|F1|$0.0 Pay-As-You-Go|

## Architecture Explanation
For the techconf app, I've elected to host the app in an App Service over migrating to a VM. Since the application is a simple webapp that does not need the robust capacity of vcpus and memory a VM has, an App Service will suffice while having the capability to scale out (if necessary) through auto-scale out on the portal.

For the long-calling HTTP function of sending notifications to attendees, I've elected to use the Azure Function App and host a Service Bus Trigger that waits for messages to go into my created Azure Service Bus Queue that holds notifications. Despite python function apps being experimental and new, Azure's offering of expanding compute capacity on-load will very much cater to the needed surge of attendees during the conference.

The application is tied together using an Azure Postgres Database that is more than capable in handling the load/requirements of the application.

Lastly, for sending out emails, I've opted to use SendGrid's API in sending out notifications to attendees as soon as a message comes into my Service Bus.
