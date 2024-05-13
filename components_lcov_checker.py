import subprocess
import csv

# List of components to be processed
components = [
    "planning", "control", "localization", "common", "map",
    "perception", "sensing", "simulator", "system", "tools",
    "vehicle", "ALL"
]

# Dictionary to store the results
results = {}

# Dictionary to store the results
results_for_csv = {
    'lines': {},
    'functions': {},
    'branches': {}
}

# Execute the command for each component
for component in components:
    print(f"Processing {component} ...")
    
    component_in_command = "**" if component == "ALL" else component
    command = f'shopt -s globstar; colcon lcov-result --verbose --paths "./src/autoware/universe/{component_in_command}/**" --filter "*/build/*" "*/test/*"'
    
    # Execute the command and capture the output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()
    
    output = stdout.decode('utf-8')
    
    # Split output into lines
    lines = output.split('\n')
    summary_lines = []
    for i in range(len(lines)-1, -1, -1):  # Start from the end of the list
        if "Summary coverage rate:" in lines[i]:
            # Extract the line where "Summary coverage rate:" appears last and the next 3 lines
            summary_lines = lines[i:i+4]
            break
    
    # Join the extracted lines for final result
    summary_output = "\n".join(summary_lines) if summary_lines else "No summary coverage rate found."
    
    results[component] = summary_output


    # Parse coverage data
    for line in summary_lines:
        if 'lines' in line:
            percentage = line.split(': ')[-1].split('%')[0]
            results_for_csv['lines'][component] = percentage
        elif 'functions' in line:
            percentage = line.split(': ')[-1].split('%')[0]
            results_for_csv['functions'][component] = percentage
        elif 'branches' in line:
            percentage = line.split(': ')[-1].split('%')[0]
            results_for_csv['branches'][component] = percentage

# Display results for each component
print("\n")
for component, result in results.items():
    if component == "**":
        print("--- TOTAL ---")
    else:
        print(f"--- {component} ---")
    print(result)
    print("\n")



# Prepare CSV output
print("Generating CSV...")
with open('components_coverage_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for key in results_for_csv:
        writer.writerow([key, 'component', ''])
        for component in components:
            if component in results_for_csv[key]:
                writer.writerow(['', component, results_for_csv[key][component]])
        writer.writerow([])  # Add a blank line between categories
print("CSV file 'components_coverage_results.csv' has been created with the coverage data.")
