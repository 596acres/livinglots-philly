from math import floor

from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.gis.geos import MultiPolygon
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from inplace.models import Place
from livinglots_lots.models import BaseLotManager

from phillydata.owners.models import Owner
from livinglotsphilly.reversion_utils import InitialRevisionManagerMixin


class LotManager(InitialRevisionManagerMixin, BaseLotManager):

    def get_lot_kwargs(self, parcel, **defaults):
        kwargs = {
            'water_parcel': parcel,
            'polygon': parcel.geometry,
            'centroid': parcel.geometry.centroid,
            'address_line1': parcel.address,
            'name': parcel.address,
            'city': 'Philadelphia',
            'state_province': 'PA',
        }
        kwargs.update(**defaults)

        # Create or get owner for parcels
        if parcel.owner1:
            (owner, created) = Owner.objects.get_or_create(
                name=parcel.owner1,
            )
            kwargs['owner'] = owner

        return kwargs


class VisibleLotManager(LotManager):
    """A manager that only retrieves lots that are publicly viewable."""

    def get_queryset(self):
        return self.get_visible()


class Lot(Place):

    objects = LotManager()
    visible = VisibleLotManager()

    owner = models.ForeignKey('owners.Owner',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The owner of this lot.'),
        verbose_name=_('owner'),
    )
    billing_account = models.ForeignKey('opa.BillingAccount',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The owner's billing account for this lot."),
        verbose_name=_('billing account'),
    )
    tax_account = models.ForeignKey('taxaccounts.TaxAccount',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The tax account for this lot."),
        verbose_name=_('tax account'),
    )
    parcel = models.ForeignKey('parcels.Parcel',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The parcel this lot is based on.'),
        verbose_name=_('parcel'),
    )
    land_use_area = models.ForeignKey('landuse.LandUseArea',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The land use area for this lot.'),
        verbose_name=_('land use'),
    )
    violations = models.ManyToManyField('violations.Violation',
        blank=True,
        null=True,
        help_text=_('The violations associated with this lot.'),
        verbose_name=_('violations'),
    )
    licenses = models.ManyToManyField('licenses.License',
        blank=True,
        null=True,
        help_text=_('The licenses associated with this lot.'),
        verbose_name=_('licenses'),
    )
    available_property = models.ForeignKey('availableproperties.AvailableProperty',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    water_parcel = models.ForeignKey('waterdept.WaterParcel',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('The parcel the Water Department defines for this lot')
    )
    known_use = models.ForeignKey('Use',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    known_use_certainty = models.PositiveIntegerField(_('known use certainty'),
        default=0,
        help_text=_('On a scale of 0 to 10, how certain are we that the known '
                    'use is correct?'),
    )
    known_use_locked = models.BooleanField(_('known use locked'),
        default=False,
        help_text=_('Is the known use field locked? If it is not, the site '
                    'will make a guess using available data. If you are '
                    'certain that the known use is correct, lock it.'),
    )
    zoning_district = models.ForeignKey('zoning.BaseDistrict',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('zoning district'),
    )
    city_council_district = models.ForeignKey('boundaries.Boundary',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('city council district'),
    )
    planning_district = models.ForeignKey('boundaries.Boundary',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('planning district'),
    )

    added = models.DateTimeField(_('date added'),
        auto_now_add=True,
        help_text=('When this lot was added'),
    )

    organizers = GenericRelation('phillyorganize.Organizer')
    steward_projects = GenericRelation('steward.StewardProject')
    steward_inclusion_opt_in = models.BooleanField(_('steward inclusion opt-in'),
        default=False,
        help_text=_('Did the steward opt in to being included on our map?'),
    )

    group = models.ForeignKey('LotGroup',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('group'),
    )

    polygon_area = models.DecimalField(_('polygon area'),
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The area of the polygon in square feet'),
    )
    polygon_width = models.DecimalField(_('polygon width'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('The width of the polygon in feet'),
    )
    polygon_tied_to_parcel = models.BooleanField(_('polygon tied to parcel'),
        default=True,
        help_text=_("Is the polygon of this lot always matched up with the "
                    "parcel's polygon on save?"),
    )


    class Meta:
        permissions = (
            ('view_all_details', 'Can view all details for lots'),
            ('view_all_filters', 'Can view all map filters for lots'),
            ('view_all_lots', 'Can view all lots'),
        )

    def __unicode__(self):
        return u'%s' % (self.address_line1,)

    @models.permalink
    def get_absolute_url(self):
        return ('lots:lot_detail', (), { 'pk': self.pk, })

    def find_nearby(self, count=5):
        return Lot.objects.find_nearby(self)[:count]
    nearby = property(find_nearby)

    def calculate_polygon_area(self):
        """Find the area of this lot in square feet using its polygon."""
        try:
            # tranform to an area-preserving projection for south PA
            return self.polygon.transform(3652, clone=True).area
        except Exception:
            return None

    def calculate_polygon_width(self):
        """
        Approximate the width (narrowest side) of this lot in feet using its
        polygon.
        """
        from django.contrib.gis.geos import LineString

        # Get the convex hull for the polygon
        convex_hull = self.polygon.convex_hull.transform(3652, clone=True)

        # Find the longest side of the convex hull
        sides = []
        longest = None
        for i in range(0, convex_hull.num_points - 1):
            side = LineString((convex_hull[0][i], convex_hull[0][i+1]),
                              srid=convex_hull.srid)
            sides.append(side)
            if not longest or side.length > longest.length:
                longest = side

        # Find the side that is closest to making the area with the longest
        # side
        closest = longest
        target_area = self.polygon.transform(3652, clone=True).area
        for side in sides:
            test_area = side.length * longest.length
            closest_area = closest.length * longest.length
            if abs(target_area - test_area) < abs(target_area - closest_area):
                closest = side

        return closest.length

    def calculate_known_use_certainty(self):
        #
        # First, the data that indicate real certainty
        #

        # If someone told us what is happening here, known_use_locked should be
        # set. Similarly if we manually changed the use for any reason.
        if self.known_use_locked:
            return self.known_use_certainty

        # If the lot is currently in the PRA's Available Property database,
        # then we know for sure
        ap = self.available_property
        if ap and ap.status is not 'no longer available':
            return 10

        #
        # Now for the fuzzy calculations
        #
        certainty = 0

        # If the land use data has this lot marked vacant
        if self.land_use_area and self.land_use_area.subcategory == 'Vacant':
            certainty += 4

        # If the L&I has given the lot "vacant" licenses
        license_certainty = 2 * self.licenses.filter(status='ACTIVE').count()
        if license_certainty > 4:
            license_certainty = 4
        certainty += license_certainty

        # If the L&I has given the lot "vacant" violations in the past year
        today = now()
        last_year = today.replace(year=today.year - 1)
        violation_count = self.violations.filter(violation_datetime__gt=last_year).count()
        violation_certainty = 2 * violation_count
        if violation_certainty > 4:
            violation_certainty = 4
        certainty += violation_certainty

        if self.water_parcel:
            # If the Water Dept's data says the lot is very permeable
            certainty += floor(self.water_parcel.percent_permeable / 20)

            if self.water_parcel.building_description:
                # If the Water Dept's data says the lot has no buildings
                description = self.water_parcel.building_description.lower()
                if description.startswith('vac land') or description.startswith('vacant'):
                    certainty += 4

        # Not really certain unless groundtruthed, which would have been
        # returned earlier
        return min(certainty, 9)

    def _get_area(self):
        if self.billing_account:
            return self.billing_account.land_area
        if self.water_parcel:
            return self.water_parcel.gross_area
        return self.calculate_polygon_area()
    area = property(_get_area)

    def _get_number_of_lots(self):
        try:
            return self.lotgroup.lot_set.count()
        except Exception:
            return 1
    number_of_lots = property(_get_number_of_lots)

    def _get_display_name(self):
        if self.name:
            return self.name
        elif self.address_line1:
            return self.address_line1
        else:
            return "%d (unknown address)" % self.pk
    display_name = property(_get_display_name)

    def _get_latitude(self):
        try:
            return self.centroid.y
        except Exception:
            return None
    latitude = property(_get_latitude)

    def _get_longitude(self):
        try:
            return self.centroid.x
        except Exception:
            return None
    longitude = property(_get_longitude)

    def _is_visible(self):
        return (
            (not self.known_use or self.known_use.visible) and
            (self.steward_projects.count() == 0 or self.steward_inclusion_opt_in) and
            self.known_use_certainty > 3
        )
    is_visible = property(_is_visible)

    @models.permalink
    def get_geojson_url(self):
        """Override inplace url"""
        return ('lots:lot_detail_geojson', (), { 'pk': self.pk })


class LotGroup(Lot):
    """A group of lots."""

    def add(self, lot):
        """Add a lot to this group."""
        lots = set(list(self.lot_set.all()))
        lots.add(lot)
        self.update(lots=lots)

    def remove(self, lot):
        """Remove a lot from this group."""
        lots = list(self.lot_set.all())
        lots.remove(lot)
        self.update(lots=lots)

    def update(self, lots=None):
        """
        Update this group with the given lots. Allow lots to be passed
        manually since this might be called on a lot's pre_save signal.
        """

        if not lots:
            lots = self.lot_set.all()

        # Update polygon
        self.polygon = None
        for lot in lots:
            if not lot.polygon: continue
            if not self.polygon:
                self.polygon = lot.polygon
            else:
                union = self.polygon.union(lot.polygon)
                if not isinstance(union, MultiPolygon):
                    union = MultiPolygon([union])
                self.polygon = union

        # Update centroid
        self.centroid = self.polygon.centroid

        # Could update other things here, but maybe we should just proxy them
        # on the fly?

        self.save()

    def __unicode__(self):
        return self.name


class Use(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200)
    visible = models.BooleanField(_('visible'),
        default=True,
        help_text=_('Should lots with this use be visible on the map? If the '
                    'use is not vacant and not a project that someone could '
                    'join, probably not.'),
    )

    def __unicode__(self):
        return self.name
