if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def validate_input_data(df, *args, **kwargs):
    """
    Custom validation block to inspect data quality before modeling.
    Checks for null values and ensures feature dimensions are valid.
    """
    # Check for missing values
    null_counts = df.isnull().sum().sum()
    if null_counts > 0:
        raise ValueError(f"Data quality check failed: Found {null_counts} missing values!")
    
    # Check dataset dimensions (Iris should have 150 rows)
    if len(df) != 150:
        raise AssertionError(f"Row count mismatch: Expected 150 rows, got {len(df)}")
        
    print(f"Data Validation Passed: {len(df)} rows processed successfully with 0 nulls.")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'