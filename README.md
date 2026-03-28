<!-- Header -->
<div align="center">
    <h1>Vaccone Score Analysis</h1>
    <p>
        A fast analytics service for tracking player ratings and match statistics
        <br />
        <a href="#installation">Installation</a>
        ·
        <a href="#related-repositories">Related Repositories</a>
    </p>
</div>

## Installation

1. Install [uv](https://docs.astral.sh/uv/)

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Clone the repository

```bash
git clone https://github.com/rvaccone/vaccone-score-analysis.git
cd vaccone-score-analysis
```

3. Create a virtual environment

```bash
uv venv
```

4. Install dependencies

```bash
uv sync --frozen
```

5. Start a Docker daemon like Docker Desktop

6. Start the development server

```bash
make dev
```

7. You should be able to access the server at `http://localhost:8000`

> [!IMPORTANT]
> This API is intended to power the Vaccone Score Web app. You can learn how to install and run the web app [here](https://github.com/rvaccone/vaccone-score-web).

## Related Repositories

- [vaccone-score-web](https://github.com/rvaccone/vaccone-score-web)
