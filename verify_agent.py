import os
import shutil
from agent import read_file, write_file, list_dir

def test_path_handling():
    print("Starting verification...")
    
    # Setup test directory
    test_dir = "test_agent_verification"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    try:
        # Test 1: Write file with relative path
        print("\nTest 1: Write file with relative path")
        result = write_file(f"{test_dir}/test.txt", "Hello World")
        print(result)
        assert "Successfully wrote to" in result
        assert os.path.exists(f"{test_dir}/test.txt")

        # Test 2: Read file with relative path
        print("\nTest 2: Read file with relative path")
        content = read_file(f"{test_dir}/test.txt")
        print(f"Content: {content}")
        assert content == "Hello World"

        # Test 3: List directory with relative path
        print("\nTest 3: List directory with relative path")
        files = list_dir(test_dir)
        print(f"Files: {files}")
        assert "test.txt" in files

        # Test 4: Path expansion (~)
        # Note: This depends on the environment having a home directory. 
        # We'll just check if it doesn't crash and returns a list or error (but not a path error)
        print("\nTest 4: List home directory (~)")
        home_files = list_dir("~")
        if isinstance(home_files, list):
            print(f"Successfully listed home directory (first 5): {home_files[:5]}")
        else:
            print(f"Failed to list home directory: {home_files}")

        # Test 5: Error handling
        print("\nTest 5: Read non-existent file")
        error_result = read_file("non_existent_file.txt")
        print(error_result)
        assert "Error reading file" in error_result

    finally:
        # Cleanup
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            
    print("\nVerification complete!")

if __name__ == "__main__":
    test_path_handling()
