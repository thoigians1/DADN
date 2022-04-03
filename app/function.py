
# Check if param exist in args
def isValidArgs(args, params):
    for par in params:
        if not par in args:
            return False
    return True
        