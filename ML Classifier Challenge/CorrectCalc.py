def compare_files_line_by_line(file1_path, file2_path):
    # Open both files and read them line by line
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    # Check if the files have the same number of lines
    if len(lines1) != len(lines2):
        print("The files have different numbers of lines, comparison may not be meaningful.")
    
    # Count identical lines
    identical_lines = 0
    total_lines = min(len(lines1), len(lines2))  # Use the length of the shorter file
    
    for line1, line2 in zip(lines1, lines2):
        if line1.strip() == line2.strip():
            identical_lines += 1

    # Calculate percentage of identical lines
    similarity_percentage = (identical_lines / total_lines) * 100
    return similarity_percentage

# File paths
file1_path = "Facit.txt"
file2_path = "EvaluateOnMe_predictions.txt"

# Calculate similarity
similarity_percentage = compare_files_line_by_line(file1_path, file2_path)
print(f"Similarity based on identical lines: {similarity_percentage:.2f}%")
