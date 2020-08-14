from datetime import datetime
import TeeOnFormFiller

def cronjob():
    print("Starting reservation script")
    TeeOnFormFiller.don_valley_form_filler()
    print("Script finished: %s" % datetime.now())