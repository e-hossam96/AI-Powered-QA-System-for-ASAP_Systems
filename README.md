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

