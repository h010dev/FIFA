from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.monitors.mixins import StatsMonitorMixin


@monitors.name('Item count')
class ItemCountMonitor(Monitor):

    @monitors.name('Minimum number of items')
    def test_minimum_number_of_items(self):
        item_extracted = getattr(
            self.data.stats, 'item_scraped_count', 0)
        minimum_threshold = 61

        msg = f'Extracted less than {minimum_threshold} items.'
        self.assertTrue(
            item_extracted >= minimum_threshold, msg=msg
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


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ItemCountMonitor,
        ItemValidationMonitor,
    ]
