from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, ControlPoint, TipoDato


def _make_numeric_control_point(**overrides):
    categoria, _ = Categoria.objects.get_or_create(nombre="Agua")
    defaults = dict(
        categoria=categoria,
        objeto="Obrador frío lavamanos 1 (ALM 1)",
        nombre="Nivel de cloro libre",
        tipo_dato=TipoDato.NUMERICO,
        valor_minimo_aceptable=Decimal("0.2"),
        valor_maximo_aceptable=Decimal("1.0"),
        unidad_medida="mg/l",
    )
    defaults.update(overrides)
    return ControlPoint(**defaults)


class ControlPointModelTests(TestCase):
    def test_numeric_control_point_with_valid_range_saves(self):
        cp = _make_numeric_control_point()
        cp.save()
        self.assertIsNotNone(cp.pk)

    def test_numeric_control_point_without_range_is_rejected(self):
        cp = _make_numeric_control_point(
            valor_minimo_aceptable=None, valor_maximo_aceptable=None
        )
        with self.assertRaises(ValidationError):
            cp.save()

    def test_numeric_control_point_with_inverted_range_is_rejected(self):
        cp = _make_numeric_control_point(
            valor_minimo_aceptable=Decimal("1.0"), valor_maximo_aceptable=Decimal("0.2")
        )
        with self.assertRaises(ValidationError):
            cp.save()

    def test_numeric_control_point_without_unit_is_rejected(self):
        cp = _make_numeric_control_point(unidad_medida="")
        with self.assertRaises(ValidationError):
            cp.save()

    def test_checkbox_control_point_cannot_carry_numeric_range(self):
        cp = _make_numeric_control_point(
            tipo_dato=TipoDato.CHECKBOX,
            nombre="Color",
            unidad_medida="",
        )
        with self.assertRaises(ValidationError):
            cp.save()

    def test_checkbox_control_point_without_range_saves(self):
        categoria, _ = Categoria.objects.get_or_create(nombre="Agua")
        cp = ControlPoint(
            categoria=categoria,
            objeto="Obrador frío lavamanos 1 (ALM 1)",
            nombre="Color",
            tipo_dato=TipoDato.CHECKBOX,
        )
        cp.save()
        self.assertIsNotNone(cp.pk)

    def test_duplicate_control_point_for_same_object_is_rejected(self):
        _make_numeric_control_point().save()
        with self.assertRaises(ValidationError):
            _make_numeric_control_point().save()


class ControlPointViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="s3cure-pass-phrase"
        )
        self.control_point = _make_numeric_control_point()
        self.control_point.save()

    def test_list_view_requires_login(self):
        response = self.client.get(reverse("control_points:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_list_view_shows_control_points_when_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("control_points:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nivel de cloro libre")

    def test_search_filters_by_objeto_and_nombre(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("control_points:list"), {"q": "cloro"})
        self.assertContains(response, "Nivel de cloro libre")

        response = self.client.get(reverse("control_points:list"), {"q": "no-coincide"})
        self.assertNotContains(response, "Nivel de cloro libre")

    def test_detail_view_requires_login(self):
        url = reverse("control_points:detail", args=[self.control_point.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_detail_view_shows_control_point(self):
        self.client.force_login(self.user)
        url = reverse("control_points:detail", args=[self.control_point.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "mg/l")
