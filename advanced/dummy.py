import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database="pii", table_name="customer_invoice_csv", transformation_ctx="datasource0")

applymapping1 = ApplyMapping.apply(frame=datasource0, mappings=[("CUST_NUM", "string", "CUST_NUM", "string"), ("CUST_STAT", "string", "CUST_STAT", "string"), ("CUST_BAL", "long", "CUST_BAL", "long"), ("INV_NO", "string", "INV_NO", "string"), ("INV_AMT", "long", "INV_AMT", "long"), ("CRID", "string", "CRID", "string"), ("SSN", "long", "SSN", "long"), ("PHONE", "long", "PHONE", "long"), ("EMAIL", "string", "EMAIL", "string")], transformation_ctx="applymapping1")

resolvechoice2 = ResolveChoice.apply(frame=applymapping1, choice="make_struct", transformation_ctx="resolvechoice2")
dropnullfields3 = DropNullFields.apply(frame=resolvechoice2, transformation_ctx="dropnullfields3")
datasink4 = glueContext.write_dynamic_frame.from_options(frame=dropnullfields3, connection_type="s3", connection_options={"path": "s3://csvtoparque"}, format="parquet", transformation_ctx="datasink4")

client = boto3.client('s3')
BUCKET_NAME = "csvtoparque"
PREFIX = "part-"
response = client.list_objects(Bucket=BUCKET_NAME, Prefix=PREFIX)

name = response["Contents"][0]["Key"]
copy_source = {'Bucket': BUCKET_NAME, 'Key': name}
copy_key = PREFIX + 'invoice_details.parquet'
client.copy(CopySource=copy_source, Bucket=BUCKET_NAME, Key=copy_key)
client.delete_object(Bucket=BUCKET_NAME, Key=name)
job.commit()
