from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from control_points.models import Categoria, ControlPoint, TipoDato

from .models import Elemento, Lectura


class ReadingsTestBase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="s3cure-pass-phrase"
        )
        self.categoria = Categoria.objects.create(nombre="Temperatura")
        self.control_point = ControlPoint.objects.create(
            categoria=self.categoria,
            objeto="Cámara de obrador",
            nombre="Temperatura de cámara",
            tipo_dato=TipoDato.NUMERICO,
            valor_minimo_aceptable=Decimal("0"),
            valor_maximo_aceptable=Decimal("5"),
            unidad_medida="°C",
        )
        self.elemento = Elemento.objects.create(
            categoria="Cámaras de Obrador", nombre="Cámara 1"
        )


class LecturaModelTests(ReadingsTestBase):
    def test_numeric_reading_with_correct_value_field_saves(self):
        lectura = Lectura(
            control_point=self.control_point,
            elemento=self.elemento,
            fecha=date(2026, 10, 1),
            valor_numerico=Decimal("3.5"),
            registrado_por=self.user,
        )
        lectura.save()
        self.assertTrue(lectura.dentro_de_rango)

    def test_numeric_reading_out_of_range_is_flagged(self):
        lectura = Lectura(
            control_point=self.control_point,
            elemento=self.elemento,
            fecha=date(2026, 10, 1),
            valor_numerico=Decimal("9.9"),
            registrado_por=self.user,
        )
        lectura.save()
        self.assertFalse(lectura.dentro_de_rango)

    def test_numeric_reading_with_wrong_value_field_is_rejected(self):
        lectura = Lectura(
            control_point=self.control_point,
            elemento=self.elemento,
            fecha=date(2026, 10, 1),
            valor_booleano=True,
            registrado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            lectura.save()

    def test_duplicate_reading_for_same_point_element_and_day_is_rejected(self):
        Lectura.objects.create(
            control_point=self.control_point,
            elemento=self.elemento,
            fecha=date(2026, 10, 1),
            valor_numerico=Decimal("3.0"),
            registrado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            Lectura(
                control_point=self.control_point,
                elemento=self.elemento,
                fecha=date(2026, 10, 1),
                valor_numerico=Decimal("3.2"),
                registrado_por=self.user,
            ).save()


class LecturaMonthListViewTests(ReadingsTestBase):
    def setUp(self):
        super().setUp()
        self.lectura = Lectura.objects.create(
            control_point=self.control_point,
            elemento=self.elemento,
            fecha=date(2026, 10, 15),
            valor_numerico=Decimal("3.5"),
            registrado_por=self.user,
        )

    def test_requires_login(self):
        url = reverse("readings:month_list", args=["Temperatura"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_shows_readings_for_requested_month(self):
        self.client.force_login(self.user)
        url = reverse("readings:month_list", args=["Temperatura"])
        response = self.client.get(url, {"year": 2026, "month": 10})
        self.assertContains(response, "Cámara 1")
        # Con LANGUAGE_CODE="es" el separador decimal se muestra como coma.
        self.assertContains(response, "3,500")

    def test_does_not_show_readings_from_other_months(self):
        self.client.force_login(self.user)
        url = reverse("readings:month_list", args=["Temperatura"])
        response = self.client.get(url, {"year": 2026, "month": 11})
        self.assertNotContains(response, "Cámara 1")

    def test_unknown_categoria_is_404(self):
        self.client.force_login(self.user)
        url = reverse("readings:month_list", args=["No Existe"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
