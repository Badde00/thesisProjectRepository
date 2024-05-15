import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'Java Resultat Analys.xlsx'
xls = pd.ExcelFile(file_path)

def get_percentage_of_correct_faults_identified(sheet_name, header_row):
  # Read specific sheet into DataFrame
  data = pd.read_excel(xls, sheet_name, header=header_row)
  
  # Convert 'Correct fault identified?' to numeric (1 for TRUE, 0 for FALSE)
  data['Correct fault identified?'] = data['Correct fault identified?'][:5].map({True: 100, False: 0})
  
  # Calculate the average
  average_correct_identified = data['Correct fault identified?'].mean()
  
  return average_correct_identified

def get_average_number_of_identified_errors(sheet_name, header_row):
  data = pd.read_excel(xls, sheet_name, header=header_row)

  data['N/o identified errors'] = pd.to_numeric(data['N/o identified errors'], errors='coerce')

  average_number_of_identified_errors = data['N/o identified errors'][:5].mean()

  return average_number_of_identified_errors

def get_percentage_of_correct_faults_identified(sheet_name, header_name, header_row):
  # Read specific sheet into DataFrame
  data = pd.read_excel(xls, sheet_name, header=header_row)
  
  # Convert 'Correct fault identified?' to numeric (1 for TRUE, 0 for FALSE)
  data[header_name] = data[header_name][:5].map({True: 100, False: 0})
  
  # Calculate the average
  average_result = data[header_name].mean()
  
  return average_result



sheets = xls.sheet_names
header_rows = {"GPT-4": 1, "CodeLLaMA": 9, "Gemini_1.0": 17 }
boolean_header_names = ["Correct fault identified?", "Error Fixed?", "Does code work?"]
all_llms = list(header_rows.keys())

results = {
  "N/o identified errors": {llm: [] for llm in all_llms},
  "Correct fault identified?": {llm: [] for llm in all_llms},
  "Error Fixed?": {llm: [] for llm in all_llms},
  "Does code work?": {llm: [] for llm in all_llms}
}

for sheet in sheets:
  for llm, header_row in header_rows.items():
    results["N/o identified errors"][llm].append(get_average_number_of_identified_errors(sheet, header_row))
    for boolean_header_name in boolean_header_names:
      results[boolean_header_name][llm].append(get_percentage_of_correct_faults_identified(sheet, boolean_header_name, header_row))


def plot_grouped_bar_chart(category_name, percentage=False):
  plt.figure(figsize=(12, 6))
  bar_width = 0.25
  index = range(len(sheets))

  colors = ['blue', 'orangered', 'green']

  for i, llm in enumerate(all_llms):
    data = results[category_name][llm]
    adjusted_data = [x+3 if percentage else x+0.2 for x in data]
    plt.bar(
      [x + i * bar_width for x in index],
      adjusted_data,
      width=bar_width,
      label=llm,
      bottom=-3 if percentage else -0.2,
      color=colors[i]
    )

  # Adjust y-axis for percentage-based graphs
  if percentage:
    plt.ylim(-3, 110)
  else:
    plt.ylim(-.2, max([max(results[category_name][llm]) for llm in all_llms]) * 1.1)

  plt.xlabel('Sheet Names (lowercase)')
  plt.ylabel(category_name)
  plt.title(f'Java - {category_name}')
  plt.xticks([x + bar_width for x in index], [sheet.lower() for sheet in sheets], rotation=-90)

  # Add a baseline bar for visibility
  plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)

  plt.legend()
  plt.grid(axis='y')
  plt.tight_layout()
  plt.show()

# Plot each graph
plot_grouped_bar_chart("N/o identified errors", percentage=False)
plot_grouped_bar_chart("Correct fault identified?", percentage=True)
plot_grouped_bar_chart("Error Fixed?", percentage=True)
plot_grouped_bar_chart("Does code work?", percentage=True)