#!/bin/bash

# Generic script to process zip files for move-rename-files task
# This script:
# 1. Extracts a zip file
# 2. Moves all files from subdirectories to a new empty folder
# 3. Renames files by replacing each digit with the next digit (1->2, 9->0)
# 4. Runs grep . * | LC_ALL=C sort | sha256sum

set -e  # Exit on any error

# Function to show usage
usage() {
    echo "Usage: $0 <zipfile>"
    echo "Example: $0 'q-move-rename-files (6).zip'"
    exit 1
}

# Check if zip file argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No zip file specified"
    usage
fi

ZIP_FILE="$1"

# Check if zip file exists
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: Zip file '$ZIP_FILE' not found"
    exit 1
fi

echo "=== Move and Rename Files Script ==="
echo "Processing zip file: $ZIP_FILE"

# Create a unique temporary directory for extraction
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Extract zip file to temporary directory
echo "Extracting zip file..."
unzip -q "$ZIP_FILE" -d "$TEMP_DIR"
echo "Extraction complete"

# Create target directory for moved files
TARGET_DIR="${TEMP_DIR}/moved_files"
mkdir -p "$TARGET_DIR"
echo "Created target directory: $TARGET_DIR"

# Function to move files recursively from all subdirectories
move_all_files() {
    local source_dir="$1"
    local target_dir="$2"
    
    # Find all files (not directories) and move them
    find "$source_dir" -type f -exec mv {} "$target_dir/" \;
}

# Move all files from extracted directories to target directory
echo "Moving all files to target directory..."
move_all_files "$TEMP_DIR" "$TARGET_DIR"

# Count moved files
file_count=$(find "$TARGET_DIR" -type f | wc -l)
echo "Moved $file_count files to target directory"

# Function to rename files by replacing digits
rename_files_with_digit_replacement() {
    local dir="$1"
    
    # Change to target directory
    cd "$dir"
    
    # Process each file
    for file in *; do
        # Skip if not a regular file
        [ -f "$file" ] || continue
        
        # Create new filename by replacing each digit with next digit
        new_name=""
        for (( i=0; i<${#file}; i++ )); do
            char="${file:$i:1}"
            case "$char" in
                0) new_name="${new_name}1" ;;
                1) new_name="${new_name}2" ;;
                2) new_name="${new_name}3" ;;
                3) new_name="${new_name}4" ;;
                4) new_name="${new_name}5" ;;
                5) new_name="${new_name}6" ;;
                6) new_name="${new_name}7" ;;
                7) new_name="${new_name}8" ;;
                8) new_name="${new_name}9" ;;
                9) new_name="${new_name}0" ;;
                *) new_name="${new_name}${char}" ;;
            esac
        done
        
        # Rename file if the name changed
        if [ "$file" != "$new_name" ]; then
            mv "$file" "$new_name"
            echo "Renamed: $file -> $new_name"
        fi
    done
}

# Rename files with digit replacement
echo "Renaming files with digit replacement..."
rename_files_with_digit_replacement "$TARGET_DIR"

# Change to target directory for final operations
cd "$TARGET_DIR"

# Show final file list
echo "Final file list:"
ls -la

# Run the grep command and calculate sha256sum
echo "Running: grep . * | LC_ALL=C sort | sha256sum"
result=$(grep . * | LC_ALL=C sort | sha256sum)

echo "=== FINAL RESULT ==="
echo "SHA256 sum: $result"

# Clean up temporary directory
echo "Cleaning up temporary directory..."
rm -rf "$TEMP_DIR"

echo "Script completed successfully!"
echo "Final answer: $result"
