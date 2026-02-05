API
============


.. code-block:: python

   # make an instance of the Modifier() class
   modifier = Modifier()

   # apply the modification to the modifier
   structure = modifier.apply_modification(structure=structure,
                                           chain_identifier='A',
                                           residue_number=50,
                                           target_abbreviation="V3H")

