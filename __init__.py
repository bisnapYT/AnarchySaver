import mods_base, unrealsdk
from save_options.options import HiddenSaveOption
from save_options.registration import register_save_options
from typing import Any

saved_anarchy = HiddenSaveOption("anarchy", 0)
def on_save():
    try:
        if unrealsdk.find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks').GetValue(mods_base.get_pc())[0] > 0.0:
            saved_anarchy.value = unrealsdk.find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks').GetValue(mods_base.get_pc())[0]
    except:
        return

def on_load():
    try:
        if unrealsdk.find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_StackCap').GetValue(mods_base.get_pc())[0] > 0.0:
            unrealsdk.find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks').SetAttributeBaseValue(mods_base.get_pc(), saved_anarchy.value)
    except:
        return

mod = mods_base.build_mod()
register_save_options(mod)