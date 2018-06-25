from collections import defaultdict
import os
import warnings

from django.core import serializers
from django.core.management.base import CommandError
from django.core.management.commands.loaddata import (
    Command as LoadDataCommand, humanize
)
from django.db import (
    DatabaseError, IntegrityError, router
)
from django.utils.encoding import force_text


class Command(LoadDataCommand):

    def load_label(self, fixture_label):
        """
        Loads fixtures files for a given label. This method is largely copied
        from django.core.management.commands.loaddata.Command but with the
        addition of using bulk_create where possible.
        """
        show_progress = self.verbosity >= 3
        for fixture_file, fixture_dir, fixture_name in self.find_fixtures(fixture_label):
            _, ser_fmt, cmp_fmt = self.parse_name(os.path.basename(fixture_file))
            open_method, mode = self.compression_formats[cmp_fmt]
            fixture = open_method(fixture_file, mode)
            try:
                self.fixture_count += 1
                objects_in_fixture = 0
                loaded_objects_in_fixture = 0
                if self.verbosity >= 2:
                    self.stdout.write(
                        "Installing %s fixture '%s' from %s."
                        % (ser_fmt, fixture_name, humanize(fixture_dir))
                    )

                objects = serializers.deserialize(
                    ser_fmt, fixture, using=self.using, ignorenonexistent=self.ignore,
                )

                models_in_file = set()
                objects_to_create = []
                for obj in objects:
                    objects_in_fixture += 1
                    if (obj.object._meta.app_config in self.excluded_apps or
                            type(obj.object) in self.excluded_models):
                        continue
                    if router.allow_migrate_model(self.using, obj.object.__class__):
                        self.models.add(obj.object.__class__)
                        models_in_file.add(obj.object.__class__)
                        objects_to_create.append(obj)

                if len(models_in_file) == 1:
                    model = list(models_in_file)[0]
                    try:
                        model_objects = []
                        m2m_related_objects = defaultdict(list)
                        for obj in objects_to_create:
                            model_objects.append(obj.object)
                            if obj.m2m_data:
                                for accessor_field, m2m_list in obj.m2m_data.items():
                                    m2m_rel = getattr(model, accessor_field).rel
                                    related_model = m2m_rel.model
                                    through_model = m2m_rel.through

                                    for m2m_id in m2m_list:
                                        model_id_field = '{}_id'.format(
                                            model._meta.model_name
                                        )
                                        related_model_id_field = '{}_id'.format(
                                            related_model._meta.model_name
                                        )
                                        m2m_related_objects[through_model].append(
                                            through_model(**{
                                                model_id_field: obj.object.pk,
                                                related_model_id_field: m2m_id
                                            })
                                        )

                        model.objects.bulk_create(model_objects)
                        for m2m_model in m2m_related_objects:
                            m2m_model.objects.bulk_create(
                                m2m_related_objects[m2m_model]
                            )
                        loaded_objects_in_fixture += len(objects_to_create)
                        if show_progress:
                            self.stdout.write(
                                '\rProcessed %i object(s).' % loaded_objects_in_fixture,
                                ending=''
                            )
                    except (DatabaseError, IntegrityError) as e:
                            e.args = ("Could not load %(app_label)s.%(object_name)s: %(error_msg)s" % {
                                'app_label': model._meta.app_label,
                                'object_name': model._meta.object_name,
                                'error_msg': force_text(e)
                            },)
                            raise
                else:
                    for obj in objects_to_create:
                        try:
                            obj.save(using=self.using)
                            loaded_objects_in_fixture += 1
                            if show_progress:
                                self.stdout.write(
                                    '\rProcessed %i object(s).' % loaded_objects_in_fixture,
                                    ending=''
                                )
                        except (DatabaseError, IntegrityError) as e:
                            e.args = ("Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                                'app_label': obj.object._meta.app_label,
                                'object_name': obj.object._meta.object_name,
                                'pk': obj.object.pk,
                                'error_msg': force_text(e)
                            },)
                            raise
                if objects and show_progress:
                    self.stdout.write('')  # add a newline after progress indicator
                self.loaded_object_count += loaded_objects_in_fixture
                self.fixture_object_count += objects_in_fixture
            except Exception as e:
                if not isinstance(e, CommandError):
                    e.args = ("Problem installing fixture '%s': %s" % (fixture_file, e),)
                raise
            finally:
                fixture.close()

            # Warn if the fixture we loaded contains 0 objects.
            if objects_in_fixture == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be "
                    "invalid.)" % fixture_name,
                    RuntimeWarning
                )
