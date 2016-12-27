import datetime
import time
import json
import os

from yattag import Doc

from automotion.constants import Constants


class HtmlReportBuilder:

    def __init__(self):
        pass

    def build_report(self, json_files, report_name=None):
        doc, tag, text, line = Doc().ttl()
        with tag('html'):
            with tag('head'):
                with tag('title'):
                    text("Automotion report")
            with tag('body'):
                with tag('div', style = 'width: 100%; background-color: rgb(0,191,255); color: white; padding: 10px'):
                    with tag('h1'):
                        text("Results from: {:%d, %b %Y}".format(datetime.date.today()))

                json_dir = os.listdir(Constants.OUTPUT_AUTOMOTION_JSON)
                if len(json_dir) > 0:
                    for filename in json_dir:
                        if filename in json_files:
                            data = json.loads(open(Constants.OUTPUT_AUTOMOTION_JSON + filename).read())
                            with tag('h1', style='color: rgb(47,79,79); margin-top: 50px'):
                                text('Scenario: "{}"'.format(data[Constants.SCENARIO]))
                            with tag('h2', style='color: rgb(0,139,139)'):
                                text('Element: "{}"'.format(data[Constants.ELEMENT_NAME]))
                            with tag('h3', style='olor: rgb(255,69,0)'):
                                text('Failures:')
                            with tag('ol'):
                                for detail in data[Constants.DETAILS]:
                                    r = detail[Constants.REASON]
                                    m = r[Constants.MESSAGE]
                                    line('li', m)
                            with tag('h4', style='color: rgb(105,105,105)'):
                                text("Time execution: {}".format(data[Constants.TIME_EXECUTION]))
                            with tag('p'):
                                doc.stag('img', src='img/{}'.format(data[Constants.SCREENSHOT]), style='width: 50%; margin-left:25%')

                            os.remove(Constants.OUTPUT_AUTOMOTION_JSON + filename)

        f = open(Constants.OUTPUT_AUTOMOTION + (report_name if not report_name == "" else "result") + str(time.mktime(time.gmtime())) + ".html", "w")
        f.write(str(doc.getvalue()))
        f.close()