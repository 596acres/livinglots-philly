import logging

from external_data_sync.synchronizers import Synchronizer
from inplace.boundaries.models import Boundary

from lots.load import (load_lots_available, load_lots_with_licenses,
                       load_lots_with_violations)
from lots.models import Lot
from .availableproperties.adapter import (find_available_properties,
                                          find_no_longer_available_properties)
from .licenses.adapter import find_licenses
from .taxaccounts.models import TaxAccount
from .violations.adapter import find_violations
from .zoning.models import BaseDistrict


logger = logging.getLogger(__name__)


class PRAAvailablePropertiesSynchronizer(Synchronizer):
    """
    Attempts to synchronize the local database with the available properties
    as listed by the Philadelphia Redevelopment Authority.

    As the PRA's data does not include timestamps for available properties,
    we load all available properties every time we synchronize, marking new
    ones (status == 'new and available'), existing ones (status ==
    'available'), and properties no longer in the PRA's data (status == 'no
    longer available').

    Once the above is accomplished, we load lots for available properties that
    are new.

    """
    def sync(self, data_source):
        logger.info('Synchronizing available properties.')
        find_available_properties()
        logger.info('Done synchronizing available properties.')

        logger.info('Synchronizing no-longer available properties.')
        find_no_longer_available_properties(data_source.last_synchronized)
        logger.info('Done synchronizing no-longer available properties.')

        logger.info('Adding lots with available properties.')
        load_lots_available(added_after=data_source.last_synchronized)
        logger.info('Done adding lots with available properties.')


class LILicensesSynchronizer(Synchronizer):
    """
    A Synchronizer that updates L&I license data.

    """
    codes = (
        '3219', # residential vacancy license
        '3634', # commercial vacancy license
    )

    def sync(self, data_source):
        logger.info('Starting to synchronize L&I license data.')
        self.update_license_data()
        logger.info('Finished synchronizing L&I license data.')

        logger.info('Adding lots with licenses.')
        load_lots_with_licenses()
        logger.info('Done adding lots with licenses.')

    def update_license_data(self):
        for code in self.codes:
            find_licenses(code, self.data_source.last_synchronized)


class LIViolationsSynchronizer(Synchronizer):
    """
    A Synchronizer that updates L&I Violation data.

    """
    # L&I says these should be the useful codes
    codes = ('CP-802', 'PM-102.4/1', 'PM-302.2/4', 'PM-306.0/2', 'PM-306.0/91',
             'PM-307.1/21',)

    def sync(self, data_source):
        logger.info('Starting to synchronize L&I Violation data.')
        self.update_violation_data()
        logger.info('Finished synchronizing L&I Violation data.')

        logger.info('Adding lots with violations.')
        load_lots_with_violations()
        logger.info('Done adding lots with violations.')

    def update_violation_data(self):
        for code in self.codes:
            find_violations(code, self.data_source.last_synchronized)


class ZoningSynchronizer(Synchronizer):
    """A Synchronizer that updates zoning for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize zoning.')
        self.update_zoning(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing zoning.')

    def update_zoning(self, count=1000):
        lots = Lot.objects.filter(zoning_district__isnull=True).order_by('?')
        for lot in lots[:count]:
            try:
                lot.zoning_district = BaseDistrict.objects.get(
                    geometry__contains=lot.centroid,
                )
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating zoning for lot '
                            '%s' % lot)


class CityCouncilSynchronizer(Synchronizer):
    """A Synchronizer that updates city council districts for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize city council districts.')
        self.update_city_council_districts(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing city council districts.')

    def update_city_council_districts(self, count=1000):
        lots = Lot.objects.filter(
            city_council_district__isnull=True
        ).order_by('?')
        for lot in lots[:count]:
            try:
                lot.city_council_district = Boundary.objects.get(
                    geometry__contains=lot.centroid,
                    layer__name='City Council Districts',
                )
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating city council '
                            'district for lot %s' % lot)


class PlanningDistrictSynchronizer(Synchronizer):
    """A Synchronizer that updates planning districts for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize planning districts.')
        self.update_planning_districts(count=data_source.batch_size or 1000)
        logger.info('Finished synchronizing planning districts.')

    def update_planning_districts(self, count=1000):
        lots = Lot.objects.filter(
            planning_district__isnull=True
        ).order_by('?')
        for lot in lots[:count]:
            try:
                lot.planning_district = Boundary.objects.get(
                    geometry__contains=lot.centroid,
                    layer__name='Planning Districts',
                )
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating planning '
                            'district for lot %s' % lot)


class TaxAccountSynchronizer(Synchronizer):
    """A Synchronizer that updates tax account data for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize tax account data.')
        self.update_tax_accounts(count=data_source.batch_size)
        logger.info('Finished synchronizing tax account data.')

    def update_tax_accounts(self, count=1000):
        lots = Lot.objects.filter(tax_account__isnull=True).order_by('?')
        for lot in lots[:count]:
            try:
                lot.tax_account = TaxAccount.objects.get(
                    property_address__icontains=lot.address_line1,
                )
                lot.save()
            except TaxAccount.DoesNotExist:
                logger.debug('Could not find tax account for lot %s' % lot)
            except Exception:
                logger.warn('Caught exception while getting tax account for '
                            'lot %s' % lot)


class UseCertaintyScoresSynchronizer(Synchronizer):
    """A Synchronizer that updates use certainty scores for lots."""

    def sync(self, data_source):
        logger.info('Starting to synchronize use certainty scores.')
        self.update_use_certainty_scores(count=data_source.batch_size)
        logger.info('Finished synchronizing use certainty scores.')

    def update_use_certainty_scores(self, count=1000):
        # Get lots that look like they haven't been updated and that we can
        # change
        lots = Lot.objects.filter(
            known_use_locked=False,
            known_use_certainty=0
        ).order_by('?')
        for lot in lots[:count]:
            try:
                lot.known_use_certainty = lot.calculate_known_use_certainty()
                lot.save()
            except Exception:
                logger.warn('Caught exception while updating use certainty '
                            'score for lot %s' % lot)
