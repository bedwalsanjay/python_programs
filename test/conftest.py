import pytest
import sys
from unittest.mock import Mock

# Add the parent directory to sys.path to import the module under test
sys.path.insert(0, '../advanced')

@pytest.fixture(scope="session", autouse=True)
def mock_aws_glue_modules():
    """Mock AWS Glue modules that are not available in local environment"""
    # Mock awsglue modules
    sys.modules['awsglue'] = Mock()
    sys.modules['awsglue.transforms'] = Mock()
    sys.modules['awsglue.utils'] = Mock()
    sys.modules['awsglue.context'] = Mock()
    sys.modules['awsglue.job'] = Mock()
    
    # Mock pyspark modules
    sys.modules['pyspark'] = Mock()
    sys.modules['pyspark.context'] = Mock()
    
    # Create mock classes for transforms
    mock_apply_mapping = Mock()
    mock_resolve_choice = Mock()
    mock_drop_null_fields = Mock()
    
    sys.modules['awsglue.transforms'].ApplyMapping = mock_apply_mapping
    sys.modules['awsglue.transforms'].ResolveChoice = mock_resolve_choice
    sys.modules['awsglue.transforms'].DropNullFields = mock_drop_null_fields
