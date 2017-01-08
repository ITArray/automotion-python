# Automotion-Python
Python version of Automotion library

### Responsive UI Validation ###
 - Responsive UI Validator allows to validate UI on web or mobile page using lots of criterias. Also it allows tu build thr HTMl report after validation.
            
            ui_validator = ResponsiveUIValidator(driver);
            
            
            result = ui_validator.init("Scenario name")
                   .find_element({rootEelement}, "Name of element")
                   .same_offset_left_as({element} "Panel 1")
                   .same_offset_left_as({element} "Button 1")
                   .same_offset_right_as({element} "Button 2")
                   .same_offset_right_as({element}, "Button 3)
                   .with_css_value("border", "2px", "solid", "#FBDCDC")
                   .with_css_value("border-radius", "4px")
                   .without_cssValue("color", "#FFFFFF")
                   .same_size_as({list_elements},)
                   .inside_of({element}, "Container")
                   .not_overlap_with({element}, "Other element")
                   .with_top_element({element}, 10, 15)
                   .change_metrics_units_to(ResponsiveUIValidator.Units.PERCENT)
                   .width_between(50, 55)
                   .heigh_between(90, 95)
                   .draw_map()
                   .validate();
            
            
            ui_validator.generate_report("Report name");
