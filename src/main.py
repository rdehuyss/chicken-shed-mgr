import gc, sys

# import update utils and delete if not necessary anymore
import app.utils.update_utils
del app.utils.update_utils
del sys.modules["app.utils.update_utils"]
del sys.modules["app.utils"]
gc.collect()

import app.start