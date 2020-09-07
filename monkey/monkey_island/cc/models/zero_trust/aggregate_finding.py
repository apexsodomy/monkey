from typing import List

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.finding_details import FindingDetails


class AggregateFinding(Finding):
    @staticmethod
    def create_or_add_to_existing(test, status, events):
        """
        Create a new finding or add the events to an existing one if it's the same (same meaning same status and same
        test).

        :raises: Assertion error if this is used when there's more then one finding which fits the query - this is not
        when this function should be used.
        """
        existing_findings = Finding.objects(test=test, status=status)
        assert (len(existing_findings) < 2), "More than one finding exists for {}:{}".format(test, status)

        if len(existing_findings) == 0:
            AggregateFinding.create_new_finding(test, status, events)
        else:
            # Now we know for sure this is the only one
            AggregateFinding.add_events(existing_findings[0], events)

    @staticmethod
    def create_new_finding(test: str, status: str, events: List[Event]):
        details = FindingDetails()
        details.events = events
        details.save()
        Finding.save_finding(test, status, details)

    @staticmethod
    def add_events(finding: Finding, events: List[Event]):
        finding.details.fetch().add_events(events)


def add_malicious_activity_to_timeline(events):
    AggregateFinding.create_or_add_to_existing(
        test=zero_trust_consts.TEST_MALICIOUS_ACTIVITY_TIMELINE,
        status=zero_trust_consts.STATUS_VERIFY,
        events=events
    )
