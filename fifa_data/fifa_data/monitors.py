from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.monitors.mixins import StatsMonitorMixin
from fifa_data.actions import CloseSpiderAction


@monitors.name('Item count')
class ItemCountMonitor(Monitor):

    @monitors.name('Minimum number of items')
    def test_minimum_number_of_items(self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0
        )
        pages_visited = getattr(
            self.data.stats, 'page_counter', 0
        )

        minimum_threshold = ((pages_visited - 1) * 60) + 1
        maximum_threshold = ((pages_visited - 1) * 60) + 61

        msg = f'Extracted {item_extracted} out of [{minimum_threshold}, {maximum_threshold}] items.'
        self.assertTrue(
            maximum_threshold >= item_extracted >= minimum_threshold, msg=msg
        )


@monitors.name('Item validation')
class ItemValidationMonitor(Monitor, StatsMonitorMixin):

    @monitors.name('No item validation errors')
    def test_no_item_validation_errors(self):
        validation_errors = getattr(
            self.stats, 'spidermon/validation/fields/errors', 0
        )
        self.assertEqual(
            validation_errors,
            0,
            msg=f'Found validation errors in {validation_errors} fields.'
        )


@monitors.name('Periodic job stats monitor')
class PeriodicJobStatsMonitor(Monitor, StatsMonitorMixin):

    @monitors.name('Maximum number of errors reached')
    def test_number_of_errors(self):
        accepted_num_errors = 6
        num_errors = self.data.stats.get('log_count/ERROR', 0)

        msg = 'The job has exceeded the maximum number of errors'
        self.assertLessEqual(num_errors, accepted_num_errors, msg=msg)


@monitors.name('Finish Reason Monitor')
class FinishReasonMonitor(Monitor):

    SPIDERMON_EXPECTED_FINISH_REASONS = ['finished', ]

    @monitors.name('Should have the expected finished reason(s)')
    def test_should_finish_with_expected_reason(self):
        expected_reasons = self.SPIDERMON_EXPECTED_FINISH_REASONS
        finished_reason = getattr(self.data.stats, 'finish_reason')
        msg = f'Finished with {finished_reason}, the expected reasons are {expected_reasons}'
        self.assertTrue(finished_reason in expected_reasons, msg=msg)


@monitors.name('Unwanted HTTP codes monitor')
class UnwantedHTTPCodesMonitor(Monitor):

    DEFAULT_ERROR_CODES = {
        code: 2
        for code in [400, 407, 429, 500, 502, 503, 504, 523, 540, 541]
    }

    @monitors.name('Should not hit the limit of unwanted http status')
    def test_check_unwanted_http_codes(self):
        error_codes = self.DEFAULT_ERROR_CODES
        for code, max_errors in error_codes.items():
            code = int(code)
            count = getattr(self.data.stats, f'downloader/response_status_count/{code}', 0)
            msg = (
                f'Found {count} Responses with status code = {code} - '
                f'This exceeds the limit of {max_errors}'
            )
            self.assertTrue(count <= max_errors, msg=msg)


class PeriodicMonitorSuite(MonitorSuite):
    monitors = [PeriodicJobStatsMonitor]
    monitors_failed_actions = [CloseSpiderAction]


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ItemCountMonitor,
        ItemValidationMonitor,
        PeriodicJobStatsMonitor,
        FinishReasonMonitor,
        UnwantedHTTPCodesMonitor
    ]
