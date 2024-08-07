# Automating Item Specifications from Range Achievement Level Descriptors (RALDs) to Support Item Writing

* To reduce costs, this process is developped to automatically generate item specifications using Python and LaTex.

* Item templates are created so that any iteration in the RALDs will automatically ramify into downstream documents.

* This automation helps content experts create item templates/item specifications efficiently.

  

## Getting Started

### Inputs:

⎼ g6_sample_for_NCME.xlsx (data file)
⎼ Item_spec_template.TeX (LaTex file specifying the item specification template)
⎼ Verb_table_template.TeX (LaTex file specifying the verb and corresponding item format template) 

### Process file:

⎼ Item_spec.py

### Output files:

⎼ Item_spec_updated.TeX (One file per Indicator_ID)

⎼ Verb_table_updated.TeX


### Installing

* Jinja2, pandas, numpy and os

* LaTex
### Executing program

* Open the python code (item_spec.py) in jupyter notebooks, spyder, or your preferred environment for python and run




