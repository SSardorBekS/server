def calculate_similarity_score(left_list, right_list):
    """
    Calculate the similarity score by counting occurrences of left list numbers in right list
    """
    # Count occurrences of each number in the right list
    right_counts = {}
    for num in right_list:
        right_counts[num] = right_counts.get(num, 0) + 1
    
    # Calculate similarity score
    similarity_score = 0
    for num in left_list:
        # Multiply each left list number by its count in the right list
        count = right_counts.get(num, 0)
        similarity_score += num * count
    
    return similarity_score

# Read input from file
with open('input.txt', 'r') as file:
    # Read lines and split into left and right lists
    lines = file.readlines()
    
    # Parse the lists
    left_list = []
    right_list = []
    
    for line in lines:
        # Split the line into left and right numbers
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)

# Calculate and print the similarity score
similarity_score = calculate_similarity_score(left_list, right_list)
print(f"Similarity score: {similarity_score}")