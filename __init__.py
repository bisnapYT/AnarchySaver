import mods_base
from mods_base import get_pc, SliderOption, keybind, BoolOption
from unrealsdk import find_object, hooks, unreal
from ui_utils import show_hud_message
from math import inf
from typing import Any
from save_options.options import HiddenSaveOption
from save_options.registration import register_save_options

def get_anarchy_attrs():
    try:
        return (
            find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks'),
            find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks').GetValue(get_pc())[0],
            find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_StackCap'),
            find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_StackCap').GetValue(get_pc())[0]
        )
    except ValueError:
        return None, None, None, None

def set_anarchy(stack: int|float):
    find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks').SetAttributeBaseValue(get_pc(), stack)

def uncap_anarchy():
    *_, stack_cap_attr, _ = get_anarchy_attrs()
    if stack_cap_attr:
        stack_cap_attr.SetAttributeBaseValue(get_pc(), inf)

def cap_anarchy():
    _, num_stacks, stack_cap_attr, stack_cap = get_anarchy_attrs()
    if stack_cap_attr and num_stacks is not None and stack_cap is not None:
        stack_cap_attr.SetAttributeBaseValue(get_pc(), 0)
        stack_cap = find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_StackCap').GetValue(get_pc())[0]
        if num_stacks > stack_cap:
                set_anarchy(stack_cap)

@mods_base.hook(
        "WillowGame.Behavior_SimpleMath:ApplyBehaviorToContext",
        hook_type=hooks.Type.POST
)
def simple_math(
    caller: unreal.UObject,
    args: unreal.WrappedStruct,
    return_value: Any,
    function: unreal.BoundFunction
) -> None:
    if not caller._path_name().startswith("GD_Tulip_Mechromancer_Skills.EmbraceChaos.Anarchy:BehaviorProviderDefinition_0"):
        return
    num_stacks = int(find_object('DesignerAttributeDefinition', 'GD_Tulip_Mechromancer_Skills.Misc.Att_Anarchy_NumberOfStacks').GetValue(get_pc())[0])
    if num_stacks == 999:
        get_pc().GetHUDMovie().ClearTrainingText()
    if num_stacks > 999:
        get_pc().GetHUDMovie().AddTrainingText(
            MessageString = f"{num_stacks:,}",
            TitleString = "Current Anarchy",
            Duration = inf,
            DrawColor = unreal.IGNORE_STRUCT,
            HUDInitializationFrame = "",
            PausesGame = False,
            PauseContinueDelay = 0,
            Related_PRI1 = get_pc().PlayerReplicationInfo,
            bIsntActuallyATrainingMessage = True
        )

def toggle_anarchy_cap(option: BoolOption, value: bool):
    if value:
        uncap_anarchy()
    else:
        cap_anarchy()

def toggle_anarchy_display(option: BoolOption, value: bool):
    if value:
        simple_math.enable()
    else:
        simple_math.disable()

stack_uncap = BoolOption(
    identifier="Uncap Anarchy Stacks",
    value=False,
    description="'On' sets your Anarchy cap to infinity. 'Off' allows the game to set your Anarchy cap as normal.",
    on_change=toggle_anarchy_cap
)

display_anarchy = BoolOption(
    identifier="Display Anarchy Past 999",
    value=False,
    description="As long as you have more than 999 Anarchy, a persistent HUD message shows your current stack count.",
    on_change=toggle_anarchy_display
)

anarchy_multiplier = SliderOption(
    identifier="Percentage of Anarchy to restore",
    value=100,
    is_integer=True,
    min_value=0,
    max_value=100,
    description="Multiplies your saved Anarchy value by the specified percentage when loading the game."
)

anarchy_keys = SliderOption(
    identifier="Anarchy stack change with keybinds",
    value=50,
    is_integer=True,
    min_value=1,
    max_value=600,
    description="How much Anarchy is added or subtracted when using the corresponding keybinds. Will not add Anarchy above your cap or subtract to below 0."
)
def get_anarchy_key_value():
    return anarchy_keys.value

@keybind("Add Anarchy")
def add_anarchy_key_pressed():
    num_stacks_attr, num_stacks, stack_cap_attr, stack_cap = get_anarchy_attrs()
    if num_stacks_attr and num_stacks is not None and stack_cap_attr and stack_cap is not None:
        if (num_stacks + get_anarchy_key_value()) > stack_cap:
            set_anarchy(stack_cap)
        else:
            set_anarchy(num_stacks + get_anarchy_key_value())

@keybind("Subtract Anarchy")
def subtract_anarchy_key_pressed():
    num_stacks_attr, num_stacks, *_ = get_anarchy_attrs()
    if num_stacks_attr and num_stacks is not None:
        if (num_stacks - get_anarchy_key_value()) < 0:
            set_anarchy(0)
        else:
            set_anarchy(num_stacks - get_anarchy_key_value())

@keybind("Display Current Anarchy")
def display_anarchy_key_pressed():
    num_stacks_attr, num_stacks, *_ = get_anarchy_attrs()
    if num_stacks_attr and num_stacks is not None:
        num_stacks = int(num_stacks)
        show_hud_message("Current Anarchy", f"{num_stacks:,}")

save_file_name = HiddenSaveOption("workaround_value", 0)
saved_anarchy = HiddenSaveOption("anarchy", 0)
def on_save():
    num_stacks_attr, num_stacks, *_ = get_anarchy_attrs()
    if num_stacks_attr and num_stacks is not None:
        save_file_name.value = get_pc().GetSaveGameNameFromId(0)
        if num_stacks >= 0.0:
            saved_anarchy.value = num_stacks
        else:
            saved_anarchy.value = 0

def on_load():
    correct_save = (save_file_name.value == get_pc().GetSaveGameNameFromId(0))
    num_stacks_attr, _, stack_cap_attr, stack_cap = get_anarchy_attrs()
    if num_stacks_attr and stack_cap_attr and stack_cap is not None:
        if saved_anarchy.value == inf:
            modified_anarchy = saved_anarchy.value
        else:
            modified_anarchy = round(saved_anarchy.value * anarchy_multiplier.value / 100)
            
        if stack_uncap.value and (correct_save):
            uncap_anarchy()
            set_anarchy(modified_anarchy)
        elif not stack_uncap.value and (correct_save):
            if modified_anarchy > stack_cap:
                set_anarchy(stack_cap)
            else:
                set_anarchy(modified_anarchy)

def on_enable() -> None:
    toggle_anarchy_cap(stack_uncap, stack_uncap.value)
    toggle_anarchy_display(display_anarchy, display_anarchy.value)
mod = mods_base.build_mod(
    keybinds = [add_anarchy_key_pressed, subtract_anarchy_key_pressed, display_anarchy_key_pressed],
    options = [anarchy_multiplier, anarchy_keys, stack_uncap, display_anarchy]
    )
register_save_options(mod)