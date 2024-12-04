# AI-Powered-QA-System-for-ASAP_Systems

AI Powered Question Answering System using LLMs. This is a take home task implementation for **ASAP Systems Barcloud** that features simple RAG to answer user queries about specific topics. The system is a straight forward _converation-memory-conservative_ application.

## Design Description

In this demonestration, we used the _models-controllers-views_ software design pattern such that any interation with the databases is the `models`' responsibility what accepts inputs and return outputs that adhere to a specific _database schema_. The `controllers` are the intermediate layers bewteen the `views` (User interface or Front End) and the `models` such that any processing needed of the user inputs to be passed to models is made by the `controllers`. The RESTful API `endpoints` / `routes` can also be considered part of the `controllers`.

What you should see in the `src` directory should reflect these concepts as follows.

```terminal
src
├── Dockerfile
├── assets
├── configs
├── controllers
├── helpers
├── locales
├── main.py
├── models
├── requirements.txt
└── routes
```

- `assets`: contains any resources and temp files needed for the porject.
- `configs`: contains all the configurations (text mappings) needed by all modules.
- `controllers`: contains all the controllers.
- `helpers`: contains the project settings (currently saved in the `.env` file. different from `configs`) and all future `utils`.
- `locales`: contains all the _prompt templates_ for the different types of _Generative AI_ behaviors (Agentic AI and such).
- `models`: contains all the models.
- `routes`: contains all the `endpoints` (info endpoints are still under development).
- `main.py`: combines all the routes connect them to the `FastAPI` _app_. You can disconnect whatever you want any time from this file.

## Setup

### Quick Setup

```terminal
.
├── LICENSE
├── README.md
├── app
│   └── Dockerfile
├── docker-compose.yml
└── src
    ├── Dockerfile
```

The code is relatively straight forward to start with. You only need `docker` engine and `git` installed to start working.

As you can see from directories above, the backend code in `src` has a `Dockerfile` that builds its image. The same is also applied for the _frontend_ code in `app` but it hasn't been added yet. All other servies that is needed for the application to run along with the `backend` code are implemented in the `docker-compose.yml` file.

To start working, implement the following steps sequentially.

- Clone the _GitHub_ repository and navigate inside its directory.

```bash
git clone https://github.com/e-hossam96/AI-Powered-QA-System-for-ASAP_Systems.git application
cd application
```

- Start the servies in the `docker-compose.yml` file.

```bash
docker compose -p application -f docker-compose.yml up --build
```

You are now up and running and can start calling the endpoints using `curl` (description below).

### Development Setup

At any point if you would like to update the codes and test them, you can create the needed `conda` environment as follows.

- Install developer tools for C++ package building.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install build-essential
```

- Download and install `miniconda`.

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ./miniconda
```

- Activate conda `base` environment.

```bash
source ./miniconda/bin/activate
```

- Create the **asap** environment.

```bash
conda create -n asap python=3.9.11
```

- Intall the `pip` dependencies.

```bash
cd src
python -m pip install -r requirements.txt
```

And now you can start developing the codes. Notice, that the `docker` services are still needed for development (except the backend image).
