from salesforce_reporting import Connection, ReportParser
import pandas as pd 
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab
from textwrap import fill



def load_report(report_id, sf):
    report = sf.get_report(report_id)
    parser = ReportParser(report)
    report = parser.records_dict()
    report = pd.DataFrame(report)
    return report