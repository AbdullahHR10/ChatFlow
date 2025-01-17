from flask import current_app


def allowed_file(filename):
    """
    Check if the file has an allowed extension.

    This function determines whether a given filename has an extension
    that is listed in the app's configuration under `ALLOWED_EXTENSIONS`.

    Args:
        filename (str): The name of the file to be checked.

    Returns:
        bool: True if the file has a valid extension, False otherwise.

    Note:
        - This function requires a Flask application context to access
          `current_app.config`.
        - Ensure that the `ALLOWED_EXTENSIONS` key is
            defined in your app's config.
    """
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in current_app.config.get('ALLOWED_EXTENSIONS',
                                                   set())

    # Return False if no '.' is found in the filename.
    return False
