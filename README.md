# debatable
LLM to address sales objections

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