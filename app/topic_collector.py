
from app import APP_NAME
from app.storage_service import BigQueryService

if __name__ == "__main__":

    bq_test = BigQueryService(dataset_name=f"{APP_NAME}_test")
    #bq_dev = BigQueryService(dataset_name=f"{APP_NAME}_development")
    #bq_prod = BigQueryService(dataset_name=f"{APP_NAME}_production")

    services = [bq_test] # [bq_test, bq_dev, bq_prod]

    for bq_service in services:
        print(bq_service.dataset_address)
        bq_service.add_topic("TEST TOPIC")
