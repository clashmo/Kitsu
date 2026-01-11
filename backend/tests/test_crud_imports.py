"""
Test that all CRUD objects can be imported successfully.
This prevents regression of the ImportError issue.
"""

import os
import sys


def test_crud_imports():
    """Test that all CRUD objects can be imported from app.crud."""
    # Set minimal environment variables required for import
    os.environ.setdefault("SECRET_KEY", "test_key_for_imports")
    os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000")
    
    # Import should not raise ImportError
    from app.crud import (
        anime_crud,
        collection_crud,
        episode_crud,
        favorite_crud,
        release_crud,
        user_crud,
        view_crud,
    )
    
    # Verify that all objects are not None
    assert anime_crud is not None, "anime_crud should not be None"
    assert collection_crud is not None, "collection_crud should not be None"
    assert episode_crud is not None, "episode_crud should not be None"
    assert favorite_crud is not None, "favorite_crud should not be None"
    assert release_crud is not None, "release_crud should not be None"
    assert user_crud is not None, "user_crud should not be None"
    assert view_crud is not None, "view_crud should not be None"
    
    print("✓ All CRUD objects imported successfully")
    return True


if __name__ == "__main__":
    try:
        test_crud_imports()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Test failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
