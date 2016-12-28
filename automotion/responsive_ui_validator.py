import json
import os

import time

import uuid as uuid

from automotion.units import Units
from automotion.html_builder import HtmlReportBuilder
from constants import Constants
from PIL import Image, ImageFont, ImageDraw


class ResponsiveUIValidator:
    MIN_OFFSET = -10000
    driver = None
    root_element = None
    root_elements = None
    root_element_name = "List of elements"
    screenshot_path = ""
    scenario_name = "Default"
    sn = {Constants.SCENARIO: "Default"}
    units = Units.PX
    with_report = False
    error_message = []
    json_files = []
    page_width = 0
    page_height = 0
    height_root = 0
    width_root = 0
    x_root = 0
    y_root = 0
    start_time = 0
    draw_left_offset_line = False
    draw_right_offset_line = False
    draw_top_offset_line = False
    draw_bottom_offset_line = False

    def __init__(self, driver):
        self.driver = driver
        self.error_message = []

    def init(self, scenario_name=None):
        self.sn[Constants.SCENARIO] = scenario_name
        return self

    def find_element(self, root_element, element_name):
        from automotion.ui_validator import UIValidator
        return UIValidator(self.driver, root_element, element_name)

    def find_elements(self, root_elements):
        from automotion.responsive_ui_chunk_validator import ResponsiveUIChunkValidator
        return ResponsiveUIChunkValidator(self.driver, root_elements)

    def change_metrics_units(self, units):
        self.units = units
        return self

    def draw_map(self):
        self.with_report = True
        # http://matthiaseisen.com/pp/patterns/p0203/ - example of how to draw on picture
        return self

    def validate(self):
        json_results = {Constants.ERROR_KEY: False}

        if self.root_element is not None:
            if len(self.error_message) > 0:
                json_results[Constants.ERROR_KEY] = True
                json_results[Constants.DETAILS] = self.error_message

                if self.with_report:
                    if not os.path.exists(Constants.OUTPUT_AUTOMOTION_IMG):
                        os.makedirs(Constants.OUTPUT_AUTOMOTION_IMG)
                    screenshot_name = "{name}-{time}.png".format(name=self.root_element_name.replace(" ", "_"),
                                                                 time=time.mktime(time.gmtime()))
                    self.screenshot_path = "{dir}{name}".format(dir=Constants.OUTPUT_AUTOMOTION_IMG,
                                                                 name=screenshot_name)
                    try:
                        self.driver.save_screenshot(self.screenshot_path)
                    except:
                        pass

                    root_details = {Constants.X: self.x_root, Constants.Y: self.y_root,
                                    Constants.WIDTH: self.width_root, Constants.HEIGHT: self.height_root}

                    json_results[Constants.SCENARIO] = self.sn[Constants.SCENARIO]
                    json_results[Constants.ROOT_ELEMENT] = root_details
                    json_results[Constants.TIME_EXECUTION] = str(
                        str(int(time.mktime(time.gmtime())) - int(self.start_time)) + " seconds")
                    json_results[Constants.ELEMENT_NAME] = self.root_element_name
                    json_results[Constants.SCREENSHOT] = screenshot_name

                    ms = time.mktime(time.gmtime())
                    uuid_str = str(uuid.uuid4())[0:7]
                    json_file_name = self.root_element_name.replace(" ", "_") + "-automotion" + str(ms) + uuid_str + ".json"

                    if not os.path.exists(Constants.OUTPUT_AUTOMOTION_JSON):
                        os.makedirs(Constants.OUTPUT_AUTOMOTION_JSON)
                    f = open(Constants.OUTPUT_AUTOMOTION_JSON + json_file_name, "w")
                    json.dump(json_results, f)
                    f.close()
                    self.json_files.append(json_file_name)

                    if bool(json_results[Constants.ERROR_KEY] is True):
                        self.draw_screenshot()
        else:
            json_results[Constants.ERROR_KEY] = True
            json_results[Constants.DETAILS] = "Set root web element"

        return not bool(json_results[Constants.ERROR_KEY] is True)

    def validate_grid_alignment(self, columns, rows):
        if self.root_elements is not None:
            map = {}
            for el in self.root_elements:
                y = el.location['y']
                if map.get(y) is None:
                    map[y] = 1
                else:
                    c = map[y]
                    c += 1
                    map[y] = c

            map_size = len(map)

            if rows > 0:
                if map_size != rows:
                    self.put_json_without_element("Elements in a grid are not aligned properly. Looks like grid has "
                                                  "wrong amount of rows. Expected is {0}. Actual is {1}".format(rows,
                                                                                                                map_size))
            if columns > 0:
                row_count = 1
                for key, value in map.items():
                    if row_count < map_size:
                        actual_in_a_row = int(value)
                        if actual_in_a_row != columns:
                            self.put_json_without_element("Elements in a grid are not aligned properly in row #{0}. "
                                                          "Expected {1} elements in a row. Actually it's {2}".format(
                                row_count, columns, actual_in_a_row))

                        row_count += 1

    def validate_elements_are_not_overlapped(self, root_elements):
        for el1 in root_elements:
            for el2 in root_elements:
                if el1 != el2:
                    if self.elements_are_overlapped(el1, el2):
                        self.put_json_with_element("Elements are overlapped", el1)
                        break

    def validate_same_size(self, root_elements, param):
        if isinstance(param, int):
            for i in range(0, len(root_elements) - 1):
                h1 = root_elements[i].size['height']
                w1 = root_elements[i].size['width']
                h2 = root_elements[i+1].size['height']
                w2 = root_elements[i+1].size['width']
                if param == 0:
                    if h1 != h2 or w1 != w2:
                        self.put_json_with_element("Element #{0} has different size. Element size is: [{1}, {2}]".format((i+1), root_elements[i].size['width'], root_elements[i].size['height']), root_elements[i])
                        self.put_json_with_element("Element #{0} has different size. Element size is: [{1}, {2}]".format((i+2), root_elements[i+1].size['width'], root_elements[i+1].size['height']), root_elements[i+1])
                elif param == 1:
                    if w1 != w2:
                        self.put_json_with_element("Element #{0} has different size. Element width is: [{1}, {2}]".format((i+1), root_elements[i].size['width'], root_elements[i].size['height']), root_elements[i])
                        self.put_json_with_element("Element #{0} has different size. Element width is: [{1}, {2}]".format((i+2), root_elements[i+1].size['width'], root_elements[i+1].size['height']), root_elements[i+1])

                elif param == 2:
                    if h1 != h2:
                        self.put_json_with_element("Element #{0} has different size. Element height is: [{1}, {2}]".format((i+1), root_elements[i].size['width'], root_elements[i].size['height']), root_elements[i])
                        self.put_json_with_element("Element #{0} has different size. Element height is: [{1}, {2}]".format((i+2), root_elements[i+1].size['width'], root_elements[i+1].size['height']), root_elements[i+1])

        else:
            w = root_elements.size['width']
            h = root_elements.size['height']

            if h != self.height_root or w != self.width_root:
                self.put_json_with_element(str("Element '{0}' has not the same width as {1}. Width of '{2}' is {3}px. "
                                               "Width of element is {4}px".format
                                               (self.root_element_name, param,
                                                self.root_element_name,
                                                self.width_root, w)), root_elements)

    def validate_right_offset_for_chunk(self, root_elements):
        for i in range(0, len(root_elements) - 1):
            if not self.elements_have_equal_left_right_offset(False, root_elements[i], root_elements[i + 1]):
                self.put_json_with_element(
                    "Element #{0} has not the same right offset as element #{1}".format(str(i + 1), str(i + 2)),
                    root_elements[i])

    def validate_left_offset_for_chunk(self, root_elements):
        for i in range(0, len(root_elements) - 1):
            if not self.elements_have_equal_left_right_offset(True, root_elements[i], root_elements[i + 1]):
                self.put_json_with_element(
                    "Element #{0} has not the same left offset as element #{1}".format(str(i + 1), str(i + 2)),
                    root_elements[i])

    def validate_top_offset_for_chunk(self, root_elements):
        for i in range(0, len(root_elements) - 1):
            if not self.elements_have_equal_top_bottom_offset(True, root_elements[i], root_elements[i + 1]):
                self.put_json_with_element(
                    "Element #{0} has not the same top offset as element #{1}".format(str(i + 1), str(i + 2)),
                    root_elements[i])

    def validate_bottom_offset_for_chunk(self, root_elements):
        for i in range(0, len(root_elements) - 1):
            if not self.elements_have_equal_top_bottom_offset(False, root_elements[i], root_elements[i + 1]):
                self.put_json_with_element(
                    "Element #{0} has not the same bottom offset as element #{1}".format(str(i + 1), str(i + 2)),
                    root_elements[i])

    def validate_equal_left_right_offset(self, root_elements, readable_name=None):
        if readable_name is None:
            for el in root_elements:
                if not self.element_has_equal_left_right_offset(el):
                    self.put_json_with_element(str("Element '{0}' has not equal left and right offset. Left offset is "
                                                   "{1}px, right is {2}px".format(self.get_formatted_message(el),
                                                                                  self.get_left_offset(el),
                                                                                  self.get_right_offset(el))), el)
        else:
            if not self.element_has_equal_left_right_offset(root_elements):
                self.put_json_with_element(str("Element '{0}' has not equal left and right offset. Left offset is {"
                                               "1}px, right is {2}px".format(readable_name, self.get_left_offset(
                    root_elements), self.get_right_offset(root_elements))), root_elements)

    def validate_equal_top_bottom_offset(self, root_elements, readable_name=None):
        if readable_name is None:
            for el in root_elements:
                if not self.element_has_equal_top_bottom_offset(el):
                    self.put_json_with_element(str("Element '{0}' has not equal top and bottom offset. Top offset is "
                                                   "{1}px, bottom is {2}px".format(self.get_formatted_message(el),
                                                                                   self.get_top_offset(el),
                                                                                   self.get_bottom_offset(el))), el)
        else:
            if not self.element_has_equal_top_bottom_offset(root_elements):
                self.put_json_with_element(str("Element '{0}' has not equal top and bottom offset. Top offset is {"
                                               "1}px, bottom is {2}px".format(readable_name, self.get_top_offset(
                    root_elements), self.get_bottom_offset(root_elements))), root_elements)

    def validate_inside_of_container(self, element, readable_name):
        x_container = element.location['x']
        y_container = element.location['y']
        width_container = element.size['width']
        height_container = element.size['height']

        if self.root_elements is None or len(self.root_elements) == 0:
            if self.x_root < x_container or self.y_root < y_container or (self.x_root + self.width_root) > (x_container + width_container) or (self.y_root + self.height_root) > (y_container + height_container):
                self.put_json_with_element("Element '{0}' is not inside of '{1}'".format(self.root_element_name, readable_name), element)
        else:
            for el in self.root_elements:
                x_root = el.location['x']
                y_root = el.location['y']
                width_root = el.size['width']
                height_root = el.size['height']
                if x_root < x_container or y_root < y_container or (x_root + width_root) > (x_container + width_container) or (y_root + height_root) > (y_container + height_container):
                    self.put_json_with_element("Element is not inside of '{0}'".format(readable_name), element)

    def put_json_without_element(self, message):
        mes = {Constants.MESSAGE: message}
        details = {Constants.DETAILS: mes}
        self.error_message.append(details)

    def put_json_with_element(self, message, element):
        x_container = element.location['x']
        y_container = element.location['y']
        width_container = element.size['width']
        height_container = element.size['height']

        el_details = {
            Constants.X: x_container,
            Constants.Y: y_container,
            Constants.WIDTH: width_container,
            Constants.HEIGHT: height_container}

        details = {Constants.REASON: {Constants.MESSAGE: message, Constants.ELEMENT: el_details}}
        self.error_message.append(details)

    def elements_are_overlapped(self, element_overlap_with, root_element=None):
        el_loc = element_overlap_with.location
        el_size = element_overlap_with.size
        if root_element is not None:
            self.x_root = root_element.location['x']
            self.y_root = root_element.location['y']
            self.width_root = root_element.size['width']
            self.height_root = root_element.size['height']

        return ((self.x_root >= el_loc['x'] and self.y_root > el_loc['y'] and self.x_root < el_loc['x'] + el_size[
            'width'] and self.y_root < el_loc['y'] + el_size['height'])
                or (self.x_root + self.width_root > el_loc['x'] and self.y_root > el_loc[
            'y'] and self.x_root + self.width_root < el_loc['x'] + el_size['width'] and self.y_root < el_loc['y'] +
                    el_size['height'])
                or (self.x_root > el_loc['x'] and self.y_root + self.height_root > el_loc['y'] and self.x_root < el_loc[
            'x'] + el_size['width'] and self.y_root + self.height_root < el_loc['y'] + el_size['height'])
                or (self.x_root + self.width_root > el_loc['x'] and self.y_root + self.height_root > el_loc[
            'y'] and self.x_root + self.width_root < el_loc['x'] + el_size['width'] and self.y_root + self.height_root <
                    el_loc['y'] + el_size['height'])) \
               or ((el_loc['x'] > self.x_root and el_loc['y'] > self.y_root and el_loc['x'] + el_size[
            'width'] < self.x_root and el_loc['y'] + el_size['height'] < self.y_root)
                   or (
                   el_loc['x'] > self.x_root + self.width_root and el_loc['y'] > self.y_root and el_loc['x'] + el_size[
                       'width'] < self.x_root + self.width_root and el_loc['y'] + el_size['height'] < self.y_root)
                   or (
                   el_loc['x'] > self.x_root and el_loc['y'] > self.y_root + self.height_root and el_loc['x'] + el_size[
                       'width'] < self.x_root and el_loc['y'] + el_size['height'] < self.y_root + self.height_root)
                   or (el_loc['x'] > self.x_root + self.width_root and el_loc['y'] > self.y_root + self.height_root and
                       el_loc['x'] + el_size['width'] < self.x_root + self.width_root and el_loc['y'] + el_size[
                           'height'] < self.y_root + self.height_root)) \
               or self.elements_are_overlapped_on_border(root_element, element_overlap_with)

    def elements_are_overlapped_on_border(self, root_element, element_overlap_with):
        el_loc = element_overlap_with.location
        el_size = element_overlap_with.size
        x_root = root_element.location['x']
        y_root = root_element.location['y']
        width_root = root_element.size['width']
        height_root = root_element.size['height']

        sq_root_element = width_root + height_root
        sq_element = el_size['width'] * el_size['height']

        if x_root < el_loc['x'] and y_root == el_loc['y']:
            sq_common = (width_root + (el_loc['x'] - (x_root + width_root) + el_size['width'])) * height_root
        elif y_root < el_loc['y'] and x_root == el_loc['x']:
            sq_common = (height_root + (el_loc['y'] - (y_root + height_root) + el_size['height'])) * width_root
        elif el_loc['x'] < x_root and y_root == el_loc['y']:
            sq_common = (el_size['width'] + (x_root - (el_loc['x'] + el_size['width']) + width_root)) * el_size[
                'height']
        elif el_loc['y'] < y_root and x_root == el_loc['x']:
            sq_common = (el_size['height'] + (y_root - (el_loc['y'] + el_size['height']) + height_root)) * el_size[
                'width']
        else:
            return False

        return sq_common < sq_root_element + sq_element

    def get_left_offset(self, el):
        return el.location['x']

    def get_right_offset(self, el):
        return self.page_width - (el.location['x'] + el.size['width'])

    def get_top_offset(self, el):
        return el.location['y']

    def get_bottom_offset(self, el):
        return self.page_height - (el.location['y'] + el.size['height'])

    def get_formatted_message(self, el):
        return str(
            "with properties: tag=[{0}], id=[{1}], class=[{2}], text=[{3}], coord=[{4},{5}], size=[{6},{7}]".format(
                el.tag_name,
                el.get_attribute('id'),
                el.get_attribute('class'),
                el.text if len(el.text) < 10 else el.text[:10] + '...',
                str(el.location['x']),
                str(el.location['y']),
                str(el.size['width']),
                str(el.size['height'])))

    def elements_have_equal_left_right_offset(self, is_left, el_root, el_to_compare):
        x_root = el_root.location['x']
        width_root = el_root.size['width']

        x_el = el_to_compare.location['x']
        width_el = el_to_compare.size['width']

        if is_left:
            return x_root == x_el
        else:
            return (self.page_width - x_root + width_root) == (self.page_width - x_el + width_el)

    def elements_have_equal_top_bottom_offset(self, is_top, el_root, el_to_compare):
        y_root = el_root.location['y']
        height_root = el_root.size['height']

        y_el = el_to_compare.location['y']
        height_el = el_to_compare.size['height']

        if is_top:
            return y_root == y_el
        else:
            return (self.page_height - y_root + height_root) == (self.page_height - y_el + height_el)

    def element_has_equal_left_right_offset(self, el):
        return self.get_left_offset(el) == self.get_right_offset(el)

    def element_has_equal_top_bottom_offset(self, el):
        return self.get_top_offset(el) == self.get_bottom_offset(el)

    def draw_screenshot(self):
        im = Image.open(self.screenshot_path)

        dr = ImageDraw.Draw(im)
        if self.draw_left_offset_line:
            dr.line(((self.x_root, 0), (self.x_root, im.height)), width=2, fill=15)
        if self.draw_right_offset_line:
            dr.line(((self.x_root + self.width_root, 0), (self.x_root + self.width_root, im.height)), width=2, fill=15)
        if self.draw_top_offset_line:
            dr.line(((0, self.y_root), (im.width, self.y_root)), width=2, fill=15)
        if self.draw_top_offset_line:
            dr.line(((0, self.y_root + self.height_root), (im.width, self.y_root + self.height_root)), width=2, fill=15)

        dr.rectangle(((self.x_root, self.y_root), (self.x_root + self.width_root, self.y_root + self.height_root)), outline="red")

        for obj in self.error_message:
            details = obj[Constants.REASON]
            num_e = details[Constants.ELEMENT]

            if num_e is not None:
                x = num_e[Constants.X]
                y = num_e[Constants.Y]
                width = num_e[Constants.WIDTH]
                height = num_e[Constants.HEIGHT]
                dr.rectangle(((x, y), (x + width, y + height)), outline="lime")

        im.save(self.screenshot_path)

    def generate_report(self, report_name=""):
        html_builder = HtmlReportBuilder()
        html_builder.build_report(self.json_files, report_name=report_name)

    def get_page_width(self):
        return self.driver.get_window_size()['width']

    def get_page_height(self):
        return self.driver.get_window_size()['height']

    def get_converted_int(self, i, horizontal):
        if self.units == Units.PX:
            return i
        else:
            if bool(horizontal) is True:
                return (i * self.page_width) / 100
            else:
                return (i * self.page_height) / 100

    def validate_not_overlapping_with_elements(self, element, element_name):
        if self.root_element != element:
            if self.elements_are_overlapped(element, root_element=self.root_element):
                self.put_json_with_element("Element '{0}' is overlapped with element '{1}' but should not".format(self.root_element_name, element_name), element)

    def validate_overlapping_with_elements(self, element, element_name):
        if self.root_element != element:
            if not self.elements_are_overlapped(element, root_element=self.root_element):
                self.put_json_with_element("Element '{0}' is not overlapped with element '{1}' but should".format(self.root_element_name, element_name), element)

    def validate_right_offset_for_elements(self, element, param):
        if self.root_element != element:
            if not self.elements_have_equal_left_right_offset(False, self.root_element, element):
                self.put_json_with_element("Element '{0}' has not the same right offset as element '{1}'".format(self.root_element_name, param), element)

    def validate_left_offset_for_elements(self, element, param):
        if self.root_element != element:
            if not self.elements_have_equal_left_right_offset(True, self.root_element, element):
                self.put_json_with_element("Element '{0}' has not the same left offset as element '{1}'".format(self.root_element_name, param), element)

    def validate_top_offset_for_elements(self, element, param):
        if self.root_element != element:
            if not self.elements_have_equal_top_bottom_offset(True, self.root_element, element):
                self.put_json_with_element("Element '{0}' has not the same top offset as element '{1}'".format(self.root_element_name, param), element)

    def validate_bottom_offset_for_elements(self, element, param):
        if self.root_element != element:
            if not self.elements_have_equal_top_bottom_offset(False, self.root_element, element):
                self.put_json_with_element("Element '{0}' has not the same bottom offset as element '{1}'".format(self.root_element_name, param), element)

    def validate_same_width(self, element, param):
        if self.root_element != element:
            w = element.size['width']
            if w != self.width_root:
                self.put_json_with_element("Element '{0}' has not the same width as {1}. Width of '{2}' is {3}px. Width of element is {4}px".format(self.root_element_name, param, self.root_element_name, self.width_root, w), element)

    def validate_min_width(self, width):
        if self.width_root < width:
            self.put_json_without_element("Expected max width of element '{0}' is: {1}px. Actual width is: {2}px".format(self.root_element_name, width, self.width_root))

    def validate_max_width(self, width):
        if self.width_root > width:
            self.put_json_without_element("Expected max width of element '{0}' is: {1}px. Actual width is: {2}px".format(self.root_element_name, width, self.width_root))

    def validate_same_height(self, element, param):
        if self.root_element != element:
            h = element.size['height']
            if h != self.height_root:
                self.put_json_with_element("Element '{0}' has not the same height as {1}. Height of '{2}' is {3}px. Height of element is {4}px".format(self.root_element_name, param, self.root_element_name, self.height_root, h), element)

    def validate_min_height(self, height):
        if self.height_root < height:
            self.put_json_without_element("Expected min height of element '{0}' is: {1}px. Actual height is: {2}px".format(self.root_element_name, height, self.height_root))

    def validate_max_height(self, height):
        if self.height_root > height:
            self.put_json_without_element("Expected max height of element '{0}' is: {1}px. Actual height is: {2}px".format(self.root_element_name, height, self.height_root))

    def validate_min_offset(self, top, right, bottom, left):
        root_element_right_offset = self.get_right_offset(self.root_element)
        root_element_bottom_offset = self.get_bottom_offset(self.root_element)
        if self.x_root < left:
            self.put_json_without_element("Expected min left offset of element '{0}' is: {1}px. Actual left offset is: {2}px".format(self.root_element_name, left, self.x_root))
        if self.y_root < top:
            self.put_json_without_element("Expected min top offset of element '{0}' is: {1}px. Actual top offset is: {2}px".format(self.root_element_name, top, self.y_root))
        if root_element_right_offset < right:
            self.put_json_without_element("Expected min right offset of element '{0}' is: {1}px. Actual right offset is: {2}px".format(self.root_element_name, right, root_element_right_offset))
        if root_element_bottom_offset < bottom:
            self.put_json_without_element("Expected min bottom offset of element '{0}' is: {1}px. Actual bottom offset is: {2}px".format(self.root_element_name, bottom, root_element_bottom_offset))

    def validate_max_offset(self, top, right, bottom, left):
        root_element_right_offset = self.get_right_offset(self.root_element)
        root_element_bottom_offset = self.get_bottom_offset(self.root_element)
        if self.x_root > left:
            self.put_json_without_element("Expected max left offset of element '{0}' is: {1}px. Actual left offset is: {2}px".format(self.root_element_name, left, self.x_root))
        if self.y_root > top:
            self.put_json_without_element("Expected max top offset of element '{0}' is: {1}px. Actual top offset is: {2}px".format(self.root_element_name, top, self.y_root))
        if root_element_right_offset > right:
            self.put_json_without_element("Expected max right offset of element '{0}' is: {1}px. Actual right offset is: {2}px".format(self.root_element_name, right, root_element_right_offset))
        if root_element_bottom_offset > bottom:
            self.put_json_without_element("Expected max bottom offset of element '{0}' is: {1}px. Actual bottom offset is: {2}px".format(self.root_element_name, bottom, root_element_bottom_offset))

    def validate_left_element(self, element, min_margin, max_margin):
        pass

    def validate_right_element(self, element, min_margin, max_margin):
        pass

    def validate_top_element(self, element, min_margin, max_margin):
        pass

    def validate_bottom_element(self, element, min_margin, max_margin):
        pass
