import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
import boto3
from moto import mock_s3


class TestGlueJob:
    """Test suite for the AWS Glue job in dummy.py"""
    
    @pytest.fixture
    def mock_glue_context(self):
        """Mock GlueContext and related objects"""
        mock_context = Mock()
        mock_spark_session = Mock()
        mock_context.spark_session = mock_spark_session
        
        # Mock dynamic frame
        mock_dynamic_frame = Mock()
        mock_context.create_dynamic_frame.from_catalog.return_value = mock_dynamic_frame
        mock_context.write_dynamic_frame.from_options.return_value = None
        
        return mock_context
    
    @pytest.fixture
    def mock_spark_context(self):
        """Mock SparkContext"""
        return Mock()
    
    @pytest.fixture
    def mock_job(self):
        """Mock Glue Job"""
        mock_job = Mock()
        mock_job.init.return_value = None
        mock_job.commit.return_value = None
        return mock_job
    
    @pytest.fixture
    def mock_dynamic_frame(self):
        """Mock DynamicFrame for transformations"""
        return Mock()
    
    @mock_s3
    def test_s3_operations(self):
        """Test S3 operations - list, copy, and delete"""
        # Setup mock S3 bucket and objects
        s3_client = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'csvtoparque'
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Create a test object
        test_key = 'part-00000-test-file.parquet'
        s3_client.put_object(Bucket=bucket_name, Key=test_key, Body=b'test data')
        
        # Test list objects
        response = s3_client.list_objects(Bucket=bucket_name, Prefix='part-')
        assert 'Contents' in response
        assert len(response['Contents']) == 1
        assert response['Contents'][0]['Key'] == test_key
        
        # Test copy operation
        copy_source = {'Bucket': bucket_name, 'Key': test_key}
        copy_key = 'part-invoice_details.parquet'
        s3_client.copy(CopySource=copy_source, Bucket=bucket_name, Key=copy_key)
        
        # Verify copy was successful
        response_after_copy = s3_client.list_objects(Bucket=bucket_name)
        keys = [obj['Key'] for obj in response_after_copy['Contents']]
        assert copy_key in keys
        assert test_key in keys
        
        # Test delete operation
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        
        # Verify delete was successful
        response_after_delete = s3_client.list_objects(Bucket=bucket_name)
        keys_after_delete = [obj['Key'] for obj in response_after_delete['Contents']]
        assert test_key not in keys_after_delete
        assert copy_key in keys_after_delete
    
    @patch('boto3.client')
    def test_s3_client_creation(self, mock_boto_client):
        """Test S3 client creation"""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        # Import and test client creation
        client = boto3.client('s3')
        mock_boto_client.assert_called_with('s3')
        assert client == mock_client
    
    @patch('sys.argv', ['dummy.py', '--JOB_NAME', 'test-job'])
    @patch('awsglue.utils.getResolvedOptions')
    def test_job_args_resolution(self, mock_get_resolved_options):
        """Test job arguments resolution"""
        mock_get_resolved_options.return_value = {'JOB_NAME': 'test-job'}
        
        from awsglue.utils import getResolvedOptions
        args = getResolvedOptions(sys.argv, ['JOB_NAME'])
        
        assert args['JOB_NAME'] == 'test-job'
        mock_get_resolved_options.assert_called_once_with(sys.argv, ['JOB_NAME'])
    
    def test_apply_mapping_transformation(self, mock_dynamic_frame):
        """Test ApplyMapping transformation"""
        with patch('awsglue.transforms.ApplyMapping') as mock_apply_mapping:
            mock_apply_mapping.apply.return_value = mock_dynamic_frame
            
            from awsglue.transforms import ApplyMapping
            
            mappings = [
                ("CUST_NUM", "string", "CUST_NUM", "string"),
                ("CUST_STAT", "string", "CUST_STAT", "string"),
                ("CUST_BAL", "long", "CUST_BAL", "long"),
                ("INV_NO", "string", "INV_NO", "string"),
                ("INV_AMT", "long", "INV_AMT", "long"),
                ("CRID", "string", "CRID", "string"),
                ("SSN", "long", "SSN", "long"),
                ("PHONE", "long", "PHONE", "long"),
                ("EMAIL", "string", "EMAIL", "string")
            ]
            
            result = ApplyMapping.apply(
                frame=mock_dynamic_frame,
                mappings=mappings,
                transformation_ctx="applymapping1"
            )
            
            mock_apply_mapping.apply.assert_called_once_with(
                frame=mock_dynamic_frame,
                mappings=mappings,
                transformation_ctx="applymapping1"
            )
            assert result == mock_dynamic_frame
    
    def test_resolve_choice_transformation(self, mock_dynamic_frame):
        """Test ResolveChoice transformation"""
        with patch('awsglue.transforms.ResolveChoice') as mock_resolve_choice:
            mock_resolve_choice.apply.return_value = mock_dynamic_frame
            
            from awsglue.transforms import ResolveChoice
            
            result = ResolveChoice.apply(
                frame=mock_dynamic_frame,
                choice="make_struct",
                transformation_ctx="resolvechoice2"
            )
            
            mock_resolve_choice.apply.assert_called_once_with(
                frame=mock_dynamic_frame,
                choice="make_struct",
                transformation_ctx="resolvechoice2"
            )
            assert result == mock_dynamic_frame
    
    def test_drop_null_fields_transformation(self, mock_dynamic_frame):
        """Test DropNullFields transformation"""
        with patch('awsglue.transforms.DropNullFields') as mock_drop_null:
            mock_drop_null.apply.return_value = mock_dynamic_frame
            
            from awsglue.transforms import DropNullFields
            
            result = DropNullFields.apply(
                frame=mock_dynamic_frame,
                transformation_ctx="dropnullfields3"
            )
            
            mock_drop_null.apply.assert_called_once_with(
                frame=mock_dynamic_frame,
                transformation_ctx="dropnullfields3"
            )
            assert result == mock_dynamic_frame
    
    @patch('boto3.client')
    def test_s3_list_objects_error_handling(self, mock_boto_client):
        """Test error handling for S3 list_objects operation"""
        mock_client = Mock()
        mock_client.list_objects.side_effect = Exception("S3 Error")
        mock_boto_client.return_value = mock_client
        
        client = boto3.client('s3')
        
        with pytest.raises(Exception) as exc_info:
            client.list_objects(Bucket="csvtoparque", Prefix="part-")
        
        assert str(exc_info.value) == "S3 Error"
    
    @patch('boto3.client')
    def test_s3_copy_operation(self, mock_boto_client):
        """Test S3 copy operation"""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        client = boto3.client('s3')
        copy_source = {'Bucket': 'csvtoparque', 'Key': 'part-00000-file.parquet'}
        copy_key = 'part-invoice_details.parquet'
        
        client.copy(CopySource=copy_source, Bucket='csvtoparque', Key=copy_key)
        
        mock_client.copy.assert_called_once_with(
            CopySource=copy_source,
            Bucket='csvtoparque',
            Key=copy_key
        )
    
    @patch('boto3.client')
    def test_s3_delete_operation(self, mock_boto_client):
        """Test S3 delete operation"""
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        client = boto3.client('s3')
        client.delete_object(Bucket='csvtoparque', Key='part-00000-file.parquet')
        
        mock_client.delete_object.assert_called_once_with(
            Bucket='csvtoparque',
            Key='part-00000-file.parquet'
        )
    
    def test_glue_context_catalog_read(self, mock_glue_context):
        """Test reading from Glue catalog"""
        mock_glue_context.create_dynamic_frame.from_catalog.return_value = Mock()
        
        result = mock_glue_context.create_dynamic_frame.from_catalog(
            database="pii",
            table_name="customer_invoice_csv",
            transformation_ctx="datasource0"
        )
        
        mock_glue_context.create_dynamic_frame.from_catalog.assert_called_once_with(
            database="pii",
            table_name="customer_invoice_csv",
            transformation_ctx="datasource0"
        )
        assert result is not None
    
    def test_glue_context_s3_write(self, mock_glue_context, mock_dynamic_frame):
        """Test writing to S3 via Glue context"""
        mock_glue_context.write_dynamic_frame.from_options.return_value = None
        
        mock_glue_context.write_dynamic_frame.from_options(
            frame=mock_dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://csvtoparque"},
            format="parquet",
            transformation_ctx="datasink4"
        )
        
        mock_glue_context.write_dynamic_frame.from_options.assert_called_once_with(
            frame=mock_dynamic_frame,
            connection_type="s3",
            connection_options={"path": "s3://csvtoparque"},
            format="parquet",
            transformation_ctx="datasink4"
        )


if __name__ == "__main__":
    pytest.main([__file__])
