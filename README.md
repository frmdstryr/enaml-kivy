# About
A Kivy widget toolkit for Enaml. Allows you to use the power of Enaml (Conditionals, Loopers, etc..) with Kivy apps!

# Why
_Why do this when Kivy lang already exists?_ 

1. Kivy lang at the moment cannot dynamically create and remove widgets without manually doing so in python. Enaml can do this using patterns such as Conditonal and Loopers.  Enaml's approach is much cleaner.
2. Enaml has more flexibility for bindings using the `<<`, `::`, and `:=` operators.  

# How
This project creates the required Enaml classes based on the Kivy widget properties.  New and custom widgets can easily be used in enaml. 

# Usage
See examples folder.

#### Differences between Kivy lang and Enaml ####

##### Referencing widgets by ID #####
For referencing other widgets instead of using `id: <widget_id>` use the enaml naming construct `Widget: <widget_id>:`. 

When doing this note that the reference is an Enaml control object NOT a Kivy widget. To get a reference to the actual Kivy widget from the enaml reference use `<ref_name>.proxy.widget`.  Kivy widget methods are proxied to make this easier.  

##### Widgets with no custom attributes #####
In enaml all widgets must have a block of code. In Kivy lang you can do 

```python

ActionBar:
    # etc...
    ActionSpacer: # This has no properties
    ActionButon:
        # etc...

```
 
 Enaml requires you use the `pass` keyword. 

 ```python

ActionBar:
    # etc...
    ActionSpacer:
        pass # This has no properties
    ActionButon:
        # etc...
```


## Issues ##

Enaml's constraints system is not yet implemented, so you must use Kivy's layouts. 

