import mods_base
from mods_base import get_pc, SliderOption, keybind, BoolOption
from unrealsdk import find_object
from save_options.options import HiddenSaveOption
from save_options.registration import register_save_options


def get_anarchy_attrs():
    try:
        return (
            find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks'),
            find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_StackCap')
        )
    except ValueError:
        return None, None

stack_uncap = BoolOption(
    identifier="Uncap Anarchy Stacks",
    value=False,
    description="'On' sets Anarchy cap to inf whenever loading from the main menu. 'Off' allows the game to sanity check based on your skill tree and will apply after the next load from the main menu."
)
def uncap_anarchy():
    _, stack_cap_attr = get_anarchy_attrs()
    if stack_cap_attr:
        stack_cap_attr.SetAttributeBaseValue(get_pc(), float('inf'))

anarchy_multiplier = SliderOption(
    identifier="Percentage of Anarchy to restore",
    value=100,
    is_integer=True,
    min_value=0,
    max_value=100,
    description="Multiplies your saved anarchy value by specified percentage when loading the game."
)

anarchy_keys = SliderOption(
    identifier="Anarchy stack change with keybinds",
    value=50,
    is_integer=True,
    min_value=1,
    max_value=600,
    description="How much Anarchy is added or subtracted when activating the corresponding keybinds. Will not add Anarchy above your cap or subtract to below 0."
)
def get_anarchy_key_value():
    return anarchy_keys.value

@keybind("Add Anarchy")
def add_anarchy_key_pressed():
    num_stacks_attr, stack_cap_attr = get_anarchy_attrs()
    if num_stacks_attr and stack_cap_attr:
        stacks, *_ = num_stacks_attr.GetValue(get_pc())
        if (stacks + get_anarchy_key_value()) > stack_cap_attr.GetValue(get_pc())[0]:
            num_stacks_attr.SetAttributeBaseValue(get_pc(), stack_cap_attr.GetValue(get_pc())[0])
        else:
            num_stacks_attr.SetAttributeBaseValue(get_pc(), stacks + get_anarchy_key_value())

@keybind("Subtract Anarchy")
def subtract_anarchy_key_pressed():
    num_stacks_attr, *_ = get_anarchy_attrs()
    if num_stacks_attr:
        stacks, *_ = num_stacks_attr.GetValue(get_pc())
        if (stacks - get_anarchy_key_value()) < 0:
            num_stacks_attr.SetAttributeBaseValue(get_pc(), 0)
        else:
            num_stacks_attr.SetAttributeBaseValue(get_pc(), stacks - get_anarchy_key_value())

save_file_name = HiddenSaveOption("workaround_value", 0)
saved_anarchy = HiddenSaveOption("anarchy", 0)
def on_save():
    num_stacks_attr, *_ = get_anarchy_attrs()
    stacks = 0.0
    if num_stacks_attr:
        stacks, *_ = num_stacks_attr.GetValue(get_pc())
        save_file_name.value = get_pc().GetSaveGameNameFromId(0)
        if stacks >= 0.0:
            saved_anarchy.value = stacks
        else:
            saved_anarchy.value = 0

def on_load():
    correct_save = (save_file_name.value == get_pc().GetSaveGameNameFromId(0))
    num_stacks_attr, stack_cap_attr = get_anarchy_attrs()
    if num_stacks_attr and stack_cap_attr:
        if saved_anarchy.value == float('inf'):
            modified_anarchy = saved_anarchy.value
        else:
            modified_anarchy = round(saved_anarchy.value * anarchy_multiplier.value / 100)
            
        if stack_uncap.value and (correct_save):
            uncap_anarchy()
            num_stacks_attr.SetAttributeBaseValue(get_pc(), modified_anarchy)
        elif not stack_uncap.value and (correct_save):
            if modified_anarchy > stack_cap_attr.GetValue(get_pc())[0]:
                num_stacks_attr.SetAttributeBaseValue(get_pc(), stack_cap_attr.GetValue(get_pc())[0])
            else:
                num_stacks_attr.SetAttributeBaseValue(get_pc(), modified_anarchy)

mod = mods_base.build_mod()
register_save_options(mod)