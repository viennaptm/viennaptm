from viennaptm.modification.modification_library import ModificationLibrary


def chemspider_link(chemspider_id: str) -> str:
    if len(chemspider_id) == 0:
        return ""
    return f"`{chemspider_id} <https://www.chemspider.com/Chemical-Structure.{chemspider_id}.html>`_"


def pubchem_link(pubchem_id: str) -> str:
    if len(pubchem_id) == 0:
        return ""
    return f"`{pubchem_id} <https://pubchem.ncbi.nlm.nih.gov/compound/{pubchem_id}>`_"


# instantiate modification library and obtain dataframe
ModificationLibrary = ModificationLibrary()
modification_metadata_df = ModificationLibrary._get_modification_metadata_df()
modification_metadata_df = modification_metadata_df.fillna(value="")

complete_string = ""
for idx, row in modification_metadata_df.iterrows():
    complete_string = complete_string + ("   * - " + row["original_abbreviation"] +
                                         "\n     - " + row["modified_abbreviation"] +
                                         "\n     - " + row["target_name"] +
                                         #"\n     - " + row["target_smiles"] +
                                         "\n     - " + pubchem_link(row["pubchem_id"]) +
                                         "\n     - " + chemspider_link(row["chemspider_id"]) + "\n")

# write string to file (not version controlled)
tmp = "./ptms_to_rst_table.temp_rst"
with open(tmp, 'w') as f:
    f.write(complete_string)

