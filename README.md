# debatable
LLM to address sales objections

---

**`debatable.py`** - python funcs to generate suggestions

**`api.py`** - REST API wrapper around `debatable.py`

**`app.py`** - streamlit app using `debatable.py`

---

> Note: the following will have to be saved as an environment variables:
> - `OPENAI_API_KEY`
> - `DETA_PROJECT_KEY`: Key for deta.space's "Base" NoSQL DB (to collect stats)

Run a FastAPI server with 

```bash
uvicorn api:app --reload # reload flag for development
```

Run streamlit app with

```bash
streamlit run app.py
```

---

**Using Codespaces/VSCode**

Everything you need will be installed when you open Codespaces/VSCode; specified in `.devcontainer/`

*Notes for Codespaces:*
- Jupyter (will be added to the devcontainer later, not used now)
  - Currently Jupyter notebook doesn’t work on Codespaces for an unknown reason, or at least I can’t, so you’ll have to use JupyterLab
  - Open with `jupyter lab --NotebookApp.allow_origin='*' --NotebookApp.ip='0.0.0.0'`
  - For more info on using see https://code.visualstudio.com/docs/datascience/notebooks-web
- Streamlit
  - `./.devcontainer/streamlit.sh` is the equivalent to running streamlit with `streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false`
  - Open with `streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false`
  - For more info see https://discuss.streamlit.io/t/how-to-make-streamlit-run-on-codespaces/24526/6
- FastAPI
  - `--reload` doesn't work in codespaces, will have to refresh to see changes
