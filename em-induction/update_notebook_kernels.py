#!/usr/bin/env python3
"""
Script to update all Jupyter notebook kernels to use 'geosci-labs'
This script will:
1. Find all .ipynb files in the current directory and subdirectories
2. Update their kernel metadata to use the 'geosci-labs' kernel
3. Preserve all other metadata and content
"""

import os
import json
import glob

def update_notebook_kernel(notebook_path, target_kernel_name="geosci-labs"):
    """
    Update a single notebook's kernel metadata
    
    Args:
        notebook_path (str): Path to the notebook file
        target_kernel_name (str): Name of the target kernel
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        
        # Get current kernel info for logging
        current_kernel = "unknown"
        if 'metadata' in notebook_data and 'kernelspec' in notebook_data['metadata']:
            current_kernel = notebook_data['metadata']['kernelspec'].get('name', 'unknown')
        
        # Skip if already using target kernel
        if current_kernel == target_kernel_name:
            print(f"✓ {notebook_path} - Already using {target_kernel_name}")
            return True
        
        # Update kernel metadata
        if 'metadata' not in notebook_data:
            notebook_data['metadata'] = {}
        
        notebook_data['metadata']['kernelspec'] = {
            "display_name": target_kernel_name,
            "language": "python", 
            "name": target_kernel_name
        }
        
        # Also update language_info if it exists to be consistent
        if 'language_info' in notebook_data['metadata']:
            notebook_data['metadata']['language_info']['name'] = 'python'
        
        # Write back the updated notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1, ensure_ascii=False)
        
        print(f"✓ {notebook_path} - Updated from '{current_kernel}' to '{target_kernel_name}'")
        return True
        
    except Exception as e:
        print(f"✗ {notebook_path} - Error: {e}")
        return False

def find_all_notebooks(root_dir="."):
    """
    Find all .ipynb files recursively in the given directory
    
    Args:
        root_dir (str): Root directory to search from
        
    Returns:
        list: List of notebook file paths
    """
    notebook_pattern = os.path.join(root_dir, "**", "*.ipynb")
    notebooks = glob.glob(notebook_pattern, recursive=True)
    
    # Filter out checkpoint files
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in nb]
    
    return sorted(notebooks)

def main():
    """Main function to update all notebooks"""
    print("🔍 Searching for Jupyter notebooks...")
    
    # Get the current working directory
    root_dir = os.getcwd()
    print(f"📁 Root directory: {root_dir}")
    
    # Find all notebooks
    notebooks = find_all_notebooks(root_dir)
    
    if not notebooks:
        print("❌ No notebooks found!")
        return
    
    print(f"📓 Found {len(notebooks)} notebooks")
    print("\n" + "="*60)
    
    # Update each notebook
    success_count = 0
    error_count = 0
    
    for notebook_path in notebooks:
        # Make path relative for cleaner output
        rel_path = os.path.relpath(notebook_path, root_dir)
        
        if update_notebook_kernel(rel_path):
            success_count += 1
        else:
            error_count += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"✅ Successfully updated: {success_count}")
    print(f"❌ Failed to update: {error_count}")
    print(f"📊 Total processed: {len(notebooks)}")
    
    if error_count == 0:
        print("\n🎉 All notebooks have been successfully updated to use 'geosci-labs' kernel!")
    else:
        print(f"\n⚠️  {error_count} notebooks had errors. Please check the output above.")

if __name__ == "__main__":
    main()
