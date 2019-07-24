import chrprofiler.count_mode as chromeMode
import chrprofiler.count_sequential as chromeSeq
import chrprofiler.count_serach_words as chromeSearchWord
import chrprofiler.count_time as chromeTime
import chrprofiler.count_url as chromeUrl
import chrprofiler.plot_correlation as chromeCorr
import chrprofiler.plot_keyword_network as chromeKeyNw
import chrprofiler.constant as constant
import os


def run():
    topdir = './chrprofiler'
    if not os.path.exists(topdir):
        os.mkdir(topdir)

    if not os.path.exists(constant.CSV_DIR):
        os.mkdir(f'{topdir}/{constant.CSV_DIR}')

    if not os.path.exists(constant.FIG_DIR):
        os.mkdir(f'{topdir}/{constant.FIG_DIR}')

    if not os.path.exists(constant.FIG_DIR):
        os.mkdir(f'{topdir}/{constant.PDF_DIR}')

    chromeMode.run()
    chromeSeq.run()
    chromeSearchWord.run()
    chromeTime.run()
    chromeUrl.run()
    chromeCorr.run()
    chromeKeyNw.run()
