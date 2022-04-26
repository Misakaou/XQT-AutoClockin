from RunClockin import RunClockin

def handler(event, context):
    RunClockin().run_in_order()
    return 'ok'
