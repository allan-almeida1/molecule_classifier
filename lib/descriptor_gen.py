#!/usr/bin/env python

from rdkit import Chem, DataStructs
import numpy as np
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors


class DescriptorGen:
    def __init__(self, desc_type="all"):
        if desc_type not in ["all", "fp", "desc"]:
            raise ValueError("desc_type  must be one of [all,fp,desc]")
        self.desc_type = desc_type
        self.property_names = list(
            rdMolDescriptors.Properties.GetAvailableProperties())
        self.property_getter = rdMolDescriptors.Properties(self.property_names)

    def from_smiles(self, smi):
        mol = Chem.MolFromSmiles(smi)
        if mol:
            return self.from_mol(mol)
        else:
            return None

    def from_mol(self, mol):
        arr = np.array([])
        if self.desc_type in ["all", "fp"]:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
            arr = np.zeros((0,), dtype=np.int8)
            DataStructs.ConvertToNumpyArray(fp, arr)
        props = np.array([])
        if self.desc_type in ["all", "desc"]:
            props = np.array(self.property_getter.ComputeProperties(mol))
        return np.append(arr, props)

 
if __name__ == "__main__":
    descriptor_gen = DescriptorGen("desc")
    desc = descriptor_gen.from_smiles("CCCC")
    print(len(desc), desc)
