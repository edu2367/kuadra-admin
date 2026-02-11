try:
    # Import app to ensure package imports correctly
    import importlib
    importlib.import_module('app.main')
    print('IMPORT_OK')
except Exception as e:
    print('IMPORT_FAIL:', e)
    raise
