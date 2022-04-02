def delete(self):
        json = request.json
        s3.delete_object(Bucket=S3_BUCKET, Key=json["filename"])
        return ("get_file_deleted", "file-deleted-successfully"), 200
