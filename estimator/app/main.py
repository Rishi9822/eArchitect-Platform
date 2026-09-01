from fastapi import FastAPI

app = FastAPI(
    title="eArchitect Estimator",
    description="Material quantity and construction cost estimation service",
    version="0.1.0",
)


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "service": "eArchitect-estimator",
    }


@app.get("/api/v1/version")
def version():
    return {
        "service": "eArchitect-estimator",
        "version": "0.1.0",
    }