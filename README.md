# TrueNas Gotify Adapter

TrueNas does not natively provide a way to send alerts and notifications to a Gotify server. This repo 'abuses' the TrueNas Slack alert integration and provides a fake slack webhook endpoint to forward alerts to a Gotify server.
Note that Slack is not required at all for this integration to work.

## Installation
1. Apps -> Discover Apps -> Custom App
    - Enter an Application Name, e.g. "truenas-gotify"
    - _Image Repository_: ghcr.io/ztube/truenas-gotify-adapter
    - _Image Tag_: main
      
    ![Screenshot 2024-09-30 221833](https://github.com/user-attachments/assets/3b2b2914-6cda-4a12-a789-5e8690cf5f79)

    - Environment Variables:
        - _Name_: GOTIFY_URL
        - _Value_: [your gotify url] e.g.https://gotify.example.com/ or service IP
        - _Name_: GOTIFY_TOKEN
        - _Value_: [your gotify app token] e.g. cGVla2Fib29v
        
    ![Screenshot 2024-09-30 221846](https://github.com/user-attachments/assets/448c9b3c-d02c-441c-950a-480e2cc6ee09)

    - Check _"Provide access to node network namespace for the workload"_
    ![Screenshot 2024-09-30 221925](https://github.com/user-attachments/assets/e494860f-3ed8-4282-a28f-8f604d4e8002)
      
    - Save

2. System Settings -> Alert Settings -> Add
    ![Screenshot 2024-09-30 222015](https://github.com/user-attachments/assets/9fb1a5e8-5e8e-440e-abed-fe3fb544ab53)

    - _Type_: Slack
    - _Webhook URL_: http://localhost:31662
   
   ![Screenshot 2024-09-30 222038](https://github.com/user-attachments/assets/75970d0f-46c7-4498-a2ef-3f2355885098)

    - Click _Send Test Alert_ to test the connection
![Screenshot 2024-09-30 222201](https://github.com/user-attachments/assets/24a1f65c-c483-4ca1-a9de-030d40c17a67)
    - Save
  
4. Gotify service
    - Example of the test alert:
    
    ![Screenshot 2024-09-30 222214](https://github.com/user-attachments/assets/69f992a2-74c0-43e6-9b33-56b34e6e5894)



