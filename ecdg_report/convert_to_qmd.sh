#!/bin/bash

# Directory where all .qmd files will be written
#OUTPUT_DIR="../qmd"

# Ensure the output directory exists
#mkdir -p "$OUTPUT_DIR"

# List of notebooks to convert — replace these with your actual file paths
notebooks=(
#    "./about.ipynb"
    "./datasets/Climate_Dataset_Overview.ipynb"
    "./datasets/climate_projection_data/Climate_Projection_Datasets.ipynb"
    "./datasets/climate_projection_data/ESPO-G6_Dataset.ipynb"
    "./datasets/observed_data/AHCCD_Station_Data.ipynb"
    "./datasets/observed_data/NRCanMET_Gridded_Data.ipynb"
    "./datasets/observed_data/Observational_Datasets.ipynb"
    "./datasets/reanalysis_data/CaSR.ipynb"
    "./datasets/reanalysis_data/ERA5-Land.ipynb"
    "./datasets/reanalysis_data/Reanalysis_Datasets.ipynb"
    "./datasets/tools/Analysis_Support_Tools.ipynb"
    "./datasets/tools/Point_Location_Compare.ipynb"
    "./FullReport_MSWord.ipynb"
#    "./index.ipynb"
    "./Introduction.ipynb"
    "./literature_review/demand.ipynb"
    "./sectors/capacity_expansion_modelling.ipynb"
    "./sectors/construction.ipynb"
    "./sectors/dam_safety_review.ipynb"
    "./sectors/demand_forecasting.ipynb"
    "./sectors/demand.ipynb"
    "./sectors/electrical_system_operations.ipynb"
    "./sectors/electricity_sector_activities.ipynb"
    "./sectors/enterprise_risk_management.ipynb"
    "./sectors/esg_and_sustainability_reporting.ipynb"
    "./sectors/forest_fire_monitoring_and_awareness.ipynb"
    "./sectors/generation_forecasting.ipynb"
    "./sectors/infrastructure_condition_assessment_and_investment_prioritization.ipynb"
    "./sectors/infrastructure_condition_assessment.ipynb"
    "./sectors/infrastructure_design.ipynb"
    "./sectors/innovation_investments.ipynb"
    "./sectors/licensing_and_impact-environmental_assessments.ipynb"
    "./sectors/nuclear_safety_review.ipynb"
    "./sectors/outage_scheduling.ipynb"
    "./sectors/proactive_management_of_heavily_loaded_assets.ipynb"
    "./sectors/resource_adequacy_planning.ipynb"
    "./sectors/support_supply_chain_decision-making.ipynb"
    "./sectors/vegetation_management.ipynb"
    "./sectors/worker_safety.ipynb"
)

# Convert each notebook to .qmd using the --output flag
for notebook in "${notebooks[@]}"; do
  if [[ -f "$notebook" ]]; then
    dir=$(dirname "$notebook")
    base=$(basename "$notebook" .ipynb)
    output_path="${dir}/${base}.qmd"
    echo "Converting $notebook -> $output_path"
    quarto convert "$notebook" --output "$output_path"
  else
    echo "File not found: $notebook"
  fi
done
