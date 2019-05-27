def convert(df):
    """Convert the query all dataframe to a download json structure"""
    data = []
    for _, row in df.iterrows():
        parent = {
            "patient_id": row.PatientID,
            "patient_birth_date": row.PatientBirthDate,
            "study_description": row.StudyDescription,
            "study_date": row.StudyDate,
            "accession_number": row.AccessionNumber,
            "study_uid": row.get("StudyInstanceUID"),  # newer ones have none!
        }
        for s in row["_childDocuments_"]:
            p = parent.copy()
            # Important: Newer versions of the crawler has the StudyInstanceUID
            # on the series level (because of GRASP e.g.) Now if the series level
            # is empty it should  use the one from the study level
            p["study_uid"] = s.get("StudyInstanceUID")
            p["series_uid"] = s["SeriesInstanceUID"]
            p["series_description"] = s.get("SeriesDescription", "")
            p["series_number"] = s.get("SeriesNumber", 9999)
            data.append(p)
    return data