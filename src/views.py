import codecs
import csv
from datetime import date
from typing import Any, Dict, Tuple

import pandas as pd
from fastapi import FastAPI, UploadFile
from fastapi.openapi.utils import get_openapi

from .db import sess
from .models import AssessmentBatch, Stat

app = FastAPI()


@app.post("/uploaddata/")
async def create_upload_file(datafile: UploadFile | None = None) -> Tuple[dict, int]:
    if datafile is None:
        return {"message": "No file uploaded."}, 400
    if datafile.content_type != "text/csv":
        return {"message": "Invalid document type."}, 415
    csv_reader = csv.DictReader(codecs.iterdecode(datafile.file, "utf-8"))
    if sorted(csv_reader.fieldnames) != ["date", "merge_time", "review_time", "team"]:
        return {"message": "Wrong headers in the CSV file."}, 400
    try:
        cleaned_data = [
            {
                "review_time": int(row["review_time"]),
                "team": row["team"],
                "date": date(*row["date"].split("-")),
                "merge_time": int(row["merge_time"]),
            }
            for row in csv_reader
        ]
    except Exception:
        return {"message": "Corrupted row in the CSV file."}, 400
    new_batch = AssessmentBatch(contents=cleaned_data)
    sess.add(new_batch)
    sess.commit()
    return {"message": "%s uploaded successfully." % datafile.filename}, 200


@app.get("/statistics/{batch_id}")
async def view_summary_statistics(batch_id) -> Tuple[dict, int]:
    stat_row = sess.query(Stat).filter(Stat.batch_id == batch_id).first()
    if stat_row is not None:
        return stat_row.dataview, 200
    batch = sess.get(AssessmentBatch, batch_id)
    if not batch:
        return {"message": "Assessment batch not found"}, 404
    data = pd.DataFrame(batch.contents)
    group_cols = ["team"]
    aggregated_cols = ["review_time", "merge_time"]
    stats = data.groupby(group_cols)[aggregated_cols].describe().to_dict()
    new_stat = Stat(dataview=stats, batch_id=batch_id)
    sess.add(new_stat)
    sess.commit()
    return stats, 200


def custom_openapi() -> Dict[str, Any]:
    """Custom OpenAPI Docs.

    Navigate to `/docs` or `/redoc` to see the OpenAPI docs.
    """
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title="Data Visualization API",
            version="1.0.0",
            description="Simple data visualization with CSV and PostgreSQL",
            routes=app.routes,
        )
    return app.openapi_schema


app.openapi = custom_openapi
