__version__ = "0.0.1"

from connect_master.monkey_patches import patch_email_account, patch_user
patch_email_account()
patch_user()
