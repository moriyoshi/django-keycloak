from django.test import TestCase

from django_keycloak.factories import RealmFactory, ServerFactory
from django_keycloak.tests.mixins import MockTestCaseMixin
from django.test.utils import override_settings

from django_keycloak.services.exceptions import MissingRealmConfiguration
from django_keycloak.services.realm import get_issuer


class ServicesRealmGetIssuerTestCase(
        MockTestCaseMixin, TestCase):

    def test_get_issuer_success(self):
        """
        Case: issuer is successfully retrieved from a Realm object.
        Expected: an issuer url.
        """
        realm = RealmFactory(
            server=ServerFactory(
                internal_url="http://internal.example.com/",
                url="http://public.example.com/"
            ),
            _well_known_oidc='{"issuer":"http://internal.example.com/foo/bar"}'
        )
        issuer = get_issuer(realm)
        self.assertEqual("http://public.example.com/foo/bar", issuer)

    def test_get_issuer_fail(self):
        """
        Case: issuer configuration is missing in well-known json object.
        Expected: a proper exception raised.
        """
        realm = RealmFactory(
            server=ServerFactory(
                internal_url="http://internal.example.com/",
                url="http://public.example.com/"
            ),
            _well_known_oidc='{}'
        )
        with self.assertRaises(MissingRealmConfiguration):
            get_issuer(realm)
