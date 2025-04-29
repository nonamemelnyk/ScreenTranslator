"""
Test script to verify that command-line arguments are properly passed to the Config class.
"""

from screentranslator.config import Config

def test_config_with_args():
    """Test Config class with command-line arguments."""
    # Test with command-line arguments
    args = ['--TRANSLATION_SERVICE=deepl', '--DEFAULT_SOURCE_LANGUAGE=fr']
    config = Config(args)
    
    # Verify that command-line arguments take precedence over environment variables
    assert config.translation_service == 'deepl'
    assert config.source_language == 'fr'
    
    # Display the configuration
    config.display()
    
    print("\nTest passed! Command-line arguments are properly passed to the Config class.")

if __name__ == '__main__':
    test_config_with_args()