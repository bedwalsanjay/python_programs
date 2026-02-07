# Test Suite for AWS Glue Job

This directory contains pytest tests for the AWS Glue job located in `../advanced/dummy.py`.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```

2. Run the tests:
   ```bash
   # Run all tests
   pytest test_dummy.py -v
   
   # Run specific test
   pytest test_dummy.py::TestGlueJob::test_s3_operations -v
   
   # Run with coverage
   pytest test_dummy.py --cov=dummy --cov-report=html
   ```

## Test Coverage

The test suite covers:

- **S3 Operations**: Testing list, copy, and delete operations using moto for S3 mocking
- **Glue Transformations**: Testing ApplyMapping, ResolveChoice, and DropNullFields
- **Job Initialization**: Testing argument resolution and job setup
- **Error Handling**: Testing exception scenarios
- **Integration**: Testing the interaction between different components

## Test Structure

- `conftest.py`: Shared pytest configuration and AWS Glue module mocking
- `test_dummy.py`: Main test file with comprehensive test cases
- `requirements-test.txt`: Test dependencies
- `README.md`: This file with instructions

## Notes

- The tests use mocking extensively since AWS Glue modules are not available in local environments
- S3 operations are tested using the `moto` library which provides AWS service mocking
- The tests focus on unit testing individual components and their interactions
