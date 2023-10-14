# Use this module to test functions & run arbitrary scripts
#within the context of this application.
# The block below must not be removed and must come firsr before any imports.
print("Initializing script runner...", end="")
######################################################################
import os                                                            #
import django                                                        #
                                                                     #
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")   #
django.setup()                                                       #
######################################################################
print("Ready!")




def process():
    # write your code here
    pass


process()