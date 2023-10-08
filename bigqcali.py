from google.cloud import bigquery


def query_cbsa(year):
    client = bigquery.Client()
    query_job = client.query(
        f"""
        SELECT *
        FROM `bigquery-public-data.census_bureau_acs`
        WHERE do_date LIKE '%re{year}'
        ORDER BY view_count DESC
        LIMIT 10"""
    )

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} : {} views".format(row.url, row.view_count))


if __name__ == "__main__":
    query_cbsa()
