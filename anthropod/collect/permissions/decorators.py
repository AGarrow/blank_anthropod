

def permission_required(*permissions):
    '''Collection is the mongo collection that permission
    is required for. The operation is 'create', 'edit', or
    'delete'.
    '''
    def decorator(view):
        '''Mark the view as requiring permissions on a certain
        collection.
        '''
        view._anthropod_permissions = permissions
        return view

    return decorator
