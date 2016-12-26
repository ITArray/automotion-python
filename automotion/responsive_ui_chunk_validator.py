import time

from automotion.responsive_ui_validator import ResponsiveUIValidator


class ResponsiveUIChunkValidator(ResponsiveUIValidator):
    def __init__(self, driver, elements):
        ResponsiveUIValidator.__init__(self, driver)
        self.root_elements = elements
        self.page_width = int(self.get_page_width())
        self.page_height = int(self.get_page_height())
        self.root_element = elements[0]
        self.start_time = time.mktime(time.gmtime())

    def change_metrics_units(self, units):
        self.units = units
        return self

    def aligned_as_grid(self, columns, rows=0):
        self.validate_grid_alignment(columns, rows)
        return self

    def are_not_overlapped_with_each_other(self):
        self.validate_elements_are_not_overlapped(self.root_elements)
        return self

    def with_same_size(self):
        self.validate_same_size(self.root_elements, 0)
        return self

    def with_same_width(self):
        self.validate_same_size(self.root_elements, 1)
        return self

    def with_same_height(self):
        self.validate_same_size(self.root_elements, 2)
        return self

    def same_right_offset(self):
        self.validate_right_offset_for_chunk(self.root_elements)
        return self

    def same_left_offset(self):
        self.validate_left_offset_for_chunk(self.root_elements)
        return self

    def same_top_offset(self):
        self.validate_top_offset_for_chunk(self.root_elements)
        return self

    def same_bottom_offset(self):
        self.validate_bottom_offset_for_chunk(self.root_elements)
        return self

    def equal_left_right_offset(self):
        self.validate_equal_left_right_offset(self.root_elements)
        return self

    def equal_top_bottom_offset(self):
        self.validate_equal_top_bottom_offset(self.root_elements)
        return self

    def inside_of(self, element, readable_name):
        self.validate_inside_of_container(element, readable_name)
        return self
