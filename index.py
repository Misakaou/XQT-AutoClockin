from RunClockin import RunClockin

def handler(event, context):
    run_clockin = RunClockin()
    run_clockin.run()
    return 'ok'
