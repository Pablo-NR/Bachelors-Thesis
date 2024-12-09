# Bachelors-Thesis
This repository contains resources and documentation related to my Bachelor's Thesis on Identity Management in cloud environments, focusing on Entra ID and the implementation of OAuth 2.0 flows.

## Overview:
In a business environment increasingly focused on cloud technologies and with a continuous migration from traditional infrastructures, identity and access management has become a key challenge for organizations and cybersecurity professionals.

This project analyzes the transition from identity management in Active Directory to Entra ID as a cloud identity provider. It explores in detail the security features and tools of Entra ID, as well as their application for effective identity management. Additionally, it studies the OAuth 2.0 flows, evaluating their functionality and potential vulnerabilities.

As a practical case, an application is integrated with Entra ID using an initially insecure OAuth 2.0 flow, demonstrating how an attacker could capture the Access Token. Then, a secure flow is implemented to mitigate these vulnerabilities, confirming that the attack is no longer possible. Finally, security is strengthened with advanced Entra ID tools to protect the application's identities and access.

## Content:
- **TFG-Memoria:** PDF of the thesis report in Spanish.
- **Thesis-Report:** PDF of the thesis report in English.
- **AuthorizationCodeFlow folder:** Folder containing the necessary files to create the web application and integrate it with Entra ID using the Authorization Code Flow.
- **ImplicitFlow folder:** Folder containing the necessary files to create the web application and integrate it with Entra ID using the Implicit Flow.

## Clone the repository:
`git clone https://github.com/Pablo-NR/Bachelors-Thesis.git`

## Contributions:
This repository is for personal use, but if you find errors or want to suggest improvements, feel free to open an issue or send a pull request.
