from loguru import logger
from halo import Halo
import time


# Initialize the logger
logger.remove()
logger.add("app.log", format="{time} {level} {message}", level="INFO", diagnose=False)

plan = [
    'step 1',
    'step 2',
    'step 3'
]


def execute_step(step: str):
    time.sleep(2)

    if step == 'step 3':
        return False

    return True


for i, step in enumerate(plan, start=1):
    # Initialize the spinner
    spinner = Halo(text=step, spinner='dots')
    spinner.start()

    try:
        result = execute_step(step)
        if result:
            spinner.succeed(step)
            logger.info(step)
        else:
            spinner.fail(step)
            logger.error(step)
    except Exception as e:
        spinner.fail(step)
        logger.error(step)

    spinner.stop()
