# -*- coding: utf-8 -*-
import colorama  # NOQA: E402
colorama.init(strip=False)
from sys import stderr  # NOQA: E402

MY_LOG_LEVEL = 7


class ConsoleLogger:
    def __init__(self, log_level):
        assert isinstance(log_level, int)
        self.log_level = log_level

    def verbose(self, *args, **kwargs):
        if self.log_level >= 7:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[92mVerbose: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.log_level >= 6:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[96mDebug: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)

    def info(self, *args, **kwargs):
        if self.log_level >= 5:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[97mInfo: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)

    def warning(self, *args, **kwargs):
        if self.log_level >= 4:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[93mWarning: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self.log_level >= 3:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[95mError: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)

    def critical(self, *args, **kwargs):
        if self.log_level >= 2:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[91mCritical: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)

    def question(self, *args, **kwargs):
        if self.log_level >= 1:
            args = len(args) > 0 and list(args) or [""]
            args[0] = "\033[94mQuestion: {}".format((args[0]))
            args[-1] = "{}\033[0m".format((args[-1]))
            kwargs['file'] = stderr
            print(*args, **kwargs)


global_console_logger = ConsoleLogger(MY_LOG_LEVEL)
verbose_print = global_console_logger.verbose
debug_print = global_console_logger.debug
info_print = global_console_logger.info
warning_print = global_console_logger.warning
error_print = global_console_logger.error
critical_print = global_console_logger.critical
question_print = global_console_logger.question
