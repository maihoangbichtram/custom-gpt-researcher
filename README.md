<div align="center" id="top">

####

[![Website](https://img.shields.io/badge/Official%20Website-platform.sh-teal?style=for-the-badge&logo=world&logoColor=white&color=0891b2)](https://main-bvxea6i-bkwpxl2cinmus.eu.platformsh.site/docs)

</div>

# 🔎 Psychology Knowledge Base

Custom GPT Researcher generates/collects unstructured data from web sources.
GraphRAG indexes unstructured data into knowledge graph.

## Demo
https://main-bvxea6i-bkwpxl2cinmus.eu.platformsh.site/docs

## Architecture


## Features

- 📝 Generate research reports using web and local documents.
- 📜 Generate reports exceeding 1000 words.
- 🌐 Aggregate over 20 sources for objective conclusions.
- 📂 Maintains memory and context throughout research.
- 📄 Export reports to .md format.

## ⚙️ Getting Started

### Installation

1. Install Python 3.11 or later. [Guide](https://www.tutorialsteacher.com/python/install-python).
2. Clone the project and navigate to the directory:

    ```bash
    git clone https://github.com/maihoangbichtram/custom-gpt-researcher.git gpt-researcher
    cd gpt-researcher
    ```

3. Set up API keys by exporting them or storing them in a `.env` file.

    ```bash
    Copy .env.example to .env
    ```

4. Configure GraphRAG
   ```bash
    cp ./rag_interface/settings.yaml ./rag
    cp -r ./rag_interface/prompts ./rag
    ```

5. Activate the virtual environment

    ```bash
    poetry shell
    ```
6. Install dependencies and start the server:

    ```bash
    poetry lock && poetry install
    python -m uvicorn main:app --reload
    ```

Visit [http://localhost:8000](http://localhost:8000) to start.

For other setups (e.g., Poetry or virtual environments), check the [Getting Started page](https://docs.gptr.dev/docs/gpt-researcher/getting-started/getting-started).


## 📄 Add Local Documents to research

You can instruct the GPT Researcher to run research tasks based on your local documents. Currently supported file formats are: plain text(.txt).

Add the env variable `DOC_PATH` pointing to the folder where your documents are located.

```bash
export DOC_PATH="./rag/input"
```


## How it works

[![Website](https://img.shields.io/badge/Website-canva-teal?style=for-the-badge&logo=world&logoColor=white&color=0891b2)](https://www.canva.com/design/DAGY4TvXaMY/rQ5scSILu-Hjt5zpP8ke0Q/view?utm_content=DAGY4TvXaMY&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hbe769c0952)


## Deployment

Check out `.platform.app.yaml` as an example how to deploy.

Note: `persistent mounts/disk` needed for /rag, /.output, /.config, and /outputs.

<p align="right">
  <a href="#top">⬆️ Back to Top</a>
</p>
