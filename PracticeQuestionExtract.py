import nbformat
import glob
import re

practiceHeadingPattern = re.compile(r'\*\*practice\s+\w+\*\*', re.IGNORECASE)

# Step 1: Locate all notebook files in the current directory
notebook_files = glob.glob("*.ipynb")

# A list to store matching markdown cells
collected_cells = []

in_practice_section = False

# Step 2: Loop through each notebook
for nb_file in notebook_files:
    nb = nbformat.read(nb_file, as_version=4)
    
    # Step 3: Check each cell in the notebook
    for cell in nb.cells:
        # Check if the cell is a markdown cell.
        if cell.cell_type == "markdown":
            # If the markdown cell is a heading that matches "practice question"
            if practiceHeadingPattern.search(cell.source):
                in_practice_section = True  # Start capturing cells
                collected_cells.append(cell)
                continue  # Move to the next cell
            
            # If we're in a practice section and encounter another markdown heading...
            if in_practice_section and (cell.source.lstrip().startswith("*") or cell.source.lstrip().startswith("#")):
                # Check if this new heading is *not* a practice question heading.
                if not practiceHeadingPattern.search(cell.source):
                    in_practice_section = False  # End the practice section capture
            
        # If we are within a practice questions section, add the cell (whether code or markdown)
        if in_practice_section:
            collected_cells.append(cell)

# Step 4: Create a new notebook with the collected markdown cells
new_nb = nbformat.v4.new_notebook()
new_nb.cells = collected_cells

# Step 5: Save the new notebook to a file
output_filename = "extracted_practice_questions.ipynb"
with open(output_filename, "w", encoding="utf-8") as f:
    nbformat.write(new_nb, f)

print(f"Extracted markdown cells have been saved to {output_filename}")
