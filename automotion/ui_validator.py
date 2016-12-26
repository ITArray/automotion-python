import time

from responsive_ui_validator import ResponsiveUIValidator


class UIValidator(ResponsiveUIValidator):
    def __init__(self, driver, element, element_name):
        ResponsiveUIValidator.__init__(self, driver)
        self.root_element = element
        self.root_element_name = element_name
        self.x_root = element.location['x']
        self.y_root = element.location['y']
        self.width_root = element.size['width']
        self.height_root = element.size['height']
        self.page_width = int(self.get_page_width())
        self.page_height = int(self.get_page_height())
        self.start_time = time.mktime(time.gmtime())

    def change_metrics_units(self, units):
        self.units = units
        return self

    def with_left_element(self, element, min_margin=None, max_margin=None):
        self.validate_left_element(element, min_margin, max_margin)
        return self

    def with_right_element(self, element, min_margin=None, max_margin=None):
        self.validate_right_element(element, min_margin, max_margin)
        return self

    def with_top_element(self, element, min_margin=None, max_margin=None):
        self.validate_top_element(element, min_margin, max_margin)
        return self

    def with_bottom_element(self, element, min_margin=None, max_margin=None):
        self.validate_bottom_element(element, min_margin, max_margin)
        return self

    def not_overlap_with(self, element_s, element_name=None):
        self.validate_not_overlapping_with_elements(element_s, element_name)
        return self

    def overlap_with(self, element_s, element_name=None):
        self.validate_overlapping_with_elements(element_s, element_name)
        return self

    def same_offset_left_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_left_offset_for_elements(element, self.get_formatted_message(element))
        else:
            self.validate_left_offset_for_elements(element_s, element_name)
        self.draw_left_offset_line = True
        return self

    def same_offset_right_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_right_offset_for_elements(element, self.get_formatted_message(element))
        else:
            self.validate_right_offset_for_elements(element_s, element_name)
        self.draw_right_offset_line = True
        return self

    def same_offset_top_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_top_offset_for_elements(element, self.get_formatted_message(element))
        else:
            self.validate_top_offset_for_elements(element_s, element_name)
        self.draw_top_offset_line = True
        return self

    def same_offset_bottom_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_bottom_offset_for_elements(element, self.get_formatted_message(element))
        else:
            self.validate_bottom_offset_for_elements(element_s, element_name)
        self.draw_bottom_offset_line = True
        return self

    def same_width_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_same_width(element, self.get_formatted_message(element))
        else:
            self.validate_same_width(element_s, element_name)
        return self

    def min_width(self, width):
        self.validate_min_width(self.get_converted_int(width, True))
        return self

    def max_width(self, width):
        self.validate_max_width(self.get_converted_int(width, True))
        return self

    def width_between(self, min, max):
        self.validate_min_width(self.get_converted_int(min, True))
        self.validate_max_width(self.get_converted_int(max, True))
        return self

    def same_height_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_same_height(element, self.get_formatted_message(element))
        else:
            self.validate_same_height(element_s, element_name)
        return self

    def min_height(self, height):
        self.validate_min_height(self.get_converted_int(height, False))
        return self

    def max_height(self, height):
        self.validate_max_height(self.get_converted_int(height, False))
        return self

    def height_between(self, min, max):
        self.validate_min_height(self.get_converted_int(min, False))
        self.validate_max_height(self.get_converted_int(max, False))
        return self

    def same_size_as(self, element_s, element_name=None):
        if element_name is None:
            for element in element_s:
                self.validate_same_size(element, self.get_formatted_message(element))
        else:
            self.validate_same_size(element_s, element_name)
        return self

    def min_offset(self, top, right, bottom, left):
        if self.get_converted_int(top, False) > self.MIN_OFFSET \
                and self.get_converted_int(right, True) > self.MIN_OFFSET \
                and self.get_converted_int(bottom, False) > self.MIN_OFFSET \
                and self.get_converted_int(left, True) > self.MIN_OFFSET:
            self.validate_min_offset(self.get_converted_int(top, False),
                                     self.get_converted_int(right, True),
                                     self.get_converted_int(bottom, False),
                                     self.get_converted_int(left, True))
        return self

    def max_offset(self, top, right, bottom, left):
        if self.get_converted_int(top, False) > self.MIN_OFFSET \
                and self.get_converted_int(right, True) > self.MIN_OFFSET \
                and self.get_converted_int(bottom, False) > self.MIN_OFFSET \
                and self.get_converted_int(left, True) > self.MIN_OFFSET:
            self.validate_max_offset(self.get_converted_int(top, False),
                                     self.get_converted_int(right, True),
                                     self.get_converted_int(bottom, False),
                                     self.get_converted_int(left, True))
        return self

    def equal_left_right_offset(self):
        self.validate_equal_left_right_offset(self.root_element, self.root_element_name)
        return self

    def equal_top_bottom_offset(self):
        self.validate_equal_top_bottom_offset(self.root_element, self.root_element_name)
        return self

    def inside_of(self, element, element_name):
        self.validate_inside_of_container(element, element_name)

