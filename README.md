# Borderlands 2 Anarchy Saver

## Features
- Saves a customizable percentage of your Anarchy stacks between save quits
- Allows you to remove the Anarchy cap
- Adds keybinds to add Anarchy, subtract Anarchy, and display current Anarchy (useful when over 999 stacks as the game does not display more than 3 digits with the exception of thin numbers like 1011)


## Version History
- 1.1 (current)
    - Adjusted user-facing descriptions
    - Added 'Display Current Anarchy' keybind 
    - Added 'Display Anarchy Past 999' option
    - Changing the 'Uncap Anarchy' option no longer requires a save quit to apply
    - Added the `set_anarchy` function. If you want to use it instead of the keybinds, in the Borderlands 2 console use `py from AnarchySaver import set_anarchy` and then `py set_anarchy(desired_stack_count)` (the function must be imported again every time you launch the game)
- 1.0.1
    - Adjusted user-facing descriptions
    - Fixed the .sdkmod file
- 1.0
    - Initial release


## Known Issues
- Due to floating point inaccuracy, Anarchy will not naturally stack higher than 16,777,216. To bypass this, you must use the 'Add Anarchy' keybind or import and use the `set_anarchy` function. This is the game's issue and not mine. Fixing this is possible, but adjusting the increment of stack gain and loss is a lot of work in determining each of which of the 24 Behavior_SimpleMath calls in the Anarchy BehaviorProviderDefinition correspond to gain or loss of stacks, as well as if Typecast Iconoclast is handled separately. I know some, but checking each and every one in several situations is time consuming for an issue that is both circumventable using the tools I've provided and unlikely to be experienced by anybody in the first place. 29,360,128% damage up is probably enough
- Discord doesn't actually drain your Anarchy if you activate it with 750 or more stacks. This is the game's issue and not mine