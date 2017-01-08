[![Gratipay User](https://img.shields.io/gratipay/user/dzaiats.svg)](https://gratipay.com/~dzaiats/)

# Automotion #
![alt tag](https://www.itarray.net/wp-content/uploads/2016/12/Automotion-2.jpg)

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
                   .change_metrics_units_to(Units.PERCENT)
                   .width_between(50, 55)
                   .heigh_between(90, 95)
                   .draw_map()
                   .validate();
            
            
            ui_validator.generate_report("Report name");
            
 - Description for each methods available in the framework:
    
    * Init method:
    
            init(); // Method that defines start of new validation. Needs to be called each time before calling findElement(), findElements()
            
            init("Scenario name"); // Method that defines start of new validation with specified name of scenario. Needs to be called each time before calling findElement(), findElements()
            
            find_element(WebElement element, String readableNameOfElement); // Main method to specify which element we want to validate (can be called only findElement() OR findElements() for single validation)
            
            find_elements(List<WebElement> elements); // Main method to specify the list of elements that we want to validate (can be called only findElement() OR findElements() for single validation)
    
    * For single element findElement({element}, "name"):
    
            inside_of(WebElement containerElement, String readableContainerName); // Verify that element is located inside of specified element
                 
            with_left_element(WebElement element, int minMargin, int maxMargin); // Verify that element which located left to is correct with specified margins
                
            with_right_element(WebElement element, int minMargin, int maxMargin); // Verify that element which located right to is correct with specified margins
                
            with_top_element(WebElement element, int minMargin, int maxMargin); // Verify that element which located top to is correct with specified margins
                
            with_bottom_element(WebElement element, int minMargin, int maxMargin); // Verify that element which located bottom to is correct with specified margins
        
            not_overlap_with(WebElement(s) element, String readableName); // Verify that element is NOT overlapped with specified element
        
            overlap_with(WebElement(s) element, String readableName); // Verify that element is overlapped with specified element
                
            same_offset_left_as(WebElement element(s), String readableName); // Verify that element has the same left offset as specified element
        
            same_offset_right_as(WebElement element(s), String readableName); // Verify that element has the same right offset as specified element
        
            same_offset_top_as(WebElement element(s), String readableName); // Verify that element has the same top offset as specified element
        
            same_offset_bottom_as(WebElement element(s), String readableName); // Verify that element has the same bottom offset as specified element
        
            same_width_as(WebElement element(s), String readableName); // Verify that element has the same width as specified element
                
            min_width(int width); // Verify that width of element is not less than specified
        
            max_width(int width); // Verify that width of element is not bigger than specified
        
            width_between(int min, int max); // Verify that width of element is in range
        
            same_heightAs(WebElement element, String readableName); // Verify that element has the same height as specified element
        
            same_heightAs(List<WebElement> elements); // Verify that element has the same height as every element in the list
        
            min_height(int height); // Verify that height of element is not less than specified
        
            max_height(int height); // Verify that height of element is not bigger than specified
        
            same_size_as(WebElement element(s), String readableName); // Verify that element has the same size as specified element
                
            height_between(int min, int max); // Verify that height of element is in range
        
            min_offset(int top, int right, int bottom, int left); // Verify that min offset of element is not less than (min value is -10000)
        
            max_offset(int top, int right, int bottom, int left); // Verify that max offset of element is not bigger than (min value is -10000)
        
            with_css_value(String cssProperty, String... args); // Verify that element has correct CSS values
        
            without_css_value(String cssProperty, String... args); // Verify that concrete CSS values are absent for specified element
        
            equal_left_right_offset(); // Verify that element has equal left and right offsets (e.g. Bootstrap container)
        
            equal_top_bottom_offset(); // Verify that element has equal top and bottom offset (aligned vertically in center)
         
            change_metrics_units_to(ResponsiveUIValidator.Units units); // Change units to Pixels or % (Units.PX, Units.PERCENT)

    * For list of elements findElements({element}):
            
            inside_of(WebElement containerElement, String readableContainerName); // Verify that elements are located inside of specified element
            
            aligned_as_grid(int horizontalGridSize); // Verify that elements are aligned in a grid view width specified amount of columns
            
            aligned_as_grid(int horizontalGridSize, int verticalGridSize); // Verify that elements are aligned in a grid view width specified amount of columns and rows
            
            are_not_overlapped_with_each_other(); // Verify that every element in the list is not overlapped with another element from this list
            
            with_same_size(); // Verify that elements in the list have the same size
            
            with_same_width(); // Verify that elements in the list have the same width
            
            with_same_height(); // Verify that elements in the list have the same height
            
            same_right_offset(); // Verify that elements in the list have the right offset
            
            same_left_offset(); // Verify that elements in the list have the same left offset
            
            same_top_offset(); // Verify that elements in the list have the same top offset
            
            same_bottom_offset(); // Verify that elements in the list have the same bottom offset
            
            equal_left_right_offset(); // Verify that every element in the list have equal right and left offset (aligned horizontally in center)
            
            equal_top_bottom_offset(); // Verify that every element in the list have equal top and bottom offset (aligned vertically in center)
            
            change_metrics_units_to(ResponsiveUIValidator.Units units); // Change units to Pixels or % (Units.PX, Units.PERCENT)
           
    * Generating results:
    
            draw_map(); // Methods needs to be called to collect all the results in JSON file and screenshots
            
            validate(); // Call method to summarize and validate the results (can be called with drawMap(). In this case result will be only True or False)
            
            generate_report(); // Call method to generate HTML report
            
            generate_report("file report name"); // Call method to generate HTML report with specified file report name

