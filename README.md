# Welcome to Test Case Backend 👋

## Get started

1. Build Containers
To set up your environment and build the containers, run the following command:

   ```bash
   make build
   ```

2. Start Services
Once the containers are built, you can start the backend services by running:

   ```bash
    make run
   ```

3. Create a Sample User (Optional)
If you'd like to create a pre-populated user for testing, follow these steps:

    1. Open a new terminal and connect to the running container:
        ```bash
        docker exec -it app /bin/sh
        ```

    2. Inside the container, create the user by running the script:
        ```bash
        PYTHONPATH=/code python app/scripts/create_user.py
        ```

    3. After the user is created, exit the container:
        ```bash
        exit
        ```

### For more available commands, check the Makefile.